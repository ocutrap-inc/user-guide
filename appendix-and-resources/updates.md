# Updates

<details>

<summary>May 4, 2026</summary>

### Firmware v706 — Reliability, Battery, and Image Improvements

> **Release date:** 4 May 2026

_Quieter LEDs, no more dropped approach photos, faster image uploads, and battery alerts that survive offline windows. Plus periodic photos while an animal is in the trap during Monitoring Mode._

***

#### How the update installs

This version is delivered **over‑the‑air (OTA)**. It downloads and installs automatically the next time the trap reboots or powers up. No manual action is required.

> **Check the version**\
> _Settings → Trap Info → Firmware_ should show `v706` or newer.

***

#### 📷 Image capture improvements

* **No more dropped approach photos (v700+).** On older firmware, if the animal moved while a photo was already being uploaded, the next approach photo would be silently dropped. v700+ defers the dropped photo into a single-slot pending queue and fires it as soon as the camera is free. If multiple approach moments collide, the **nearest** distance wins — so you see the most useful frame.
* **Faster image transfers (v705+).** Modern cameras now use a 100 ms chunk-read timeout (down from 200 ms). Image uploads finish noticeably faster on cellular, especially during heavy transfers.
* **Periodic photos during Monitoring (v675+).** While an animal stays inside a detection zone in Monitoring Mode, the trap now requests a fresh photo about every 30 seconds — so you can watch activity unfold instead of seeing only the entry shot. Tunable per-trap with `monImgInt`.

#### 🔋 Battery and power

* **LED off during low-power sleep (v702+).** The status LED no longer stays solid red while the trap is in deep sleep. Eliminates a small but constant battery drain.
* **20%/10% battery alerts now durable (v704+).** Low-battery notifications now survive offline windows and reboots — they queue up if the trap can't reach the cloud and deliver the next time it connects.
* **`Low battery shutdown` events captured at runtime (v704+).** Previously, the cause of an emergency shutdown was only logged at the next boot. Now the event is queued at runtime so it reaches the cloud reliably.

#### 🛠️ Reliability

* **Hibernation retries on sleep-fail (v703+).** If the trap can't enter sleep cleanly, it now retries instead of staying awake. Cellular connections also auto-recover after sleep-related stalls.
* **Boot-time emergency-halt loop replaced (v706+).** The legacy `System.sleep` API at boot is gone; the main loop now handles the retry instead. Fewer mysterious hangs after power events.
* **`pwrOff` always reported (v701+).** The power-off setting now appears in `callback_settings` even when at default — useful for fleet diagnostics.

#### 🩺 Diagnostics (for fleet operators)

* **`arm=N pend=N` visible on the serial heartbeat (v700+).** Real-time visibility into armed-detection state and any pending approach photo. Helps diagnose why a detection cycle did or didn't fire.

***

#### Monitoring Mode is now documented

Full customer documentation for **Monitoring Mode** (use it for scouting without closing the door) is now live in the docs at **Getting Started → App → Monitoring Mode**, including the firmware-version requirements table and troubleshooting tips. Most deployed traps run **v550** as of April 2026, which **does not support** Monitoring Mode — see [Updating firmware](../faqs/updating-firmware.md) to bring your trap up to date.

***

#### Version note

If you are checking with support, the firmware version for this release is **`v706`**. Individual feature notes above call out the exact version each capability landed in (v675, v700, v701, v702, v703, v704, v705, v706).

***

</details>

<details>

<summary>April 3, 2026</summary>

### Firmware v2.1.2-632 — Monitoring Mode Update

> **Release date:** 3 Apr 2026

> ⚠️ **Note:** Monitoring Mode is not yet released and is currently in testing. This feature is not available to users at this time.

_Monitoring mode now uses the live armed detection logic for scouting without closing the trap._

***

#### What changed

* Added a dedicated **Monitoring Mode** behavior for scouting
* The trap now requires the **door to be fully open** before monitoring can start
* Monitoring sends an alert when an animal reaches the **pre-capture distance**
* Monitoring sends another alert if the animal reaches the **trigger distance**
* The trap **does not close the door** while in monitoring mode
* After the animal leaves, monitoring resets and applies a **5-minute cooldown** before a new monitoring alert cycle can begin

***

#### Version note

If you are checking with support, the firmware version for this release is **`v2.1.2-632`**.

***

</details>

<details>

<summary>April 21, 2024</summary>

### Firmware v1.12.7‑250 — Release Notes

> **Release date:** 21 Apr 2025

_New toggle for keeping the trap awake while unarmed, plus faster GPS, clearer battery readings, and assorted fixes._

***

#### How the update installs

This version is delivered **over‑the‑air (OTA)**. It downloads and installs automatically the next time the trap reboots or powers up (for example, after a battery swap). No manual action is required.

> **Check the version**\
> \&#xNAN;_Settings → Device Info → Firmware_ should show `v1.12.7‑250`.

***

#### 🎛️ New — Unarmed Hibernation Control

| Setting                | Behaviour                                                                              | Default |
| ---------------------- | -------------------------------------------------------------------------------------- | ------- |
| **Unarmed Sleep Mode** | After 2 h unarmed & idle, the trap enters full hibernation (power‑off) to save battery | **Yes** |

**Change it:**\
`Settings → More Settings → Unarmed Sleep Mode` → toggle **No** to keep the trap fully powered while unarmed.

> **Heads‑up:** Disabling sleep increases battery usage.

***

#### 🔧 General improvements

* Faster location fixes & steadier GPS reporting
* Smoother, more accurate battery percentages and voltage readings
* Sharper, better‑timed images in all lighting conditions
* Overall stability and performance enhancements

***

</details>

<details>

<summary>Jan 8, 2023</summary>

**New Update: Dark Mode and UI Improvements on OcuTrap**

1. **Dark Mode Added:** A new Dark Mode option is now available, reducing screen glare and making the website comfortable to use in various lighting conditions.
2. **UI Enhancements:** The user interface has been improved for better navigation and responsiveness across devices.

</details>
