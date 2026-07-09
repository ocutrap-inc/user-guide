# Arm / Disarm

_Make sure you are logged in to your account and on the Traps page._

You set the trap's mode — **Off**, **Scout**, or **Armed** — from the **arm-mode dropdown** at the top of the trap's **Controls** card. The dropdown lists what each mode does, so the difference is clear before you choose. Picking the mode the trap is already in does nothing.

### Armed State

* **Purpose**: The trap is set to capture an animal.
* **Safety Requirement**: The user must manually open the door to activate this state. This ensures safety during the arming process.
* **Behavior**: Once armed and the door is confirmed open, the trap enters a low-power mode, conserving energy while remaining active for an animal to enter.
* **Notifications**: The trap sends periodic updates while armed. It may also use a low-power check-in cycle (about every **20 minutes**) and can appear briefly offline between check-ins — this is normal. You will receive an alert if the trap stays disconnected for more than an hour.

### Scouting State

* **Purpose**: The trap watches activity without closing the door.
* **Safety Requirement**: The door must already be fully open before Scouting Mode can be enabled.
* **Behavior**: Scouting detects animals like Armed mode, but the door stays open.
* **Notifications**: You can receive a Scout Alert when an animal first enters the pre-capture area and a Scout Trigger if it reaches the normal trigger distance. Each alert type can send once every 5 minutes. Photos may still continue during that window.

For full details, see the [Scouting Mode](scouting-mode.md) page.

### Unarmed State

* **Purpose**: The trap is not set to capture and is in a standby mode.
* **Behavior**: In this state, the trap listens for commands and does not close the door automatically if motion is detected.
* **Transition**: After a verified capture, the trap moves to **Captured** state — door closed and locked — and stays there until you tap **Open door** (which releases the door and returns to Unarmed) or **Disarm** / set the mode to **Off** (which returns to Unarmed but leaves the door closed). See [After a Capture](after-capture.md) for the full guarantee.
