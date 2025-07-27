---
description: >-
  Get notified when an animal is about to enter the trap—before a capture
  happens.
---

# Pre-Capture Notification

### What It Does

When enabled, **Pre-Capture Notification** alerts you when an animal is detected approaching the trigger point. This early warning system sends a notification and a photo (if applicable), helping you stay ahead of trap activity.

### How It Works

OcuTrap uses a distance sensor to detect animals before they reach the capture zone. It monitors two key areas:

* **Early Detection Zone**: Approximately 6 inches (150mm) _before_ your set capture distance
  *   #### Example

      If your **capture distance** is set to **8 inches**, then:

      * The **Primary Detection Zone** starts at **8 inches** from the sensor (this is when a capture can occur).
      * The **Early Detection Zone** starts at **14 inches**—**6 inches before** your capture distance.

      In this case, if an animal is detected at 13 inches, you’ll receive an **"Early pre-capture"** alert with the message:

      > “Early pre-capture: 13.0 in detected”

      This gives you an early warning before the trap activates at 8 inches.

If motion is detected in either zone, the trap will:

1. Take a **pre-capture photo**&#x20;
2. Send a **push/email alert** with the estimated distance

#### Example Alerts

* "Pre-capture: 10.0 in detected"
* "Early pre-capture: 15.7 in detected"

> Units (inches or centimeters) depend on your trap’s settings under **Units**.

### How to Enable or Disable

This setting is configured per trap:

1. Open the OcuTrap app or [base.ocutrap.com](https://base.ocutrap.com)
2. Tap on the trap you want to edit
3. Go to **Settings → More Settings**
4. Find the **Pre-Capture Notification** option
5. Toggle to **On** or **Off**

> Default setting: **On**

### Why Use This Feature?

* See what’s approaching your trap before it’s too late
* Detect non-target animals early (like pets or skunks)
* Monitor animal behavior without needing a capture
* Improve trap placement and setup based on activity patterns

### Need to Turn It Off?

If you prefer to only be notified after a capture, you can disable **Pre-Capture Notification** in settings at any time. It will not affect the actual capture or release functions.
