---
description: >-
  Learn how to enable and configure the Accessory Port on your OcuTrap. This
  guide covers activation, timing settings, and power limits.
---

# Accessory Port

### **Enabling the Accessory Port**

To enable or disable the **Accessory Port**, follow these steps:

1. Open the **OcuTrap Mobile App**.
2. Navigate to **Trap Settings**.
3. Select **More Settings**.
4. Find the **Accessory** section.
5. Toggle **Enable or Disable Accessory Port** as needed.

#### **Accessory Timing**

You can configure the duration for which the accessory port remains active:

1. Under **Trap Settings → More Settings → Accessory**, locate **Accessory Timing**.
2. Set the desired activation duration in seconds.
3. Save your settings.

### **Controls Menu Update**

Once the **Accessory Port** is enabled, a new **Accessory Control Button** will appear in the trap’s **Controls Menu**. This allows you to manually activate the accessory directly from the app.

1. Open the **Controls Menu** for the trap.
2. Locate the **Accessory** button (wrench icon 🛠️).
3. Tap the button to activate the accessory for the configured duration.
4. The accessory will automatically turn off after the preset time.

If the **Accessory Port** is disabled in settings, the **Accessory Button** will not appear in the controls menu.

### **Electrical Specifications**

* **Voltage:** 12V DC
* **Control:** MOSFET-driven circuit (IRLML6344TRPBF)
* **Default State:** Disabled (requires activation via app)
* **Activation Method:** Software-controlled toggle in the app
* **Maximum Continuous Current:** **4A**
* **Maximum Stall Current (for motors):** **Less than 4A**

### **Important Usage Notes**

#### **1. Do Not Use the Accessory and Main Door Motor Simultaneously**

* **The accessory port and the main door motor should not be activated at the same time** because both draw power from the **same 12V battery**.
* The **trap door motor** can momentarily draw up to **5A**, and if an accessory is also in use, it can exceed the power supply limits.
* **Result:** Excessive current draw may cause:
  * Device shutdown due to voltage drop.
  * Overheating and potential failure of the power circuit.
  * Reduced battery life.

#### **2. Motor Limitations**

* If connecting a **motor**, ensure its **stall current does not exceed 4A**, as excessive current draw can **damage the MOSFET** and **cause overheating**.
* Most small **DC motors and actuators** designed for **12V systems** operate within this limit, but high-power motors may require **a separate relay or motor driver**.
* If your accessory draws more than **4A**, consider using an **external MOSFET, relay, or motor driver module**.

#### **3. Timing Conflicts**

* If the **trap door is operating**, avoid triggering the accessory at the same time.
* If using an automated system, **set a delay** between **door operation** and **accessory activation** in the app settings.

### **Potential Use Cases for OcuTrap’s Accessory Port**

The **Accessory Port** on OcuTrap enables **automation and remote activation** of various external devices, making it highly versatile for different applications. Below are some **potential use cases**:

1. **Rebaiter / Feeder** – Automatically dispense bait at specific intervals to keep the trap effective longer.
2. **Vaccine Feeder** – Deliver oral vaccines to target animals, aiding in disease control efforts.
3. **Lure Dispenser** – Release scent-based attractants to increase trapping efficiency for specific species.

### Accessory Shutdown When Door Motor is Operated

**Important:** If the door motor is moved to an open or closed position while the accessory is running, the accessory will automatically power off. This behavior is an intentional safety feature designed to prevent potential conflicts between the door mechanism and the accessory. To avoid an unexpected shutdown, always ensure that the accessory is stopped before adjusting the door motor.
