# Guest WiFi Access Portal — Deploy Guide

Grace of Jesus Christ Ministries, Kitintale.
Temporary WiFi access tied to guest registration. Full spec in [SRS.md](SRS.md),
visual concept in [ui-mockup.html](ui-mockup.html).

---

## How it works

```
Guest joins church WiFi
   -> scans printed QR  ->  https://guest.church-registration-grace.web.app
   -> registers Full Name + Phone Number
   -> gets a 45-minute session (one per phone per day)
   -> views Programs / Sermons / Giving / Contact
   -> at 0:00 the portal locks and shows "session ended"
```

**The portal needs nothing from the church network.** It is hosted on Firebase
Hosting, so guests load it over the internet like any website. No static IP, no
DNS, no router changes are required for v1.

---

## Status

| Piece | State |
|---|---|
| `index.html` — 5 screens | done |
| `styles.css` — from the mockup | done |
| `app.js` — session logic, countdown, Firestore | done |
| `manifest.json` — PWA | done |
| `make_qr.py` — QR generator | done |
| `firebase.json` — two hosting sites | done |
| `firestore.rules` — `wifi_sessions` guard | done (needs deploy) |
| `.firebaserc` — hosting targets | main mapped, **guest needs init** |

---

## Deploy

Run all commands from `churchregistration/`.

### 1. Create the guest hosting site (once)

The subdomain must exist in the project before it can be targeted.

```bash
firebase init hosting
```

- Select the existing project `church-registration-grace`
- Choose **Add a new site** and give it the id **`guest`**
- Decline to configure as a single-page app

That writes the `guest` target into `.firebaserc`.

### 2. Deploy the Firestore rules

Required before any guest can create a session. Without it every write is
rejected with `403 Missing or insufficient permissions`.

```bash
firebase deploy --only firestore:rules
```

### 3. Deploy the sites independently

```bash
firebase deploy --only hosting:main    # existing church site
firebase deploy --only hosting:guest   # new WiFi portal
```

`firebase.json` keeps the main site ignoring `guest-access/**`, so the portal is
never published twice.

---

## Firestore data model

### `wifi_sessions/{phone}_{YYYY-MM-DD}` — e.g. `771234567_2026-10-01`

```js
{
  phone: '771234567',        // 9 digits, matches the counseling form
  name: 'John Smith',
  origin: 'Kitintale',
  startTime: Timestamp,
  expiresAt: Timestamp,      // always startTime + 45m
  durationMinutes: 45,
  date: '2026-10-01',
  status: 'active',
  source: 'guest-access-portal'
}
```

One document per phone per day, keyed by date. That single key enforces the
one-session-per-day rule at the data layer, not just in the UI.

### `registrations/{phone}` — existing collection, read and create only

`recordGuestIfNew()` checks first and **only creates when absent**. An existing
church registration is never overwritten by a WiFi sign-up.

---

## Rules: why the guard looks like this

```js
match /wifi_sessions/{document} {
  allow read: if true;
  allow create: if request.resource.data.durationMinutes == 45
                && request.resource.data.durationMinutes is int
                && request.resource.data.phone is string
                && request.resource.data.date is string
                && request.resource.data.expiresAt
                   == request.resource.data.startTime + duration.value(45, 'm');
  allow update, delete: if false;
}
```

- `expiresAt == startTime + 45m` — a tampered client cannot request a longer
  session, because the expiry is pinned to the server-checkable start time.
- `allow update, delete: if false` — a guest cannot extend their session or
  delete today's record to start a fresh one.
- Staff can still manage sessions through the catch-all rule (admin uid).

---

## Known limitation: soft enforcement

The 45-minute limit is enforced **in the portal only**. A guest whose timer hits
zero sees the "session ended" screen, but nothing stops them reopening the
Activities tab in the same browser, or continuing to use the network.

This is deliberate for v1 — see SRS 5.4. Real disconnect needs a router with a
guest network and walled garden (MikroTik hEX, TP-Link Omada, or a Raspberry Pi
gateway) that can be told to drop the client at 45 minutes.

If that phase happens, the domain allowlist is:

```
*.firebaseapp.com   *.web.app
*.googleapis.com    *.gstatic.com
fonts.googleapis.com   fonts.gstatic.com
```

Allowlist **domains, not IPs** — Firebase Hosting is anycast.

---

## Print the QR code

```bash
pip install qrcode[pil]
python make_qr.py
```

Writes `wifi-qr-512.png` and `wifi-qr-1024.png`. Use the 1024 for A4/poster
printing. Test the printed code on 2-3 phones before laminating.

---

## Local testing

Apache must be serving `C:\xampp\htdocs`. Then:

```
http://localhost/churchregistration/guest-access/
```

Note that session writes need the rules deployed (step 2) — locally you get a
403 until then, and the UI shows a friendly "Could not start your session"
message rather than breaking.