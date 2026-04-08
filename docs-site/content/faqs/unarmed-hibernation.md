# Unarmed Hibernation

{% hint style="warning" %}
Applies to OcuTrap R1 firmware v1.12.3-218 and later
{% endhint %}

**Overview**

The **unarmedHibernation** setting controls whether the device will enter hibernation mode after extended periods of inactivity while in the **unarmed state**. This setting helps manage battery life and power consumption when the trap is not in use.

#### **Location**

This setting can be found in each traps **Settings** popup within the OcuTrap app.

#### **Setting Type**

* **Type:** `true` / `false`
* **Default:** `true`

#### **Functionality**

**When Enabled (`true`)**

* The device will enter **hibernation mode** after approximately **2 hours** of inactivity while unarmed.
* A **warning notification** is sent **15 minutes** before entering hibernation.
* The device **completely powers down** to conserve battery.
* To wake up, press the **power button**.

**When Disabled (`false`)**

* The device remains in **low power mode indefinitely** while unarmed.
* It **will not enter hibernation**, even after extended inactivity.
* Cloud connectivity and sensor monitoring remain **active**, but this consumes more power.

#### **Important Notes**

* This setting **only affects the unarmed state**.
* It does **not** impact hibernation triggered by **low battery** or **manual hibernation commands**.
* Disabling this feature results in **higher power consumption** since the device will not enter its lowest power state.



For optimal battery performance, we recommend keeping this setting enabled unless continuous low-power monitoring is required.
