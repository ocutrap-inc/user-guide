---
description: >-
  Get notified (only in ARMED mode) when an animal is about to enter the trap,
  before a capture happens.
---

# Pre-capture notification

### What It Does

**When enabled and the trap is in Armed Mode**, Pre-Capture Notification alerts you when an animal is detected approaching the trigger point. This early warning system sends a notification and a photo (if applicable), helping you stay ahead of trap activity.

### How It Works

OcuTrap uses a distance sensor to detect animals before they reach the capture point. It watches two areas:

* **Detection area (out to about 34 in / 875 mm from the sensor)**: The trap tracks an approaching animal and may send a pre-capture alert with a photo.
* **Capture point (your capture-distance setting; default 8 in / 200 mm)**: The door closes once the animal is confirmed at or inside this distance.

**Default capture distance** is **8 inches (200 mm)**, adjustable from **6 to 18 inches** in the app. Pre-capture alerts can fire while an animal is still approaching in the detection area, before the door closes.

#### Example

With the default **8 in (200 mm)** capture distance:

* As the animal approaches within the detection area (out to ~34 in), you may receive a **Pre-Capture Alert** with an approach photo.
* At **~8 in (200 mm) or closer**, the trap confirms capture and the door closes.

In the app, the notification shows as a **Pre-Capture Alert**. It tells you an animal is approaching before a capture happens and includes an approach photo when available. In [Scouting Mode](../app/scouting-mode.md) the same approach event shows as a **Scout Alert** instead. The distance the animal was detected at is recorded on the event details.

> Units (inches or millimeters) depend on your trap's **Units** setting. For the full sensor model, see [Technical Specifications](../technical-specifications.md).

### How to Enable or Disable

This setting is configured per trap:

1. Open the OcuTrap app or [app.ocutrap.com](https://app.ocutrap.com)
2. Tap on the trap you want to edit
3. Go to **Settings → More Settings**
4. Find the **Pre-Capture Notification** option
5. Toggle to **On** or **Off**

> Default setting: **On**

### Why Use This Feature?

* See what’s approaching your trap before it’s too late
* Detect non-target animals early (like pets or skunks)
* Monitor animal behavior without needing a capture, or use [Scouting Mode](../app/scouting-mode.md) to watch activity without closing the door
* Improve trap placement and setup based on activity patterns

### What you'll see (alert motion gate, firmware v906+)

| Signal | When it fires |
| --- | --- |
| **Pre-Capture Alert** | After the animal shows **real inward movement** (~3 in / 75 mm) toward the trap: static grass or debris in the detection zone will **not** trigger the alert |
| **Approach photos** | On zone entry and during approach: **not** blocked by the motion gate that holds the alert |
| **Door close** | Only when the animal is confirmed in the capture zone (Armed mode) |

> **Testing tip:** To verify pre-capture behavior, arm the trap normally with the door open and approach slowly. Scout mode uses the same motion gate for its alert; approach photos are not held by that gate.

### Need to Turn It Off?

If you prefer to only be notified after a capture, you can disable **Pre-Capture Notification** in settings at any time. It will not affect the actual capture or release functions.
