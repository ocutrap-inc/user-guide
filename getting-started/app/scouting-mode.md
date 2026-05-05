# Scouting Mode

Scouting Mode lets you observe trap activity — see what's approaching the trap and what's coming back — without ever closing the door. Use it for scouting, fine-tuning placement, and confirming that the right animals are visiting before you commit to a real capture.

## How it differs from Armed mode

|                              | Armed                               | Scouting                                                                                                                                 |
| ---------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Detects animals**          | Yes (same detection logic)          | Yes (same detection logic)                                                                                                               |
| **Closes the door**          | Yes — on first verified detection   | **Never** — observation only                                                                                                             |
| **Sends pre-capture alerts** | Yes (if enabled)                    | Yes                                                                                                                                      |
| **Captures images**          | Yes — at zone entry and at trigger  | Yes — on detection and about every 60 s while the animal stays in the trap (configurable 15 s – 5 min)                                   |
| **Reset after activity**     | N/A (door closed; trap is captured) | Auto-reset about 5 minutes after the trap confirms the animal has departed (departure is confirmed after \~30 seconds of clear readings) |

## Activating Scouting Mode (walkthrough)

In the OcuTrap app, **Open** / **Close** / **Arm** live on the trap card itself, and **Scout** lives one tap away inside the **Controls** popup for that trap. Here's the full flow:

1. **Open the OcuTrap app** at [app.ocutrap.com](https://app.ocutrap.com) (or the OcuTrap mobile app) and sign in. You'll land on your trap list.
2. **Find the trap you want to scout.** Each trap appears as a card showing its status (for example, _Open / Unarmed_), battery percentage, and a green dot if the trap is online.
3. **Confirm the door is fully open.** Look at the status line on the trap card — it should read **Open / Unarmed**. If the door is closed, tap **Open** on the trap card first and wait for the status to update to **Open** before continuing. Scouting will refuse to start unless the door is fully open and the trap is unarmed.
4. **Open the Controls popup.** On the trap card, tap **Controls** (the button under the trap name, next to **Settings**). A popup titled _Controls for \<trap ID>_ will appear. The top row of icons reads: **GPS**, **Data**, **Buzzer**, **Reboot**, **Hibernation**, **Scout**.
5. **Tap Scout.** The icon is on the right end of the top row (eye icon, labelled **Scout**). The trap runs an obstruction check (same routine as arming). If something is in the capture zone — a stick, a paw, debris — scouting will be refused with an error so you can clear it and try again.
6. **Wait for confirmation.** Once the obstruction check passes, the trap's card status switches to **Scouting**, and inside the Controls popup the rightmost icon flips from **Scout** (open eye) to **Stop Scout** (eye with a slash). From this point on, photos and alerts behave as described below.

> **Tip:** If tapping **Scout** seems to do nothing or the popup shows an error, the most common causes are: the door isn't reporting fully open yet, the trap is offline (no green dot on the card), or the trap hasn't checked in recently (look at the **Last heard** time at the bottom of the Controls popup). Wait for the next check-in or tap **Open** again from the trap card.

## What you'll see while Scouting Mode is active

* **Pre-capture alerts** — when an animal enters the outer detection zone (if pre-capture alerts are enabled in your trap settings).
* **Trigger alerts** — when an animal reaches the trigger distance. The trap takes a photo and sends it to you, but the door **does not close**.
* **Periodic photos while the animal is in the trap** — once an animal enters a detection zone, the trap sends a fresh photo about every 60 seconds (default; configurable from 15 seconds to 5 minutes) for as long as something stays in the zone, so you can watch the activity unfold instead of seeing only the entry shot. If the previous photo is still being transmitted, the trap waits for it to finish before starting the next one — you'll never get half a photo or two photos competing for the same connection.
* **No more lost approach photos** — if the animal moves while a photo is already being uploaded, the trap holds onto the most recent approach moment and sends it as soon as the camera is free. You see the closest, most useful frame.
* **Faster image uploads** — photos finish transferring noticeably faster on cellular, especially when many are queued.
* **Cooldown after departure** — the trap first needs to see about **30 seconds of clear readings** to confirm the animal has actually left (rather than briefly stepping out of frame). Once departure is confirmed, it waits another **\~5 minutes** before re-arming the pre-capture and trigger alerts. So from the last in-zone reading to the next round of alerts you'll typically see about 5.5 minutes of quiet. This prevents the same animal from generating a flood of duplicate notifications as it moves around near the trap.
* **Battery usage** — Scouting Mode uses the same low-power detection as Armed mode, so idle battery life is similar. The periodic photo cadence draws meaningfully more power while an animal is parked in the trap; if you want to stretch battery life on a long deployment, ask your fleet admin to lengthen the interval or turn the periodic photos off.

## Exiting Scouting Mode

You can exit Scouting Mode at any time in two ways:

1. **Tap Stop Scout in the Controls popup.** While scouting is active, the rightmost icon in the top row of the Controls popup is **Stop Scout** (eye-with-slash icon). Tapping it returns the trap to **Unarmed** with the door still open.
2. **Tap Close on the trap card.** The trap closes the door and returns to **Unarmed** in one step — no need to stop scouting first.

After exiting, you can arm the trap normally if you want to start capturing.



## When Scouting Mode **isn't** what you want

* **You want to capture an animal you're confident about.** Tap **Arm** on the trap card — same detection logic, but the door closes on the first verified detection.
* **You want a one-off photo.** Open the Controls popup and tap **Request Image** (camera icon, below the top row). Scouting Mode is for ongoing observation; for a single image, Request Image is faster and doesn't change the trap's state.
* **You're testing the trap door mechanism.** Use **Open** and **Close** on the trap card; Scouting Mode won't move the door.

## Troubleshooting

* **"Scouting was refused with an obstruction error"** — clear the capture zone. The trap won't enter Scouting Mode with something in the line of sight, the same way it won't arm.
* **"Scouting was refused with a door-not-open error"** — tap **Open** on the trap card, wait for the status line to read **Open**, then re-open the Controls popup and try **Scout** again. Scouting Mode requires a fully open door.
* **"I'm getting alerts every few minutes from the same animal"** — the 5-minute reset cooldown (plus the \~30 seconds the trap waits to confirm the animal has actually left) should suppress this. If it isn't, the animal is likely cycling in and out of the detection zones faster than the cooldown timer can reset; this is expected behavior.
