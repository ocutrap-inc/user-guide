# Scouting Mode

Scouting Mode lets you observe trap activity — see what's approaching the trap and what's coming back — without ever closing the door. Use it for scouting, fine-tuning placement, and confirming that the right animals are visiting before you commit to a real capture.

## How it differs from Armed mode

|                       | Armed                                                  | Scouting                                                       |
| --------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| **Detects animals**   | Yes (same detection logic)                             | Yes (same detection logic)                                     |
| **Closes the door**   | Yes — on first verified detection                      | **Never** — observation only                                   |
| **Sends pre-capture alerts** | Yes (if enabled)                                | Yes                                                            |
| **Captures images**   | Yes — at zone entry and at trigger                     | Yes — on detection and every ~30 s while the animal stays in the trap |
| **Reset after activity** | N/A (door closed; trap is captured)                 | Auto-reset ~5 minutes after the animal leaves                  |

## Activating Scouting Mode (walkthrough)

The Scout button lives in the same trap controls popup as Arm, Open, and Close. Here is the full flow from the OcuTrap app:

1. **Open the OcuTrap app** at [app.ocutrap.com](https://app.ocutrap.com) (or the OcuTrap mobile app) and sign in.
2. **Pick the trap** you want to scout from your trap list / dashboard. Tap it to open its detail view.
3. **Open the trap controls popup.** This is the popup that contains the door and arm buttons (Open, Close, Arm, Scout, Camera). On the trap detail page, tap the trap controls button to open it if it isn't already showing.
4. **Confirm the door is fully open.** If the door isn't fully open, tap **Open** first and wait for the trap to report **Open** before continuing. Scouting will not start with the door anywhere other than fully open — this is the same safety gate as arming.
5. **Tap Scout.** The trap runs an obstruction check (same routine as arming). If something is in the capture zone — a stick, a paw, debris — scouting will be refused with an error message so you can clear the obstruction and try again.
6. **Wait for confirmation.** Once the obstruction check passes, the trap's status in the app changes to **Scouting**. From this point on, photos and alerts behave as described below.

> **Tip:** If the Scout button is greyed out, it usually means the door isn't reporting fully open yet, or the trap is offline / hasn't checked in recently. Wait for the trap to come back online or tap **Open** again.

## What you'll see while Scouting Mode is active

* **Pre-capture alerts** — when an animal enters the outer detection zone (if pre-capture alerts are enabled in your trap settings).
* **Trigger alerts** — when an animal reaches the trigger distance. The trap takes a photo and sends it to you, but the door **does not close**.
* **Periodic photos while the animal is in the trap** — once an animal enters a detection zone, the trap sends a fresh photo about every 30 seconds for as long as something stays in the zone, so you can watch the activity unfold instead of seeing only the entry shot. If the previous photo is still being transmitted, the trap waits for it to finish before starting the next one — you'll never get half a photo or two photos competing for the same connection.
* **No more lost approach photos** — if the animal moves while a photo is already being uploaded, the trap holds onto the most recent approach moment and sends it as soon as the camera is free. You see the closest, most useful frame.
* **Faster image uploads** — photos finish transferring noticeably faster on cellular, especially when many are queued.
* **Cooldown after departure** — once the animal leaves the detection zones, the trap waits about 5 minutes before re-arming the alerts. This prevents the same animal from generating a flood of duplicate notifications as it moves around near the trap.
* **Battery usage** — Scouting Mode uses the same low-power detection as Armed mode, so battery life is similar. The 30-second photo cadence draws meaningfully more power while an animal is parked in the trap; if you want to stretch battery life on a long deployment, ask your fleet admin to lengthen the interval or turn the periodic photos off.

## Exiting Scouting Mode

You can exit Scouting Mode at any time in two ways:

1. **Tap Stop Scouting** in the app. The trap goes back to **Unarmed** with the door still open.
2. **Close the door** from the app. The trap closes the door and goes to **Unarmed** in one step — no need to manually stop scouting first.

After exiting, you can arm the trap normally if you want to start capturing.

## Image quality in Scouting Mode

By default, scouting uses higher-quality photos than Armed mode. The reasoning is that scouting images are for human review while you're observing, so a sharper photo is worth the slower transmission; armed-mode images are forensic confirmation of a real capture, where speed matters more.

If you want to override the default — higher resolution for very sharp scouting photos, or lower resolution to save battery on long deployments — ask your installer or fleet admin.

## When Scouting Mode **isn't** what you want

* **You want to capture an animal you're confident about.** Use Armed mode — it's the same detection logic but with the door close.
* **You want a one-off photo.** Use the Camera button in trap controls instead. Scouting Mode is for ongoing observation; for a single image, the camera button is faster.
* **You're testing the trap door mechanism.** Use the Open / Close buttons in trap controls; Scouting Mode won't move the door.

## Troubleshooting

* **"Scouting was refused with an obstruction error"** — clear the capture zone. The trap won't enter Scouting Mode with something in the line of sight, the same way it won't arm.
* **"Scouting was refused with a door-not-open error"** — open the door from trap controls, then try again. Scouting Mode requires a fully open door.
* **"I'm getting alerts every few minutes from the same animal"** — the 5-minute reset cooldown should suppress this. If it isn't, the animal is likely cycling in and out of the detection zones faster than the cooldown timer; this is expected behavior.
