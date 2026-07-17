---
description: >-
  This guide explains what each LED color and pattern means on your OcuTrap
  device. Use the interactive diagnostic — pick the color, then the pattern — or
  read the full reference table. Covers system status, user-button
  interactions, and low-battery behavior.
---

# LED Guide

The light on your OcuTrap tells you what the trap is doing. **Pick the color you
see, then how it's behaving, and this guide takes you straight to what it means
and how to fix it.** Prefer a table? The full reference is right below the
diagnostic.

On **battery**, the light stays off between brief check-in flashes — roughly one
quick flash every ~10 seconds is normal. On **external/USB power** (or for a few
seconds after a command) the light stays on continuously.

```led-diagnostics
# ─────────────────────────────────────────────────────────────────────────────
# SINGLE SOURCE OF TRUTH for the interactive LED diagnostic wizard (SW-333 /
# SITE-10) AND the reference table rendered on this page. Edit entries here —
# the wizard and the table both update on the next deploy, with no code changes.
#
# Each entry:
#   color    a color id: blue | green | cyan | yellow | magenta | white | red |
#            no-light   (drives the swatch shown in the wizard)
#   pattern  solid | breathing | blinking | fast-blink | off
#   meaning  what this color+pattern indicates
#   action   (optional) what the customer should do
#   context  (optional) short qualifier, e.g. "idle on power", "after a command"
#   links    (optional) site-absolute paths into the relevant fix pages
#
# The same color+pattern may carry more than one meaning (the LEDs reuse
# combinations) — just add multiple entries; the wizard lists them together.
# ─────────────────────────────────────────────────────────────────────────────
entries:
  - color: cyan
    pattern: breathing
    context: idle on power
    meaning: Connected to the cloud and fully operational.
    action: Your trap is online — nothing to do.
  - color: cyan
    pattern: fast-blink
    meaning: Connecting to the cloud.
    action: Wait a few minutes while it connects.
    links:
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect

  - color: green
    pattern: solid
    meaning: Unarmed, with the door closed.
    action: Normal resting state when the trap is not armed and the door is closed.
  - color: green
    pattern: blinking
    context: idle on power
    meaning: Searching for a cellular signal (looking for internet).
    action: Move the trap outdoors or to an area with better cellular coverage, then give it a few minutes to reconnect.
    links:
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
      - label: Connectivity & Coverage
        href: /getting-started/connectivity-and-coverage
  - color: green
    pattern: blinking
    context: just after a command
    meaning: Closing the door after a manual close command.
    action: Normal for a few seconds — the light returns to its resting state once the door finishes closing.

  - color: blue
    pattern: solid
    meaning: Unarmed, with the door open.
    action: Normal resting state when the trap is not armed and the door is open.
  - color: blue
    pattern: blinking
    context: just after a command
    meaning: Opening the door after a manual open command.
    action: Normal for a few seconds while the door opens.

  - color: yellow
    pattern: solid
    meaning: Armed and ready to capture.
    action: The trap is watching the capture zone. Nothing to do.
  - color: yellow
    pattern: blinking
    context: just after arming
    meaning: Arming the trap — checking the capture zone.
    action: Wait a few seconds. If it flashes solid red instead, arming was blocked — clear the obstruction or clean the sensor window and try again.

  - color: magenta
    pattern: solid
    meaning: An animal has been captured.
    action: Approach carefully and handle the captured animal safely.
    links:
      - label: Handling a Captured Animal
        href: /getting-started/handling-a-captured-animal
  - color: magenta
    pattern: blinking
    meaning: Firmware update in progress, or booting in safe mode.
    action: Leave the trap powered on and wait — do not disconnect the battery.
    links:
      - label: Updating Firmware
        href: /faqs/updating-firmware

  - color: white
    pattern: blinking
    context: just after a command
    meaning: Unarming the trap.
    action: Normal for a few seconds while the trap disarms.

  - color: red
    pattern: solid
    context: ~2 seconds after an arm command
    meaning: Arming was blocked — something is in the way, the sensor window needs cleaning, or an update is pending. The trap did NOT arm.
    action: Clear the obstruction or clean the sensor window, then try arming again.
  - color: red
    pattern: solid
    context: at boot, or staying red while idle
    meaning: Battery critically low at startup, or the trap is hibernating / shut down.
    action: Charge or replace the battery, then press the power button to wake the trap.
    links:
      - label: Battery
        href: /faqs/battery
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
  - color: red
    pattern: fast-blink
    meaning: Powering down — the power button is being held to shut the trap down.
    action: Release within ~3 seconds to cancel. Otherwise the LED goes solid red and the trap powers off. Rapid red blinking is not a fault code — genuine faults show as brief flash bursts (see the note below the table).

  - color: no-light
    pattern: off
    meaning: No power, hibernating, or a failed boot. On battery, brief flashes every ~10 seconds are normal — only a light that never appears is a problem.
    action: Reconnect the yellow battery connector, press the power button once, then send any command from the app to confirm the trap is awake.
    links:
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
      - label: Power Modes
        href: /faqs/power-modes
```

> **Note:** Rapid red blinking is **not** an error code — it means the trap is powering down. Genuine faults show as brief flash bursts: **3 orange flashes** for a sensor error (clean the lens and power-cycle) or **5 magenta flashes** for a data error. If a fault repeats, [contact support](../support/support.md). These states are managed automatically; only use the power button if the LED does not respond.

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

### 🎛️ User Button Interactions

The color and pattern for each of these actions is in the diagnostic and table
above. This section covers **how to trigger** them with the physical buttons.

#### Manual Door Control

To manually open or close the trap door:

1. Press the **User Button** once.
2. Press it again and **hold for about 5 seconds**. After a short confirmation delay (about **7 seconds total** from the start of the hold), the door actuates.

Hold the button for the full duration — releasing early cancels the action. The door then opens (or closes) and stays in that position; there is no auto-close timer.

The door light blinks **blue** while opening and **green** while closing.

#### Arm / Unarm the Trap

1. Press the **User Button**, then the **Power Button**

The light blinks **yellow** while arming and **white** while unarming.

***

### Notes

* LED brightness may dim in low power mode to conserve battery.
* No LED means the device is off or in hibernation.
* Any pattern not listed here may indicate a malfunction — [contact support](../support/support.md) if unsure.
