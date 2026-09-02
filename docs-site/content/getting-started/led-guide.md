---
description: >-
  Identify OcuTrap LED colors and patterns with the interactive diagnostic or
  reference table, including buttons and low-battery behavior.
---

# LED Guide

_Applies to: OcuTrap R1 and R2._

The light on your OcuTrap tells you what the trap is doing. **Pick the color you
see, then how it's behaving, and this guide takes you straight to what it means
and how to fix it.** Prefer a table? The full reference is right below the
diagnostic.

On **battery**, the light stays off between brief check-in flashes. Roughly one
quick flash every ~10 seconds is normal. On **external/USB power** (or for a few
seconds after a command) the light stays on continuously.

```led-diagnostics
# ─────────────────────────────────────────────────────────────────────────────
# SINGLE SOURCE OF TRUTH for the interactive LED diagnostic wizard (SW-333 /
# SITE-10) AND the reference table rendered on this page. Edit entries here.
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
# combinations). Add multiple entries; the wizard lists them together.
# ─────────────────────────────────────────────────────────────────────────────
entries:
  - color: cyan
    pattern: breathing
    context: idle on power
    meaning: Connected to the cloud and fully operational.
    action: Your trap is online. Nothing to do.
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
    action: Normal for a few seconds. The light returns to its resting state once the door finishes closing.

  - color: blue
    pattern: solid
    meaning: Unarmed, with the door open.
    action: Normal resting state when the trap is not armed and the door is open.
  - color: blue
    pattern: blinking
    context: just after a command
    meaning: Opening the door after a manual open command.
    action: Normal for a few seconds while the door opens.
  - color: blue
    pattern: fast-blink
    context: idle, not after a command
    meaning: The trap is trying to join the cellular network and cannot. It keeps retrying and never reaches the cloud, so it stays offline in the app.
    action: Move the trap outdoors or to an area with better cellular coverage and give it 10 minutes. If it is still blinking blue quickly, contact support with your Trap ID.
    links:
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
      - label: Connectivity & Coverage
        href: /getting-started/connectivity-and-coverage
      - label: Contact Support
        href: /support/support

  - color: yellow
    pattern: solid
    meaning: Armed and ready to capture.
    action: The trap is watching the capture zone. Nothing to do.
  - color: yellow
    pattern: blinking
    context: just after arming
    meaning: Arming the trap and checking the capture zone.
    action: Wait a few seconds. If it flashes solid red instead, arming was blocked. Clear the obstruction or clean the sensor window and try again.

  - color: magenta
    pattern: solid
    meaning: An animal has been captured.
    action: Approach carefully and handle the captured animal safely.
    links:
      - label: Handling a Captured Animal
        href: /getting-started/handling-a-captured-animal
  - color: magenta
    pattern: blinking
    context: on battery, idle (one short flash every 3 seconds)
    meaning: An animal is captured and the door is closed. This is the normal captured indication on battery power.
    action: Check the app for the capture photo and release the animal when ready.
    links:
      - label: After a Capture
        href: /getting-started/app/after-capture
      - label: Handling a Captured Animal
        href: /getting-started/handling-a-captured-animal
  - color: magenta
    pattern: blinking
    meaning: Firmware update in progress, or booting in safe mode.
    action: Leave the trap powered on and wait. Do not disconnect the battery.
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
    meaning: Arming was blocked. Something is in the way, the sensor window needs cleaning, or an update is pending. The trap did NOT arm.
    action: Clear the obstruction or clean the sensor window, then try arming again.
  - color: red
    pattern: solid
    context: at boot, or staying red while idle
    meaning: Battery critically low at startup, or the trap is hibernating / shut down.
    action: Charge or replace the battery, then press the power button to wake the trap.
    links:
      - label: Battery Overview
        href: /getting-started/battery-overview
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
  - color: red
    pattern: fast-blink
    meaning: Powering down while the power button is being held to shut the trap down.
    action: Release within ~3 seconds to cancel. Otherwise the LED goes solid red and the trap powers off. Rapid red blinking is not a fault code. Genuine faults show as brief flash bursts (see the note below the table).

  - color: no-light
    pattern: off
    meaning: No power, hibernating, or a failed boot. On battery, brief flashes every ~10 seconds are normal. Only a light that never appears is a problem.
    action: Reconnect the yellow battery connector, press the power button once, then send any command from the app to confirm the trap is awake.
    links:
      - label: Trap Offline or Won't Connect
        href: /troubleshooting/trap-offline-or-wont-connect
      - label: Power Modes
        href: /faqs/power-modes
```

> **Note:** Rapid red blinking is **not** an error code. It means the trap is powering down. Genuine faults show as brief flash bursts: **3 orange flashes** for a sensor error (clean the lens and power-cycle) or **5 magenta flashes** for a data error. If a fault repeats, [contact support](../support/support.md). These states are managed automatically; only use the power button if the LED does not respond.

***

### ⚠️ Low Battery Startup Behavior

When the battery is **critically low at startup**, the following will happen:

* The trap shows a **solid red LED** during boot.
* Sends a cloud error notification (if connected).
* Automatically shuts down and enters hibernation.
* It wakes once an hour to re-check, for two attempts. If the battery is still low after that, it stays off until you press the Power button.

To recover, charge or replace the battery and press the power button again.

***

### 🎛️ User Button Interactions

The color and pattern for each of these actions is in the diagnostic and table
above. This section covers **how to trigger** them with the physical buttons.
For the full how-to, including arming failures and power off, see
[Using the Buttons on the Trap](using-the-trap-buttons.md).

#### Manual Door Control

To manually open or close the trap door:

1. Press the **User Button** once.
2. Press it again and **hold for about 5 seconds**. After a short confirmation delay (about **7 seconds total** from the start of the hold), the door actuates.

Hold the button for the full duration. Releasing early cancels the action. The door then opens (or closes) and stays in that position; there is no auto-close timer.

The door light blinks **blue** while opening and **green** while closing.

#### Arm / Unarm the Trap

1. Press the **User Button**, then the **Power Button**

The light blinks **yellow** while arming and **white** while unarming.

***

### Pattern animations

The GIFs below are short visual examples of the most common **connection** patterns. They do not replace the reference above.

#### Connected Mode

* **Breathing Cyan**: The trap is connected to the cloud and online.
* <img src="../.gitbook/assets/Breathing Cyan.gif" alt="" data-size="line">

#### Connecting to the Cloud

* **Rapidly Blinking Cyan**: The trap is connecting to the cloud, usually after finding cellular signal.
* <img src="../.gitbook/assets/Untitled design (5).gif" alt="" data-size="line">

#### OTA Firmware Update

* **Blinking Magenta**: A firmware update is in progress, or the trap is captured and running on battery. Leave the trap powered on and wait, and check the app for a capture.
* <img src="../.gitbook/assets/Rapidly Blinking Magenta.gif" alt="" data-size="line">

#### Looking for Internet

* **Blinking Green**: The device is attempting to establish a cellular connection.
* <img src="../.gitbook/assets/Rapidly Blinking Green.gif" alt="" data-size="line">

#### Red light or no light?

Rapid red blinking usually means the trap is **powering down** (power button held), not an SOS/error code. Solid red, brief red flashes after a command, and “no light” cases are all covered above. If the LED never comes on after you reconnect the battery and press power, see [Trap Offline or Won't Connect](../troubleshooting/trap-offline-or-wont-connect.md).

***

### Notes

* LED brightness may dim in low power mode to conserve battery.
* No LED means the device is off or in hibernation.
* Any pattern not listed here may indicate a malfunction. [Contact support](../support/support.md) if unsure.
