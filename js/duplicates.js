/* ─── DUPLICATE REVIEW ─── */

const ADMIN_UID = 'Bi68Kqd5jBPun5bIgXo0u5yTNmj2';

const firebaseConfig = {
  apiKey: "AIzaSyDyARd_4HXdx9gEOguMDvncPV17j7kum-s",
  authDomain: "church-registration-grace.firebaseapp.com",
  projectId: "church-registration-grace",
  storageBucket: "church-registration-grace.firebasestorage.app",
  messagingSenderId: "402796692999",
  appId: "1:402796692999:web:15f01064b41197c4c9cca2",
  measurementId: "G-L3CD5ZX957"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const auth = firebase.auth();

let isLoggedIn = false;
let groups = [];
let scanned = 0;
let searchTerm = '';

/* ─── HELPERS ─── */

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function cleanPhone(phone) {
  return String(phone || '').replace(/\D/g, '').slice(-9);
}

function formatDate(value) {
  try {
    if (!value) return '—';
    const d = value.toDate ? value.toDate() : new Date(value);
    if (isNaN(d.getTime())) return '—';
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  } catch (e) {
    return '—';
  }
}

/* ─── NAME MATCHING (same rules as the importers) ─── */

function normalizeNameForMatch(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/^\s*\d{1,3}\s*[.)-]\s*/, '')
    .replace(/([a-z0-9])\.{2,}([a-z0-9])/g, '$1*$2')
    .replace(/\.{2,}/g, '*')
    .replace(/[^a-z0-9 *]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function nameTokensForMatch(name) {
  const normalized = normalizeNameForMatch(name);
  return normalized ? normalized.split(' ') : [];
}

function wildcardTokenRegExp(token) {
  if (token.replace(/\*/g, '').length < 2) return null;
  const escaped = token
    .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\*/g, '.*');
  return new RegExp('^' + escaped + '$');
}

function nameTokenMatches(a, b) {
  if (a === b) return true;
  if (a.indexOf('*') !== -1) {
    const re = wildcardTokenRegExp(a);
    return re ? re.test(b) : false;
  }
  if (b.indexOf('*') !== -1) {
    const re = wildcardTokenRegExp(b);
    return re ? re.test(a) : false;
  }
  if (a.length === 1 && b.charAt(0) === a) return true;
  if (b.length === 1 && a.charAt(0) === b) return true;
  if (a.length >= 3 && b.startsWith(a)) return true;
  if (b.length >= 3 && a.startsWith(b)) return true;
  return false;
}

function namesMatch(a, b) {
  const ta = nameTokensForMatch(a);
  const tb = nameTokensForMatch(b);
  if (!ta.length || !tb.length || ta.length !== tb.length) return false;
  const used = new Array(tb.length).fill(false);
  for (let i = 0; i < ta.length; i++) {
    let matched = false;
    for (let j = 0; j < tb.length; j++) {
      if (!used[j] && nameTokenMatches(ta[i], tb[j])) {
        used[j] = true;
        matched = true;
        break;
      }
    }
    if (!matched) return false;
  }
  return true;
}

/* ─── SCORING: which record is the best one to keep ─── */

function recordScore(r) {
  let score = 0;
  if (r.welcomeSent) score += 100;               // keeps the record already contacted
  if (r.whatsappStatus === 'on') score += 40;    // has a confirmed WhatsApp number
  if (cleanPhone(r.phone).length === 9) score += 20;
  if (r.name && r.name.indexOf('...') === -1) score += 10; // full name beats truncated
  ['residence', 'location', 'department', 'email'].forEach(function (f) {
    if (r[f]) score += 3;
  });
  return score;
}

/* ─── LOAD + CLUSTER ─── */

async function loadRecords() {
  const snap = await db.collection('registrations').get();
  const list = [];
  snap.docs.forEach(function (doc) {
    const d = doc.data() || {};
    list.push({
      id: doc.id,
      name: d.name || '',
      phone: d.phone || d.whatsapp || '',
      residence: d.residence || d.location || '',
      location: d.location || '',
      department: d.department || '',
      email: d.email || '',
      status: d.status || '',
      whatsappStatus: d.whatsappStatus || 'unknown',
      welcomeSent: d.welcomeSent === true,
      imported: d.imported === true,
      source: d.source || '',
      createdAt: d.timestamp || d.importedAt || d.createdAt || null,
      keep: true
    });
  });
  return list;
}

function buildGroups(records) {
  const parent = records.map(function (_, i) { return i; });
  function find(i) {
    while (parent[i] !== i) {
      parent[i] = parent[parent[i]];
      i = parent[i];
    }
    return i;
  }
  function union(a, b) {
    a = find(a); b = find(b);
    if (a !== b) parent[b] = a;
  }

  // Same contact (last 9 digits)
  const byPhone = {};
  records.forEach(function (r, i) {
    const cp = cleanPhone(r.phone);
    if (cp && cp.length === 9) {
      (byPhone[cp] = byPhone[cp] || []).push(i);
    }
  });
  Object.keys(byPhone).forEach(function (cp) {
    const list = byPhone[cp];
    for (let i = 1; i < list.length; i++) union(list[0], list[i]);
  });

  // Same name
  for (let i = 0; i < records.length; i++) {
    for (let j = i + 1; j < records.length; j++) {
      if (find(i) === find(j)) continue;
      if (namesMatch(records[i].name, records[j].name)) union(i, j);
    }
  }

  const buckets = {};
  records.forEach(function (r, i) {
    const root = find(i);
    (buckets[root] = buckets[root] || []).push(r);
  });

  return Object.keys(buckets)
    .map(function (k) { return buckets[k]; })
    .filter(function (g) { return g.length > 1; })
    .map(function (g) {
      const reasons = [];
      let samePhone = false;
      let sameName = false;
      for (let i = 0; i < g.length && !(samePhone && sameName); i++) {
        for (let j = i + 1; j < g.length; j++) {
          if (cleanPhone(g[i].phone) && cleanPhone(g[i].phone) === cleanPhone(g[j].phone)) samePhone = true;
          if (namesMatch(g[i].name, g[j].name)) sameName = true;
        }
      }
      if (sameName) reasons.push('same name');
      if (samePhone) reasons.push('same contact');
      return { records: g, reasons: reasons };
    })
    .sort(function (a, b) { return b.records.length - a.records.length; });
}

/* ─── SCAN ─── */

async function scanDuplicates() {
  const btn = document.getElementById('scanBtn');
  const resultEl = document.getElementById('dupResult');
  const progressWrap = document.getElementById('dupProgressWrap');
  const progressBar = document.getElementById('dupProgress');
  const progressText = document.getElementById('dupProgressText');

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning…';
  resultEl.style.display = 'none';
  progressWrap.style.display = 'block';
  progressBar.style.width = '35%';
  progressText.textContent = 'Reading members from the database…';

  try {
    const records = await loadRecords();
    scanned = records.length;
    progressBar.style.width = '70%';
    progressText.textContent = 'Comparing ' + records.length + ' members…';
    await new Promise(function (r) { setTimeout(r, 30); });

    groups = buildGroups(records);

    progressBar.style.width = '100%';
    progressText.textContent = 'Done.';
    setTimeout(function () { progressWrap.style.display = 'none'; }, 500);

    renderGroups();
  } catch (err) {
    console.error('Duplicate scan failed:', err);
    progressWrap.style.display = 'none';
    resultEl.style.display = 'block';
    resultEl.className = 'result-box warn';
    resultEl.innerHTML = '<strong>Could not scan.</strong> ' + escapeHtml(err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-magnifying-glass"></i> Scan for duplicates';
  }
}

/* ─── RENDER ─── */

function visibleGroups() {
  if (!searchTerm) return groups;
  const term = searchTerm.toLowerCase();
  return groups.filter(function (g) {
    return g.records.some(function (r) {
      return String(r.name).toLowerCase().indexOf(term) !== -1 ||
             String(r.phone).toLowerCase().indexOf(term) !== -1;
    });
  });
}

function renderGroups() {
  const listEl = document.getElementById('dupList');
  const deleteBtn = document.getElementById('deleteBtn');
  const backupBtn = document.getElementById('backupBtn');
  searchTerm = (document.getElementById('dupSearch').value || '').trim();

  const shown = visibleGroups();
  let deleteCount = 0;
  let keepCount = 0;
  groups.forEach(function (g) {
    g.records.forEach(function (r) {
      if (r.keep) keepCount++; else deleteCount++;
    });
  });

  document.getElementById('statRecords').textContent = scanned;
  document.getElementById('statGroups').textContent = groups.length;
  document.getElementById('statDelete').textContent = deleteCount;
  document.getElementById('statKeep').textContent = keepCount;

  deleteBtn.disabled = deleteCount === 0;
  backupBtn.disabled = groups.length === 0;

  if (!groups.length) {
    listEl.innerHTML =
      '<div class="dup-empty ok"><i class="fas fa-circle-check"></i>' +
      '<p>No duplicates found. Every member has a unique name and contact.</p></div>';
    return;
  }

  if (!shown.length) {
    listEl.innerHTML = '<div class="dup-empty"><i class="fas fa-filter"></i><p>No groups match your search.</p></div>';
    return;
  }

  listEl.innerHTML = shown.map(function (g) {
    const gi = groups.indexOf(g);
    const rows = g.records.map(function (r, ri) {
      const created = formatDate(r.createdAt);
      return '' +
        '<div class="dup-row' + (r.keep ? '' : ' is-delete') + '">' +
          '<label class="dup-check">' +
            '<input type="checkbox"' + (r.keep ? ' checked' : '') +
            ' onchange="toggleKeep(' + gi + ',' + ri + ',this.checked)">' +
            '<span>' + (r.keep ? 'Keep' : 'Delete') + '</span>' +
          '</label>' +
          '<div class="dup-name">' + escapeHtml(r.name || '(no name)') +
            (r.imported ? ' <span class="dup-tag">imported</span>' : '') +
          '</div>' +
          '<div class="dup-phone">' + escapeHtml(r.phone || '—') + '</div>' +
          '<div class="dup-res">' + escapeHtml(r.residence || '—') + '</div>' +
          '<div class="dup-wa">' + escapeHtml(r.whatsappStatus || 'unknown') + '</div>' +
          '<div class="dup-created">' + escapeHtml(created) + '</div>' +
        '</div>';
    }).join('');

    return '' +
      '<div class="dup-group">' +
        '<div class="dup-group-head">' +
          '<div class="dup-group-title">' +
            '<span class="dup-count">' + g.records.length + ' records</span>' +
            g.reasons.map(function (reason) {
              return '<span class="dup-badge">' + escapeHtml(reason) + '</span>';
            }).join('') +
          '</div>' +
          '<div class="dup-group-tools">' +
            '<button class="btn-link" onclick="keepGroup(' + gi + ')">Keep all</button>' +
            '<button class="btn-link" onclick="bestGroup(' + gi + ')">Keep best only</button>' +
          '</div>' +
        '</div>' +
        '<div class="dup-table">' +
          '<div class="dup-row dup-row-head">' +
            '<div>Action</div><div>Name</div><div>Phone</div><div>Residence</div>' +
            '<div>WhatsApp</div><div>Added</div>' +
          '</div>' +
          rows +
        '</div>' +
      '</div>';
  }).join('');
}

/* ─── SELECTION ─── */

function toggleKeep(gi, ri, checked) {
  groups[gi].records[ri].keep = checked;
  renderGroups();
}

function keepGroup(gi) {
  groups[gi].records.forEach(function (r) { r.keep = true; });
  renderGroups();
}

function bestGroup(gi) {
  const recs = groups[gi].records;
  let best = 0;
  for (let i = 1; i < recs.length; i++) {
    if (recordScore(recs[i]) > recordScore(recs[best])) best = i;
  }
  recs.forEach(function (r, i) { r.keep = i === best; });
  renderGroups();
}

function keepAll() {
  groups.forEach(function (g) {
    g.records.forEach(function (r) { r.keep = true; });
  });
  renderGroups();
}

function selectBestAll() {
  groups.forEach(function (g) {
    let best = 0;
    for (let i = 1; i < g.records.length; i++) {
      if (recordScore(g.records[i]) > recordScore(g.records[best])) best = i;
    }
    g.records.forEach(function (r, i) { r.keep = i === best; });
  });
  renderGroups();
}

/* ─── BACKUP + DELETE ─── */

function pendingDeletions() {
  const out = [];
  groups.forEach(function (g) {
    g.records.forEach(function (r) {
      if (!r.keep) out.push(r);
    });
  });
  return out;
}

function downloadBackup() {
  const rows = pendingDeletions();
  const payload = {
    exportedAt: new Date().toISOString(),
    project: 'church-registration-grace',
    collection: 'registrations',
    count: rows.length,
    records: rows.map(function (r) {
      return {
        id: r.id, name: r.name, phone: r.phone, residence: r.residence,
        location: r.location, department: r.department, email: r.email,
        status: r.status, whatsappStatus: r.whatsappStatus,
        welcomeSent: r.welcomeSent, imported: r.imported, source: r.source
      };
    })
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'duplicates-backup-' + new Date().toISOString().slice(0, 10) + '.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
}

async function deleteUnchecked() {
  if (!isLoggedIn) { showLoginModal(); return; }

  // Never allow a whole group to be emptied.
  for (let i = 0; i < groups.length; i++) {
    const kept = groups[i].records.filter(function (r) { return r.keep; }).length;
    if (kept === 0) {
      const names = groups[i].records.map(function (r) { return r.name; }).join(', ');
      alert('Group ' + (i + 1) + ' would lose every record.\n\n' + names +
            '\n\nTick at least one record to keep before deleting.');
      return;
    }
  }

  const rows = pendingDeletions();
  if (!rows.length) return;

  if (!confirm('Permanently delete ' + rows.length + ' duplicate record(s)?\n\n' +
               'The remaining ' + (scanned - rows.length) + ' member(s) are kept.\n\n' +
               'A backup file will download first.')) return;

  downloadBackup();

  const btn = document.getElementById('deleteBtn');
  const resultEl = document.getElementById('dupResult');
  const progressWrap = document.getElementById('dupProgressWrap');
  const progressBar = document.getElementById('dupProgress');
  const progressText = document.getElementById('dupProgressText');

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting…';
  resultEl.style.display = 'none';
  progressWrap.style.display = 'block';
  progressBar.style.width = '0%';
  progressText.textContent = 'Starting…';

  let deleted = 0;
  let failed = 0;
  const chunkSize = 400;

  try {
    for (let start = 0; start < rows.length; start += chunkSize) {
      const chunk = rows.slice(start, start + chunkSize);
      const batch = db.batch();
      chunk.forEach(function (r) {
        batch.delete(db.collection('registrations').doc(r.id));
      });
      await batch.commit();
      deleted += chunk.length;

      const pct = Math.round((deleted / rows.length) * 100);
      progressBar.style.width = pct + '%';
      progressText.textContent = deleted + ' of ' + rows.length + ' deleted (' + pct + '%)';
    }
  } catch (err) {
    console.error('Delete failed:', err);
    failed = rows.length - deleted;
  }

  resultEl.style.display = 'block';
  resultEl.className = 'result-box ' + (failed ? 'warn' : 'ok');
  resultEl.innerHTML = '<strong>Cleanup finished.</strong> Deleted ' + deleted + ' duplicate record(s).' +
    (failed ? ' ' + failed + ' could not be deleted — check that you are signed in as admin.' : '') +
    '<div style="margin-top:12px;"><button class="btn-primary" onclick="scanDuplicates()">' +
    '<i class="fas fa-rotate"></i> Scan again</button></div>';

  btn.innerHTML = '<i class="fas fa-trash-can"></i> Delete unchecked';

  // Drop deleted rows from local state so the page stays accurate.
  groups.forEach(function (g) {
    g.records = g.records.filter(function (r) { return r.keep; });
  });
  groups = groups.filter(function (g) { return g.records.length > 1; });
  scanned -= deleted;
  renderGroups();
  setTimeout(function () { progressWrap.style.display = 'none'; }, 800);
}

/* ─── AUTH ─── */

function showLoginModal() { document.getElementById('loginModal').classList.add('show'); }
function hideLoginModal() { document.getElementById('loginModal').classList.remove('show'); }

function handleAdminBtn() {
  if (isLoggedIn) auth.signOut();
  else showLoginModal();
}

auth.onAuthStateChanged(function (user) {
  if (user && user.uid === ADMIN_UID) {
    isLoggedIn = true;
    document.getElementById('adminBtn').textContent = 'Logout';
    document.getElementById('authNotice').classList.add('is-admin');
    document.getElementById('loginError').style.display = 'none';
    hideLoginModal();
  } else if (user && user.uid !== ADMIN_UID) {
    auth.signOut();
    const errEl = document.getElementById('loginError');
    if (errEl) {
      errEl.textContent = 'Access denied. You are not authorized as admin.';
      errEl.style.display = 'block';
    }
  } else {
    isLoggedIn = false;
    document.getElementById('adminBtn').textContent = 'Admin Login';
    document.getElementById('authNotice').classList.remove('is-admin');
  }
});

document.getElementById('loginForm').onsubmit = function (e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  const errorEl = document.getElementById('loginError');
  errorEl.style.display = 'none';

  if (document.getElementById('rememberEmail').checked) {
    localStorage.setItem('adminEmail', email);
    localStorage.setItem('rememberEmail', 'true');
  } else {
    localStorage.removeItem('adminEmail');
    localStorage.setItem('rememberEmail', 'false');
  }

  auth.signInWithEmailAndPassword(email, password)
    .then(function (userCred) {
      if (userCred.user.uid !== ADMIN_UID) {
        auth.signOut();
        errorEl.textContent = 'Access denied. You are not authorized as admin.';
        errorEl.style.display = 'block';
      }
    })
    .catch(function (err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
    });
};

/* ─── INIT ─── */

(function init() {
  document.getElementById('currentDate').textContent = new Date().toLocaleDateString(undefined, {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });

  const savedEmail = localStorage.getItem('adminEmail');
  if (savedEmail) document.getElementById('loginEmail').value = savedEmail;
  document.getElementById('rememberEmail').checked = localStorage.getItem('rememberEmail') !== 'false';

  scanDuplicates();
})();
