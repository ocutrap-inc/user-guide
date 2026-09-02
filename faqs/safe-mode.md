---
description: >-
  Safe Mode is a recovery step for a trap stuck in a crash or boot loop.
  Button sequence, the magenta LED, and when support will ask you to use it.
---

# Safe-mode

**What Safe Mode is for:** Safe Mode is a recovery mode built into the trap's cellular controller. In Safe Mode the device still starts up and connects to the cloud, but it does **not** run the trap's normal program. That lets it accept a firmware update (or clear a bad state) when the trap is stuck in a crash or boot loop and won't come online on its own. It's an advanced step. You normally only need it when **OcuTrap Support** asks you to use it while recovering a device.

While in Safe Mode the LED shows **magenta** (the same firmware-update color you'll see in the [LED Guide](../getting-started/led-guide.md)).

**Buttons:** The **RESET** and **MODE** buttons referred to below are the two small buttons on the trap's internal cellular controller (the cellular module inside the POD), not the User and Power buttons you use for everyday operation.

**Prerequisite:** Make sure the device has enough battery charge. If it will not turn on, charge the battery and try again.

**To put your device in Safe Mode:**

1. Hold down BOTH buttons (RESET and MODE).
2. Release only the RESET button, while continuing to hold down the MODE button.
3. Wait for the LED to start blinking magenta.
4. Release the MODE button.

Before the LED blinks magenta, the trap goes through its normal startup sequence (blinking green, then blinking cyan). If the trap cannot connect to the cloud, you may not see breathing magenta. If the LED is blinking magenta after you release the MODE button, Safe Mode is active.

If you're not sure whether your trap needs Safe Mode, [contact support](../support/support.md) before using it.
