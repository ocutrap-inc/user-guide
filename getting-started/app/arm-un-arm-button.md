# Arm/ Un-arm Button

&#x200B;_&#x4D;ake sure you are logged in to your account and on the traps page._

### Armed State

* **Purpose**: The trap is set to capture an animal.
* **Safety Requirement**: The user must manually open the door to activate this state. This ensures safety during the arming process.
* **Behavior**: Once armed and the door is confirmed open, the trap enters a low-power mode, conserving energy while remaining active for an animal to enter.
* **Notifications**: The trap maintains a connection by sending periodic updates. If disconnected for more than an hour, a notification is sent to the user.

### Monitoring State

* **Purpose**: The trap is set for scouting and activity monitoring without closing the door.
* **Safety Requirement**: The door must already be fully open before monitoring can be enabled.
* **Behavior**: Monitoring uses the same animal-detection logic as armed mode, including the outer pre-capture zone and the final trigger-distance zone, but it never closes the door.
* **Notifications**: The user can receive an alert when an animal first approaches and another alert if it reaches the trigger distance. After the animal leaves, monitoring resets and waits about 5 minutes before sending a new set of scouting alerts.

### Unarmed State

* **Purpose**: The trap is not set to capture and is in a standby mode.
* **Behavior**: In this state, the trap listens for commands and does not initiate the door closure if motion is detected.
* **Transition**: After capturing an animal, the trap automatically shifts to this state, signaling the door is securely closed.
