---
description: >-
  How OcuTrap stays connected over 4G LTE cellular, what to expect from coverage,
  and how the trap keeps working when signal is weak.
---

# Connectivity and cellular coverage

OcuTrap connects to the OcuTrap app over **4G LTE cellular**, the same kind of network your phone uses. There is **no Wi-Fi and nothing to set up**. Power the trap on, and it connects automatically.

***

## How OcuTrap Connects

* **Cellular only.** OcuTrap uses **multi-network 4G LTE** across the **United States and Canada**. It does **not** use Wi-Fi, and no local network setup is required.
* **Data included.** The cellular data your trap uses is **included in your OcuTrap subscription**. There's no separate data plan or SIM card to buy. See [Your OcuTrap Subscription](../account-and-billing/subscription-overview.md).
* **Automatic.** On power-up, the trap finds a network and comes online on its own.
* **No hotspot or router needed.** You don't need any other equipment in the field.

The trap is not tied to a single carrier. It reaches **multiple nationwide 4G LTE networks** and picks whichever one has the best usable signal at your site, switching automatically if that network fails. If a trap sits in marginal coverage, work through [Improving a Weak Cellular Signal](../troubleshooting/improving-a-weak-cellular-signal.md).

***

## What Affects Coverage

Like any cellular device, OcuTrap needs a usable signal where it's deployed.

* **Available in the US and Canada.** OcuTrap's cellular service covers the **United States and Canada**. The trap is not supported in other countries.
* **Place it where there's signal.** Areas with **strong cellular signal** give you the most reliable connection *and* the best battery life. A weak signal makes the trap work harder to stay connected and drains the battery faster.
* **Obstacles matter.** Dense buildings, deep valleys, and very remote backcountry may have little or no coverage.
* **GPS is separate.** Location uses a built-in GPS module (clear view of the sky helps) and updates about every 8 hours. See [GPS](../faqs/gps.md).

{% hint style="info" %}
For battery and signal tips on where to place a trap, see **Optimal Trap Placement** in [Tips and Tricks](tips-and-tricks.md).
{% endhint %}

***

## Staying Armed When Signal Is Weak

OcuTrap is built to keep working through brief connectivity gaps:

* In **Armed Sleep Offline** mode, the trap **stays armed and monitoring for captures even while disconnected**, checking in with the cloud about every **20 minutes**.
* If a **capture happens while offline**, the trap **reports it at its next check-in**. You won't lose the event.
* See [Power Modes](../faqs/power-modes.md) for how the trap balances connectivity and battery.

{% hint style="warning" %}
When a trap is in **Hibernation** (very low battery, long idle, or powered off), it **cannot send or receive anything**. See [Power Modes](../faqs/power-modes.md).
{% endhint %}

***

## Checking Your Trap's Connection

* The app shows each trap's status and how long ago it last checked in.
* If a trap won't come online, work through [Trap Offline or Won't Connect](../troubleshooting/trap-offline-or-wont-connect.md).

***

## Connectivity and Reporting

* **Regular Updates**: The trap pings several times an hour to report its status and confirm network connection.
* **Disconnection Alert**: Users are alerted if the trap loses network connectivity for over an hour.

***

## See also

* [Technical Specifications](technical-specifications.md): cellular, GPS, and sensor details.
* [Power Modes](../faqs/power-modes.md): how the trap conserves battery and stays armed offline.
* [GPS](../faqs/gps.md): location tracking and map view.
* [Trap Offline or Won't Connect](../troubleshooting/trap-offline-or-wont-connect.md): troubleshooting connection issues.
