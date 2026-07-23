---
description: >-
  Below is a description of each available setting in the trap settings panel.
  These settings control power behavior, notifications, camera behavior, and
  hardware features.
---

# More Settings Overview

> **Note:** After changing any settings, a reboot of the trap is recommended to ensure all changes are applied correctly.

***

#### Battery Type

Selects the battery configuration installed in the trap. This setting is used to improve battery level estimation, charging behavior, and low battery alerts. Always match this setting to the actual battery installed.

***

#### Accessory

Enables or disables the accessory port on the trap. When enabled, the accessory port can power external devices such as dispensers or add-on hardware.

***

#### Accessory Timing

Controls how long the accessory port remains powered when activated. Shorter durations reduce power consumption, while longer durations may be required for certain accessories.

***

#### Enhanced Door Closing

Re-seats the door after every close, including closes on a capture. The door backs off slightly, then drives closed again to seat under the locking rod.

This improves the chance the door locks. It does not confirm the lock. Enabled by default. Turn it off only if support asks. See [Enhanced Door Closing](../../trap-settings/enhanced-door-closing.md).

***

#### EDC Backoff

Sets how far the door backs off during Enhanced Door Closing, in milliseconds. Options run from 30 ms to 130 ms in 10 ms steps. Default is 50 ms.

Every trap door is slightly different, and door speed rises with battery voltage. Two symptoms tell you to adjust:

- Door reverses too far while closing, most often right after installing a freshly charged battery: pick a lower value. Try 50 ms.
- Door closes but never locks under the rod: pick a higher value. Try 100 ms.

Change one step at a time and re-test with a fully charged battery. That is the worst case for over-reversing.

Requires trap firmware v2.3.2-1010 or newer. Older firmware ignores this setting. Only applies while Enhanced Door Closing is On. If adjusting it does not fix the door, the mechanism needs physical inspection. Contact support.

***

#### Camera Time Lapse

Sets how often the camera captures periodic photos in any mode (including Unarmed and Armed idle). Independent of the Scout photo interval. More frequent photos provide better visibility but increase power and data usage.

***

#### Camera Quality

Controls the image quality of photos taken by the trap camera. Higher quality images improve clarity but increase capture time, data usage, and power consumption.

***

#### Rotate Image

Adjusts the orientation of captured images. This is useful if the trap is mounted in a non-standard orientation.

***

#### Dark Lux Threshold

Defines the ambient light level at which the system considers the environment to be dark. This threshold is used to determine when infrared lighting should be activated.

***

#### Minimum IR Brightness

Sets the minimum brightness level for the infrared LEDs. This ensures a baseline level of illumination in dark environments.

***

#### Maximum IR Brightness

Sets the maximum brightness level for the infrared LEDs. Limiting the maximum brightness can help reduce glare, reflections, and power usage.

***

#### Battery Alerts

Enables or disables low battery alerts. When enabled, the system will notify users when the battery voltage drops below a defined threshold.

***

#### Pre-Capture Alerts

Enables or disables alerts that occur before a capture event. These alerts can provide early notification of activity near or inside the trap.

***

#### GPS Interval

Sets how often the trap updates its GPS location. Shorter intervals provide more frequent location updates but increase power consumption.

***

#### Location

Enables or disables periodic location logging. When enabled, the trap logs its location at regular intervals for tracking and history purposes.

***
