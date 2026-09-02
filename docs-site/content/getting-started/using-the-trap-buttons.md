---
description: >-
  Arm, unarm, open the door, check status, and power the trap off using the two
  buttons on the POD. Every step works at the trap, with no app and no signal.
---

# Using the buttons on the trap

_Applies to: OcuTrap R1 and R2._

The trap has two buttons on the POD: the **Power button** on the left and the **User button** on the right.

Everything on this page works with the buttons alone. No app. No cell signal. Use it when you are standing at the trap and need to arm it, unarm it, open the door, or shut it down.

{% hint style="info" %}
Every button action on this page works even when the trap has no cellular signal. The trap updates the app the next time it connects.
{% endhint %}

***

## Check the trap's status

Press the **User button** once. You get a short beep, and the LED shows the trap's state for about 5 seconds.

| LED | State |
| --- | --- |
| Magenta | Captured |
| Yellow | Armed |
| Alternating yellow and blue | Scouting |
| Blue | Unarmed, door open |
| Green | Unarmed, door closed |

Press again to keep the display up longer.

Every color and blink pattern is in the [LED Guide](led-guide.md).

***

## Open or close the door

1. Press the **User button** once. The status color shows.
2. Within 5 seconds, press the **User button** again and keep holding it.
3. After a moment the LED starts blinking the color of what will happen. Blue means the door will open. Green means the door will close.
4. Keep holding about 5 seconds, until the LED goes solid. Then release.
5. The trap beeps rapidly for 2 seconds as a warning, then the door moves.

To cancel, let go while the LED is still blinking.

{% hint style="danger" %}
Keep hands and fingers out of the door opening once the rapid beeps start. The beeps mean the door is about to move.
{% endhint %}

***

## Arm the trap

The door must be fully open before the trap will arm. Open it first, with the **Open** button in the app or with the hold sequence above.

1. Press the **User button** once.
2. Within 5 seconds, press the **Power button** once.
3. The LED blinks yellow while the trap checks that the capture zone is clear. This takes a few seconds.
4. One long high beep and a solid yellow LED confirm the trap is armed.

### If the trap refuses to arm

* **Door not fully open.** The LED pulses green and red a few times. Open the door fully and try again.
* **Something in the capture zone.** The LED pulses red a few times. Clear the area in front of the sensor and try again.
* **A sensor fault.** The LED pulses red a few times. Power the trap off and back on, then try again.
* **A firmware update is in progress.** The LED pulses red. Wait a minute and try again.

{% hint style="info" %}
Scouting mode cannot be started from the buttons. Start it in the app. See [Scouting Mode](app/scouting-mode.md).
{% endhint %}

***

## Unarm the trap

Same sequence as arming. Press the **User button** once, then press the **Power button** once. The LED blinks white, then goes solid white, with one long high beep.

This works while the trap is armed, while it is scouting, and after a capture.

{% hint style="info" %}
After a capture, User then Power unarms the trap but leaves the door closed, so the animal stays contained. To open the door and release the animal, use the open sequence above. Details: [After a Capture](app/after-capture.md).
{% endhint %}

Pressing either button on a captured trap also acknowledges the capture and quiets the capture reminder notifications.

***

## Power off and on

Hold the **Power button** about 3 seconds. The LED flashes red while you hold, then goes solid red with a descending beep, and the trap shuts down.

It stays off until you press the **Power button** again.

See [Power Modes](../faqs/power-modes.md) for what the trap is doing in each state.

***

## No signal? The buttons still work

Arming, unarming, opening the door, closing the door, checking status, and powering off all happen on the trap itself. None of them need a connection.

An armed trap keeps watching for animals with or without signal. The app catches up the next time the trap checks in, about every 20 minutes while armed.

See [Connectivity & Coverage](connectivity-and-coverage.md) and [Improving a Weak Cellular Signal](../troubleshooting/improving-a-weak-cellular-signal.md).

***

## See also

* [Trap Control](app/trap-control.md): setting the mode and sending door commands from the app.
* [After a Capture](app/after-capture.md): what Open and Unarm each do once the trap is closed.
* [LED Guide](led-guide.md): every color and blink pattern.
* [Handling & Releasing a Captured Animal](handling-a-captured-animal.md): what to do in the field.
* [Improving a Weak Cellular Signal](../troubleshooting/improving-a-weak-cellular-signal.md): getting a trap back online.
