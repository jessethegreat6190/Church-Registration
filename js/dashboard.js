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

let allMembers = [];
let allRegistrations = [];
let isLoggedIn = false;
let importCandidates = [];
let importBlockCount = 1;
let currentBulkWaMembers = [];

// Church details used to build the WhatsApp thank-you / welcome message.
const churchPrograms = {
  sunday: "8:00 AM",
  monday: "6:00 AM - 7:00 AM",
  wednesday: "5:00 PM - 7:00 PM",
  tueThu: "7:00 AM - 3:00 PM",
  friday: "3:00 PM, 2:30 AM, 3:00 AM (Not overnight)",
  baptism: "Baptism: date to be announced",
  crossover: "31st Cross Over Night: 31 Dec 2026, 9:00 PM - 4:00 AM",
  contacts: "0730 938085 / 0730 909434",
  whatsappLink: "https://chat.whatsapp.com/Bd2AT6h45KgKMTUwCod89h",
  youtubeVideo: "https://youtu.be/NfUe8Z7xj6U?si=aYQc4RO2O9vNDloG",
  mapsLink: "https://maps.google.com/?q=Grace+of+Jesus+Christ+Ministries,+Kitintale,+Luzira,+Kampala"
};

const WEEKLY_VERSES = [
  "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you. (Numbers 6:24-25)",
  "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you. (Jeremiah 29:11)",
  "The Lord is my shepherd; I shall not want. He makes me lie down in green pastures. (Psalm 23:1-2)",
  "Trust in the Lord with all your heart and lean not on your own understanding. (Proverbs 3:5)",
  "But those who hope in the Lord will renew their strength. They will soar on wings like eagles. (Isaiah 40:31)",
  "The Lord your God is with you, the Mighty Warrior who saves. He will take great delight in you. (Zephaniah 3:17)",
  "I can do all this through him who gives me strength. (Philippians 4:13)",
  "And my God will meet all your needs according to the riches of his glory in Christ Jesus. (Philippians 4:19)",
  "Fear not, for I am with you; be not dismayed, for I am your God. I will strengthen you and help you. (Isaiah 41:10)",
  "The Lord will fight for you; you need only to be still. (Exodus 14:14)",
  "Ask and it will be given to you; seek and you will find; knock and the door will be opened to you. (Matthew 7:7)",
  "Cast all your anxiety on him because he cares for you. (1 Peter 5:7)",
  "The peace of God, which transcends all understanding, will guard your hearts and your minds. (Philippians 4:7)",
  "Commit to the Lord whatever you do, and he will establish your plans. (Proverbs 16:3)",
  "The Lord is good, a refuge in times of trouble. He cares for those who trust in him. (Nahum 1:7)",
  "Draw near to God and He will draw near to you. (James 4:8)",
  "The Lord is my light and my salvation—whom shall I fear? (Psalm 27:1)",
  "He gives strength to the weary and increases the power of the weak. (Isaiah 40:29)",
  "Delight yourself in the Lord, and he will give you the desires of your heart. (Psalm 37:4)",
  "The name of the Lord is a fortified tower; the righteous run to it and are safe. (Proverbs 18:10)",
  "Give thanks to the Lord, for he is good; his love endures forever. (Psalm 107:1)",
  "I will never leave you nor forsake you. (Hebrews 13:5)",
  "The Lord is close to the brokenhearted and saves those who are crushed in spirit. (Psalm 34:18)",
  "In all these things we are more than conquerors through him who loved us. (Romans 8:37)",
  "But seek first his kingdom and his righteousness, and all these things will be given to you as well. (Matthew 6:33)",
  "Everything is possible for one who believes. (Mark 9:23)",
  "He restores my soul. He leads me in paths of righteousness for his name's sake. (Psalm 23:3)",
  "God is our refuge and strength, an ever-present help in trouble. (Psalm 46:1)",
  "The Lord is faithful, and he will strengthen you and protect you from the evil one. (2 Thessalonians 3:3)",
  "The joy of the Lord is your strength. (Nehemiah 8:10)",
  "Blessed is the one who trusts in the Lord, whose confidence is in him. (Jeremiah 17:7)",
  "Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here! (2 Corinthians 5:17)",
  "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up. (Galatians 6:9)",
  "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go. (Joshua 1:9)",
  "God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. (John 3:16)",
  "The Lord is my strength and my shield; my heart trusts in him, and he helps me. (Psalm 28:7)"
];

function getWeeklyVerse() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const dayOfYear = Math.floor((now - start) / (1000 * 60 * 60 * 24));
  return WEEKLY_VERSES[Math.floor(dayOfYear / 2) % WEEKLY_VERSES.length];
}

function buildProgramsText() {
  let text = 'Church Programs:\n' +
    '• Sunday Services: ' + churchPrograms.sunday + '\n' +
    '• Monday Kyoto Prayers: ' + churchPrograms.monday + '\n' +
    '• Wednesday Evening Glory: ' + churchPrograms.wednesday + '\n' +
    '• Tue & Thu Counseling: ' + churchPrograms.tueThu + '\n' +
    '• Friday Night Prayers: ' + churchPrograms.friday;
  text += '\n• ' + churchPrograms.baptism + ' — register: https://church-registration-grace.web.app/baptism-registration.html';
  text += '\n• ' + churchPrograms.crossover;
  return text;
}

// Escape user-provided text before inserting it into innerHTML.
function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Escape a string for safe use inside a JavaScript string literal (onclick handlers).
function escapeJs(value) {
  return String(value == null ? '' : value)
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r');
}

// Registrations are stored with the phone number as the document ID, so
// Firestore returns them in ID order. Sort by date so the newest ones show
// first in the dashboard, reports and members tables.
function regTime(r) {
  const t = r.timestamp || r.createdAt;
  if (!t) return 0;
  if (typeof t.toDate === 'function') return t.toDate().getTime();
  const ms = new Date(t).getTime();
  return isNaN(ms) ? 0 : ms;
}

function sortNewestFirst(list) {
  return list.slice().sort((a, b) => regTime(b) - regTime(a));
}

function regDate(r) {
  const ms = regTime(r);
  return ms ? new Date(ms).toLocaleDateString() : '-';
}

/* ─── WHATSAPP PENDING HELPERS ─── */
// A member is pending until an admin marks their welcome message as sent.
function isWhatsAppPending(m) {
  return !m || m.welcomeSent !== true;
}

// Entries added through the importer keep a marker so the dashboard can
// highlight them as brand-new.
function isImportedMember(m) {
  return !!m && (m.source === 'import' || m.imported === true);
}

function isValidWhatsAppPhone(phone) {
  return /^[76]\d{8}$/.test(cleanPhone(phone));
}

function waBadge(m) {
  return isWhatsAppPending(m)
    ? '<span class="wa-badge pending"><i class="fab fa-whatsapp"></i> WhatsApp pending</span>'
    : '<span class="wa-badge sent"><i class="fab fa-whatsapp"></i> Sent</span>';
}

document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

var savedEmail = localStorage.getItem('adminEmail');
var rememberEmail = localStorage.getItem('rememberEmail');
if (savedEmail && rememberEmail !== 'false') {
  document.getElementById('loginEmail').value = savedEmail;
  document.getElementById('rememberEmail').checked = true;
} else {
  document.getElementById('rememberEmail').checked = false;
}

// Remove the auto-redirect timer so the admin can log in without being rushed.
// The login modal is shown when "Admin Login" is clicked, and dashboard
// sections check isLoggedIn before loading data.
let wasAdmin = false;

auth.onAuthStateChanged(function(user) {
  if (user && user.uid === ADMIN_UID) {
    wasAdmin = true;
    isLoggedIn = true;
    document.getElementById('adminBtn').textContent = 'Logout';
    document.getElementById('loginError').style.display = 'none';
    hideLoginModal();
    // Load the dashboard immediately after login. Without this the page stays
    // on the default "0 / Loading..." state until another sidebar item is clicked.
    const dashboardSection = document.getElementById('section-dashboard');
    if (dashboardSection && dashboardSection.classList.contains('active')) loadDashboard();
  } else if (user && user.uid !== ADMIN_UID) {
    auth.signOut();
    const errEl = document.getElementById('loginError');
    if (errEl) {
      errEl.textContent = 'Access denied. You are not authorized as admin.';
      errEl.style.display = 'block';
    }
  } else {
    isLoggedIn = false;
  }
});

function showSection(section) {
  if (!isLoggedIn) { showLoginModal(); return; }
  document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
  document.getElementById('section-' + section).classList.add('active');
  document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
  const activeItem = document.querySelector('[data-section="' + section + '"]');
  if (activeItem) activeItem.classList.add('active');
  
  if (section === 'dashboard') loadDashboard();
  if (section === 'members') loadMembers();
  if (section === 'events') loadEvents();
  if (section === 'communications') loadAnnouncements();
  if (section === 'programs') loadPrograms();
}

function showLoginModal() { document.getElementById('loginModal').classList.add('show'); }
function hideLoginModal() { document.getElementById('loginModal').classList.remove('show'); }

document.getElementById('loginForm').onsubmit = function(e) {
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
    .then(function(userCred) {
      if (userCred.user.uid !== ADMIN_UID) {
        auth.signOut();
        errorEl.textContent = 'Access denied. You are not authorized as admin.';
        errorEl.style.display = 'block';
      }
    })
    .catch(function(err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
    });
};

function handleAdminBtn() {
  if (isLoggedIn) {
    auth.signOut();
  } else {
    showLoginModal();
  }
}

async function loadDashboard() {
  try {
    const snapshot = await db.collection('registrations').get();
    allRegistrations = snapshot.docs.map(d => {
      const data = d.data();
      return {
        id: d.id,
        ...data,
        status: data.status || 'active'
      };
    });
    allRegistrations = sortNewestFirst(allRegistrations);
    allMembers = allRegistrations.slice();
    const newRegs = allRegistrations.filter(r => r.status === 'new' || r.status === 'pending');
    const pendingWa = allRegistrations.filter(isWhatsAppPending);

    document.getElementById('totalMembers').textContent = allRegistrations.length;
    document.getElementById('newRegistrations').textContent = newRegs.length;
    document.getElementById('whatsappPending').textContent = pendingWa.length;

    document.getElementById('recentRegistrations').innerHTML = allRegistrations.slice(0, 5).map(r => {
      const imported = isImportedMember(r);
      const pending = isWhatsAppPending(r);
      return '<tr class="' + (pending ? 'row-pending-wa' : '') + (imported ? ' row-imported' : '') + '">' +
        '<td>' + (formatName(r.name) || '-') + (imported ? ' <span class="tag-new">New</span>' : '') + '</td>' +
        '<td>' + (r.phone || '-') + '</td>' +
        '<td>' + (r.department || r.registrationType || '-') + '</td>' +
        '<td>' + regDate(r) + '</td>' +
        '<td>' + waBadge(r) + '</td></tr>';
    }).join('');

    const attendance = JSON.parse(localStorage.getItem('today_attendance') || '[]');
    const rate = allRegistrations.length > 0 ? Math.round((attendance.length / allRegistrations.length) * 100) : 0;
    document.getElementById('attendanceRate').textContent = rate + '%';
    document.getElementById('upcomingEvents').textContent = '5';
    updateWelcomePendingCount();
  } catch (e) {
    console.error('Dashboard load error:', e);
    const tbody = document.getElementById('recentRegistrations');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#e74c3c">Could not load registrations: ' + escapeHtml(e.message) + '</td></tr>';
  }
}

async function loadMembers() {
  try {
    const snapshot = await db.collection('registrations').get();
    allMembers = snapshot.docs.map(d => {
      const data = d.data();
      return { id: d.id, ...data, status: data.status || 'active' };
    });
    allMembers = sortNewestFirst(allMembers);
    applyMemberFilters();
    updateWelcomePendingCount();
  } catch (e) {
    console.error('Error loading members:', e);
    document.getElementById('membersTable').innerHTML = '<tr><td colspan="5" style="text-align:center;color:#e74c3c">Error loading members</td></tr>';
  }
}

function renderMembers(members) {
  const tbody = document.getElementById('membersTable');
  if (!members.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#6c757d">No members match the current filters.</td></tr>';
  } else {
    tbody.innerHTML = members.map(m => {
      const id = escapeHtml(m.id);
      const pending = isWhatsAppPending(m);
      const imported = isImportedMember(m);
      const rowClass = (pending ? 'row-pending-wa' : '') + (imported ? ' row-imported' : '');
      const phoneWarning = isValidWhatsAppPhone(m.phone)
        ? ''
        : ' <span style="color:#c0392b;font-size:11px;" title="This is not a valid Uganda mobile number for WhatsApp">&#9888;</span>';
      return '<tr class="' + rowClass + '">' +
        '<td><input type="checkbox" class="attend-checkbox" data-phone="' + cleanPhone(m.phone) + '"> ' +
          (formatName(m.name) || '-') +
          (imported ? ' <span class="tag-new">New</span>' : '') +
          ' ' + waBadge(m) +
        '</td>' +
        '<td>' + (m.phone || '-') + phoneWarning + '</td>' +
        '<td>' + (m.department || '-') + '</td>' +
        '<td>' + regDate(m) + '</td>' +
        '<td class="member-actions">' +
          '<button class="btn-icon btn-edit" data-action="edit" data-id="' + id + '" title="Edit member"><i class="fas fa-pen"></i></button>' +
          '<button class="btn-icon btn-wa' + (pending ? '' : ' sent') + '" data-action="welcome" data-id="' + id + '" title="Open WhatsApp with the thank-you message"><i class="fab fa-whatsapp"></i> ' + (pending ? 'Send' : 'Sent') + '</button>' +
          '<button class="btn-icon btn-delete" data-action="delete" data-id="' + id + '" title="Delete member"><i class="fas fa-trash"></i></button>' +
        '</td>' +
      '</tr>';
    }).join('');
  }

  let saveBtn = document.getElementById('saveAttendanceBtn');
  if (!saveBtn) {
    saveBtn = document.createElement('button');
    saveBtn.id = 'saveAttendanceBtn';
    saveBtn.className = 'btn-primary';
    saveBtn.style.marginTop = '15px';
    saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Attendance';
    saveBtn.onclick = saveAttendance;
    tbody.parentElement.appendChild(saveBtn);
  }
}

// One delegated listener so the action buttons keep working after every
// search/filter re-render.
document.getElementById('membersTable').addEventListener('click', function(e) {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;
  const id = btn.dataset.id;
  if (btn.dataset.action === 'edit') editMember(id);
  else if (btn.dataset.action === 'delete') deleteMember(id);
  else if (btn.dataset.action === 'welcome') sendMemberWelcome(id);
});

function editMember(id) {
  if (!isLoggedIn) { showLoginModal(); return; }
  const m = allMembers.find(x => x.id === id);
  if (!m) return;
  document.getElementById('editMemberId').value = id;
  document.getElementById('editMemberName').value = m.name || '';
  document.getElementById('editMemberPhone').value = m.phone || '';
  document.getElementById('editMemberDepartment').value = m.department || '';
  document.getElementById('editMemberLocation').value = m.location || '';
  document.getElementById('editMemberModal').classList.add('show');
}

function hideEditMemberModal() {
  document.getElementById('editMemberModal').classList.remove('show');
}

document.getElementById('editMemberForm').onsubmit = async function(e) {
  e.preventDefault();
  const id = document.getElementById('editMemberId').value;
  const name = formatName(document.getElementById('editMemberName').value);
  const phone = document.getElementById('editMemberPhone').value.trim();
  const department = document.getElementById('editMemberDepartment').value;
  const location = document.getElementById('editMemberLocation').value.trim();
  if (!name || !phone) { alert('Name and phone are required.'); return; }
  try {
    const newId = cleanPhone(phone);
    if (newId && newId !== id) {
      // Phone changed: move the record to the new phone-based document ID.
      const oldDoc = await db.collection('registrations').doc(id).get();
      const data = oldDoc.exists ? oldDoc.data() : {};
      await db.collection('registrations').doc(newId).set({
        ...data, name, phone, department, location, whatsapp: phone, cleanPhone: newId
      });
      await db.collection('registrations').doc(id).delete();
    } else {
      await db.collection('registrations').doc(id).update({
        name, phone, department, location, whatsapp: phone, cleanPhone: newId
      });
    }
    hideEditMemberModal();
    await loadMembers();
    await loadDashboard();
  } catch (err) {
    alert('Could not save changes: ' + err.message);
  }
};

async function deleteMember(id) {
  if (!isLoggedIn) { showLoginModal(); return; }
  const m = allMembers.find(x => x.id === id);
  const label = m ? (formatName(m.name) || m.phone || id) : id;
  if (!confirm('Delete ' + label + '? This cannot be undone.')) return;
  try {
    await db.collection('registrations').doc(id).delete();
    allMembers = allMembers.filter(x => x.id !== id);
    allRegistrations = allRegistrations.filter(x => x.id !== id);
    applyMemberFilters();
    loadDashboard();
  } catch (err) {
    alert('Could not delete: ' + err.message);
  }
}

// Open WhatsApp with the same thank-you / welcome message used after a normal
// registration, then mark the member as welcomed.
async function sendMemberWelcome(id) {
  if (!isLoggedIn) { showLoginModal(); return; }
  const m = allMembers.find(x => x.id === id);
  if (!m) return;
  const rawPhone = String(m.phone || '').replace(/\D/g, '');
  if (!rawPhone) { alert('This member has no phone number.'); return; }
  if (!isValidWhatsAppPhone(m.phone) &&
      !confirm('This phone number does not look like a valid Uganda mobile number for WhatsApp:\n' + m.phone + '\n\nTry to open WhatsApp anyway?')) {
    return;
  }
  const intlPhone = rawPhone.startsWith('0')
    ? '256' + rawPhone.substring(1)
    : (rawPhone.length === 9 ? '256' + rawPhone : rawPhone);

  const blessing = getWeeklyVerse();
  let welcome = `Hello ${formatName(m.name) || 'friend'}! Thank you for registering at Grace of Jesus Christ Ministries.\n\n` +
    `*A Blessing for you:* "${blessing}"\n\n${buildProgramsText()}`;
  welcome += '\n\nJoin our WhatsApp Group: ' + churchPrograms.whatsappLink;
  welcome += '\n\nChurch Contacts (WhatsApp):\n• 0730 938085\n• 0730 909434';
  welcome += '\n\nChurch Location:\nKitintale, Kasoli stage, Old Port Bell Road, Luzira, Kampala';
  welcome += '\nOpen in Google Maps: ' + churchPrograms.mapsLink;
  welcome += '\n\nSubscribe to our YouTube: https://www.youtube.com/@encounter_GJM';
  welcome += '\n\nWatch our latest message: ' + churchPrograms.youtubeVideo;
  welcome += '\n\n*An encounter with the Holy Spirit*';

  // Open before awaiting so the browser treats it as a user gesture.
  window.open('https://wa.me/' + intlPhone + '?text=' + encodeURIComponent(welcome), '_blank');

  try {
    await db.collection('registrations').doc(id).update({
      welcomeSent: true,
      welcomeSentAt: firebase.firestore.FieldValue.serverTimestamp(),
      whatsappStatus: 'on'
    });
    m.welcomeSent = true;
    applyMemberFilters();
    updateWelcomePendingCount();
  } catch (err) {
    console.warn('Could not mark welcome as sent:', err.message);
  }
}

// Send the thank-you / welcome WhatsApp message to ALL members (including
// those already marked welcomed). Shows everyone so you can see exactly who
// has been sent and who hasn't. One click per member opens one WhatsApp tab —
// browsers block automatic multi-tab opening.
async function sendWelcomeToAll() {
  if (!isLoggedIn) { showLoginModal(); return; }
  const all = allMembers.slice(); // all members, not filtered
  if (!all.length) {
    alert('No members found.');
    return;
  }
  showBulkWaModal(all);
}

// Send WhatsApp messages only to members who have not received one yet.
// Pass onlyImported=true right after an import to target just the new entries.
function sendPendingWelcomes(onlyImported) {
  if (!isLoggedIn) { showLoginModal(); return; }
  const pending = allMembers.filter(m => isWhatsAppPending(m) && (!onlyImported || isImportedMember(m)));
  if (!pending.length) {
    alert(onlyImported
      ? 'All imported members have already received a WhatsApp message.'
      : 'All members have already received a WhatsApp message.');
    return;
  }
  showBulkWaModal(pending);
}

// Show the bulk WhatsApp sender modal with ALL members.
// Each row shows a "Send" button if not yet welcomed, or "Sent" if already done.
function showBulkWaModal(members) {
  const list = document.getElementById('bulkWaList');
  if (!list) return;
  list.innerHTML = '';
  currentBulkWaMembers = members.slice();

  if (members.length === 0) {
    list.innerHTML = '<div style="text-align:center;color:#6c757d;">No members found.</div>';
    return;
  }

  const unwelcomed = members.filter(isWhatsAppPending).length;
  const welcomed = members.filter(m => !isWhatsAppPending(m)).length;

  // Header summary
  const header = document.createElement('div');
  header.style.cssText = 'display:flex; justify-content:space-between; padding:6px 8px; background:var(--gray-100); border-radius:var(--radius-sm); margin-bottom:10px; font-size:13px; font-weight:600;';
  header.innerHTML =
    '<span>Total: ' + members.length + ' members</span>' +
    '<span style="color:var(--success);">✅ ' + welcomed + ' Sent</span>' +
    '<span style="color:var(--danger);">⏳ ' + unwelcomed + ' Pending</span>';
  list.appendChild(header);

  members.forEach(m => {
    const rawPhone = String(m.phone || '').replace(/\D/g, '');
    const intlPhone = rawPhone.startsWith('0')
      ? '256' + rawPhone.substring(1)
      : (rawPhone.length === 9 ? '256' + rawPhone : rawPhone);

    const blessing = getWeeklyVerse();
    let welcome = `Hello ${formatName(m.name) || 'friend'}! Thank you for registering at Grace of Jesus Christ Ministries.\n\n` +
      `*A Blessing for you:* "${blessing}"\n\n${buildProgramsText()}`;
    welcome += '\n\nJoin our WhatsApp Group: ' + churchPrograms.whatsappLink;
    welcome += '\n\nChurch Contacts (WhatsApp):\n• 0730 938085\n• 0730 909434';
    welcome += '\n\nChurch Location:\nKitintale, Kasoli stage, Old Port Bell Road, Luzira, Kampala';
  welcome += '\nOpen in Google Maps: ' + churchPrograms.mapsLink;
    welcome += '\n\nSubscribe to our YouTube: https://www.youtube.com/@encounter_GJM';
  welcome += '\n\nWatch our latest message: ' + churchPrograms.youtubeVideo;
    welcome += '\n\n*An encounter with the Holy Spirit*';

    const waUrl = 'https://wa.me/' + intlPhone + '?text=' + encodeURIComponent(welcome);
    const isSent = !isWhatsAppPending(m);
    const validPhone = isValidWhatsAppPhone(m.phone);
    const imported = isImportedMember(m);

    const row = document.createElement('div');
    row.style.cssText = 'display:flex; justify-content:space-between; align-items:center; padding:8px 6px; border-bottom:1px solid #eee; gap:10px;' + (isSent ? ' opacity:0.6;' : '');
    row.innerHTML =
      '<div style="flex:1; min-width:0;">' +
      '<div style="font-weight:600;' + (isSent ? ' text-decoration:line-through;' : '') + '">' + escapeHtml(formatName(m.name) || '-') +
        (imported ? ' <span class="tag-new">New</span>' : '') + '</div>' +
      '<div style="font-size:12px;color:#6c757d;">' + escapeHtml(m.phone || '-') + ' • ' + escapeHtml(m.location || '-') +
        (validPhone ? '' : ' <span style="color:#c0392b;font-weight:600;">⚠ not a valid WhatsApp mobile</span>') + '</div>' +
      '</div>' +
      '<div style="display:flex; align-items:center; gap:6px;">' +
      (isSent
        ? '<span style="font-size:11px;color:var(--success); font-weight:600;">Sent</span>'
        : '<button onclick="sendBulkWa(\'' + escapeJs(m.id) + '\', \'' + escapeJs(formatName(m.name) || '-') + '\', \'' + escapeJs(m.phone || '-') + '\')" class="btn-icon btn-wa" style="padding:5px 10px;font-size:11px;"><i class="fab fa-whatsapp"></i> Send</button>') +
      '</div>';

    list.appendChild(row);
  });

  document.getElementById('bulkWaModal').classList.add('show');
}

function hideBulkWaModal() {
  document.getElementById('bulkWaModal').classList.remove('show');
}

// Open WhatsApp for one member and mark them as welcomed.
async function sendBulkWa(id, name, phone) {
  const rawPhone = String(phone || '').replace(/\D/g, '');
  if (!rawPhone) { alert('This member has no phone number.'); return; }
  if (!isValidWhatsAppPhone(phone) &&
      !confirm('This phone number does not look like a valid Uganda mobile number for WhatsApp:\n' + phone + '\n\nTry to open WhatsApp anyway?')) {
    return;
  }
  const intlPhone = rawPhone.startsWith('0')
    ? '256' + rawPhone.substring(1)
    : (rawPhone.length === 9 ? '256' + rawPhone : rawPhone);

  const blessing = getWeeklyVerse();
  let welcome = `Hello ${name || 'friend'}! Thank you for registering at Grace of Jesus Christ Ministries.\n\n` +
    `*A Blessing for you:* "${blessing}"\n\n${buildProgramsText()}`;
  welcome += '\n\nJoin our WhatsApp Group: ' + churchPrograms.whatsappLink;
  welcome += '\n\nChurch Contacts (WhatsApp):\n• 0730 938085\n• 0730 909434';
  welcome += '\n\nChurch Location:\nKitintale, Kasoli stage, Old Port Bell Road, Luzira, Kampala';
  welcome += '\nOpen in Google Maps: ' + churchPrograms.mapsLink;
  welcome += '\n\nSubscribe to our YouTube: https://www.youtube.com/@encounter_GJM';
  welcome += '\n\nWatch our latest message: ' + churchPrograms.youtubeVideo;
  welcome += '\n\n*An encounter with the Holy Spirit*';

  window.open('https://wa.me/' + intlPhone + '?text=' + encodeURIComponent(welcome), '_blank');

  try {
    await db.collection('registrations').doc(id).update({
      welcomeSent: true,
      welcomeSentAt: firebase.firestore.FieldValue.serverTimestamp(),
      whatsappStatus: 'on'
    });
    // Update local copy and refresh the members table + modal
    const idx = allMembers.findIndex(m => m.id === id);
    if (idx >= 0) {
      allMembers[idx].welcomeSent = true;
      applyMemberFilters();
      updateWelcomePendingCount();
    }
    // Refresh the bulk modal list if still open (keeps the current filter)
    const modal = document.getElementById('bulkWaModal');
    if (modal && modal.classList.contains('show')) {
      showBulkWaModal(currentBulkWaMembers);
    }
  } catch (err) {
    console.warn('Could not mark welcome as sent:', err.message);
    alert('WhatsApp opened but could not mark as welcomed: ' + err.message);
  }
}

// Mark all pending members as welcomed without opening WhatsApp.
async function markAllWelcomed() {
  if (!isLoggedIn) { showLoginModal(); return; }
  const pending = allMembers.filter(isWhatsAppPending);
  if (!pending.length) {
    alert('All members have already been welcomed.');
    hideBulkWaModal();
    return;
  }
  if (!confirm('Mark all ' + pending.length + ' member(s) as welcomed without opening WhatsApp?')) return;

  for (const m of pending) {
    try {
      await db.collection('registrations').doc(m.id).update({
        welcomeSent: true,
        welcomeSentAt: firebase.firestore.FieldValue.serverTimestamp(),
        whatsappStatus: 'on'
      });
      m.welcomeSent = true;
    } catch (err) { console.warn('Could not mark ' + m.id, err.message); }
  }
  applyMemberFilters();
  updateWelcomePendingCount();
  hideBulkWaModal();
  alert('All ' + pending.length + ' members marked as welcomed.');
}

// Reset all members to unwelcomed so you can send welcome messages again.
async function resetAllWelcomes() {
  if (!isLoggedIn) { showLoginModal(); return; }
  const allWelcomed = allMembers.filter(m => m.welcomeSent);
  if (!allWelcomed.length) {
    alert('No members are marked as welcomed.');
    return;
  }
  if (!confirm('Reset ALL ' + allWelcomed.length + ' member(s) to unwelcomed? You can then send welcome messages again.')) return;

  for (const m of allWelcomed) {
    try {
      await db.collection('registrations').doc(m.id).update({
        welcomeSent: false,
        whatsappStatus: 'unknown'
      });
      m.welcomeSent = false;
    } catch (err) { console.warn('Could not reset ' + m.id, err.message); }
  }
  applyMemberFilters();
  updateWelcomePendingCount();
  hideBulkWaModal();
  alert('All ' + allWelcomed.length + ' members reset to unwelcomed. Open Bulk WhatsApp Sender to send messages.');
}

function updateWelcomePendingCount() {
  const el = document.getElementById('welcomePendingCount');
  const pendingList = allMembers.filter(isWhatsAppPending);
  const pending = pendingList.length;
  const importedPending = pendingList.filter(isImportedMember).length;

  if (el) el.textContent = pending + ' member(s) awaiting welcome message';

  const stat = document.getElementById('whatsappPending');
  if (stat) stat.textContent = pending;

  const banner = document.getElementById('waPendingBanner');
  const bannerText = document.getElementById('waPendingBannerText');
  if (banner && bannerText) {
    if (pending > 0) {
      banner.style.display = 'flex';
      bannerText.innerHTML = '<strong>' + pending + '</strong> member(s) have not received a WhatsApp message' +
        (importedPending ? ' — <strong>' + importedPending + '</strong> new import(s)' : '') + '.';
    } else {
      banner.style.display = 'none';
    }
  }

  const newBtn = document.getElementById('waNewBtn');
  if (newBtn) {
    if (importedPending > 0) {
      newBtn.style.display = '';
      newBtn.innerHTML = '<i class="fas fa-file-import"></i> Send New Imports (' + importedPending + ')';
    } else {
      newBtn.style.display = 'none';
    }
  }
}

function applyMemberFilters() {
  const q = (document.getElementById('memberSearch').value || '').trim().toLowerCase();
  const d = document.getElementById('departmentFilter').value;
  const pendingOnly = document.getElementById('pendingOnlyFilter') && document.getElementById('pendingOnlyFilter').checked;

  let list = allMembers;
  if (q) {
    list = list.filter(m =>
      (m.name || '').toLowerCase().includes(q) ||
      String(m.phone || '').toLowerCase().includes(q) ||
      (m.location || '').toLowerCase().includes(q)
    );
  }
  if (d) list = list.filter(m => m.department === d);
  if (pendingOnly) list = list.filter(isWhatsAppPending);

  renderMembers(list);
}

function searchMembers() { applyMemberFilters(); }
function filterMembers() { applyMemberFilters(); }

async function reviewPendingWhatsApp() {
  if (!isLoggedIn) { showLoginModal(); return; }
  showSection('members');
  await loadMembers();
  sendPendingWelcomes();
}

async function loadEvents() {
  document.getElementById('eventsGrid').innerHTML = `
    <div class="stat-card"><div class="stat-value">Sunday Service</div><div class="stat-label">Every Sunday 8:00 AM</div></div>
    <div class="stat-card"><div class="stat-value">Monday Kyoto</div><div class="stat-label">6:00-7:00 AM</div></div>
    <div class="stat-card"><div class="stat-value">Wed Glory</div><div class="stat-label">5:00-7:00 PM</div></div>
    <div class="stat-card"><div class="stat-value">Counseling</div><div class="stat-label">Tue/Thu 7AM-3PM</div></div>
    <div class="stat-card"><div class="stat-value">Friday Prayers</div><div class="stat-label">3PM, 2:30AM, 3AM</div></div>
    <div class="stat-card"><div class="stat-value">Baptism</div><div class="stat-label">Date to be announced</div></div>
    <div class="stat-card"><div class="stat-value">Cross Over Night</div><div class="stat-label">31 Dec 2026, 9PM-4AM</div></div>
  `;
}

let adminPrograms = [];

function showProgramModal(index) {
  document.getElementById('programModal').classList.add('show');
  if (index !== undefined && adminPrograms[index]) {
    document.getElementById('progIndex').value = index;
    document.getElementById('progIcon').value = adminPrograms[index].icon || '';
    document.getElementById('progTitle').value = adminPrograms[index].title || '';
    document.getElementById('progDate').value = adminPrograms[index].date || '';
    document.getElementById('progTime').value = adminPrograms[index].time || '';
    document.getElementById('progDesc').value = adminPrograms[index].description || '';
  } else {
    document.getElementById('programForm').reset();
    document.getElementById('progIndex').value = '';
  }
}

function hideProgramModal() {
  document.getElementById('programModal').classList.remove('show');
}

document.getElementById('programForm').onsubmit = function(e) {
  e.preventDefault();
  const index = document.getElementById('progIndex').value;
  const prog = {
    icon: document.getElementById('progIcon').value.trim(),
    title: document.getElementById('progTitle').value.trim(),
    date: document.getElementById('progDate').value.trim(),
    time: document.getElementById('progTime').value.trim(),
    description: document.getElementById('progDesc').value.trim()
  };
  if (index !== '') {
    adminPrograms[Number(index)] = prog;
  } else {
    adminPrograms.push(prog);
  }
  savePrograms();
  renderPrograms();
  hideProgramModal();
};

function renderPrograms() {
  document.getElementById('programsTable').innerHTML = adminPrograms.map((p, i) =>
    '<tr><td><i class="fas ' + (p.icon || 'fa-calendar') + '"></i></td><td>' + (p.title || '-') + '</td><td>' + (p.date || '-') + '</td><td>' + (p.time || '-') + '</td><td>' + (p.description || '-') + '</td><td><button class="action-btn edit" onclick="showProgramModal(' + i + ')">Edit</button><button class="action-btn delete" onclick="deleteProgram(' + i + ')">Delete</button></td></tr>'
  ).join('');
}

function deleteProgram(index) {
  if (confirm('Delete this program?')) {
    adminPrograms.splice(index, 1);
    savePrograms();
    renderPrograms();
  }
}

async function loadPrograms() {
  try {
    const snap = await db.collection('settings').doc('programs').get();
    if (snap.exists && snap.data().upcoming) {
      adminPrograms = snap.data().upcoming;
    }
  } catch (e) {
    console.warn('Could not load programs from Firestore:', e);
  }
  renderPrograms();
}

function savePrograms() {
  db.collection('settings').doc('programs').set({ upcoming: adminPrograms, updatedAt: new Date().toISOString() })
    .catch(e => console.warn('Save programs error:', e));
}

async function loadAnnouncements() { document.getElementById('announcementsTable').innerHTML = ''; }
function showAnnouncementModal() { alert('Announcement form coming soon'); }
function showComTab(tab) {
  document.querySelectorAll('[id^="com-"]').forEach(t => t.style.display = 'none');
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('com-' + tab).style.display = 'block';
  document.querySelector('[data-comtab="' + tab + '"]').classList.add('active');
}
function saveAttendance() {
  const checkboxes = document.querySelectorAll('.attend-checkbox:checked');
  const attendance = Array.from(checkboxes).map(cb => cb.dataset.phone);
  localStorage.setItem('today_attendance', JSON.stringify(attendance));
  alert('Attendance saved! (' + attendance.length + ' present)');
}

/* ─── IMPORT NEW MEMBERS (imports/new.json) ─── */

// Some exported JSON files contain non-breaking spaces that make JSON.parse
// fail. Normalise them before parsing.
function cleanJsonText(text) {
  return String(text || '')
    .replace(/^\uFEFF/, '')
    .replace(/[\u00A0\u2007\u202F]/g, ' ')
    .replace(/[\u200B-\u200D]/g, '');
}

// Files pasted together can contain several JSON values in one file, e.g.
// "[ {...} ][ {...} ]" or one value per line. Collect every top-level value.
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

function importRecordsFromValue(data) {
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
  throw new Error('Expected a "records" array.');
}

function parseImportJson(text) {
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

  let records = [];
  blocks.forEach(function (data) {
    records = records.concat(importRecordsFromValue(data));
  });
  records.jsonBlocks = blocks.length;
  return records;
}

function openImportModal() {
  if (!isLoggedIn) { showLoginModal(); return; }
  importCandidates = [];
  document.getElementById('importModal').classList.add('show');
  document.getElementById('importSummary').innerHTML = 'Loading <code>imports/new.json</code>…';
  document.getElementById('importPreview').innerHTML = '';
  document.getElementById('importResult').innerHTML = '';
  const btn = document.getElementById('importConfirmBtn');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-file-import"></i> Import';
  loadImportFile();
}

function hideImportModal() {
  document.getElementById('importModal').classList.remove('show');
}

async function loadImportFile() {
  const summaryEl = document.getElementById('importSummary');
  try {
    const res = await fetch('imports/new.json?t=' + Date.now(), { cache: 'no-store' });
    if (!res.ok) throw new Error('HTTP ' + res.status + ' — make sure imports/new.json exists.');
    const text = await res.text();
    const records = parseImportJson(text);
    importBlockCount = records.jsonBlocks || 1;
    await prepareImport(records);
  } catch (err) {
    console.error('Import load error:', err);
    summaryEl.innerHTML = '<div class="import-error"><i class="fas fa-triangle-exclamation"></i> Could not read imports/new.json: ' + escapeHtml(err.message) + '</div>';
  }
}

function handleImportFileInput(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = async function() {
    try {
      const records = parseImportJson(reader.result);
      importBlockCount = records.jsonBlocks || 1;
      document.getElementById('importResult').innerHTML = '';
      await prepareImport(records);
    } catch (err) {
      document.getElementById('importSummary').innerHTML = '<div class="import-error">Could not read the selected file: ' + escapeHtml(err.message) + '</div>';
    }
  };
  reader.readAsText(file);
}

/* ─── IMPORT DUPLICATE MATCHING ─── */
// A record is a duplicate when EITHER its name OR its contact already exists.
// Names are normalised (case, spacing, punctuation, leading list numbers) and
// truncated names such as "Nam... Gideon" still match "Namutamba Gideon".
function normalizeNameForMatch(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/^\s*\d{1,3}\s*[.)-]\s*/, '') // "01. ", "3. ", "06. "
    .replace(/([a-z0-9])\.{2,}([a-z0-9])/g, '$1*$2') // "Sse...ongo" -> "sse*ongo"
    .replace(/\.{2,}/g, '*')                          // "Nam..." -> "nam*"
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
  // A truncated token with an ellipsis is matched as a wildcard.
  if (a.indexOf('*') !== -1) {
    const re = wildcardTokenRegExp(a);
    return re ? re.test(b) : false;
  }
  if (b.indexOf('*') !== -1) {
    const re = wildcardTokenRegExp(b);
    return re ? re.test(a) : false;
  }
  // A single letter is treated as an initial: "M" matches "Mary", "N" matches "Nabirye".
  if (a.length === 1 && b.charAt(0) === a) return true;
  if (b.length === 1 && a.charAt(0) === b) return true;
  // Truncated names: "nam" matches "namutamba", "sse" matches "sserubiri".
  if (a.length >= 3 && b.startsWith(a)) return true;
  if (b.length >= 3 && a.startsWith(b)) return true;
  return false;
}

function namesMatch(a, b) {
  const ta = nameTokensForMatch(a);
  const tb = nameTokensForMatch(b);
  if (!ta.length || !tb.length || ta.length !== tb.length) return false;
  // Match tokens in any order because names are sometimes stored surname-first.
  const used = new Array(tb.length).fill(false);
  for (const token of ta) {
    let matched = false;
    for (let i = 0; i < tb.length; i++) {
      if (!used[i] && nameTokenMatches(token, tb[i])) {
        used[i] = true;
        matched = true;
        break;
      }
    }
    if (!matched) return false;
  }
  return true;
}

async function prepareImport(records) {
  // Load existing registrations once so duplicate detection is reliable.
  const snap = await db.collection('registrations').get();
  const existingPhones = new Set();
  const existingNames = [];
  snap.docs.forEach(d => {
    const data = d.data();
    existingPhones.add(String(d.id));
    const cp = cleanPhone(data.phone || d.id);
    if (cp) existingPhones.add(cp);
    if (data.name) existingNames.push(data.name);
  });

  const filePhones = new Set();
  const fileNames = [];
  importCandidates = records.map((r, index) => {
    const rawName = String(r.name || r.fullName || '').replace(/\s+/g, ' ').trim();
    const rawPhone = String(r.contact || r.phone || '').trim();
    const residence = String(r.residence || r.location || '').replace(/\s+/g, ' ').trim();
    const cp = cleanPhone(rawPhone);
    const item = {
      row: index + 1,
      name: formatName(rawName),
      phone: rawPhone,
      residence,
      cleanPhone: cp,
      validPhone: isValidWhatsAppPhone(rawPhone),
      duplicate: false,
      reason: ''
    };

    if (!rawName && !cp) { item.duplicate = true; item.reason = 'No name or phone'; }
    else if (!rawName) { item.duplicate = true; item.reason = 'No name'; }
    else if (!cp) { item.duplicate = true; item.reason = 'No phone number'; }
    else if (filePhones.has(cp)) { item.duplicate = true; item.reason = 'Duplicate contact in file'; }
    else if (fileNames.some(n => namesMatch(n, rawName))) { item.duplicate = true; item.reason = 'Duplicate name in file'; }
    else if (existingPhones.has(cp)) { item.duplicate = true; item.reason = 'Contact already in database'; }
    else if (existingNames.some(n => namesMatch(n, rawName))) { item.duplicate = true; item.reason = 'Name already in database'; }

    if (cp) filePhones.add(cp);
    if (rawName) fileNames.push(rawName);
    return item;
  });

  renderImportPreview();
}

function renderImportPreview() {
  const summaryEl = document.getElementById('importSummary');
  const previewEl = document.getElementById('importPreview');
  const btn = document.getElementById('importConfirmBtn');

  const total = importCandidates.length;
  const duplicates = importCandidates.filter(c => c.duplicate).length;
  const ready = importCandidates.filter(c => !c.duplicate);
  const invalid = ready.filter(c => !c.validPhone).length;

  summaryEl.innerHTML =
    '<strong>Found ' + total + ' row(s) in imports/new.json</strong>' +
    (importBlockCount > 1
      ? '<div class="import-note"><i class="fas fa-layer-group"></i> The file contained ' + importBlockCount + ' separate JSON blocks, which were combined.</div>'
      : '') +
    '<div class="import-counts">' +
      '<span class="ok">✅ ' + ready.length + ' ready to import</span>' +
      '<span class="warn">⏭ ' + duplicates + ' skipped (same name or contact)</span>' +
      (invalid ? '<span class="bad">⚠ ' + invalid + ' invalid WhatsApp number(s)</span>' : '') +
    '</div>';

  if (!total) {
    previewEl.innerHTML = '';
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-file-import"></i> Nothing to import';
    return;
  }

  previewEl.innerHTML = '<table><thead><tr><th>#</th><th>Name</th><th>Phone</th><th>Residence</th><th>Status</th></tr></thead><tbody>' +
    importCandidates.map(c => {
      let status;
      if (c.duplicate) status = '<span class="import-status skip">' + escapeHtml(c.reason) + '</span>';
      else if (!c.validPhone) status = '<span class="import-status warn">⚠ Invalid WhatsApp number</span>';
      else status = '<span class="import-status ok">Ready</span>';
      return '<tr class="' + (c.duplicate ? 'import-row-skip' : '') + '">' +
        '<td>' + c.row + '</td>' +
        '<td>' + escapeHtml(c.name || '-') + '</td>' +
        '<td>' + escapeHtml(c.phone || '-') + '</td>' +
        '<td>' + escapeHtml(c.residence || '-') + '</td>' +
        '<td>' + status + '</td>' +
      '</tr>';
    }).join('') +
  '</tbody></table>';

  btn.disabled = ready.length === 0;
  btn.innerHTML = '<i class="fas fa-file-import"></i> Import ' + ready.length + ' new member(s)';
}

async function confirmImport() {
  let toImport = importCandidates.filter(c => !c.duplicate);
  if (!toImport.length) return;

  const btn = document.getElementById('importConfirmBtn');
  const resultEl = document.getElementById('importResult');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking duplicates…';
  resultEl.innerHTML = '';

  // Final safety gate: re-read the database immediately before writing and
  // drop anything that duplicates an existing member or another row. A
  // duplicate must never be written, even if the database changed after the
  // preview was generated.
  let blocked = 0;
  try {
    const snap = await db.collection('registrations').get();
    const freshPhones = new Set();
    const freshNames = [];
    snap.docs.forEach(d => {
      const data = d.data();
      freshPhones.add(String(d.id));
      const cp = cleanPhone(data.phone || d.id);
      if (cp) freshPhones.add(cp);
      if (data.name) freshNames.push(data.name);
    });

    const acceptedPhones = new Set();
    const acceptedNames = [];
    const safe = [];
    toImport.forEach(c => {
      const isDup = freshPhones.has(c.cleanPhone)
        || acceptedPhones.has(c.cleanPhone)
        || freshNames.some(n => namesMatch(n, c.name))
        || acceptedNames.some(n => namesMatch(n, c.name));
      if (isDup) {
        c.duplicate = true;
        c.reason = 'Already in system (final check)';
        blocked++;
      } else {
        acceptedPhones.add(c.cleanPhone);
        acceptedNames.push(c.name);
        safe.push(c);
      }
    });
    toImport = safe;
  } catch (err) {
    console.error('Final duplicate check failed:', err);
    resultEl.innerHTML = '<div class="bad">❌ Could not verify duplicates, so nothing was imported: ' + escapeHtml(err.message) + '</div>';
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-file-import"></i> Import';
    return;
  }

  renderImportPreview();

  if (!toImport.length) {
    resultEl.innerHTML = '<div class="warn">⏭ Nothing imported. All ' + blocked + ' selected record(s) already exist in the system.</div>';
    return;
  }

  if (!confirm('Import ' + toImport.length + ' new member(s) into the church database?\n\n' +
    (blocked ? blocked + ' duplicate(s) will be skipped and never saved.\n\n' : '') +
    'They will be marked as WhatsApp pending.')) return;

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Importing…';

  try {
    const buildDoc = c => ({
      name: c.name,
      phone: c.phone,
      location: c.residence || '',
      residence: c.residence || '',
      department: '',
      registrationType: 'general',
      registered: 'yes',
      firstTime: 'yes',
      whatsapp: c.phone,
      volunteering: '',
      referredBy: '',
      status: 'pending',
      whatsappStatus: 'unknown',
      welcomeSent: false,
      source: 'import',
      imported: true,
      importedAt: firebase.firestore.FieldValue.serverTimestamp(),
      cleanPhone: c.cleanPhone,
      timestamp: firebase.firestore.FieldValue.serverTimestamp()
    });

    // The web SDK has no batch.create(). A transaction reads the target
    // documents first and writes only the ones that do not exist, so an
    // import can never overwrite an existing record.
    const chunkSize = 200;
    let imported = 0;
    let conflicts = 0;
    let failed = 0;

    for (let start = 0; start < toImport.length; start += chunkSize) {
      const chunk = toImport.slice(start, start + chunkSize);
      const refs = chunk.map(c => db.collection('registrations').doc(c.cleanPhone));
      try {
        const outcome = await db.runTransaction(async tx => {
          const snaps = await Promise.all(refs.map(ref => tx.get(ref)));
          let ok = 0;
          let skip = 0;
          snaps.forEach((snap, i) => {
            if (snap.exists) { skip++; return; }
            tx.set(refs[i], buildDoc(chunk[i]));
            ok++;
          });
          return { ok, skip };
        });
        imported += outcome.ok;
        conflicts += outcome.skip;
      } catch (chunkErr) {
        console.warn('Import chunk failed; retrying rows individually.', chunkErr);
        for (const c of chunk) {
          try {
            const result = await db.runTransaction(async tx => {
              const ref = db.collection('registrations').doc(c.cleanPhone);
              const snap = await tx.get(ref);
              if (snap.exists) return 'conflict';
              tx.set(ref, buildDoc(c));
              return 'imported';
            });
            if (result === 'imported') imported++;
            else conflicts++;
          } catch (rowErr) {
            failed++;
            console.warn('Import failed for ' + c.name + ':', rowErr);
          }
        }
      }
    }

    const skipped = importCandidates.filter(c => c.duplicate).length + conflicts;
    resultEl.innerHTML = '<div class="ok">✅ Imported ' + imported + ' new member(s).' +
      (skipped ? ' Skipped ' + skipped + ' duplicate(s) — duplicates are never saved.' : '') +
      (failed ? ' ' + failed + ' failed.' : '') +
      ' They are highlighted as WhatsApp pending.</div>';

    await loadMembers();
    await loadDashboard();

    if (imported > 0) {
      const sendNow = confirm('Imported ' + imported + ' new member(s).\n\nOpen the WhatsApp sender for these new entries now?');
      hideImportModal();
      if (sendNow) sendPendingWelcomes(true);
    } else {
      hideImportModal();
    }
  } catch (err) {
    console.error('Import error:', err);
    resultEl.innerHTML = '<div class="bad">❌ Import failed: ' + escapeHtml(err.message) + '</div>';
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-file-import"></i> Retry Import';
  }
}

/* ─── CSV EXPORT ─── */
async function exportCSV() {
  let data = allRegistrations.length ? allRegistrations : allMembers;
  if (!data.length) {
    try {
      const snapshot = await db.collection('registrations').get();
      data = sortNewestFirst(snapshot.docs.map(d => ({ id: d.id, ...d.data() })));
    } catch (e) {
      alert('Could not load registrations for export: ' + e.message);
      return;
    }
  }
  const headers = ['Name', 'Phone', 'Registration Type', 'Baptized Before', 'Prayer Request', 'Department', 'Location', 'Referred By', 'Join WhatsApp Group', 'WhatsApp Chat Opened', 'Registered', 'Status'];
  const rows = data.map(r => [
    formatName(r.name) || '', r.phone || '', r.registrationType || '', r.baptismBefore || '', r.prayerRequest || '',
    r.department || '', r.location || '', r.referredBy || '',
    r.joinGroup === true ? 'Yes' : (r.joinGroup === false ? 'No' : ''),
    r.whatsappOpened ? 'Yes' : 'No',
    regDate(r), r.status || 'new'
  ]);
  const csv = [headers.join(','), ...rows.map(row => row.map(c => '"' + String(c).replace(/"/g, '""') + '"').join(','))].join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'registrations_report_' + new Date().toISOString().slice(0, 10) + '.csv';
  a.click();
  URL.revokeObjectURL(url);
}

function cleanPhone(phone) {
  return String(phone || '').replace(/\D/g, '').slice(-9);
}

// Show names in title case in the dashboard, even for older records that were
// saved in lowercase or ALL CAPS. e.g. "JOHN DOE" -> "John Doe".
function formatName(name) {
  return String(name || '')
    .trim()
    .replace(/\s+/g, ' ')
    .toLowerCase()
    .split(' ')
    .filter(word => word.length > 0)
    .map(word => word.replace(/(^|[-'’])([a-z])/g, (match, sep, letter) => sep + letter.toUpperCase()))
    .join(' ');
}

document.querySelectorAll('.sidebar-item[data-section]').forEach(item => {
  item.addEventListener('click', () => {
    if (!isLoggedIn) {
      showLoginModal();
      return;
    }
    showSection(item.dataset.section);
  });
});

if (auth.currentUser) {
  loadDashboard();
}
