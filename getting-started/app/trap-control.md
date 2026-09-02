---
description: >-
  The Trap Controls bar in detail: arm mode, door commands, quick actions like
  image and location, advanced commands, and command status.
---

# Trap control

Each trap's detail screen has a **Trap Controls** bar. This card sets the trap's arm mode and sends commands to the device. (It replaces the older pop-up control panel.)

### Arm mode

At the top of the controls is the **arm-mode selector**. Set the trap's mode to **Off**, **Scout**, or **Armed** from the **arm-mode dropdown** at the top of the trap's **Controls** card. The dropdown explains each mode before you choose. Picking the mode the trap is already in does nothing.

{% hint style="info" %}
You can also arm and unarm at the trap itself, using the User and Power buttons on the POD. That works even when the trap has no cellular signal. See [Using the buttons on the trap](../using-the-trap-buttons.md).
{% endhint %}

#### Armed State

* **Purpose**: The trap is set to capture an animal.
* **Safety Requirement**: The user must manually open the door to activate this state. This ensures safety during the arming process.
* **Behavior**: Once armed and the door is confirmed open, the trap enters a low-power mode, conserving energy while remaining active for an animal to enter.
* **Notifications**: The trap sends periodic updates while armed. It may also use a low-power check-in cycle (about every **20 minutes**) and can appear briefly offline between check-ins. This is normal. You will receive an alert if the trap stays disconnected for more than an hour.

#### Scouting State

* **Purpose**: The trap watches activity without closing the door.
* **Safety Requirement**: The door must already be fully open before Scouting Mode can be enabled.
* **Behavior**: Scouting detects animals like Armed mode, but the door stays open.
* **Notifications**: You can receive a Scout Alert when an animal first enters the pre-capture area and a Scout Trigger if it reaches the normal trigger distance. Each alert type can send once every 5 minutes. Photos may still continue during that window.

For full details, see the [Scouting mode](scouting-mode.md) page.

#### Unarmed State

* **Purpose**: The trap is not set to capture and is in a standby mode.
* **Behavior**: In this state, the trap listens for commands and does not close the door automatically if motion is detected.
* **Transition**: After a verified capture, the trap moves to **Captured** state with the door closed and locked. It stays there until you tap **Open door** (which releases the door and returns to Unarmed) or **Disarm** / set the mode to **Off** (which returns to Unarmed but leaves the door closed). See [After a capture](after-capture.md) for the full guarantee.

### Primary action

Below the arm mode is the main door control:

* **Open door / Close door:** moves the door.
* The control shows the last door state the trap reported.
* When the trap is **Captured**, the primary action becomes **Disarm & release** (returns to Unarmed and opens the door) with a **Snooze** option for the capture reminders. See [After a capture](after-capture.md).

> **Releasing a captured animal:** tap **Open**. This releases the door and returns the trap to **Unarmed** in one step. The trap never auto-releases. See [After a capture](after-capture.md).

> **Before Scouting Mode:** the door must be fully open. See [Scouting mode](scouting-mode.md) for how scouting works without closing the door.

### Quick actions

A row of quick actions handles the most common commands:

* **Request Image:** request a fresh photo from the camera. See [Requesting photos](requesting-photos.md).
* **Location:** request an updated GPS location. See [GPS](../../faqs/gps.md).
* **Buzz:** sound the trap's buzzer, handy for locating the trap or confirming it's responsive.

### Advanced

Expand **Advanced** for less-common commands:

* **Data refresh:** ask the trap to take a fresh set of readings and send them in right now, instead of waiting for its next scheduled check-in. Use it when you want up-to-the-minute battery, signal, or temperature values. The trap has to be awake and in range to answer. On the mobile app this command is called **Status Check**.
* **Reboot:** restart the device. Asks you to confirm first.
* **Sleep:** put the trap into hibernation (sleeps until you press the power button or change the battery). Asks you to confirm first. See [Power modes](../../faqs/power-modes.md).

### Command status

After you send a command, a status line under the controls shows its progress: **Sending…**, then confirmed or failed, and **Image incoming…** when you request a photo. This tells you whether the trap received your command.

### Checking data, network, and charts

Device and network details live outside the controls bar, on the trap detail screen:

* **Vitals**: battery, signal, temperature, and **Last heard**. Select **Last heard** to **Ping** the trap (ask it to check in right now). When the trap answers, **Last heard** updates to show that check-in. That is how you pull the latest data on demand: it will check in right away if it's connected.
* **Charts**: graphical history of the trap's performance over time. Pick a reading (battery, signal, and more) and a time range. A trap builds this history as it checks in, so a newly added trap has little to show at first and fills in over the following days.

The camera view and the map for the trap are on that same detail screen.
