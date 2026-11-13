/* ─── BULK IMPORT SYSTEM ─── */

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
let allRows = [];
let existingPhones = new Set();
let existingNames = [];
let existingLoaded = false;
let sourceLabel = '';

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

function isValidWhatsAppPhone(phone) {
  return /^[76]\d{8}$/.test(cleanPhone(phone));
}

// Capitalise the first letter of every name word, including hyphenated and
// apostrophe names. Also removes leading list numbers and joins truncated
// fragments such as "Sse...ongo" -> "Sseongo".
function titleCaseName(name) {
  let s = String(name || '').replace(/\s+/g, ' ').trim();
  s = s.replace(/^\s*\d{1,3}\s*[.)-]\s*/, '');
  s = s.replace(/\.{2,}/g, '');
  s = s.replace(/\s+/g, ' ').trim();
  return s
    .toLowerCase()
    .replace(/(^|[\s\-'’])([a-z])/g, function (match, sep, letter) {
      return sep + letter.toUpperCase();
    });
}

/* ─── NAME MATCHING ─── */

function normalizeNameForMatch(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/^\s*\d{1,3}\s*[.)-]\s*/, '')
    .replace(/([a-z0-9])\.{2,}([a-z0-9])/g, '$1*$2') // "sse...ongo" -> "sse*ongo"
    .replace(/\.{2,}/g, '*')                          // "nam..." -> "nam*"
    .replace(/[^a-z0-9 *]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function nameTokensForMatch(name) {
  const normalized = normalizeNameForMatch(name);
  return normalized ? normalized.split(' ') : [];
}

// An ellipsis marks missing middle letters: "sse*ongo" matches "ssentongo".
function wildcardTokenRegExp(token) {
  const literals = token.replace(/\*/g, '').length;
  if (literals < 2) return null;
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

/* ─── FILE PARSING ─── */

function cleanJsonText(text) {
  return String(text || '')
    .replace(/^\uFEFF/, '')
    .replace(/[\u00A0\u2007\u202F]/g, ' ')
    .replace(/[\u200B-\u200D]/g, '');
}

// Exported files are sometimes pasted together, producing several JSON values
// in one file: "[ {...} ][ {...} ]" or one value per line (NDJSON). JSON.parse
// only accepts the first value, so collect every complete top-level value.
function splitJsonValues(text) {
  const values = [];
  let depth = 0;
  let inString = false;
  let escaped = false;
  let start = -1;

  for (let i = 0; i < text.length; i++) {
    const ch = text.charAt(i);
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') { inString = true; continue; }
    if (ch === '[' || ch === '{') {
      if (depth === 0) start = i;
      depth++;
    } else if (ch === ']' || ch === '}') {
      if (depth > 0) depth--;
      if (depth === 0 && start !== -1) {
        values.push(text.slice(start, i + 1));
        start = -1;
      }
    }
  }
  return values;
}

function jsonRecordsFromValue(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.records)) return data.records;
  if (Array.isArray(data.data)) return data.data;
  if (Array.isArray(data.members)) return data.members;
  // A single record exported on its own (common in line-by-line JSON).
  if (data && typeof data === 'object' &&
      (data.name || data.fullName || data.full_name || data.names ||
       data.contact || data.phone || data.mobile || data.telephone || data.whatsapp || data.number)) {
    return [data];
  }
  throw new Error('JSON must be an array or contain a "records" array.');
}

function parseJsonRecords(text) {
  const cleaned = cleanJsonText(text);
  let blocks;

  try {
    blocks = [JSON.parse(cleaned)];
  } catch (firstError) {
    const chunks = splitJsonValues(cleaned);
    if (!chunks.length) {
      throw new Error('This does not look like valid JSON. ' + firstError.message);
    }
    blocks = chunks.map(function (chunk, i) {
      try {
        return JSON.parse(chunk);
      } catch (err) {
        throw new Error('Block ' + (i + 1) + ' of ' + chunks.length +
          ' is not valid JSON (' + err.message + '). Check for a missing comma or bracket near the top of that block.');
      }
    });
  }

  let list = [];
  blocks.forEach(function (data) {
    list = list.concat(jsonRecordsFromValue(data));
  });
  if (!list.length) throw new Error('No records were found in the JSON.');

  const records = list.map(function (r) {
    return {
      name: r.name || r.fullName || r.full_name || r.names || '',
      contact: r.contact || r.phone || r.mobile || r.telephone || r.whatsapp || r.number || '',
      residence: r.residence || r.location || r.address || r.area || r.village || ''
    };
  });
  records.jsonBlocks = blocks.length;
  return records;
}

function detectDelimiter(text) {
  const firstLine = String(text || '').split('\n')[0] || '';
  let best = ',';
  let bestCount = 0;
  [',', ';', '\t', '|'].forEach(function (delim) {
    let count = 0;
    let inQuotes = false;
    for (let i = 0; i < firstLine.length; i++) {
      const ch = firstLine.charAt(i);
      if (ch === '"') inQuotes = !inQuotes;
      else if (!inQuotes && ch === delim) count++;
    }
    if (count > bestCount) { bestCount = count; best = delim; }
  });
  return best;
}

function parseCsvText(text) {
  const s = String(text || '')
    .replace(/^\uFEFF/, '')
    .replace(/[\u00A0\u2007\u202F]/g, ' ')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n');
  const delim = detectDelimiter(s);
  const rows = [];
  let field = '';
  let row = [];
  let inQuotes = false;

  for (let i = 0; i < s.length; i++) {
    const ch = s.charAt(i);
    if (inQuotes) {
      if (ch === '"') {
        if (s.charAt(i + 1) === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === delim) {
      row.push(field); field = '';
    } else if (ch === '\n') {
      row.push(field); rows.push(row); row = []; field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  while (rows.length && rows[rows.length - 1].every(function (c) { return !String(c).trim(); })) rows.pop();
  if (!rows.length) return [];

  const header = rows[0].map(function (h) {
    return String(h).toLowerCase().replace(/[^a-z0-9]/g, '');
  });
  function findIdx() {
    const names = Array.prototype.slice.call(arguments);
    return header.findIndex(function (h) { return names.indexOf(h) !== -1; });
  }

  let nameIdx = findIdx('name', 'fullname', 'fullnames', 'names', 'membername', 'member');
  let contactIdx = findIdx('contact', 'phone', 'phonenumber', 'telephone', 'mobile', 'mobilenumber', 'whatsapp', 'whatsappnumber', 'number');
  let residenceIdx = findIdx('residence', 'location', 'address', 'area', 'village', 'zone');
  let dataRows = rows.slice(1);

  if (nameIdx === -1 && contactIdx === -1) {
    nameIdx = 0; contactIdx = 1; residenceIdx = 2; dataRows = rows;
  } else {
    if (nameIdx === -1) nameIdx = 0;
    if (contactIdx === -1) contactIdx = 1;
  }

  return dataRows
    .filter(function (r) { return r.some(function (c) { return String(c).trim(); }); })
    .map(function (r) {
      return {
        name: r[nameIdx] || '',
        contact: r[contactIdx] || '',
        residence: residenceIdx >= 0 ? (r[residenceIdx] || '') : ''
      };
    });
}

function parseFileText(text) {
  const trimmed = String(text || '').trim();
  if (!trimmed) return [];
  if (trimmed.charAt(0) === '[' || trimmed.charAt(0) === '{') return parseJsonRecords(trimmed);
  return parseCsvText(trimmed);
}

/* ─── LIVE DATABASE CHECK ─── */

async function loadExisting() {
  if (existingLoaded) return;
  const snap = await db.collection('registrations').get();
  existingPhones = new Set();
  existingNames = [];
  snap.docs.forEach(function (d) {
    const data = d.data();
    existingPhones.add(String(d.id));
    if (/^\d{9}$/.test(String(d.id))) existingPhones.add(String(d.id));
    const phone = data.phone || data.contact || data.whatsapp || '';
    const cp = cleanPhone(phone);
    if (cp) existingPhones.add(cp);
    const name = data.name || data.fullName || '';
    if (name) existingNames.push(name);
  });
  existingLoaded = true;
}

/* ─── ANALYSE ROWS ─── */

function analyze(records) {
  const filePhones = new Set();
  const fileNames = [];

  allRows = records.map(function (r, i) {
    const rawName = String(r.name || '').replace(/\s+/g, ' ').trim();
    const rawPhone = String(r.contact || '').trim();
    const residence = String(r.residence || '').replace(/\s+/g, ' ').trim();
    const cp = cleanPhone(rawPhone);

    const row = {
      index: i + 1,
      rawName: rawName,
      name: titleCaseName(rawName),
      phone: rawPhone,
      residence: residence,
      cleanPhone: cp,
      validPhone: isValidWhatsAppPhone(rawPhone),
      duplicate: false,
      reason: '',
      include: true,
      imported: false
    };

    if (!rawName && !cp) { row.duplicate = true; row.reason = 'No name or contact'; }
    else if (!rawName) { row.duplicate = true; row.reason = 'No name'; }
    else if (!cp) { row.duplicate = true; row.reason = 'No contact'; }
    else if (filePhones.has(cp)) { row.duplicate = true; row.reason = 'Duplicate contact in file'; }
    else if (fileNames.some(function (n) { return namesMatch(n, rawName); })) { row.duplicate = true; row.reason = 'Duplicate name in file'; }
    else if (existingPhones.has(cp)) { row.duplicate = true; row.reason = 'Contact already in system'; }
    else if (existingNames.some(function (n) { return namesMatch(n, rawName); })) { row.duplicate = true; row.reason = 'Name already in system'; }

    if (row.duplicate) row.include = false;
    // Never import an invalid WhatsApp number unless the admin ticks it
    // individually; this prevents junk document IDs such as "123".
    else if (!row.validPhone) row.include = false;
    if (cp) filePhones.add(cp);
    if (rawName) fileNames.push(rawName);
    return row;
  });
}

/* ─── RENDERING ─── */

function setBusy(busy) {
  const dz = document.getElementById('dropZone');
  if (!dz) return;
  dz.classList.toggle('is-busy', busy);
  const strong = dz.querySelector('strong');
  if (strong) strong.textContent = busy ? 'Checking the database…' : 'Drag & drop your file here';
}

function renderPreview() {
  const tbody = document.getElementById('bulkTableBody');
  const q = (document.getElementById('bulkSearch').value || '').trim().toLowerCase();
  const filter = document.getElementById('bulkFilter').value;

  const visible = allRows.filter(function (r) {
    if (q) {
      const hay = (r.name + ' ' + r.phone + ' ' + r.residence).toLowerCase();
      if (hay.indexOf(q) === -1) return false;
    }
    if (filter === 'ready' && (r.duplicate || r.imported)) return false;
    if (filter === 'duplicate' && !r.duplicate) return false;
    if (filter === 'invalid' && (r.duplicate || r.validPhone)) return false;
    return true;
  });

  tbody.innerHTML = visible.map(function (r) {
    let status;
    let rowClass = '';
    if (r.imported) {
      status = '<span class="status-badge ok">Imported</span>';
      rowClass = 'row-imported';
    } else if (r.duplicate) {
      status = '<span class="status-badge dup">' + escapeHtml(r.reason) + '</span>';
      rowClass = 'row-dup';
    } else if (!r.validPhone) {
      status = '<span class="status-badge warn">⚠ Invalid WhatsApp</span>';
      rowClass = 'row-invalid';
    } else {
      status = '<span class="status-badge ok">Ready</span>';
    }

    return '<tr class="' + rowClass + '">' +
      '<td><input type="checkbox" ' + (r.duplicate || r.imported ? 'disabled' : '') + ' ' + (r.include ? 'checked' : '') + ' onchange="setInclude(' + r.index + ', this.checked)"></td>' +
      '<td>' + r.index + '</td>' +
      '<td>' + escapeHtml(r.name || '-') + '</td>' +
      '<td>' + escapeHtml(r.phone || '-') + '</td>' +
      '<td>' + escapeHtml(r.residence || '-') + '</td>' +
      '<td>' + status + '</td>' +
    '</tr>';
  }).join('') || '<tr><td colspan="6" class="empty">No rows match the current filter.</td></tr>';

  updateSummary();
}

function updateSummary() {
  const ready = allRows.filter(function (r) { return !r.duplicate && !r.imported; });
  const selected = ready.filter(function (r) { return r.include; });
  const invalid = ready.filter(function (r) { return !r.validPhone; });

  document.getElementById('tileTotal').textContent = allRows.length;
  document.getElementById('tileReady').textContent = ready.length;
  document.getElementById('tileDup').textContent = allRows.filter(function (r) { return r.duplicate; }).length;
  document.getElementById('tileInvalid').textContent = invalid.length;

  const btn = document.getElementById('bulkImportBtn');
  btn.disabled = selected.length === 0 || !isLoggedIn;
  btn.innerHTML = !isLoggedIn
    ? '<i class="fas fa-lock"></i> Login to import'
    : '<i class="fas fa-file-import"></i> Import ' + selected.length + ' member(s)';

  const selectAll = document.getElementById('selectAllReady');
  if (selectAll) {
    const allSelected = ready.length > 0 && ready.every(function (r) { return r.include; });
    const someSelected = ready.some(function (r) { return r.include; });
    selectAll.checked = allSelected;
    selectAll.indeterminate = !allSelected && someSelected;
  }
}

function setInclude(index, checked) {
  const row = allRows.find(function (r) { return r.index === index; });
  if (!row || row.duplicate || row.imported) return;
  row.include = checked;
  updateSummary();
}

function toggleAllReady(checked) {
  allRows.forEach(function (r) {
    if (!r.duplicate && !r.imported && r.validPhone) r.include = checked;
  });
  renderPreview();
}

function toggleSkipInvalid(checked) {
  if (checked) {
    allRows.forEach(function (r) {
      if (!r.duplicate && !r.imported && !r.validPhone) r.include = false;
    });
  }
  renderPreview();
}

/* ─── FILE HANDLING ─── */

async function handleRecords(records, label) {
  setBusy(true);
  try {
    existingLoaded = false;
    await loadExisting();
    analyze(records);
    sourceLabel = label || 'file';

    const info = document.getElementById('fileInfo');
    const blocks = records.jsonBlocks || 1;
    info.style.display = 'block';
    info.innerHTML = '<i class="fas fa-file-circle-check"></i> Loaded <strong>' + records.length +
      '</strong> row(s) from <strong>' + escapeHtml(sourceLabel) + '</strong>.' +
      (blocks > 1
        ? ' The file contained <strong>' + blocks + '</strong> separate JSON blocks, which were combined.'
        : '');

    document.getElementById('reviewSection').style.display = 'block';
    document.getElementById('bulkResult').style.display = 'none';
    document.getElementById('bulkProgressWrap').style.display = 'none';
    document.getElementById('selectAllReady').checked = false;
    document.getElementById('skipInvalid').checked = false;
    renderPreview();
    document.getElementById('reviewSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    console.error('Bulk import check failed:', err);
    alert('Could not check the file against the database:\n' + err.message);
  } finally {
    setBusy(false);
  }
}

function readFile(file) {
  if (!file) return;
  if (file.size > 15 * 1024 * 1024) {
    alert('That file is larger than 15 MB. Please split it into smaller files.');
    return;
  }
  const reader = new FileReader();
  reader.onload = function () {
    try {
      const records = parseFileText(reader.result);
      if (!records.length) throw new Error('No rows were found in the file.');
      handleRecords(records, file.name);
    } catch (err) {
      alert('Could not read the file:\n' + err.message);
    }
  };
  reader.onerror = function () { alert('Could not read the file.'); };
  reader.readAsText(file);
}

async function loadServerFile() {
  try {
    setBusy(true);
    const res = await fetch('imports/new.json?t=' + Date.now(), { cache: 'no-store' });
    if (!res.ok) throw new Error('HTTP ' + res.status + ' — make sure imports/new.json exists.');
    const records = parseJsonRecords(await res.text());
    if (!records.length) throw new Error('No rows were found in imports/new.json.');
    await handleRecords(records, 'imports/new.json');
  } catch (err) {
    alert('Could not load imports/new.json:\n' + err.message);
  } finally {
    setBusy(false);
  }
}

function downloadSample(kind) {
  let content;
  let type;
  let filename;
  if (kind === 'json') {
    content = JSON.stringify([
      { name: 'Jane Nakato', contact: '0700123456', residence: 'Luzira' },
      { name: 'John Okello', contact: '+256 772 123456', residence: 'Kitintale' }
    ], null, 2);
    type = 'application/json';
    filename = 'members-sample.json';
  } else {
    content = 'name,contact,residence\nJane Nakato,0700123456,Luzira\nJohn Okello,+256 772 123456,Kitintale\n';
    type = 'text/csv';
    filename = 'members-sample.csv';
  }
  const blob = new Blob([content], { type: type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
}

function resetImport() {
  allRows = [];
  sourceLabel = '';
  existingLoaded = false;
  document.getElementById('reviewSection').style.display = 'none';
  document.getElementById('fileInfo').style.display = 'none';
  document.getElementById('bulkFileInput').value = '';
  document.getElementById('bulkResult').style.display = 'none';
  document.getElementById('bulkProgressWrap').style.display = 'none';
  document.getElementById('bulkSearch').value = '';
  document.getElementById('bulkFilter').value = 'all';
  document.getElementById('selectAllReady').checked = false;
  document.getElementById('skipInvalid').checked = false;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ─── IMPORT ─── */

function buildDoc(row) {
  return {
    name: row.name,
    phone: row.phone,
    location: row.residence || '',
    residence: row.residence || '',
    department: '',
    registrationType: 'general',
    registered: 'yes',
    firstTime: 'yes',
    whatsapp: row.phone,
    volunteering: '',
    referredBy: '',
    status: 'pending',
    whatsappStatus: 'unknown',
    welcomeSent: false,
    source: 'import',
    imported: true,
    importedAt: firebase.firestore.FieldValue.serverTimestamp(),
    cleanPhone: row.cleanPhone,
    timestamp: firebase.firestore.FieldValue.serverTimestamp()
  };
}

// A chunk transaction reads every target document first, then writes only the
// ones that do not exist. This guarantees an import never overwrites a record.
async function importChunk(chunk) {
  const refs = chunk.map(function (r) {
    return db.collection('registrations').doc(r.cleanPhone);
  });

  try {
    return await db.runTransaction(async function (tx) {
      const snaps = await Promise.all(refs.map(function (ref) { return tx.get(ref); }));
      let imported = 0;
      let conflicts = 0;
      const importedRows = new Set();

      snaps.forEach(function (snap, i) {
        if (snap.exists) { conflicts++; return; }
        tx.set(refs[i], buildDoc(chunk[i]));
        imported++;
        importedRows.add(chunk[i].index);
      });

      return { imported: imported, conflicts: conflicts, failed: 0, importedRows: importedRows };
    });
  } catch (err) {
    console.warn('Chunk transaction failed; retrying rows individually.', err);
    let imported = 0;
    let conflicts = 0;
    let failed = 0;
    const importedRows = new Set();

    for (let i = 0; i < chunk.length; i++) {
      const row = chunk[i];
      try {
        const result = await db.runTransaction(async function (tx) {
          const ref = db.collection('registrations').doc(row.cleanPhone);
          const snap = await tx.get(ref);
          if (snap.exists) return 'conflict';
          tx.set(ref, buildDoc(row));
          return 'imported';
        });
        if (result === 'imported') { imported++; importedRows.add(row.index); }
        else conflicts++;
      } catch (rowErr) {
        failed++;
        console.warn('Import failed for ' + row.name + ':', rowErr);
      }
    }

    return { imported: imported, conflicts: conflicts, failed: failed, importedRows: importedRows };
  }
}

// Final safety gate: re-read the database and refuse to write any row that
// duplicates an existing member, or another row in this import. This runs
// immediately before the first write so a record added after the preview
// cannot be imported by mistake.
async function recheckBeforeWrite(rows) {
  existingLoaded = false;
  await loadExisting();

  const allowed = [];
  const blocked = [];
  const acceptedNames = [];
  const acceptedPhones = new Set();

  rows.forEach(function (row) {
    const name = row.rawName || row.name;
    let reason = '';
    if (!row.cleanPhone) reason = 'No contact';
    else if (existingPhones.has(row.cleanPhone)) reason = 'Contact already in system';
    else if (existingNames.some(function (n) { return namesMatch(n, name); })) reason = 'Name already in system';
    else if (acceptedPhones.has(row.cleanPhone)) reason = 'Duplicate contact in file';
    else if (acceptedNames.some(function (n) { return namesMatch(n, name); })) reason = 'Duplicate name in file';

    if (reason) {
      row.duplicate = true;
      row.reason = reason;
      row.include = false;
      blocked.push(row);
    } else {
      acceptedPhones.add(row.cleanPhone);
      acceptedNames.push(name);
      allowed.push(row);
    }
  });

  return { allowed: allowed, blocked: blocked };
}

async function runImport() {
  if (!isLoggedIn) { showLoginModal(); return; }

  const btn = document.getElementById('bulkImportBtn');
  const resultEl = document.getElementById('bulkResult');
  const initialHtml = btn.innerHTML;

  let selected = allRows.filter(function (r) {
    return !r.duplicate && !r.imported && r.include;
  });
  if (!selected.length) return;

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking duplicates…';

  let check;
  try {
    check = await recheckBeforeWrite(selected);
  } catch (err) {
    console.error('Final duplicate check failed:', err);
    alert('Could not verify duplicates against the database, so nothing was imported.\n\n' + err.message);
    btn.disabled = false;
    btn.innerHTML = initialHtml;
    updateSummary();
    return;
  }

  selected = check.allowed;
  const blocked = check.blocked;

  if (!selected.length) {
    btn.disabled = false;
    btn.innerHTML = initialHtml;
    resultEl.style.display = 'block';
    resultEl.className = 'result-box warn';
    resultEl.innerHTML = '<strong>Nothing imported.</strong> All ' + blocked.length +
      ' selected row(s) already exist in the system, so they were skipped.';
    renderPreview();
    updateSummary();
    return;
  }

  const warning = blocked.length
    ? '\n\n' + blocked.length + ' duplicate(s) in this selection will be skipped and never saved.'
    : '';
  if (!confirm('Import ' + selected.length + ' member(s)?' + warning + '\n\nRows whose name or contact already exists are excluded.')) {
    btn.disabled = false;
    btn.innerHTML = initialHtml;
    renderPreview();
    updateSummary();
    return;
  }

  const progressWrap = document.getElementById('bulkProgressWrap');
  const progressBar = document.getElementById('bulkProgress');
  const progressText = document.getElementById('bulkProgressText');

  progressWrap.style.display = 'block';
  resultEl.style.display = 'none';
  progressBar.style.width = '0%';
  progressText.textContent = 'Starting…';

  let imported = 0;
  let conflicts = 0;
  let failed = 0;
  const chunkSize = 200;

  for (let start = 0; start < selected.length; start += chunkSize) {
    const chunk = selected.slice(start, start + chunkSize);
    const outcome = await importChunk(chunk);
    imported += outcome.imported;
    conflicts += outcome.conflicts;
    failed += outcome.failed;

    chunk.forEach(function (r) {
      if (outcome.importedRows.has(r.index)) {
        r.imported = true;
        r.include = false;
      }
    });

    const done = Math.min(start + chunk.length, selected.length);
    const pct = Math.round((done / selected.length) * 100);
    progressBar.style.width = pct + '%';
    progressText.textContent = done + ' of ' + selected.length + ' processed (' + pct + '%)';
  }

  resultEl.style.display = 'block';
  resultEl.className = 'result-box ' + (failed ? 'warn' : 'ok');
  const skipped = allRows.filter(function (r) { return r.duplicate; }).length + conflicts;
  resultEl.innerHTML =
    '<strong>Import finished.</strong> Imported ' + imported + ' member(s).' +
    (skipped ? ' Skipped ' + skipped + ' duplicate(s) — duplicates are never saved.' : '') +
    (failed ? ' ' + failed + ' failed.' : '') +
    '<div style="margin-top:12px;"><a class="btn-primary" href="dashboard.html"><i class="fas fa-arrow-right"></i> Open Dashboard</a></div>';

  renderPreview();
  updateSummary();
  existingLoaded = false;
}

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
    updateSummary();
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
    updateSummary();
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

  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('bulkFileInput');

  dropZone.addEventListener('click', function (e) {
    if (e.target === fileInput) return;
    fileInput.click();
  });
  dropZone.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });
  ['dragenter', 'dragover'].forEach(function (ev) {
    dropZone.addEventListener(ev, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragover');
    });
  });
  ['dragleave', 'drop'].forEach(function (ev) {
    dropZone.addEventListener(ev, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    });
  });
  dropZone.addEventListener('drop', function (e) {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (file) readFile(file);
  });
  fileInput.addEventListener('change', function (e) {
    const file = e.target.files && e.target.files[0];
    if (file) readFile(file);
  });

  updateSummary();
})();
