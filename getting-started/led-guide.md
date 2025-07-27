---
description: >-
  This guide explains what each LED pattern means on your OcuTrap device. It
  includes normal system statuses, user-button interactions, and low-battery
  behavior.
---

# LED Guide

## System Status Indicators

These patterns occur during power-up, connectivity, or firmware activity.

| Status               | LED Pattern        | Description                                               |
| -------------------- | ------------------ | --------------------------------------------------------- |
| Connected Mode       | Breathing Cyan     | Connected to the cloud and fully operational.             |
| Connecting to Cloud  | Fast Blinking Cyan | Attempting to connect to the cloud.                       |
| OTA Firmware Update  | Blinking Magenta   | Firmware update or booting in safe mode.                  |
| Looking for Internet | Blinking Green     | Searching for a cellular signal.                          |
| Red Flash SOS        | Rapid Red Blinks   | Firmware crash. Contact support if >10 blinks.            |
| No Status LED        | No Light           | Device has no power or failed to boot.                    |
| Hibernation          | LED Off            | Trap has entered low-power sleep. Wake with power button. |

> Note: These modes are managed automatically. Only use the power button if the LED does not respond.

***

### ⚠️ Low Battery Startup Behavior

When the battery is too low (below 9.6V at startup), the following will happen:

* The trap shows a **solid red LED** during boot.
* Sends a cloud error notification (if connected).
* Automatically shuts down and enters hibernation.
* Will not auto-recover — must be awakened manually using the power button.
* If voltage is still low, it will repeat the cycle.

To recover, charge or replace the battery and press the power button again.

***

### 🎛️ User Button LED Patterns

These appear when using the physical **User Button** or **Power Button** on the device.

#### Device State Indicators

| State              | LED Pattern   |
| ------------------ | ------------- |
| Unarmed and Open   | Solid Blue    |
| Unarmed and Closed | Solid Green   |
| Armed Mode         | Solid Yellow  |
| Armed and Captured | Solid Magenta |

#### Manual Door Control

To manually open or close the trap door:

1. Press the **User Button**
2. Press again and hold for 5 seconds

| Action     | LED Pattern    |
| ---------- | -------------- |
| Open Door  | Blinking Blue  |
| Close Door | Blinking Green |

#### Arm/Unarm the Trap

1. Press the **User Button**, then the **Power Button**

| Action     | LED Pattern     |
| ---------- | --------------- |
| Arm Trap   | Blinking Yellow |
| Unarm Trap | Blinking White  |

***

### Notes

* LED brightness may dim in low power mode to conserve battery.
* No LED means the device is off or in hibernation.
* Any pattern not listed here may indicate a malfunction — [contact support ](../support/support.md)if unsure.
