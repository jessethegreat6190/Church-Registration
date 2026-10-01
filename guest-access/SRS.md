# Software Requirements Specification (SRS)

## Guest Access Portal — Grace of Jesus Christ Ministries, Kitintale

**Version:** 1.0 (Draft)
**Status:** Planning
**Created:** 2026-08-31

---

## 1. Project Overview

### 1.1 Purpose
The **Guest Access Portal** is a web application that provides one-time, time-limited
WiFi access to guests of Grace of Jesus Christ Ministries (Kitintale) while capturing
their registration details and onboarding them into the church's activities.

Guests connect to the church WiFi first, register with their phone number, receive a
**45-minute session**, and are then able to view church activities (programs, sermons,
giving, contact information).

### 1.2 Scope
- A standalone, cross-platform, mobile-first web application.
- Delivered in its own folder (`guest-access-portal/`), separate from the existing
  church website and registration system.
- Provides QR-based or link-based access for guests.
- Registers new guests (new guests only receive WiFi access).
- Enforces a one-time 45-minute session per phone number per day.
- Integrates with the existing church data (Firebase `church-registration-grace`).

### 1.3 Stakeholders
- **Church administration** — manage guest registrations and view activity.
- **Guests / first-time visitors** — register and use WiFi + view activities.
- **Church staff / welcome team** — direct guests to the portal (QR, sign, desk).

### 1.4 Definitions / Terminology
| Term | Definition |
|------|------------|
| Guest | A first-time or visiting person with an unregistered phone number. |
| Session | A single 45-minute period of allowed access for one phone number. |
| Returning | A phone number that has already registered with the church before. |
| Portal | The web app guests land on when granted WiFi access. |

---

## 2. Functional Requirements

### 2.1 Guest Access Flow
- FR-01: A guest connects to the church WiFi network.
- FR-02: The guest is presented with the portal (via QR code scan or open-captive redirect).
- FR-03: The portal displays a welcome page branded for Grace of Jesus Christ Ministries.

### 2.2 Registration
- FR-04: The portal collects at minimum a **Full Name** and **Phone Number**.
- FR-05: The phone number is used to check whether the guest is new or returning.
- FR-06: **Only new (unregistered) guests** are granted WiFi access.
- FR-07: New registrations are saved to the church's registration database
  (`registrations` collection in Firebase Firestore).
- FR-08: Fields already present in the existing church registration may be reused
  (e.g. location, registration type) but are not required for this portal's initial
  deployment.

### 2.3 Session Control (45-Minute Limit)
- FR-09: Each new guest receives a single **45-minute** session.
- FR-10: A phone number may receive **one** session per day (soft-enforced in v1).
- FR-11: When the 45-minute timer expires, the guest is notified that their session
  has ended.
- FR-12: A guest whose session has ended (or who is returning) is told to re-register
  or see staff, and is not granted a new session that day.
- FR-13: Session state is tracked per phone number and per day.

### 2.4 Church Activities (After Registration)
- FR-14: After successful registration and session start, the guest can view church
  activities: programs, sermons, giving, and contact information.
- FR-15: Activity content may be linked from or mirrored from the existing church
  website (`churchregistration/`).

### 2.5 Administration (optional / future)
- FR-16: A simple admin view to view today's registrations and active/expired sessions.

---

## 3. Non-Functional Requirements

### 3.1 Hosting & Cost
- NFR-01: Must run on **free hosting** (e.g. GitHub Pages / Firebase Hosting).
- NFR-02: Must **not require new hardware** or ongoing subscription costs.
- NFR-03: Must not require a dedicated always-on device at the church in v1.

### 3.2 Platform & Devices
- NFR-04: Must be **mobile-first** and work on guest smartphones.
- NFR-05: Must work in modern browsers (Chrome, Safari, mobile).

### 3.3 Reliability & Offline
- NFR-06: Should handle brief connection loss gracefully (queue/pending registration
  where feasible).
- NFR-07: Graceful loading and error states for the registration save.

### 3.4 Data & Security
- NFR-08: Guest personal data (name, phone) is stored securely and only used for
  church registration purposes.
- NFR-09: No payment data involved; access is free.
- NFR-10: Privacy/consent messaging shown to guests when collecting details.

### 3.5 Maintainability
- NFR-11: Single, self-contained codebase easy to host and update.
- NFR-12: Reuse the existing Firebase project and conventions where possible.

---

## 4. UI / Design Details

### 4.1 Design Language
- Matches **Grace of Jesus Christ Ministries** branding (colors, logo, typography).
- Clean, spacious, warm, and welcoming to first-time visitors.
- Mobile-first layout; large touch targets; minimal typing.

### 4.2 Screens
1. **Welcome Screen** — church logo, "Welcome to Grace of Jesus Christ Ministries WiFi",
   connection/start CTA.
2. **Registration Screen** — Full Name + Phone Number form, privacy note, submit button.
3. **Session Countdown Screen** — shows 45-minute countdown, session active state.
4. **Activities Screen** — sections for Programs, Sermons, Giving, Contact with links.
5. **Session Ended / Returning Message** — "Your session has ended" or "New guests only,
   please see staff."

### 4.3 States / Workflow Diagram (planned)
```
Connect to WiFi
   -> Welcome Screen
   -> Registration (Name + Phone)
      -> Already registered?  ->  Returning message (no new session)
      -> New guest?           ->  Save registration + start 45-min session
           -> Session Countdown Screen
           -> Activities Screen (Programs, Sermons, Giving, Contact)
   -> After 45 minutes: Session Ended message / re-register prompt
```

---

## 5. Architecture Overview

### 5.1 Components
| Component | Description |
|-----------|-------------|
| **Frontend (Web App)** | Mobile-first web app served from free hosting. |
| **Backend / Data** | Firebase Firestore (existing project `church-registration-grace`). |
| **Authentication (optional)** | Not required for guests in v1; admin uses existing auth. |
| **Access Entry** | QR code (printed/sign) or optional captive-portal redirect link. |

### 5.2 Data Flow
1. Guest connects to WiFi.
2. Guest opens portal via QR link.
3. Portal checks phone number against Firestore `registrations`.
4. If new: portal writes new registration to `registrations` and starts a 45-min session
   (tracked in a `wifi_sessions` collection, keyed by phone + date).
5. If returning/expired: portal shows the corresponding message.

### 5.3 Proposed Firebase Collections
- `registrations` — existing church registrations (reused).
- `wifi_sessions` (new) — `{ phone, name, startTime, expiresAt, date, status }`.

### 5.4 WiFi Integration (v1 — soft enforcement)
- v1 does **not** connect to or control the WiFi router directly.
- Access entry is via QR code. The 45-minute cutoff is **soft-enforced** on the portal
  (session expiry messaging); the guest's network connection itself remains managed by
  the router.
- A hard network cutoff (true disconnect at 45 minutes) requires a router with captive
  portal / hotspot session control (e.g. MikroTik, business TP-Link, or a Raspberry Pi
  gateway) — planned as a future phase, outside v1 scope.

### 5.5 Technology (proposed)
- HTML / CSS / JavaScript (vanilla or minimal framework).
- Firebase Firestore JS SDK (v9 compat, matching existing project).
- Hosted on GitHub Pages or Firebase Hosting.

---

## 6. Open Questions / Future Phases
- Confirm the church WiFi router model and whether it supports captive portal / guest
  hotspot settings (relevant for hard 45-minute disconnect in a later phase).
- Decide whether returning members should ever receive a session (v1: new guests only).
- Decide exact activity content source (link to existing site vs. mirrored content).
- Whether an admin dashboard is required in the first release.
