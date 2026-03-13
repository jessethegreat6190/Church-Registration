// js/dashboard.js — Admin Dashboard · Grace of Jesus Christ Ministries
import {
  isUpcomingBirthday,
  getDaysUntilBirthday,
  formatBirthday
} from './utils.js';

/* ── Constants ───────────────────────────────────────────────
   Same GAS deployment handles GET (doGet) and POST (doPost).
   Split into separate constants so either can be updated independently.
   ─────────────────────────────────────────────────────────── */
const GET_DATA_API_URL  = 'https://script.google.com/macros/s/AKfycbxep7hhQKPfuPBG9q9oig8D892E2d4bdBdPvGct48jlAFIUP6bmSu06tIbbl-6pmISsOQ/exec';
const SAVE_DATA_API_URL = 'https://script.google.com/macros/s/AKfycbxep7hhQKPfuPBG9q9oig8D892E2d4bdBdPvGct48jlAFIUP6bmSu06tIbbl-6pmISsOQ/exec';

/* ── DOM refs ────────────────────────────────────────────── */
const tableBody           = document.getElementById('tableBody');
const searchBar           = document.getElementById('searchBar');
const exportBtn           = document.getElementById('exportBtn');
const totalCount          = document.getElementById('totalCount');
const saveProgramsBtn     = document.getElementById('saveProgramsBtn');
const birthdayAlerts      = document.getElementById('birthdayAlerts');
const birthdayList        = document.getElementById('birthdayList');
const editModal           = document.getElementById('editModal');
const saveEditBtn         = document.getElementById('saveEditBtn');
const cancelEditBtn       = document.getElementById('cancelEditBtn');
const viewTabs            = document.getElementById('viewTabs');
const authOverlay         = document.getElementById('authOverlay');
const loginForm           = document.getElementById('loginForm');
const loginBtn            = document.getElementById('loginBtn');
const logoutBtn           = document.getElementById('logoutBtn');
const loginError          = document.getElementById('loginError');
const rememberMe          = document.getElementById('rememberMe');
const mediaGrid           = document.getElementById('mediaGrid');
const fileInput           = document.getElementById('fileInput');
const uploadBtn           = document.getElementById('uploadBtn');
const mediaCategoryInput  = document.getElementById('mediaCategory');
const filterMediaCategory = document.getElementById('filterMediaCategory');
const uploadProgressBar   = document.getElementById('uploadProgressBar');
const uploadProgressDiv   = document.getElementById('uploadProgress');
const uploadStatus        = document.getElementById('uploadStatus');

/* ── State ──────────────────────────────────────────────── */
let allRegistrations = [];
let allMedia         = [];
let db               = null;
let storage          = null;
let editingId        = null;
let currentFilter    = 'all';
let regChart         = null;
let ministryChart    = null;

/* ── Data normaliser ─────────────────────────────────────
   Collapses mixed-case field names from Firestore & Sheets
   into a single consistent shape. Run once after fetch.
   ─────────────────────────────────────────────────────── */
function normalise(reg) {
  return {
    id:              reg.id || null,
    name:            reg.name         || reg.Name         || 'Unknown',
    phone:           reg.phone        || reg.Phone        || '—',
    location:        reg.location     || reg.Location     ||
                    reg.residence    || reg.Residence    || '—',
    birthDay:        reg.birthDay    || reg.birthday     || reg['Birth Day']    || '',
    birthMonth:      reg.birthMonth  || reg.birthmonth   || reg['Birth Month']  || '',
    firstTime:       String(reg.registered || reg.Registered ||
                         reg.firstTime  || reg.firsttime  || '').toLowerCase(),
    volunteering:    reg.volunteering || reg.Volunteering || '',
    referredBy:      reg.referredBy   || reg.referredby   || reg['Referred By']  || '—',
    whatsapp:        reg.whatsapp     || reg.Whatsapp     || '',
    timestamp:       reg.timestamp    || reg.date         || reg.DATE || reg.Timestamp || null,
    registrationType: reg.registrationType || reg.registrationtype || 'general',
    groomName:       reg.groomName    || '',
    brideName:       reg.brideName    || '',
    weddingDate:     reg.weddingDate  || '',
    baptismDate:     reg.baptismDate  || '',
    ageGroup:        reg.ageGroup     || '',
    deceasedName:    reg.deceasedName || '',
    funeralDate:     reg.funeralDate  || '',
    contactPerson:   reg.contactPerson|| '',
    counselingTopic: reg.counselingTopic|| '',
    preferredDate:   reg.preferredDate|| '',
    status:          reg.status       || 'pending',
    attendedDate:    reg.attendedDate || null,
    _source:         reg.id ? 'firestore' : 'sheets'
  };
}

/* ── Phone key helper (last 9 digits, digits only) ────── */
function phoneKey(phone) {
  return String(phone || '').replace(/\D/g, '').slice(-9);
}

/* ── Toast notifications ─────────────────────────────── */
function toast(msg, type = 'success', duration = 3500) {
  const container = document.getElementById('toastContainer');
  const el = document.createElement('div');
  el.className = `toast toast--${type}`;
  el.textContent = msg;
  container.appendChild(el);
  requestAnimationFrame(() => el.classList.add('toast--show'));
  setTimeout(() => {
    el.classList.remove('toast--show');
    el.addEventListener('transitionend', () => el.remove(), { once: true });
  }, duration);
}

/* ── Section tabs ────────────────────────────────────── */
document.querySelectorAll('.section-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.dashboard-section').forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.section).classList.add('active');
  });
});

/* ── Stat cards ──────────────────────────────────────── */
function updateStatCards(data) {
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

  document.getElementById('stat-total').textContent =
    data.length;
  document.getElementById('stat-firsttimers').textContent =
    data.filter(r => r.firstTime === 'yes').length;
  document.getElementById('stat-whatsapp').textContent =
    data.filter(r => r.whatsapp && r.whatsapp !== '—').length;
  document.getElementById('stat-week').textContent =
    data.filter(r => r.timestamp && new Date(r.timestamp) >= oneWeekAgo).length;
}

/* ── Password show / hide ────────────────────────────── */
document.getElementById('togglePassword').addEventListener('click', () => {
  const pwd = document.getElementById('loginPassword');
  const btn = document.getElementById('togglePassword');
  const isHidden = pwd.type === 'password';
  pwd.type = isHidden ? 'text' : 'password';
  btn.textContent = isHidden ? '🙈' : '👁';
  btn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
});

/* ── Authentication ──────────────────────────────────── */
window.addEventListener('load', () => {
  const saved = localStorage.getItem('church_admin_email');
  if (saved) {
    document.getElementById('loginEmail').value = saved;
    rememberMe.checked = true;
  }
  if (typeof firebase !== 'undefined') initAuth();
});

function initAuth() {
  authOverlay.style.display = 'flex';
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      authOverlay.style.display = 'none';
      if (!db)      db      = firebase.firestore();
      if (!storage) storage = firebase.storage();
      fetchRegistrations();
      fetchMedia();
    } else {
      authOverlay.style.display = 'flex';
      allRegistrations = [];
      allMedia         = [];
      renderTable([]);
      renderMedia([]);
    }
  });
}

loginForm.addEventListener('submit', async e => {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value.trim();
  const pass  = document.getElementById('loginPassword').value;
  loginError.style.display = 'none';

  if (!email || !pass) {
    loginError.textContent = 'Please enter email and password.';
    loginError.style.display = 'block';
    return;
  }

  rememberMe.checked
    ? localStorage.setItem('church_admin_email', email)
    : localStorage.removeItem('church_admin_email');

  try {
    loginBtn.disabled    = true;
    loginBtn.textContent = 'Logging in…';
    await firebase.auth().signInWithEmailAndPassword(email, pass);
  } catch (err) {
    loginError.textContent   = 'Login failed: ' + err.message;
    loginError.style.display = 'block';
  } finally {
    loginBtn.disabled    = false;
    loginBtn.textContent = 'Access Dashboard';
  }
});

logoutBtn.addEventListener('click', () => firebase.auth().signOut());

/* ── Registrations fetch ──────────────────────────────
   Deduplication strategy:
   1. Firestore is the source of truth.
   2. Google Sheets rows are merged in only if their
      phone key (last 9 digits) is not already present.
   This ensures NO duplicates in allRegistrations.
   ─────────────────────────────────────────────────── */
async function fetchRegistrations() {
  try {
    let fireData = [];

    if (db) {
      const snap = await db.collection('registrations').orderBy('timestamp', 'desc').get();
      fireData = snap.docs.map(doc => {
        const d = doc.data();
        d.id = doc.id;
        if (d.timestamp?.toDate) d.timestamp = d.timestamp.toDate();
        return normalise(d);
      });

      const progDoc = await db.collection('settings').doc('programs').get();
      if (progDoc.exists) loadProgramFields(progDoc.data());
    }

    // Merge Sheets data — skip any phone already in Firestore set
    const firestoreKeys = new Set(fireData.map(r => phoneKey(r.phone)));

    const res = await fetch(GET_DATA_API_URL);
    if (res.ok) {
      const sheetData = await res.json();
      sheetData.forEach(reg => {
        if (reg.name === 'SYSTEM_PROGRAMS') {
          if (fireData.length === 0) {
            try { loadProgramFields(JSON.parse(reg.location)); } catch {}
          }
          return;
        }
        const key = phoneKey(reg.phone || reg.Phone);
        if (!firestoreKeys.has(key)) {
          firestoreKeys.add(key);          // prevent Sheet duplicates too
          fireData.push(normalise(reg));
        }
      });
    }

    allRegistrations = fireData;
    renderTable(allRegistrations);
    displayBirthdayAlerts(allRegistrations);
    updateCharts(allRegistrations);
    updateStatCards(allRegistrations);
  } catch (err) {
    console.error('Fetch error:', err);
    tableBody.innerHTML = `<tr><td colspan="9" style="text-align:center;color:red;">Error loading data. ${err.message}</td></tr>`;
  }
}

function loadProgramFields(progs) {
  document.getElementById('prog-sunday').value        = progs.sunday        || '';
  document.getElementById('prog-monday').value        = progs.monday        || '';
  document.getElementById('prog-wednesday').value     = progs.wednesday     || 'Evening Glory 5pm-7pm';
  document.getElementById('prog-tue-thu').value       = progs.tueThu        || '';
  document.getElementById('prog-friday').value        = progs.friday        || '';
  document.getElementById('prog-custom').value        = progs.custom        || '';
  document.getElementById('prog-whatsapp-link').value = progs.whatsappLink  || '';
}

/* ── Birthday alerts ─────────────────────────────────── */
function displayBirthdayAlerts(data) {
  const upcoming = data
    .filter(r => isUpcomingBirthday(r.birthMonth, r.birthDay))
    .sort((a, b) =>
      getDaysUntilBirthday(a.birthMonth, a.birthDay) -
      getDaysUntilBirthday(b.birthMonth, b.birthDay)
    );

  if (!upcoming.length) { birthdayAlerts.style.display = 'none'; return; }

  birthdayAlerts.style.display = 'block';
  birthdayList.innerHTML = upcoming.map(r => {
    const days = getDaysUntilBirthday(r.birthMonth, r.birthDay);
    const label = days === 0 ? 'Today! 🎂' : `in ${days} day${days === 1 ? '' : 's'}`;
    return `
      <div class="birthday-alert-item">
        <strong>${r.name}</strong> — ${formatBirthday(r.birthMonth, r.birthDay)}
        <span class="birthday-tag">${label}</span>
        ${r.whatsapp ? `<br><small style="color:#666;">📱 ${r.whatsapp}</small>` : ''}
      </div>`;
  }).join('');
}

/* ── Programs save ───────────────────────────────────── */
saveProgramsBtn.addEventListener('click', async () => {
  const progs = {
    sunday:       document.getElementById('prog-sunday').value.trim(),
    monday:       document.getElementById('prog-monday').value.trim(),
    wednesday:    document.getElementById('prog-wednesday').value.trim(),
    tueThu:       document.getElementById('prog-tue-thu').value.trim(),
    friday:       document.getElementById('prog-friday').value.trim(),
    custom:       document.getElementById('prog-custom').value.trim()        || null,
    whatsappLink: document.getElementById('prog-whatsapp-link').value.trim() || null
  };

  saveProgramsBtn.disabled    = true;
  saveProgramsBtn.textContent = 'Saving…';

  try {
    if (db) await db.collection('settings').doc('programs').set(progs);

    const params = new URLSearchParams({
      name: 'SYSTEM_PROGRAMS', phone: '000',
      location: JSON.stringify(progs), whatsapp: '', prayers: ''
    });
    await fetch(SAVE_DATA_API_URL, { method: 'POST', body: params.toString() });

    toast('Schedule saved successfully!');
  } catch (err) {
    toast('Error saving schedule: ' + err.message, 'error');
  } finally {
    saveProgramsBtn.disabled    = false;
    saveProgramsBtn.textContent = 'Save Schedule';
  }
});

/* ── Charts ──────────────────────────────────────────── */
function updateCharts(data) {
  const today   = new Date();
  const last7   = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() - (6 - i));
    return d.toLocaleDateString('en-US', { weekday: 'short' });
  });
  const counts  = new Array(7).fill(0);
  data.forEach(r => {
    if (!r.timestamp) return;
    const diff = Math.floor((today - new Date(r.timestamp)) / 86400000);
    if (diff >= 0 && diff < 7) counts[6 - diff]++;
  });

  if (regChart) regChart.destroy();
  regChart = new Chart(document.getElementById('registrationChart').getContext('2d'), {
    type: 'line',
    data: {
      labels: last7,
      datasets: [{ label: 'New Registrations', data: counts,
        borderColor: '#27ae60', backgroundColor: 'rgba(39,174,96,0.1)',
        fill: true, tension: 0.4 }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  const m = { Ushering: 0, Choir: 0, Instruments: 0, Venue: 0, Other: 0 };
  data.forEach(r => {
    const v = r.volunteering.toLowerCase();
    if (v.includes('usher'))      m.Ushering++;
    if (v.includes('choir'))      m.Choir++;
    if (v.includes('instrument')) m.Instruments++;
    if (v.includes('venue'))      m.Venue++;
    if (v.includes('other'))      m.Other++;
  });

  if (ministryChart) ministryChart.destroy();
  ministryChart = new Chart(document.getElementById('ministryChart').getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: Object.keys(m),
      datasets: [{ data: Object.values(m),
        backgroundColor: ['#3498db','#e74c3c','#f1c40f','#9b59b6','#95a5a6'] }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { title: { display: true, text: 'Ministry Interests' } }
    }
  });
}

/* ── View tabs (ministry filter) ─────────────────────── */
viewTabs.addEventListener('click', e => {
  const tab = e.target.closest('.view-tab');
  if (!tab) return;
  document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
  tab.classList.add('active');
  currentFilter = tab.dataset.filter;
  renderTable(allRegistrations);
});

/* ── Search ──────────────────────────────────────────── */
searchBar.addEventListener('input', () => renderTable(allRegistrations));

/* ── Filtered slice (single source of truth) ─────────── */
function getFiltered(data) {
  let result = data;
  
  // Ministry filter
  if (currentFilter !== 'all') {
    result = result.filter(r =>
      r.volunteering.toLowerCase().includes(currentFilter.toLowerCase())
    );
  }
  
  // Event type filter
  const eventTypeFilter = document.getElementById('filterEventType')?.value;
  if (eventTypeFilter) {
    result = result.filter(r => r.registrationType === eventTypeFilter);
  }
  
  // Status filter (attendance)
  const statusFilter = document.getElementById('filterStatus')?.value;
  if (statusFilter) {
    result = result.filter(r => r.status === statusFilter);
  }
  
  // Date filter
  const dateFilter = document.getElementById('filterDate')?.value;
  if (dateFilter) {
    result = result.filter(r => {
      if (!r.timestamp) return false;
      const regDate = new Date(r.timestamp).toISOString().split('T')[0];
      return regDate === dateFilter;
    });
  }
  
  // Search filter
  const term = searchBar.value.toLowerCase();
  if (term) {
    result = result.filter(r =>
      r.name.toLowerCase().includes(term)     ||
      r.phone.toLowerCase().includes(term)    ||
      r.location.toLowerCase().includes(term)
    );
  }
  return result;
}

/* ── Render table ────────────────────────────────────── */
function renderTable(data) {
  const filtered = getFiltered(data);
  totalCount.textContent = `Total: ${filtered.length}`;

  if (!filtered.length) {
    tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:20px;">No records found.</td></tr>';
    return;
  }

  tableBody.innerHTML = '';
  filtered.forEach(r => {
    const dateStr = r.timestamp ? new Date(r.timestamp).toLocaleDateString() : 'N/A';
    const bday    = formatBirthday(r.birthMonth, r.birthDay);
    const isUp    = isUpcomingBirthday(r.birthMonth, r.birthDay);
    const volStr  = r.volunteering.length > 30 ? r.volunteering.substring(0, 30) + '…' : (r.volunteering || '—');

    const tr = document.createElement('tr');
    if (isUp) tr.classList.add('upcoming-birthday');

    tr.innerHTML = `
      <td>${dateStr}</td>
      <td><strong>${r.name}</strong></td>
      <td>${r.phone}</td>
      <td>${r.location}</td>
      <td>${bday}${isUp ? '<span class="birthday-tag">Soon!</span>' : ''}</td>
      <td>${r.firstTime === 'yes' ? '✓ Yes' : '—'}</td>
      <td title="${r.volunteering}" style="font-size:0.85rem;">${volStr}</td>
      <td>${r.referredBy}</td>
      <td class="actions">
        <div class="action-stack">
          <div class="action-row">
            ${r.whatsapp
              ? `<a href="https://wa.me/${r.whatsapp.replace(/\D/g,'')}" target="_blank" class="whatsapp-link" title="Chat on WhatsApp">WA</a>`
              : ''}
            <button onclick="sendTemplate('${r.name}','${r.phone}','welcome')" class="btn-tpl btn-tpl--welcome">Welcome</button>
            <button onclick="sendTemplate('${r.name}','${r.phone}','birthday')" class="btn-tpl btn-tpl--bday">Bday</button>
          </div>
          <div class="action-row">
            ${r._source === 'firestore'
              ? `<button onclick="editMember('${r.id}')" class="btn-edit">Edit</button>
                 <button onclick="deleteMember('${r.id}')" class="btn-del">Del</button>`
              : '<span class="sheet-only">Sheet-only</span>'}
          </div>
        </div>
      </td>`;
    tableBody.appendChild(tr);
  });
}

/* ── WhatsApp message templates ──────────────────────── */
window.sendTemplate = function(name, phone, type) {
  if (!phone || phone === '—') { toast('No phone number available.', 'warn'); return; }
  let clean = phone.replace(/\D/g, '');
  if (clean.startsWith('0'))   clean = '256' + clean.substring(1);
  else if (clean.length === 9) clean = '256' + clean;

  const msg = type === 'welcome'
    ? `Hello ${name}! It was a blessing to have you with us at Grace of Jesus Christ Ministries. We look forward to seeing you again. God bless you!`
    : `Happy Birthday ${name}! Grace of Jesus Christ Ministries celebrates you today. May the Lord shower you with His blessings and favor in this new year!`;

  window.open(`https://wa.me/${clean}?text=${encodeURIComponent(msg)}`, '_blank');
};

/* ── Edit member ─────────────────────────────────────── */
window.editMember = function(id) {
  const r = allRegistrations.find(r => r.id === id);
  if (!r) return;
  editingId = id;
  document.getElementById('edit-name').value         = r.name;
  document.getElementById('edit-phone').value        = r.phone;
  document.getElementById('edit-residence').value    = r.location;
  document.getElementById('edit-consent').value      = r.whatsapp;
  document.getElementById('edit-bday').value         = r.birthDay;
  document.getElementById('edit-bmonth').value       = r.birthMonth;
  document.getElementById('edit-registered').value   = r.firstTime || 'no';
  document.getElementById('edit-volunteering').value = r.volunteering;
  document.getElementById('edit-referred').value     = r.referredBy === '—' ? '' : r.referredBy;
  editModal.style.display = 'flex';
};

saveEditBtn.addEventListener('click', async () => {
  if (!editingId || !db) return;
  saveEditBtn.disabled    = true;
  saveEditBtn.textContent = 'Saving…';
  try {
    await db.collection('registrations').doc(editingId).update({
      name:         document.getElementById('edit-name').value.trim(),
      phone:        document.getElementById('edit-phone').value.trim(),
      location:     document.getElementById('edit-residence').value.trim(),
      residence:    document.getElementById('edit-residence').value.trim(),
      whatsapp:     document.getElementById('edit-consent').value.trim(),
      birthDay:     document.getElementById('edit-bday').value,
      birthMonth:   document.getElementById('edit-bmonth').value,
      registered:   document.getElementById('edit-registered').value,
      volunteering: document.getElementById('edit-volunteering').value.trim(),
      referredBy:   document.getElementById('edit-referred').value.trim()
    });
    editModal.style.display = 'none';
    editingId = null;
    toast('Member updated successfully!');
    fetchRegistrations();
  } catch (err) {
    toast('Error updating member: ' + err.message, 'error');
  } finally {
    saveEditBtn.disabled    = false;
    saveEditBtn.textContent = 'Save Changes';
  }
});

cancelEditBtn.addEventListener('click', () => {
  editModal.style.display = 'none';
  editingId = null;
});

/* ── Delete member ───────────────────────────────────── */
window.deleteMember = async function(id) {
  if (!db || !confirm('Delete this registration? This cannot be undone.')) return;
  try {
    await db.collection('registrations').doc(id).delete();
    toast('Member deleted.');
    fetchRegistrations();
  } catch (err) {
    toast('Error deleting member: ' + err.message, 'error');
  }
};

/* ── Export CSV ──────────────────────────────────────── */
exportBtn.addEventListener('click', () => {
  const filtered = getFiltered(allRegistrations);
  if (!filtered.length) { toast('No data to export.', 'warn'); return; }

  const headers = ['Date','Name','Phone','Residence','Birth Month','Birth Day','Registered?','WhatsApp','Volunteering','Referred By'];
  const rows    = filtered.map(r => {
    const dateStr = r.timestamp ? new Date(r.timestamp).toLocaleDateString() : 'N/A';
    return [dateStr, r.name, r.phone, r.location, r.birthMonth, r.birthDay,
            r.firstTime, r.whatsapp, r.volunteering, r.referredBy]
      .map(v => `"${String(v ?? '').replace(/"/g, '""')}"`);
  });

  const csv  = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url  = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `Church_Registrations_${new Date().toLocaleDateString()}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
});

/* ── Media management ────────────────────────────────── */
async function fetchMedia() {
  if (!db) return;
  try {
    const snap = await db.collection('media').orderBy('timestamp', 'desc').get();
    allMedia   = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderMedia(allMedia);
  } catch (err) {
    console.error('Error fetching media:', err);
    mediaGrid.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:red;">Error loading media library.</div>';
  }
}

function renderMedia(data) {
  const filter   = filterMediaCategory.value;
  const filtered = filter === 'all' ? data : data.filter(m => m.category === filter);

  if (!filtered.length) {
    mediaGrid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:#777;">No images found in this category.</div>';
    return;
  }

  mediaGrid.innerHTML = filtered.map(item => `
    <div class="media-item">
      <span class="category-badge">${item.category || 'General'}</span>
      <img src="${item.url}" alt="Church photo" loading="lazy"
           onclick="window.open('${item.url}', '_blank')">
      <div class="media-item__name">${item.name}</div>
      <div class="media-actions-inline">
        <button class="btn-download" onclick="downloadImage('${item.url}','${item.name}')">Download</button>
        <button class="btn-delete-media" onclick="deleteMedia('${item.id}','${item.storagePath}')">Delete</button>
      </div>
    </div>`).join('');
}

window.downloadImage = async function(url, name) {
  try {
    const res  = await fetch(url);
    const blob = await res.blob();
    const bUrl = URL.createObjectURL(blob);
    const link = Object.assign(document.createElement('a'), { href: bUrl, download: name || 'image.jpg' });
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
    URL.revokeObjectURL(bUrl);
  } catch {
    window.open(url, '_blank');
  }
};

window.deleteMedia = async function(id, storagePath) {
  if (!confirm('Delete this image? Download it first if you need it.')) return;
  try {
    if (storagePath) await storage.ref(storagePath).delete();
    await db.collection('media').doc(id).delete();
    fetchMedia();
    toast('Image deleted.');
  } catch (err) {
    toast('Error deleting image: ' + err.message, 'error');
  }
};

uploadBtn.addEventListener('click', async () => {
  const files = fileInput.files;
  if (!files.length) { toast('Please select images first.', 'warn'); return; }

  const category = mediaCategoryInput.value;
  uploadBtn.disabled           = true;
  uploadProgressDiv.style.display = 'block';
  uploadStatus.style.display   = 'block';
  let ok = 0, fail = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    if (file.size > 5 * 1024 * 1024) {
      toast(`Skipping ${file.name}: max 5 MB.`, 'warn');
      fail++; continue;
    }
    const ts          = Date.now();
    const safeName    = file.name.replace(/[^a-z0-9.]/gi, '_').toLowerCase();
    const storagePath = `media/${category}/${ts}_${safeName}`;
    const ref         = storage.ref(storagePath);

    try {
      uploadStatus.textContent = `Uploading ${file.name} (${i + 1}/${files.length})…`;
      const task = ref.put(file);
      task.on('state_changed', snap => {
        uploadProgressBar.style.width = ((snap.bytesTransferred / snap.totalBytes) * 100) + '%';
      });
      await task;
      const url = await ref.getDownloadURL();
      await db.collection('media').add({
        name: file.name, url, storagePath, category,
        timestamp: firebase.firestore.FieldValue.serverTimestamp()
      });
      ok++;
    } catch (err) {
      console.error('Upload error:', err);
      fail++;
    }
  }

  uploadBtn.disabled              = false;
  uploadProgressDiv.style.display = 'none';
  uploadProgressBar.style.width   = '0%';
  uploadStatus.style.display      = 'none';
  fileInput.value                 = '';
  document.getElementById('uploadText').textContent = 'Click to select photos';

  if (ok > 0) { fetchMedia(); toast(`Uploaded ${ok} image(s).${fail ? ` (${fail} failed)` : ''}`); }
  else if (fail > 0) toast('All uploads failed. Check console.', 'error');
});

filterMediaCategory.addEventListener('change', () => renderMedia(allMedia));

fileInput.addEventListener('change', e => {
  const count = e.target.files.length;
  document.getElementById('uploadText').textContent =
    count > 0 ? `${count} file(s) selected` : 'Click to select photos';
});
