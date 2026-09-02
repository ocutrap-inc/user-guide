---
description: >-
  When and how often your OcuTrap takes approach, scouting, capture, and
  time-lapse photos, and what controls the timing.
---

# When Your Trap Takes Photos

Your OcuTrap takes photos automatically at different times depending on what mode it's in and what's happening at the trap. This page explains when to expect photos and roughly how often.

{% hint style="info" %}
Photos only flow when the trap has cellular signal and enough battery. On low battery the trap pauses scheduled photos to protect runtime, and it never starts a new photo while the previous one is still uploading.
{% endhint %}

## Quick reference

| Situation | When photos are taken |
| --- | --- |
| **Armed, animal approaching** | A photo the moment an animal is detected, then more as it moves deeper in |
| **Armed, animal lingering in range** | Every **15 seconds** at first, stretching to about **every 4 minutes** if it stays put |
| **Scouting Mode** | Fast photos about every **15 seconds** while an animal is active, with the same stretch-out if it stays put |
| **At capture** | One photo when the door closes |
| **After a capture** | A short burst (~every 15 s for the first minute), then one **every 2 hours** |
| **Time-lapse** | **Every 6 hours** by default, in every mode (adjustable, or off) |
| **On demand** | Instantly, whenever you tap the camera button in the app |

## Approach photos (Armed Mode)

When the trap is **Armed** and an animal enters the detection area, the camera powers up and takes a first photo right away, even if the animal never comes closer. As the animal continues in, you'll get more:

* An initial **burst of up to two** quick photos.
* After that, a new approach photo each time the animal moves **about 3 inches (75 mm) closer**.
* If the animal stops and lingers, the trap still checks in with a photo **about every 10 minutes**.

Approach photos use a **fast, lower-resolution** setting so they arrive quickly during the action.

## Presence photos (Armed or Scouting)

While an animal stays within the detection area without triggering a capture, the trap keeps sending photos. The two modes use different photo types:

* **Armed Mode:** a **full-quality** photo about every **15 seconds**.
* **Scouting Mode:** a **fast** photo about every **15 seconds**. Scouting saves the full-quality shot for the moment an animal reaches the trigger distance (the **Scout Trigger** photo).

If the animal stays put, the trap stretches the spacing to protect battery: after the first few photos the gap doubles each time, up to about **4 minutes**. Fresh movement toward the trap (about 3 inches) snaps it back to 15 seconds. In Scouting Mode photos are movement-based, so a parked animal or a fixed object like a branch will not generate an endless photo stream.

In **Scouting Mode**, this is how you watch what's visiting without closing the door. You'll also get a **Scout Alert** when an animal first enters and a **Scout Trigger** if it reaches the trigger distance. Repeat alerts from the same visit are throttled so your activity feed isn't flooded, but **photos keep coming** either way. The scouting photo interval is adjustable in settings (from 15 seconds up to 5 minutes, or off).

See [Scouting Mode](scouting-mode.md) and [Pre-Capture Notification](../capture-behavior/pre-capture-notification.md).

## Capture and after-capture photos

* **At capture:** the trap takes one photo when the door closes.
* **After capture:** to document the catch, the trap takes a short burst (about every 15 seconds for the first minute), then settles into one **check-in photo every 2 hours** while the animal is held. See [After a Capture](after-capture.md).

## Time-lapse photos

Independent of animal activity, the trap takes periodic **time-lapse** photos in **every mode**: unarmed, armed, scouting, even while holding a catch. The default is **every 6 hours**. You can change the interval (up to 24 hours) or turn it off in [Settings](trap-settings/settings-reference.md).

## On-demand photos

Any time, you can request a photo from the app. Tap the **camera** button for a full-quality image or the **lightning-bolt** for a fast image. On-demand photos ignore all the timers above and capture right away. See [Requesting photos](requesting-photos.md).

## What affects the timing

{% hint style="warning" %}
A few things can stretch out the intervals above:

* **Low battery / power-saving:** scheduled photos pause until the trap is back on normal power.
* **Slow cellular or a photo backlog:** the trap automatically spaces photos out so uploads can catch up.
* **Detection range:** the trap only acts on animals within about **34 inches (875 mm)** of the sensor. Anything farther out won't trigger a photo.
{% endhint %}

***

Need image quality, night-vision, or resolution settings instead? See the [Camera FAQ](../../faqs/camera.md) and [Settings Reference](trap-settings/settings-reference.md).
