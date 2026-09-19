# Notes & Public Documents

This repository hosts public documents, policies, and notes by [Tal Rosner](https://github.com/RosnerTal).

## MapMe Google Play Compliance Documents

The official Google Play Store compliance documents for the **MapMe** Android app (`com.talapp.mapme`):

- 🔒 **[MapMe Privacy Policy](MapMe/privacy-policy.html)**: Comprehensive policy detailing location tracking (foreground & background), Google Sign-In, Firebase Cloud Firestore storage, and OpenStreetMap/OSRM routing.
- 🗑️ **[MapMe Data Deletion Instructions](MapMe/data-deletion.html)**: Step-by-step instructions for in-app trip deletion and complete account/cloud data erasure per Google Play Data Safety requirements.
- 🌐 **[MapMe Portal](MapMe/index.html)**: Legal and privacy landing page.

---

### Google Play Console Reference URLs

When providing links in Google Play Console (Policy > Privacy Policy and Data safety > Delete account URL):

- **Privacy Policy URL:**
  `https://raw.githack.com/RosnerTal/notes/main/MapMe/privacy-policy.html`  
  *(or via GitHub Pages if enabled: `https://rosnertal.github.io/notes/MapMe/privacy-policy.html`)*

- **Account & Data Deletion URL:**
  `https://raw.githack.com/RosnerTal/notes/main/MapMe/data-deletion.html`  
  *(or via GitHub Pages if enabled: `https://rosnertal.github.io/notes/MapMe/data-deletion.html`)*

- 🎥 **Foreground Service Location Video Demo Page:**
  `https://raw.githack.com/RosnerTal/notes/main/MapMe/video-demo.html`  
  *(or via GitHub Pages if enabled: `https://rosnertal.github.io/notes/MapMe/video-demo.html`)*

- ⬇️ **Direct MP4 Video File URL:**
  `https://github.com/RosnerTal/notes/raw/main/MapMe/mapme-foreground-service-demo.mp4`

---

### Google Play Foreground Service Declaration Text

When prompted in Google Play Console to describe the task requiring `FOREGROUND_SERVICE_LOCATION`:

> **Tasks that require the permission:** Check **Navigation** (and/or **Other: Route Exploration Recording**)
>
> **User-facing explanation:**  
> MapMe is a personal street exploration and turn-by-turn navigation application. When a user explicitly taps "Start Walk", "Start Drive", or initiates navigation, the app must continuously record GPS coordinates to color visited streets on an OpenStreetMap map and compute real-time turn maneuvers. Because users walk or drive with their phone in their pocket or screen turned off, MapMe uses FOREGROUND_SERVICE_LOCATION to prevent the Android operating system from killing location updates in the background. A persistent, user-facing ongoing notification is displayed in the system notification shade at all times with live duration, distance, and pause/stop controls. Location data is never shared with third-party advertisers.

