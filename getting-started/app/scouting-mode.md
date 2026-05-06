# Scouting Mode

Scouting Mode lets you observe trap activity without ever closing the door — useful for confirming the right animals are visiting before you commit to a real capture.

## How it differs from Armed mode

|                              | Armed                              | Scouting                                                                 |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------------------------ |
| **Detects animals**          | Yes                                | Yes (same logic as Armed)                                                |
| **Closes the door**          | Yes — on first verified detection  | **Never** — observation only                                             |
| **Sends pre-capture alerts** | Yes (if enabled)                   | Yes                                                                      |
| **Captures images**          | Yes — at zone entry and at trigger | Yes — on detection, then about every 60 s while in zone (15 s – 5 min)   |
| **Reset after activity**     | N/A (door closes; trap captured)   | Auto-reset ~5 min after departure is confirmed (~30 s of clear readings) |

> **Door behavior in Scouting:** the door **never** closes, opens, or moves on its own — regardless of how many animals come and go. The only things that move the door are commands you send: **Close**, **Open**, **Arm**, or **Stop Scout** + **Close**. Whatever the animal does, the trap stays in Scouting with the door open until you change it.

## Activating Scouting Mode (walkthrough)

**Open** / **Close** / **Arm** are on the trap card. **Scout** lives one tap away inside that card's **Controls** popup.

1. Sign in to the OcuTrap app at [app.ocutrap.com](https://app.ocutrap.com) (or the mobile app). You'll land on your trap list.
2. Find the trap you want to scout. Each card shows its status, battery %, and a green dot if online.
3. Confirm the status reads **Open / Unarmed**. If the door is closed, tap **Open** on the trap card first and wait for the status to update.
4. Tap **Controls** on the trap card. A popup opens with a top row of icons: **GPS**, **Data**, **Buzzer**, **Reboot**, **Hibernation**, **Scout**.
5. Tap **Scout** (rightmost, eye icon). The trap runs an obstruction check — if anything is in the capture zone, scouting is refused so you can clear it and retry.
6. Once the check passes, the card status flips to **Scouting** and the popup icon flips to **Stop Scout** (eye with slash).

> **Tip:** If **Scout** seems unresponsive, the door usually isn't fully open, the trap is offline, or **Last heard** at the bottom of the popup is stale. Wait for the next check-in or re-open the door.

## What you'll see while scouting

* **Pre-capture alerts** when an animal enters the outer detection zone (if enabled).
* **Trigger alerts** when an animal reaches the trigger distance. The trap takes a photo but the door **does not close**.
* **Periodic photos** about every 60 seconds (configurable 15 s – 5 min) while the animal stays in zone. The trap waits for each photo to finish before starting the next, and saves the closest approach frame if the camera is busy. The interval is set fleet-wide and isn't a control in the app today — message support if you'd like it shorter (more photos, more battery drain) or longer (fewer photos, longer battery life).
* **Alert cooldown after departure** — the trap waits ~30 seconds of clear readings to confirm the animal has actually left, then another ~5 minutes before re-arming **alerts and periodic photos**. Expect about 5.5 minutes of quiet after the last in-zone reading. This cooldown is *only* about pausing notifications; **the door does not move during or after this period**.

## Exiting Scouting Mode

1. **Stop Scout** in the Controls popup — returns the trap to Unarmed, door still open.
2. **Close** on the trap card — closes the door and returns to Unarmed in one step.

## What happens if the trap actually does capture (Armed mode only)

This applies only when you've switched to **Armed** — Scouting Mode never closes the door. But because it's a common worry: once an Armed trap closes on a verified detection, the door **stays closed until you manually open it**. There is no auto-release on a timer, no auto-release if the animal calms down, no auto-release if the animal leaves a previous detection zone. The trap holds until you tap **Open** (releases the animal, returns to Unarmed) or **Unarm** (returns to Unarmed; you still need to tap **Open** afterwards to release the door). You can be hours away from the trap; it will stay locked.

## When Scouting Mode **isn't** what you want

* **Capturing a confirmed animal** — tap **Arm** on the trap card.
* **A one-off photo** — open Controls and tap **Request Image** (doesn't change trap state).
* **Testing the door mechanism** — use **Open** / **Close** on the trap card.

## Troubleshooting

* **"Refused with an obstruction error"** — clear the capture zone, then retry.
* **"Refused with a door-not-open error"** — tap **Open** on the trap card, wait for the status to read **Open**, then retry **Scout**.
* **Repeated alerts from the same animal** — expected if the animal is cycling in and out of detection zones faster than the ~5.5 minute cooldown can reset.
