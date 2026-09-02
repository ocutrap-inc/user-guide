---
description: Check every OcuTrap setting, including ranges, defaults, locations, and what each option controls.
---

# Settings reference

Use this reference to check every configurable OcuTrap setting, including ranges and defaults.

> **Note:** After changing settings, a reboot of the trap is recommended to ensure all changes are applied correctly.

---

## Capture & Detection Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Capture Distance** | 6 to 18 in (app presets) | 8 in | How far inside the trap an animal must be before the door closes. |
| **Pre-Capture Alerts** | On/Off | On | Sends an alert when an animal enters the detection zone (before capture). Includes a 60-second cooldown between alerts. |

### Detection Zones Explained

OcuTrap uses two steps to verify captures and reduce false triggers:

- **Detection area** (out to ~34 in / 875 mm from the sensor): The animal is approaching; you may get a pre-capture alert
- **Capture zone** (your set distance, default ~8 in): The door closes when the animal reaches this point

This two-step check prevents false triggers from rain, debris, or quick movements.

---

## Camera Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Camera Time Lapse** | 0 to 24 hours | 6 hours | How often the camera takes periodic photos in every mode (unarmed, armed, scouting, and after a capture). Set to 0 to disable timelapse. |
| **Camera Quality** | 1 to 6 | 2 | Image resolution size (1=QVGA smallest, 6=UXGA largest). Higher = better quality but more data/power. |
| **Rotate Image** | 0°, 90°, 180°, 270° | 0° | Rotates captured images. Useful if trap is mounted in non-standard orientation. |
| **Dark Lux Threshold** | 1 to 100 lux | 25 lux | Light level below which the environment is considered "dark" and IR lighting activates. |
| **Minimum IR Brightness** | 0 to 100% | 10% | Minimum infrared LED brightness in dark conditions. |
| **Maximum IR Brightness** | 0 to 100% | 100% | Maximum infrared LED brightness. Lower values reduce glare and save power. |

### Camera Quality Levels

| Level | Resolution | Best For |
|-------|------------|----------|
| 1 | QVGA (320×240) | Fastest transfer, lowest data usage |
| 2 | VGA (640×480) | Good balance of quality and speed (default) |
| 3 | SVGA (800×600) | Better detail |
| 4 | XGA (1024×768) | High detail |
| 5 | SXGA (1280×1024) | Very high detail |
| 6 | UXGA (1600×1200) | Maximum detail, highest data usage |

---

## Battery & Power Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Battery Type** | 5200 mAh / 10000 mAh | KBT 5,200 mAh (56 Wh) | Must match installed battery for accurate level estimation. |
| **Battery Alerts** | On/Off | On | Enables low battery notifications at 20% and 10% levels. |
| **Power-Off Voltage** | Set by Battery Type (9.6 V for both packs) | 9.6V | Voltage threshold below which the trap automatically hibernates. |

### Battery Alert Thresholds

| Alert Level | Default Voltage | Description |
|-------------|-----------------|-------------|
| 20% Warning | 10.4V | Low battery warning sent |
| 10% Critical | 10.2V | Critical battery warning sent |
| Auto Power-Off | 9.6V | Trap enters hibernation to protect battery |
| Reset Threshold | 11.0V | Battery must reach this level to clear low-battery flags |

Voltages shown are for the 5,200 mAh pack. The 10,000 mAh pack uses 10.2 V (20%) and 10.0 V (10%).

---

## Temperature Alert Settings

These alerts watch the **outdoor weather at the trap's location**, not the trap's own internal sensor. The trap's location can come from its GPS fix or from a location you set manually. See [Temperature alerts](#temperature-alerts) below.

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Temperature Alerts** | On/Off | Off | Enables alerts when the outdoor temperature at the trap passes a limit below. |
| **High Temperature Limit** | Configurable | 45°C (113°F) | Alert sent if the outdoor temperature rises above this. |
| **Low Temperature Limit** | Configurable | -10°C (14°F) | Alert sent if the outdoor temperature falls below this. |
| **Temperature Alert Interval** | 1 to 24 hours | 6 hours | Minimum time between repeat temperature alerts. |

---

## GPS & Location Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Location (GPS)** | On/Off | On | Location (GPS) is on or off. When on, the trap gets a fix 15 minutes after boot and then every 8 hours; the interval is fixed. Turn it off for indoor or covered deployments to save battery. |

### GPS Behavior Details

- **First fix delay**: 15 minutes after boot before the first GPS acquisition
- **Acquisition timeout**: 3 minutes for first fix, 2 minutes for subsequent fixes
- **Fix requirements**: Minimum 5 satellites, 3D fix required for valid position
- **Captures take priority**: A capture in progress pauses GPS until it finishes; GPS never interrupts a capture

---

## Accessory Port Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Accessory Port on-duration** | 0 to 30,000 ms | 0 (off) | How long the 12V accessory port stays powered when activated. 0 means off. The **Accessory** quick action appears in Controls only when the duration is above 0. |

The 12V accessory port can power external devices like dispensers, pumps, or other add-on hardware.

---

## Capture Alert Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Capture Alerts Interval** | 0 to 48 hours | 8 hours | Minimum time between capture alert notifications. Prevents repeated alerts for same capture. |

---

## Hardware & Feedback Settings

| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| **Enhanced Door Closing** | On/Off | On | Re-seats the door under the locking rod after every close, captures included. Improves the chance the door locks. Does not confirm it. |
| **EDC Backoff (ms)** | 30 to 130 ms (10 ms steps) | 50 ms | **Advanced per-trap setting.** Leave it at 50 ms if the door consistently finishes under the fixed bar. An incorrect value can prevent EDC recovery or leave the door effectively unlocked. If calibration is needed, use an empty trap and change one 10 ms step at a time. Needs firmware v2.3.2-1010+. |
| **Actuator Inverse** | On/Off | Off | Reverses the door motor drive direction. Turn On if your motor is going the wrong way and the door opens when it should close. |
| **Units** | Metric/Imperial | Imperial | Display units for distance and temperature throughout the app. |

---

## Image Cropping Settings

These settings remove portions of the image before processing. Values are percentages of the image dimension.

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Left Crop** | 0 to 50% | 0% | Removes left portion of image |
| **Right Crop** | 0 to 50% | 0% | Removes right portion of image |
| **Top Crop** | 0 to 50% | 0% | Removes top portion of image |
| **Bottom Crop** | 0 to 50% | 0% | Removes bottom portion of image |

---

## Enhanced door closing and EDC backoff

Enhanced Door Closing re-seats the door after every close, including closes on a capture. The door backs off slightly, then drives closed again to seat under the locking rod. This improves the chance the door locks. It does not confirm the lock. Enabled by default. Turn it off only if support asks. See [Enhanced Door Closing](../../capture-behavior/enhanced-door-closing.md).

EDC Backoff sets how long the door reverses during Enhanced Door Closing. A higher time reverses farther; a lower time reverses less. Options run from 30 to 130 ms in 10 ms steps. Default is 50 ms, and most traps calibrate between about 40 and 120 ms.

{% hint style="warning" %}
**Advanced setting:** Leave EDC Backoff at its **50 ms default** if the door consistently finishes underneath the locking bar. An incorrect value can prevent EDC recovery or reverse the door too far and leave it effectively unlocked. Adjust only while calibrating an empty trap.
{% endhint %}

Every trap door is slightly different, and a fully charged battery can move the motor faster. Both too little and too much reverse can leave the door on top of the fixed locking bar:

- Door does not retract enough to re-seat: raise the value by 10 ms.
- Door retracts so far that it begins to lift and lands on top of the bar again: lower the value by 10 ms.

Start at 40 ms and change one step at a time, testing with a fully charged battery. Pass only when repeated cycles finish underneath the bar every time. See [Enhanced Door Closing](../../capture-behavior/enhanced-door-closing.md) for the complete calibration and optional recovery test.

Requires trap firmware v2.3.2-1010 or newer. Older firmware ignores this setting. Only applies while Enhanced Door Closing is On. If adjusting it does not fix the door, the mechanism needs physical inspection. Contact support.

---

## Temperature alerts

Only a trap that has neither, one that has never reported a location and never had one set, cannot check the weather. If that happens, set the location yourself and the checks begin at the next interval.

The selected interval determines how often the weather is checked.

Until the first check comes back, the card shows **Not checked yet** and no temperature. Checks run on a schedule rather than the moment you switch them on, so give it up to an hour to fill in.

Temperature limits use the selected unit system, shown as Imperial in the interface. **Above Upper Limit** sets the maximum temperature; an alert is sent if the outdoor temperature at the trap rises above this value. **Below Lower Limit** sets the minimum temperature; an alert is sent if the outdoor temperature at the trap falls below this value.

---

## Image cropping

Cropping adjusts how images are cropped before being processed or uploaded. Use it to remove unnecessary areas of the image, reduce file size, or focus on a specific region inside the trap.

---

## Settings Locations

Settings are accessible in different locations:

| Location | Settings Available |
|----------|-------------------|
| **App → Trap → Settings → More Settings** | Most user settings |
| **App → Trap → Settings → Advanced Settings** | Temperature alerts, image cropping |
| **App → Account** | Notification preferences, units |

---

## Tips for Optimal Settings

### For Maximum Battery Life
- Turn Location (GPS) off if you do not need location tracking
- Use Camera Quality level 1 to 2
- Set Camera Time Lapse to 6+ hours or disable
- Reduce Maximum IR Brightness if images are overexposed

### For Best Image Quality
- Use Camera Quality level 4 to 6
- Adjust Dark Lux Threshold based on your deployment (lower = earlier IR activation)
- Fine-tune IR brightness settings for your environment

### For Fastest Response
- Keep Location (GPS) on so the map stays current
- Enable Pre-Capture Alerts to see animals approaching
- Use shorter Capture Alert Intervals if monitoring actively
