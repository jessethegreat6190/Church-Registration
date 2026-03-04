// js/app.js — Grace of Jesus Christ Ministries Registration
import {
  formatName,
  isUpcomingBirthday,
  getDaysUntilBirthday,
  formatBirthday,
  getWeeklyVerse,
  WEEKLY_VERSES,
  DEFAULT_CHURCH_PROGRAMS
} from './utils.js';

/* ── Constants ─────────────────────────────────────────────
   Both currently point to the same Google Apps Script deployment
   which handles POST (doPost) and GET (doGet) at the same URL.
   Update GET_DATA_API_URL if a separate read endpoint is created.
   ─────────────────────────────────────────────────────────── */
const REGISTER_API_URL = 'https://script.google.com/macros/s/AKfycbxep7hhQKPfuPBG9q9oig8D892E2d4bdBdPvGct48jlAFIUP6bmSu06tIbbl-6pmISsOQ/exec';
const GET_DATA_API_URL  = 'https://script.google.com/macros/s/AKfycbxep7hhQKPfuPBG9q9oig8D892E2d4bdBdPvGct48jlAFIUP6bmSu06tIbbl-6pmISsOQ/exec';

/* ── DOM refs ───────────────────────────────────────────── */
const step1El         = document.getElementById('step-1');
const step2El         = document.getElementById('step-2');
const step3El         = document.getElementById('step-3');
const nextBtn1        = document.getElementById('nextBtn1');
const nextBtn2        = document.getElementById('nextBtn2');
const backBtn2        = document.getElementById('backBtn2');
const editBtn         = document.getElementById('editBtn');
const saveBtn         = document.getElementById('saveBtn');
const saveBtnText     = document.getElementById('saveBtnText');
const saveSpinner     = document.getElementById('saveSpinner');
const detailsList     = document.getElementById('detailsList');
const blessingOverlay = document.getElementById('fullBlessingOverlay');
const progressBar     = document.getElementById('progressBar');
const instrCheckbox   = document.getElementById('vol-instruments');
const instrInput      = document.getElementById('instrument-type');

/* ── State ──────────────────────────────────────────────── */
let currentEntry     = null;
let allRegistrations = [];
let db               = null;
let currentStep      = 1;
let churchPrograms   = { ...DEFAULT_CHURCH_PROGRAMS };

/* ── Firebase Init ──────────────────────────────────────── */
window.addEventListener('load', () => {
  try {
    if (typeof firebase !== 'undefined') {
      db = firebase.firestore();
      setTimeout(prefetchData, 1000);
    }
  } catch (e) {
    console.warn('Firebase not initialised (running locally?):', e.message);
  }
});

/* ── Instrument checkbox toggle ─────────────────────────── */
instrInput.disabled = true;
instrCheckbox.addEventListener('change', () => {
  instrInput.disabled = !instrCheckbox.checked;
  if (!instrCheckbox.checked) instrInput.value = '';
});

/* ── Inline field errors ────────────────────────────────── */
function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = msg;
    el.setAttribute('aria-live', 'polite');
  }
}

function clearError(id) {
  const el = document.getElementById(id);
  if (el) el.textContent = '';
}

/* ── Progress bar ───────────────────────────────────────── */
function setProgress(step) {
  if (!progressBar) return;
  progressBar.style.width = Math.round((step / 3) * 100) + '%';
}

/* ── Step Navigation ────────────────────────────────────── */
function showStep(n) {
  [step1El, step2El, step3El].forEach(el => {
    el.classList.remove('active', 'step--slide');
  });
  const target = document.getElementById('step-' + n);
  target.classList.add('active');
  requestAnimationFrame(() => target.classList.add('step--slide'));
  currentStep = n;
  updateStepIndicator();
  setProgress(n);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateStepIndicator() {
  const isFirstTime = getFirstTimeValue() === 'yes';
  [1, 2, 3].forEach(n => {
    const si = document.getElementById('si-' + n);
    const sc = document.getElementById('sc-' + n);
    si.classList.remove('active', 'done');

    if (n < currentStep && !(n === 2 && !isFirstTime)) {
      si.classList.add('done');
      sc.textContent = '✓';
    } else if (n === currentStep) {
      si.classList.add('active');
      sc.textContent = n;
    } else {
      sc.textContent = n;
    }
  });

  document.getElementById('sl-1').classList.toggle('done', currentStep > 1);
  document.getElementById('sl-2').classList.toggle('done', currentStep > 2);
}

/* ── Helpers ────────────────────────────────────────────── */
function getFirstTimeValue() {
  return document.querySelector('input[name="firstTime"]:checked')?.value || 'no';
}

// Uganda phone: 07x/06x (10 digits) or +256/256 prefix
const UGANDA_PHONE_RE = /^(07|06)\d{8}$|^(\+?256)(7|6)\d{8}$/;

/* ── Step 1 → Next ──────────────────────────────────────── */
nextBtn1.addEventListener('click', () => {
  const name     = document.getElementById('name').value.trim();
  const phone    = document.getElementById('phone').value.trim().replace(/\s+/g, '');
  const location = document.getElementById('location').value.trim();

  let valid = true;

  if (!name) {
    showError('err-name', 'Full name is required.');
    valid = false;
  } else {
    clearError('err-name');
  }

  if (!phone) {
    showError('err-phone', 'Phone number is required.');
    valid = false;
  } else if (!UGANDA_PHONE_RE.test(phone)) {
    showError('err-phone', 'Enter a valid Uganda number (e.g. 0700 000 000).');
    valid = false;
  } else {
    clearError('err-phone');
  }

  if (!location) {
    showError('err-location', 'Residence is required.');
    valid = false;
  } else {
    clearError('err-location');
  }

  if (!valid) return;

  if (getFirstTimeValue() === 'yes') {
    showStep(2);
  } else {
    buildEntry();
    showStep(3);
  }
});

/* ── Step 2 ─────────────────────────────────────────────── */
backBtn2.addEventListener('click', () => showStep(1));

nextBtn2.addEventListener('click', () => {
  buildEntry();
  showStep(3);
});

/* ── Step 3 ─────────────────────────────────────────────── */
editBtn.addEventListener('click', () => {
  showStep(getFirstTimeValue() === 'yes' ? 2 : 1);
});

/* ── Build currentEntry ─────────────────────────────────── */
function buildEntry() {
  const firstTimeValue = getFirstTimeValue();
  const volunteering   = [];

  if (firstTimeValue === 'yes') {
    document.querySelectorAll('#step-2 input[type="checkbox"]:checked')
      .forEach(cb => {
        if (cb.id === 'vol-instruments') {
          const inst = instrInput.value.trim();
          volunteering.push(`Instruments: ${inst || 'General'}`);
        } else if (cb.value) {
          volunteering.push(cb.value);
        }
      });
  }

  currentEntry = {
    name:       formatName(document.getElementById('name').value.trim()),
    phone:      document.getElementById('phone').value.trim(),
    location:   document.getElementById('location').value.trim(),
    firstTime:  firstTimeValue,
    birthDay:   firstTimeValue === 'yes' ? (document.getElementById('birthDay').value  || '') : '',
    birthMonth: firstTimeValue === 'yes' ? (document.getElementById('birthMonth').value || '') : '',
    referredBy: firstTimeValue === 'yes' ? (document.getElementById('referredBy').value.trim() || null) : null,
    volunteering,
    consent: firstTimeValue === 'yes' ? document.getElementById('consent').checked : false
  };

  renderConfirmation(currentEntry);
}

/* ── Render Confirmation (Step 3) ───────────────────────── */
function renderConfirmation(data) {
  const birthdayStr = formatBirthday(data.birthMonth, data.birthDay);
  let birthdayDisplay = birthdayStr;

  if (data.birthDay && data.birthMonth) {
    const daysUntil = getDaysUntilBirthday(Number(data.birthMonth), Number(data.birthDay));
    if (daysUntil !== null && daysUntil <= 7) {
      birthdayDisplay += daysUntil === 0
        ? ' 🎂 <strong>Today!</strong>'
        : ` 🎂 in ${daysUntil} day${daysUntil === 1 ? '' : 's'}`;
    }
  }

  const volStr = data.volunteering.length > 0
    ? data.volunteering.join(', ') : 'Not interested';

  if (data.firstTime === 'no') {
    detailsList.innerHTML = `
      <li><strong>Name</strong> ${data.name}</li>
      <li><strong>Phone</strong> ${data.phone}</li>
      <li><strong>Residence</strong> ${data.location}</li>
      <li><strong>Type</strong> Returning visitor</li>
    `;
  } else {
    detailsList.innerHTML = `
      <li><strong>Name</strong> ${data.name}</li>
      <li><strong>Phone</strong> ${data.phone}</li>
      <li><strong>Residence</strong> ${data.location}</li>
      <li><strong>Birthday</strong> ${birthdayDisplay}</li>
      <li><strong>Type</strong> First-time online</li>
      <li><strong>Volunteer</strong> ${volStr}</li>
      <li><strong>WhatsApp</strong> ${data.consent ? 'Yes – add me' : 'No thanks'}</li>
    `;
  }
}

/* ── Save Registration ──────────────────────────────────── */
saveBtn.addEventListener('click', handleSave);

async function handleSave() {
  if (!currentEntry) return;

  saveBtn.disabled = true;
  saveBtnText.textContent = 'Saving…';
  saveSpinner.style.display = 'inline-block';

  const blessing = getWeeklyVerse(WEEKLY_VERSES);

  const formData = {
    name:         currentEntry.name,
    phone:        currentEntry.phone,
    location:     currentEntry.location,
    birthMonth:   currentEntry.birthMonth  || '',
    birthDay:     currentEntry.birthDay    || '',
    registered:   currentEntry.firstTime,
    whatsapp:     currentEntry.consent ? currentEntry.phone : '—',
    volunteering: currentEntry.volunteering.join(', '),
    referredBy:   currentEntry.referredBy  || ''
  };

  const cleanInputPhone = (currentEntry.phone || '').replace(/\D/g, '').slice(-9);
  let isReturning = false;

  /* Check for duplicate */
  try {
    if (db) {
      const docSnap = await db.collection('registrations').doc(cleanInputPhone).get();
      if (docSnap.exists) {
        isReturning = true;
      } else {
        const snap = await db.collection('registrations')
          .where('phone', '==', currentEntry.phone).get();
        isReturning = !snap.empty;
      }
    }
    if (!isReturning) {
      isReturning = allRegistrations.some(r =>
        String(r.phone || '').replace(/\D/g, '').slice(-9) === cleanInputPhone
      );
    }
  } catch (e) {
    console.warn('Duplicate check fallback:', e.message);
    isReturning = allRegistrations.some(r =>
      String(r.phone || '').replace(/\D/g, '').slice(-9) === cleanInputPhone
    );
  }

  try {
    if (!isReturning) {
      /* A. Firebase Firestore */
      if (db) {
        await db.collection('registrations').doc(cleanInputPhone).set({
          ...formData,
          cleanPhone: cleanInputPhone,
          timestamp:  firebase.firestore.FieldValue.serverTimestamp()
        });
      }

      /* B. Google Sheets backup via hidden form */
      let tempForm = document.getElementById('temp_gas_form');
      if (!tempForm) {
        tempForm = document.createElement('form');
        tempForm.id     = 'temp_gas_form';
        tempForm.style.display = 'none';
        tempForm.method = 'POST';
        tempForm.action = REGISTER_API_URL;
        tempForm.target = 'hidden_iframe';
        if (!document.getElementById('hidden_iframe')) {
          const iframe      = document.createElement('iframe');
          iframe.id         = 'hidden_iframe';
          iframe.name       = 'hidden_iframe';
          iframe.style.display = 'none';
          document.body.appendChild(iframe);
        }
        document.body.appendChild(tempForm);
      }
      tempForm.innerHTML = '';
      Object.entries(formData).forEach(([k, v]) => {
        const inp = document.createElement('input');
        inp.type  = 'hidden';
        inp.name  = k;
        inp.value = v;
        tempForm.appendChild(inp);
      });
      tempForm.submit();
    }

    /* Build WhatsApp message */
    let whatsappUrl = null;
    if (!isReturning) {
      let raw = currentEntry.phone.replace(/\D/g, '');
      if (raw.startsWith('0'))     raw = '256' + raw.substring(1);
      else if (raw.length === 9)   raw = '256' + raw;

      let prog =
        'Church Programs:\n' +
        '• Sunday Services: '        + churchPrograms.sunday    + '\n' +
        '• Monday Kyoto Prayers: '   + churchPrograms.monday    + '\n' +
        '• Wednesday Evening Glory: ' + churchPrograms.wednesday + '\n' +
        '• Tue & Thu Counseling: '   + churchPrograms.tueThu   + '\n' +
        '• Friday Night Prayers: '   + churchPrograms.friday;
      if (churchPrograms.custom?.trim()) prog += '\n• ' + churchPrograms.custom;

      let msg =
        `Hello ${currentEntry.name}! Thank you for registering at Grace of Jesus Christ Ministries.\n\n` +
        `🕊 *A Blessing for you:* "${blessing}"\n\n${prog}`;

      if (currentEntry.consent)
        msg += '\n\nJoin our WhatsApp Group: ' + (churchPrograms.whatsappLink || 'https://chat.whatsapp.com/Bd2AT6h45KgKMTUwCod89h');

      msg += '\n\nSubscribe to our YouTube: https://www.youtube.com/@encounter_GJM\n\n*An encounter with the Holy Spirit*';
      whatsappUrl = `https://wa.me/${raw}?text=${encodeURIComponent(msg)}`;
    }

    /* Show blessing overlay */
    setTimeout(() => {
      const thankYouNote = document.getElementById('thankYouNote');
      const blessingPara = document.getElementById('blessingText');

      if (isReturning) {
        thankYouNote.textContent = 'Welcome Back!';
        blessingPara.textContent = `You are already registered! "${blessing}"`;
      } else {
        thankYouNote.textContent = 'Thank You for Registering!';
        if (whatsappUrl) {
          window.open(whatsappUrl, '_blank');
          blessingPara.innerHTML =
            `"${blessing}"<br><br>` +
            `<a href="${whatsappUrl}" target="_blank" ` +
            `style="color:#25D366;font-size:0.9rem;font-weight:bold;text-decoration:none;">` +
            `Tap here to open WhatsApp if it didn't launch automatically</a>`;
        } else {
          blessingPara.textContent = `"${blessing}"`;
        }
      }
      blessingOverlay.style.display = 'flex';
    }, 700);

  } catch (error) {
    console.error('Save error:', error);
    alert('❌ Error saving registration. Please try again.');
  } finally {
    saveBtn.disabled = false;
    saveBtnText.textContent = 'Save Registration';
    saveSpinner.style.display = 'none';
  }
}

/* ── Close Blessing & Reset ─────────────────────────────── */
window.closeBlessing = function () {
  blessingOverlay.style.display = 'none';
  resetForm();
};

function resetForm() {
  ['name', 'phone', 'location', 'birthDay', 'instrument-type', 'referredBy']
    .forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
  ['err-name', 'err-phone', 'err-location'].forEach(clearError);
  document.getElementById('birthMonth').value = '';
  document.getElementById('ft-no').checked = true;
  document.getElementById('consent').checked = true;
  document.querySelectorAll('#step-2 input[type="checkbox"]')
    .forEach(cb => { cb.checked = false; });
  instrInput.disabled = true;
  currentEntry = null;
  showStep(1);
  prefetchData();
}

/* ── Prefetch registrations + programs ──────────────────── */
async function prefetchData() {
  try {
    if (db) {
      const snap = await db.collection('registrations').get();
      allRegistrations = snap.docs.map(d => d.data());
      const progDoc = await db.collection('settings').doc('programs').get();
      if (progDoc.exists) churchPrograms = { ...churchPrograms, ...progDoc.data() };
    }
    const res = await fetch(GET_DATA_API_URL);
    if (res.ok) {
      const data = await res.json();
      data.forEach(reg => {
        if (reg.name !== 'SYSTEM_PROGRAMS') {
          const ph = String(reg.phone || '').replace(/\D/g, '').slice(-9);
          if (!allRegistrations.some(r =>
            String(r.phone || '').replace(/\D/g, '').slice(-9) === ph
          )) allRegistrations.push(reg);
        } else if (!churchPrograms.custom) {
          try {
            const parsed = JSON.parse(reg.location);
            churchPrograms = { ...churchPrograms, ...parsed };
          } catch (e) {}
        }
      });
    }
  } catch (e) {
    console.warn('Prefetch error:', e.message);
  }
}

/* ── Service Worker ─────────────────────────────────────── */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js')
      .then(() => console.log('SW registered'))
      .catch(e => console.warn('SW failed:', e));
  });
}

/* ── Init ───────────────────────────────────────────────── */
updateStepIndicator();
setProgress(1);
