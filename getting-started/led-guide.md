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
| Powering Down        | Rapid Red Blinks   | The power button is being held to shut the trap down. Release within ~3 seconds to cancel; otherwise the LED goes solid red and the trap powers off. |
| No Status LED        | No Light           | Device has no power or failed to boot.                    |
| Hibernation          | LED Off / Solid Red | Trap has entered low-power sleep (often after a low-battery shutdown). Wake with power button. |

> Note: Rapid red blinking is **not** an error code — it means the trap is powering down. Genuine faults show as brief flash bursts: **3 orange flashes** for a sensor error (clean the lens and power-cycle) or **5 magenta flashes** for a data error. If a fault repeats, [contact support](../support/support.md). These modes are managed automatically; only use the power button if the LED does not respond.

***

### ⚠️ Low Battery Startup Behavior

When the battery is **critically low at startup**, the following will happen:

* The trap shows a **solid red LED** during boot.
* Sends a cloud error notification (if connected).
* Automatically shuts down and enters hibernation.
* Low-battery hibernation auto-wakes about once an hour to re-check the battery (v946+); it recovers on its own once voltage is back. Only a manual power-button shutdown stays off until you press the power button.
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

1. Press the **User Button** once.
2. Press it again and **hold for about 5 seconds**. After a short confirmation delay (about **7 seconds total** from the start of the hold), the door actuates.

Hold the button for the full duration — releasing early cancels the action. The door then opens (or closes) and stays in that position; there is no auto-close timer.

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
* Any pattern not listed here may indicate a malfunction — [contact support](../support/support.md) if unsure.
