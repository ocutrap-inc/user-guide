---
description: >-
  A quick side-by-side for customers moving from the old OcuTrap app to the new
  one — the same features, with a few renamed screens and controls.
---

# What's new: old app vs. new app

Everything you did in the old app you can still do in the new one — a few things just have clearer names or live on a tidier screen. Use this page as a quick translation guide.

<!--
EDITOR NOTE (SW-317 / SW-361): Arm-mode labels below follow the app's CURRENT
control-bar labels per app/requirements.md §5.1 (setArmMode: off = "Disarmed",
monitor = "Monitor", armed = "Armed"). SW-361 (needs-graham) may rename these to
Unarmed / Scouting / Armed to match this guide's legacy pages and firmware
strings ("Scout Alert"). This page is written around what each mode DOES so it
survives either decision; if SW-361 lands on Unarmed/Scouting, update only the
mode-name cells in the table below and the one line under "Arming your trap".
-->

***

## Signing in

| Old app | New app |
| --- | --- |
| `base.ocutrap.com` | `app.ocutrap.com` |
| Your old username and password | The **same email**, with a new password you set from your welcome email — your account is already set up, see [Switching to the new OcuTrap app](README.md) |

***

## Screens and terms that changed

| In the old app | In the new app | What it is |
| --- | --- | --- |
| Arm / Un-arm button and Scouting Mode | One **arm control** in the **Trap Control Bar**, with three modes | Pick how your trap behaves — see "Arming your trap" below |
| Open & Closed button | **Door control** in the Trap Control Bar | Open or close the door remotely |
| Trap Control | **Trap Control Bar** | The controls bar on each trap's page: arm mode, door, release, and snooze |
| Logs | **Activity** (and a per-trap **Audit log**) | A timeline of what your trap did and what commands were sent |
| Image Recognition | **Detections** | Photos are automatically tagged with what was seen; filter your photos by **Captured**, **Triggered**, and **Test** |
| Photos / camera view | **Captures** (also shown as Images) | Your trap's photo gallery, across one trap or all of them |
| Notifications | **Inbox** | Where delivered alerts and reminders collect; you still choose what you're notified about in **Notification settings** |
| Billing (per trap) | **Billing** — a per-trap page **and** an account overview | Each trap still has its own subscription; the account view shows them together |

***

## Arming your trap

Arming moved into a single control in the **Trap Control Bar** with three modes. Same behavior you already know, in one place:

* **Armed** — normal operation; the trap actively catches.
* **Monitor** — the trap watches and sends detections/alerts without running the full catch cycle. (This is what the old app called **Scouting**.)
* **Off** — the trap is not actively catching.

Pick a mode and the trap updates over cellular; the control shows the current mode at a glance.

{% hint style="info" %}
The old **Scouting Mode** page maps to **Monitor** here. If you see "Scouting" anywhere in this guide, it means the same as **Monitor** in the app.
{% endhint %}

***

## New in the new app

A few things the old app didn't have:

* **Map** — see all your traps on a map with their live location.
* **Analytics** — capture trends and a species breakdown across your fleet.
* **Organizations** — share a fleet with a team and bill it together (great for programs and multi-user operations). See [Sharing Traps](../faqs/sharing-traps/README.md).
* **Command menu** — press <kbd>Cmd/Ctrl</kbd>&nbsp;+&nbsp;<kbd>K</kbd> on the web app to jump to any trap or screen.

***

## What didn't change

* Each trap still has **its own subscription**, and cellular data is still included.
* Notifications still come from your trap's own firmware — the app just delivers and labels them.
* Your capture history and images all came across with you.

Still have a question? **[Contact support](../support/support.md)** — we're happy to help you get oriented.
