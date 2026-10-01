/* ═══════════════════════════════════════════════════════════════
   Guest Access Portal — Grace of Jesus Christ Ministries, Kitintale
   Temporary WiFi access tied to guest registration.

   Model: "new guest" = this phone number has no wifi_sessions record
   for today. Existing church registrations are never overwritten.
   Session limit is enforced in-app (soft) — see SRS 5.4.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Config ─────────────────────────────────────────── */

  const firebaseConfig = {
    apiKey: 'AIzaSyDyARd_4HXdx9gEOguMDvncPV17j7kum-s',
    authDomain: 'church-registration-grace.firebaseapp.com',
    projectId: 'church-registration-grace',
    storageBucket: 'church-registration-grace.firebasestorage.app',
    messagingSenderId: '402796692999',
    appId: '1:402796692999:web:15f01064b41197c4c9cca2',
    measurementId: 'G-L3CD5ZX957'
  };

  const MAIN_SITE = 'https://church-registration-grace.web.app';
  const SESSION_MINUTES = 45;
  const STORE_KEY = 'gjcm_wifi_session';

  // Matches the validation already used by the counseling form (js/app.js:194)
  const UGANDA_PHONE_RE = /^(07|06)\d{8}$|^(\+?256)(7|6)\d{8}$/;

  let db = null;
  let ticker = null;

  /* ── Helpers ────────────────────────────────────────── */

  const $ = (id) => document.getElementById(id);

  /**
   * Validation form: strip whitespace only, keeping the leading 0 or 256.
   * This mirrors the counseling form (js/app.js:199) — the regex expects
   * that shape, so it must NOT be run against the 9-digit doc form.
   */
  function phoneForValidation(raw) {
    return String(raw || '').replace(/\s+/g, '');
  }

  /** Firestore document-ID form: last 9 digits, same as the counseling form. */
  function cleanPhone(raw) {
    return String(raw || '').replace(/\D/g, '').slice(-9);
  }

  function todayKey(d) {
    d = d || new Date();
    const p = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  }

  function sessionId(phone, day) {
    return `${phone}_${day}`;
  }

  function msToClock(ms) {
    const total = Math.max(0, Math.floor(ms / 1000));
    const m = String(Math.floor(total / 60)).padStart(2, '0');
    const s = String(total % 60).padStart(2, '0');
    return `${m}:${s}`;
  }

  function show(screenId) {
    document.querySelectorAll('.screen').forEach((el) => {
      el.classList.toggle('active', el.id === screenId);
    });
    window.scrollTo(0, 0);
  }

  function saveSession(data) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(data)); } catch (e) { /* private mode */ }
  }

  function loadSession() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); } catch (e) { return null; }
  }

  function clearSession() {
    try { localStorage.removeItem(STORE_KEY); } catch (e) { /* ignore */ }
  }

  function showError(msg) {
    const box = $('alert-error');
    box.textContent = msg;
    box.classList.add('show');
  }

  function hideError() {
    $('alert-error').classList.remove('show');
  }

  /* ── Activities ─────────────────────────────────────── */

  function wireActivityLinks() {
    const map = {
      'link-programs': '#programs',
      'link-sermons': '#sermons',
      'link-giving': '#giving',
      'link-contact': '#contact'
    };
    Object.keys(map).forEach((id) => {
      const el = $(id);
      el.href = `${MAIN_SITE}/${map[id]}`;
      el.target = '_blank';
      el.rel = 'noopener';
    });
  }

  /* ── Countdown ──────────────────────────────────────── */

  function stopTicker() {
    if (ticker) { clearInterval(ticker); ticker = null; }
  }

  function renderClock(remainingMs) {
    const clock = msToClock(remainingMs);
    const timeEl = $('cd-time');
    timeEl.innerHTML = `${clock} <small>left</small>`;
    timeEl.classList.toggle('warning', remainingMs <= 5 * 60 * 1000);
    $('cd-bar').style.width = `${Math.max(0, (remainingMs / (SESSION_MINUTES * 60000)) * 100)}%`;
    $('activities-time').textContent = clock;
  }

  function startTicker(expiresAtMs) {
    stopTicker();
    const tick = () => {
      const remaining = expiresAtMs - Date.now();
      renderClock(remaining);
      if (remaining <= 0) {
        stopTicker();
        onSessionExpired();
      }
    };
    tick();
    ticker = setInterval(tick, 1000);
  }

  function onSessionExpired() {
    showEnded('expired');
    show('screen-ended');
  }

  /* ── Ended screen states ────────────────────────────── */

  function showEnded(reason) {
    stopTicker();
    if (reason === 'used') {
      $('ended-pill').className = 'pill gold';
      $('ended-pill').textContent = 'New Guests Only';
      $('ended-title').textContent = 'This number has already had WiFi today';
      $('ended-msg').textContent =
        'WiFi access is offered to first-time guests, one session per phone number per day. ' +
        'Please speak to our welcome team if you need more time.';
    } else {
      $('ended-pill').className = 'pill red';
      $('ended-pill').innerHTML = '&#9679; Session Ended';
      $('ended-title').textContent = 'Your 45 minutes are up';
      $('ended-msg').textContent =
        "Thanks for visiting Grace of Jesus Christ Ministries. We hope you enjoyed the service. " +
        "Please see our welcome team if you'd like more access.";
    }
  }

  /* ── Session flow ───────────────────────────────────── */

  function greet(name) {
    const first = String(name || 'Guest').trim().split(/\s+/)[0];
    const text = `Welcome, ${first}!`;
    $('active-greet').textContent = text;
    $('activities-greet').textContent = text;
  }

  /** Render the live session screens from a session record. */
  function enterActiveSession(rec) {
    greet(rec.name);
    const expiresAtMs = rec.expiresAt.toMillis ? rec.expiresAt.toMillis() : Number(rec.expiresAt);
    if (expiresAtMs - Date.now() <= 0) { onSessionExpired(); return; }
    show('screen-active');
    startTicker(expiresAtMs);
  }

  /**
   * Look up today's session for this phone.
   * Returns 'none' | 'active' | 'expired' alongside the record.
   */
  async function findSession(phone, day) {
    const snap = await db.collection('wifi_sessions').doc(sessionId(phone, day)).get();
    if (!snap.exists) return { state: 'none' };
    const rec = snap.data();
    const expiresAtMs = rec.expiresAt.toMillis ? rec.expiresAt.toMillis() : Number(rec.expiresAt);
    return {
      state: expiresAtMs > Date.now() ? 'active' : 'expired',
      rec: rec,
      expiresAtMs: expiresAtMs
    };
  }

  /**
   * Record the guest in `registrations` only if they are genuinely new.
   * Checks first and creates only when absent, so an existing church
   * registration is never overwritten by a WiFi sign-up (and we never
   * issue a write the Firestore rules would reject).
   */
  async function recordGuestIfNew(phone, name, origin) {
    try {
      const ref = db.collection('registrations').doc(phone);
      const snap = await ref.get();
      if (snap.exists) return; // Already registered with the church — leave it alone.
      await ref.set({
        phone: phone,
        cleanPhone: phone,
        name: name,
        origin: origin || '',
        source: 'wifi-portal',
        registeredAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    } catch (e) {
      // Non-fatal: the WiFi session is what matters.
      console.warn('Could not record registration:', e && e.message);
    }
  }

  async function submitRegistration() {
    const btn = $('btn-submit');
    const name = $('in-name').value.trim();
    const origin = $('in-from').value.trim();
    const rawPhone = $('in-phone').value.trim();
    const phone = cleanPhone(rawPhone);

    hideError();
    $('in-name').classList.remove('error');
    $('in-phone').classList.remove('error');

    if (name.length < 2) {
      $('in-name').classList.add('error');
      showError('Please enter your full name.');
      return;
    }
    if (!UGANDA_PHONE_RE.test(phoneForValidation(rawPhone))) {
      $('in-phone').classList.add('error');
      showError('That phone number does not look right. Use a Ugandan number like 0771 234 567.');
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Starting your session…';

    const day = todayKey();

    try {
      // Read existing state first (transaction requires all reads up front).
      const existing = await findSession(phone, day);

      if (existing.state === 'active') {
        // Already running today — resume rather than create a duplicate.
        saveSession({ phone: phone, name: existing.rec.name || name, day: day });
        enterActiveSession(existing.rec);
        return;
      }
      if (existing.state === 'expired') {
        saveSession({ phone: phone, name: name, day: day });
        showEnded('used');
        show('screen-ended');
        return;
      }

      // No session today → create one atomically so two simultaneous
      // submissions for the same number cannot both succeed.
      const startTime = firebase.firestore.Timestamp.now();
      const expiresAt = firebase.firestore.Timestamp.fromMillis(
        startTime.toMillis() + SESSION_MINUTES * 60000
      );
      const payload = {
        phone: phone,
        name: name,
        origin: origin,
        startTime: startTime,
        expiresAt: expiresAt,
        durationMinutes: SESSION_MINUTES,
        date: day,
        status: 'active',
        source: 'guest-access-portal'
      };

      await db.runTransaction(async (tx) => {
        const ref = db.collection('wifi_sessions').doc(sessionId(phone, day));
        const snap = await tx.get(ref);
        if (snap.exists) throw new Error('SESSION_EXISTS');
        tx.set(ref, payload);
      });

      await recordGuestIfNew(phone, name, origin);

      saveSession({ phone: phone, name: name, day: day });
      enterActiveSession(payload);

    } catch (e) {
      if (e && e.message === 'SESSION_EXISTS') {
        showEnded('used');
        show('screen-ended');
      } else {
        console.error(e);
        showError('Could not start your session. Please check your connection and try again.');
      }
    } finally {
      btn.disabled = false;
      btn.textContent = 'Start My 45-Min Session';
    }
  }

  /* ── Restore on load ────────────────────────────────── */

  async function restore() {
    const saved = loadSession();

    if (saved && saved.phone && saved.day === todayKey()) {
      try {
        const found = await findSession(saved.phone, todayKey());
        if (found.state === 'active') { enterActiveSession(found.rec); return; }
        if (found.state === 'expired') { showEnded('used'); show('screen-ended'); return; }
      } catch (e) {
        console.warn('Restore failed:', e && e.message);
      }
      clearSession();
    }

    show('screen-welcome');
  }

  /* ── Offline indicator ──────────────────────────────── */

  function wireOffline() {
    const bar = $('offlineBar');
    const update = () => bar.classList.toggle('show', !navigator.onLine);
    window.addEventListener('online', update);
    window.addEventListener('offline', update);
    update();
  }

  /* ── Boot ───────────────────────────────────────────── */

  function init() {
    wireActivityLinks();
    wireOffline();

    $('btn-start').addEventListener('click', () => {
      hideError();
      show('screen-register');
    });
    $('btn-submit').addEventListener('click', submitRegistration);
    $('btn-explore').addEventListener('click', () => show('screen-activities'));
    $('btn-view-activities').addEventListener('click', () => {
      show('screen-activities');
      stopTicker(); // No live clock once the session is over.
      $('activities-time').textContent = '0:00';
    });

    ['in-name', 'in-phone'].forEach((id) => {
      $(id).addEventListener('input', () => {
        $(id).classList.remove('error');
        hideError();
      });
    });

    try {
      if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
      db = firebase.firestore();
    } catch (e) {
      console.error('Firebase init failed:', e);
      show('screen-welcome');
      return;
    }

    restore();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();