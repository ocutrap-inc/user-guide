# Settings Reference

Every trap setting lives in the **Settings** tab of the trap's detail page — open a trap and select **Settings**. All settings are in that one place; there is no separate "More Settings" or "Advanced Settings" screen.

> **Note:** After changing settings, a reboot of the trap is recommended so all changes take effect.

Ranges and defaults below match the app. Sliders show their current value as you drag.

## Battery Alerts

| Setting | Options / range | Description |
|---|---|---|
| **Battery Type** | Not specified · 5000mAh LiPo 12V (~60Wh) · 111Wh 12V (LiFePO4 / lead-acid) · AA Alkaline pack | Match this to the battery installed so level estimates and alerts are accurate. Default: Not specified. |
| **Low battery threshold** | 15–50% | Battery level at which you get a low-battery alert. Default: 20%. |
| **Critical battery threshold** | 5–20% | Battery level at which you get a critical alert. Default: 10%. |

## Weather Alerts

Get notified when the **outdoor temperature** at the trap's location crosses limits you set — useful for protecting a captured animal in extreme heat or cold.

## General

| Setting | Options | Description |
|---|---|---|
| **Enable Beeps** | On / Off | Audible beeps from the trap for button presses and state changes. |
| **Use Metric Units** | On / Off | Show measurements in metric. |
| **Enable GPS** | On / Off | Let the trap report its GPS location. |

## Camera

| Setting | Options | Description |
|---|---|---|
| **Image Size** | Small (640×480) · Medium (1280×720) · Large (1920×1080) | Resolution of captured photos. Larger = more detail, more data and power. |
| **Image Rotation** | 0° · 90° · 180° · 270° | Rotate photos if the trap is mounted in a non-standard orientation. Default: 0°. |
| **Time-lapse Interval** | Disabled · 1h · 2h · 4h · 6h · 12h · 24h | How often the camera takes periodic photos while armed. Default: Disabled. |

## Scout

| Setting | Options | Description |
|---|---|---|
| **Scout Image Quality** | QQVGA (160×120) · QVGA (320×240) · VGA (640×480) · SVGA (800×600) · XGA (1024×768) · HD (1280×720) | Resolution of photos while in Scout mode. Default: VGA (640×480). |
| **Scout Photo Interval** | Disabled (only on detection) · 15s · 30s · 1m · 2m · 5m | How often Scout takes photos while an animal is present. Default: 30s. |

## Image Cropping

| Setting | Range | Description |
|---|---|---|
| **Crop Top / Bottom / Left / Right** | 0–50% (step 5%) | Trim edges out of the photo — e.g. to cut a bright cage bar or the sky. Default: 0% (no crop). |

## Motion Detection

| Setting | Range | Description |
|---|---|---|
| **Capture Distance** | 100–2000 mm (step 50) | How far inside the trap an animal must be before the door closes. |
| **Accelerometer Time** | 100–5000 ms (step 100) | How long movement must persist to count as motion. |
| **Dark Threshold** | 1–100 lux | Light level below which the trap treats the scene as dark and turns on IR lighting. |
| **Min IR Brightness** | 0–255 (step 5) | Minimum infrared LED brightness in the dark. |
| **Max IR Brightness** | 0–255 (step 5) | Maximum infrared LED brightness. Lower values cut glare and save power. |

## Alerts

| Setting | Options | Description |
|---|---|---|
| **Capture Alert Mode** | Disabled · On Motion · Always | When to send capture alerts. |
| **Pre-Capture Alerts** | On / Off | Alert when an animal enters the detection area, before a capture. |
| **Battery Alerts** | On / Off | Send low- and critical-battery notifications. |

## Battery Thresholds (advanced)

These calibrate the voltages behind the battery percentages above. Most users won't need to touch them.

| Setting | Range | Description |
|---|---|---|
| **20% Alert Voltage** | 3.0–4.2 V | Voltage treated as the 20% (low) level. |
| **10% Alert Voltage** | 3.0–4.2 V | Voltage treated as the 10% (critical) level. |
| **Full Battery Voltage** | 3.8–4.2 V | Voltage treated as a full battery. |

## Power Management (advanced)

| Setting | Range / options | Description |
|---|---|---|
| **Power Off Voltage** | 3.0–3.6 V | The trap powers down to protect the battery below this voltage. |
| **Arm When Offline** | On / Off | Let the trap arm even when it can't reach the network. |
