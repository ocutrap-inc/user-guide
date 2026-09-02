---
description: >-
  See what each More Settings option controls, including the battery,
  accessory port, door, camera, alerts, and GPS.
---

# More Settings Overview

> **Note:** After changing any settings, a reboot of the trap is recommended to ensure all changes are applied correctly.

***

#### Battery Type

Selects the battery configuration installed in the trap. This setting is used to improve battery level estimation, charging behavior, and low battery alerts. Always match this setting to the actual battery installed.

***

#### Accessory Port on-duration

The accessory port has a single control: how long it stays powered when activated, from 0 to 30,000 ms. Set it to 0 to turn the port off. There is no separate on/off toggle. The **Accessory** quick action appears in Controls only when the duration is above 0. The port can power external devices such as dispensers or add-on hardware.

***

#### Enhanced Door Closing

Re-seats the door after every close, including closes on a capture. The door backs off slightly, then drives closed again to seat under the locking rod.

This improves the chance the door locks. It does not confirm the lock. Enabled by default. Turn it off only if support asks. See [Enhanced Door Closing](../../trap-settings/enhanced-door-closing.md).

***

#### EDC Backoff

Sets how long the door reverses during Enhanced Door Closing. A higher time reverses farther; a lower time reverses less. Options run from 30 to 130 ms in 10 ms steps. Default is 50 ms, and most traps calibrate between about 40 and 120 ms.

{% hint style="warning" %}
**Advanced setting:** Leave EDC Backoff at its **50 ms default** if the door consistently finishes underneath the locking bar. An incorrect value can prevent EDC recovery or reverse the door too far and leave it effectively unlocked. Adjust only while calibrating an empty trap.
{% endhint %}

Every trap door is slightly different, and a fully charged battery can move the motor faster. Both too little and too much reverse can leave the door on top of the fixed locking bar:

- Door does not retract enough to re-seat: raise the value by 10 ms.
- Door retracts so far that it begins to lift and lands on top of the bar again: lower the value by 10 ms.

Start at 40 ms and change one step at a time, testing with a fully charged battery. Pass only when repeated cycles finish underneath the bar every time. See [Enhanced Door Closing](../../trap-settings/enhanced-door-closing.md) for the complete calibration and optional recovery test.

Requires trap firmware v2.3.2-1010 or newer. Older firmware ignores this setting. Only applies while Enhanced Door Closing is On. If adjusting it does not fix the door, the mechanism needs physical inspection. Contact support.

***

#### Camera Time Lapse

Sets how often the camera captures periodic photos in every mode (unarmed, armed, scouting, and after a capture). More frequent photos provide better visibility but increase power and data usage.

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

#### Location

Location (GPS) is on or off. When on, the trap gets a fix 15 minutes after boot and then every 8 hours; the interval is fixed. Turn it off for indoor or covered deployments to save battery.

***
