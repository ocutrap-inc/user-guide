# Power Modes

OcuTrap is designed with multiple power modes to **maximize battery life** while maintaining functionality in the field. These modes ensure that the device can operate efficiently for extended periods while allowing users to interact when needed.

The power management system optimizes energy consumption by adjusting connectivity, sensor activity, and LED brightness based on usage. This allows for **extended deployment without frequent battery replacements or recharges**.

> **Quick Reference**: OcuTrap has 6 power modes ranging from full operation to complete shutdown. The device automatically transitions between modes based on activity, battery level, and armed state.

***

### Power Modes

#### 1. Normal Power Mode

* **Description**: This is the highest power state where OcuTrap is fully operational.
* **When Active**: When the user is interacting with the device through commands or pressing buttons.
* **Indicators**: LED at full brightness.

***

#### 2. Low Power Idle Mode

* **Description**: A power-saving mode where the device reduces energy consumption while waiting for user interaction.
* **When Active**: After a period of inactivity in normal power mode.
* **Indicators**: LED brightness is dimmed.

***

#### 3. Low Power Armed Mode

* **Description**: Same as Low Power Idle, but the trap is armed and ready to capture an animal.
* **When Active**: When the trap is armed and waiting.
* **Indicators**: LED brightness is dimmed.
* **Sensor Activity**: Time-of-Flight sensor operating at ~300ms intervals (optimized for battery)

> **Important**: When in **armed mode**, the device will **not enter hibernation** unless a **very** **low battery event** occurs.

***

#### 4. Sleep Mode

* **Description**: A deeper power-saving state where most systems are powered down except essential wake functions.
* **When Active**: Extended periods of inactivity without being armed.
* **Indicators**: LED is powered off.
* **Power Consumption**: Very low — most sensors disabled.
* **Wake Events**: Button press, scheduled check-in, or incoming cloud command.

***

#### 5. Armed Sleep Offline Mode

* **Description**: A specialized armed mode that extends battery life further by periodically checking in with the cloud while keeping the internet disconnected in between. The trap remains armed and monitoring for captures even when offline.
* **When Active**: When armed, but conserving power between check-ins, or when cellular connectivity is unavailable.
* **Check-In Interval**: Every **20 minutes** (fixed, cannot be changed by the user).
* **Power Consumption**: Lower than Low Power Armed Mode due to reduced network usage.
* **Indicators**: LED flashes at 3-second intervals.
* **Capture Behavior**: If a capture occurs while offline, the trap will report it at the next check-in.

***

#### 6. Hibernation Mode

* **Description**: The lowest power state where the device is completely inactive. No communication is possible in this mode.
* **When Active**:
  * If the **battery is too low** to continue operation.
  * If the device is **idle for 1 hour and 45 minutes** and **not armed**. _(Unless prevent idle hibernation is enabled — Coming Soon)_
  * If the **power button is held down for 3+ seconds**.
* **Power Consumption**: Minimal.
* **Indicators**: LED is powered off.
* **Recovery**:
  * If due to **low battery**, the user must **replace or recharge** the battery.
  * If due to **idle timeout or power button press**, the user must **press the power button to wake the device**.

> **Note:** In hibernation mode, **OcuTrap cannot receive messages or send notifications**.

***

### Power Mode Transitions

#### Automatic Transitions:

* **Normal Power Mode → Low Power Idle Mode** (after inactivity).
* **Low Power Idle Mode → Low Power Armed Mode** (when armed).
* **Armed Sleep Offline → Cloud Check-in** (every 20 minutes).
* **Any Mode → Hibernation** (if low battery).
* **Low Power Idle Mode → Hibernation** (if unarmed and idle for 1 hour 45 minutes).

#### User-Controlled Transitions:

* **Power Button Press**: Can wake the device from hibernation.
* **Sending a Command**: Resets the idle timer and returns to normal power mode.

***

### Battery & Power Alerts

To ensure users are aware of power status, **OcuTrap sends battery warnings** at:

* **20% Battery** – Low battery warning.
* **10% Battery** – Critical battery warning.
* **Hibernation** – Final alert before shutdown.

These alerts help prevent unexpected downtime and allow users to take action before the device powers off.

***

### Future Enhancements _(Coming Soon)_

* **Prevent Idle Hibernation** setting to keep the device awake indefinitely when unarmed.

***

#### Summary Table

| Power Mode                 | Description                                | LED Status       | Can Receive Commands?    | Can Send Data?           |
| -------------------------- | ------------------------------------------ | ---------------- | ------------------------ | ------------------------ |
| **Normal Power Mode**      | Full power, user interaction               | Full brightness  | ✅ Yes                    | ✅ Yes                    |
| **Low Power Idle Mode**    | Reduced power while waiting                | Dimmed           | ✅ Yes                    | ✅ Yes                    |
| **Low Power Armed Mode**   | Trap is armed, waiting                     | Dimmed           | ✅ Yes                    | ✅ Yes                    |
| **Sleep Mode**             | Deep sleep, most systems off               | Off              | ✅ Yes (wakes on command) | ✅ Yes (when awake)       |
| **Armed Sleep Offline**    | Periodic check-ins, no internet in between | Flashing (3s)    | ❌ No (Between check-ins) | ✅ Yes (During check-ins) |
| **Hibernation**            | Fully powered down, no communication       | Off              | ❌ No                     | ❌ No                     |



