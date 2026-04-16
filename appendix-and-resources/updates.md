# Updates

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
