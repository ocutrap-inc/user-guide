# Settings Reference

This page provides a complete reference of all configurable settings on your OcuTrap, including their ranges, defaults, and descriptions.

> **Note:** After changing settings, a reboot of the trap is recommended to ensure all changes are applied correctly.

---

## Capture & Detection Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Capture Distance** | 125–1000mm (5–39 in) | 250mm (10 in) | Distance from sensor that triggers a capture. Objects crossing this threshold will close the door. |
| **Pre-Capture Alerts** | On/Off | On | Sends an alert when an animal enters the detection zone (before capture). Includes a 2-minute cooldown between alerts. |

### Detection Zones Explained

OcuTrap uses two detection zones to verify captures and reduce false triggers:

- **Detection Zone**: 300–450mm from sensor — Object must show 3+ consecutive valid readings here first
- **Capture Zone**: 0–250mm from sensor — Final trigger point that closes the door

This dual-zone system prevents false triggers from rain, debris, or quick movements.

---

## Camera Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Camera Time Lapse** | 0–24 hours | 6 hours | How often the camera takes periodic photos while armed. Set to 0 to disable timelapse. |
| **Camera Quality** | 1–6 | 2 | Image resolution size (1=QVGA smallest, 6=UXGA largest). Higher = better quality but more data/power. |
| **Rotate Image** | 0°, 90°, 180°, 270° | 0° | Rotates captured images. Useful if trap is mounted in non-standard orientation. |
| **Dark Lux Threshold** | 1–100 lux | 25 lux | Light level below which the environment is considered "dark" and IR lighting activates. |
| **Minimum IR Brightness** | 0–100% | 10% | Minimum infrared LED brightness in dark conditions. |
| **Maximum IR Brightness** | 0–100% | 100% | Maximum infrared LED brightness. Lower values reduce glare and save power. |

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
| **Battery Type** | 5Ah / 10Ah | Varies by region | Must match installed battery for accurate level estimation. |
| **Battery Alerts** | On/Off | On | Enables low battery notifications at 20% and 10% levels. |
| **Power-Off Voltage** | 7.0–12.0V | 9.6V | Voltage threshold below which the trap automatically hibernates. |

### Battery Alert Thresholds

| Alert Level | Default Voltage | Description |
|-------------|-----------------|-------------|
| 20% Warning | 10.4V | Low battery warning sent |
| 10% Critical | ~9.5V | Critical battery warning sent |
| Auto Power-Off | 9.6V | Trap enters hibernation to protect battery |
| Reset Threshold | 11.0V | Battery must reach this level to clear low-battery flags |

---

## Temperature Alert Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Temperature Alerts** | On/Off | On | Enables alerts when temperature exceeds thresholds. |
| **High Temperature Limit** | Configurable | 45°C (113°F) | Alert sent if internal temperature rises above this. |
| **Low Temperature Limit** | Configurable | -10°C (14°F) | Alert sent if internal temperature falls below this. |
| **Temperature Alert Interval** | 0–48 hours | 8 hours | Minimum time between temperature alerts. Set to 0 to disable repeat alerts. |

---

## GPS & Location Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Location (GPS)** | On/Off | On | Enables periodic GPS location updates. |
| **GPS Interval** | Configurable | 8 hours | How often the trap updates its GPS position. Longer intervals save battery. |

### GPS Behavior Details

- **First fix delay**: 5-minute initial delay after boot before first GPS acquisition
- **Acquisition timeout**: 3 minutes for first fix, 2 minutes for subsequent fixes
- **Fix requirements**: Minimum 5 satellites, 3D fix required for valid position
- **Automatic updates**: GPS automatically triggered on capture events

---

## Accessory Port Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Accessory** | On/Off | Off | Enables the 12V accessory port for external devices. |
| **Accessory Timing** | 0–30,000ms | — | Duration the accessory port remains powered when activated. |

The 12V accessory port can power external devices like dispensers, pumps, or other add-on hardware.

---

## Capture Alert Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Capture Alerts Interval** | 0–48 hours | 8 hours | Minimum time between capture alert notifications. Prevents repeated alerts for same capture. |

---

## Hardware & Feedback Settings

| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| **User Beeps** | On/Off | On | Audible beeps for button presses, state changes, and feedback. |
| **Enhanced Door Closing** | On/Off | Off | Performs additional open/close cycle to ensure door is fully locked. |
| **Units** | Metric/Imperial | Imperial | Display units for distance and temperature throughout the app. |

---

## Image Cropping Settings

These settings remove portions of the image before processing. Values are percentages of the image dimension.

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Left Crop** | 0–50% | 0% | Removes left portion of image |
| **Right Crop** | 0–50% | 0% | Removes right portion of image |
| **Top Crop** | 0–50% | 0% | Removes top portion of image |
| **Bottom Crop** | 0–50% | 0% | Removes bottom portion of image |

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
- Set GPS Interval to 8+ hours
- Use Camera Quality level 1–2
- Set Camera Time Lapse to 6+ hours or disable
- Reduce Maximum IR Brightness if images are overexposed

### For Best Image Quality
- Use Camera Quality level 4–6
- Adjust Dark Lux Threshold based on your deployment (lower = earlier IR activation)
- Fine-tune IR brightness settings for your environment

### For Fastest Response
- Keep GPS enabled for accurate location on captures
- Enable Pre-Capture Alerts to see animals approaching
- Use shorter Capture Alert Intervals if monitoring actively
