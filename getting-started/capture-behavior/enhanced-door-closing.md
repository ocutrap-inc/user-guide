---
description: >-
  Set and calibrate Enhanced Door Closing backoff so the trap door can re-seat
  under the locking bar without reversing too little or too far.
---

# Enhanced Door Closing

_Applies to: OcuTrap R1 and R2._

**Enhanced Door Closing (EDC)** re-seats the trap door after every close, including closes on a capture. **EDC Backoff (ms)** controls how long the door reverses during that re-seat.

## Why it exists

The locking bar is fixed. The door locks by rotating down and then sliding **under** the bar at the bottom of the trap. An obstruction can make the door come to rest **on top of** the bar instead. It looks shut from a distance, but it is not locked and an animal may be able to push it back open.

Enhanced Door Closing makes a second attempt after each close. The door backs off slightly, then drives closed again to seat under the bar.

## What EDC Backoff changes

EDC Backoff is the duration of that brief reverse movement. A higher time reverses the door farther. A lower time reverses it less.

| Timing | What happens | Result |
| --- | --- | --- |
| Too short | The door does not retract far enough to reset its position. | The second close may still leave the door on top of the bar. |
| Correct | The door retracts far enough to drop flat, then slides forward again. | The door finishes underneath the locking bar. |
| Too long | The door travels beyond the needed sliding movement and begins to lift. | The second close may put the door back on top of the bar, effectively leaving it unlocked. |

The app offers **30 to 130 ms** in 10 ms steps and defaults to **50 ms**. Most traps calibrate between about **40 and 120 ms**, but there is no single best value for every trap. Do not copy a value from another unit.

{% hint style="warning" %}
**Advanced setting:** EDC Backoff defaults to **50 ms**. If the door consistently finishes underneath the locking bar at 50 ms, **do not change it**. An incorrect value can prevent EDC from recovering after an obstruction or can reverse the door too far, leaving it on top of the bar and effectively unlocked. Adjust it only while calibrating an empty trap, one 10 ms step at a time.
{% endhint %}

Battery voltage changes motor speed. A fully charged battery makes the motor move faster; lower voltage makes it move more slowly. Always calibrate with a fully charged battery so you test the fastest normal movement and the greatest risk of reversing too far.

## Enabled or disabled

* **Enabled (default):**\
  Every close is followed by a re-seat attempt.
* **Disabled:**\
  The door closes once. No re-seat. A capture is held by whatever that single close achieved.

> **Leave this on.** Turn it off only if OcuTrap support asks you to. With it off, a trap that closes on an animal gets no second attempt to lock.

## What it does not do

Enhanced Door Closing improves the chance the door locks. It does not check whether the door locked.

The trap has no sensor that can tell a locked door from a merely closed one. The app reports **Closed** for both. Enhanced Door Closing does not change that, and no setting will confirm the lock for you. Always inspect the door at the trap during calibration and whenever a capture matters.

## Find the settings

1. Open the trap you want to update.
2. Go to **Settings**.
3. In the advanced layout, open **More Settings → Advanced Settings**, then find **Enhanced Door Closing Timing**. In the newer web and mobile layout, open the **Door** section.
4. Turn **Enhanced Door Closing** on and select **EDC Backoff (ms)**.
5. Save and allow the setting to sync to the trap.

EDC Backoff requires trap firmware **v2.3.2-1010 or newer**. Older firmware ignores it.

## Calibrate EDC Backoff

{% hint style="danger" %}
Calibrate an **empty, unarmed trap** on a stable surface. Keep hands, fingers, clothing, and your body out of the door opening whenever the door can move.
{% endhint %}

1. Fully charge the battery and install it in the trap.
2. Confirm that the door, hinge, and locking area are clean, aligned, and moving freely. Timing cannot correct a damaged or binding mechanism.
3. Turn **Enhanced Door Closing** on.
4. Close the door using **Close** in the app or the [physical-button door sequence](../using-the-trap-buttons.md#open-or-close-the-door). Inspect it at the trap and confirm it is underneath the locking bar before continuing.
5. Set **EDC Backoff (ms)** to **40 ms**, save, and wait for the setting to sync.
6. Run a complete [Open and Close cycle in the app](../app/trap-control.md), or use the physical buttons. Watch for the brief reverse followed by the second close.
7. Inspect the door at the trap. A successful cycle ends with the door underneath the locking bar, not resting on top of it.
8. Repeat the cycle several times. If the door does not retract far enough to re-seat, increase the setting by **10 ms**, save, and test again.
9. Stop at the **lowest value that ends under the bar every time**. If the reverse begins lifting the door or the door travels too far, reduce the setting by 10 ms.

| Observation | Adjustment |
| --- | --- |
| Door barely reverses and remains on top of the bar | Increase by 10 ms. |
| Door retracts, drops flat, and re-closes under the bar every time | Calibration passes. Keep this value. |
| Door reverses so far that it begins to lift, then lands on top of the bar | Decrease by 10 ms. |

If you cannot get repeatable success within the usual **40 to 120 ms** window, stop adjusting the timing and [contact OcuTrap support](../../support/support.md). The door mechanism may need inspection or alignment.

## Optional recovery test

This test checks whether EDC can recover after an obstructed first close, similar to a door that met part of an animal before reaching the locked position.

{% hint style="warning" %}
Use caution. Test only with an empty, unarmed trap. Work from outside the cage with a long **wooden broom handle** and keep your hands and body clear. Do not use your hand, a screwdriver, or another conductive metal tool. Remove the handle before the EDC reverse begins. Stop immediately if the mechanism binds or the object becomes trapped.
{% endhint %}

1. First complete the normal calibration above.
2. Open the empty trap and position yourself outside the door's travel.
3. Start a Close cycle. During the first closing movement, briefly use the wooden handle to prevent the door from completing its normal slide under the bar.
4. As soon as the door reaches the top of the locking bar, remove the handle and stay clear. Do not obstruct the EDC re-seat.
5. Watch the automatic EDC reverse and second close, then inspect the final position.

| Final position | Meaning | Next step |
| --- | --- | --- |
| Door is underneath the bar | Pass. EDC recovered and re-locked the door. | Repeat to confirm consistent operation. |
| Door remains on top after only a small reverse | Backoff is probably too short. | Increase by 10 ms and re-test. |
| Door reverses too far, lifts, and lands on top again | Backoff is too long. | Decrease by 10 ms and re-test. |

This test demonstrates recovery only. It does not add a lock sensor or make the app able to verify the final door position.

The setting syncs to the trap on its next check-in.

> **Note:** Enhanced Door Closing is enabled by default on every trap. Leave it on unless OcuTrap support directs otherwise.
