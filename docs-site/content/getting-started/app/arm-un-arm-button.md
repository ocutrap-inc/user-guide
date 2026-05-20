# Arm / Unarm Button

_Make sure you are logged in to your account and on the Traps page._

### Armed State

* **Purpose**: The trap is set to capture an animal.
* **Safety Requirement**: The user must manually open the door to activate this state. This ensures safety during the arming process.
* **Behavior**: Once armed and the door is confirmed open, the trap enters a low-power mode, conserving energy while remaining active for an animal to enter.
* **Notifications**: The trap maintains a connection by sending periodic updates. If disconnected for more than an hour, a notification is sent to the user.

### Scouting State

* **Purpose**: The trap watches activity without closing the door.
* **Safety Requirement**: The door must already be fully open before Scouting Mode can be enabled.
* **Behavior**: Scouting detects animals like Armed mode, but the door stays open.
* **Notifications**: You can receive a Scout Alert when an animal first enters the pre-capture area and a Scout Trigger if it reaches the normal trigger distance. Each alert type can send once every 5 minutes. Photos may still continue during that window.

For full details, see the [Scouting Mode](scouting-mode.md) page.

### Unarmed State

* **Purpose**: The trap is not set to capture and is in a standby mode.
* **Behavior**: In this state, the trap listens for commands and does not close the door automatically if motion is detected.
* **Transition**: After a verified capture, the trap moves to **Captured** state — door closed and locked — and stays there until you tap **Open** (which releases the door and returns to Unarmed) or **Unarm** (which returns to Unarmed but leaves the door closed). See [After a Capture](after-capture.md) for the full guarantee.
