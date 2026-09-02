---
description: >-
  A closed trap holds the animal until you release it. There is no auto-
  release. Open versus Unarm, on-trap buttons, and what the app shows.
---

# After a capture

## What does *not* happen

* The door does **not** reopen on a timer.
* The door does **not** reopen if the animal calms down or stops moving.
* The door does **not** reopen because of a cooldown or any sensor reading.
* The trap does **not** auto-disarm itself or change state on its own.

You can be 15 minutes away or 15 hours away, and the trap will stay locked.

## What you control

Two buttons matter after a capture:

| Button | What it does |
| --- | --- |
| **Open** | Releases the door **and** returns the trap to **Unarmed**. Use this most of the time: one tap frees the animal and resets the trap for inspection. |
| **Unarm** | Returns the state to **Unarmed** but **leaves the door closed**. Use this if you want to keep the animal contained while you transport the trap, then tap **Open** later when you're ready to release. |

### On-trap buttons (v927+)

| Buttons | From **Captured** | Result |
| --- | --- | --- |
| **User + Power** (arm/disarm sequence) | Disarm **in place** | **Unarmed**, door **unchanged** (stays closed), same as cloud **Unarm** |
| **User hold-open** (press User once, then press again and **hold**; door opens ~7 s later) | Release door | Door **opens** and trap returns to **Unarmed**, same as cloud **Open**. Use this to free the animal, not User+Power |

> **Do not confuse the two:** User+Power disarms without opening. To release an animal, use **Open** in the app or the **hold-open** button sequence on the trap.

For full step-by-step instructions on both sequences, see [Using the Buttons on the Trap](../using-the-trap-buttons.md).

## What you'll see in the app while captured

* Trap card status reads **Captured / Closed**.
* You'll get repeat reminders for up to 48 hours so a captured animal isn't forgotten. They stop after 48 hours by design.
* Manual **Request Image** still works if you want a fresh photo of the captured animal.

## Common questions

**Q: If I'm out of cell range, will the trap eventually open?**
No. The trap holds locally. Without a cloud command, the door does not move.

**Q: If the battery dies while captured, does the door open?**
No. The latch is mechanical; loss of power does not release it.

**Q: Can I close a trap that's already in Captured state?**
The door is already closed. Tapping **Close** while in Captured is a no-op (it stays Captured).

**Q: How do I get the trap ready for the next capture?**
After tapping **Open**, the trap is in **Unarmed / Open**. Tap **Arm** on the trap card to put it back into Armed mode for the next capture.

## See also

* [Trap Control](trap-control.md): how the modes relate and how to send door commands.
* [Scouting Mode](scouting-mode.md): non-trapping observation mode.
