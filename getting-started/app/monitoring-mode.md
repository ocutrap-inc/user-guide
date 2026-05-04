# Monitoring Mode

Monitoring mode lets you observe trap activity — see what's approaching the trap and what's coming back — without ever closing the door. Use it for scouting, fine-tuning placement, and confirming that the right animals are visiting before you commit to a real capture.

## How it differs from Armed mode

|                       | Armed                                                        | Monitoring                                                     |
| --------------------- | ------------------------------------------------------------ | -------------------------------------------------------------- |
| **Detects animals**   | Yes (same detection logic)                                   | Yes (same detection logic)                                     |
| **Closes the door**   | Yes — on first verified detection                            | **Never** — observation only                                   |
| **Sends pre-capture alerts** | Yes (if enabled)                                       | Yes                                                            |
| **Captures images**   | Yes — at zone entry and at trigger                           | Yes — on detection **and** every ~30 s while animal stays in the trap (v675+) |
| **Reset after activity** | N/A (door closed; trap is captured)                       | Auto-reset ~5 minutes after the animal leaves                  |

## Activating monitoring mode

1. Make sure the trap door is **fully open**. The trap will refuse to enter monitoring mode if the door isn't open, the same way it would refuse to arm.
2. From the trap's screen in the OcuTrap app, tap **Monitor**.
3. The trap will run an obstruction check (same as arming). If something is in the capture zone — a stick, a paw, debris — monitoring will be refused with an error so you can clear it first.
4. Once monitoring is active, the trap reports its status as **Monitoring** in the app.

## What you'll see while monitoring is active

* **Pre-capture alerts** — when an animal enters the outer detection zone (if pre-capture alerts are enabled in your trap settings).
* **Trigger alerts** — when an animal reaches the trigger distance. The trap takes a photo and sends it to you, but the door **does not close**.
* **Periodic photos while the animal is in the trap (v675+)** — once an animal enters a detection zone, the trap requests a fresh photo about every 30 seconds for as long as something stays in the zone, so you can watch the activity unfold instead of seeing only the entry shot. If the previous monitoring image is still being transmitted (slow signal, large image), the trap waits for it to finish before starting the next one — you'll never get half a photo or two photos competing for the same connection. Older firmware (v598–v674) only takes a photo on initial detection.
* **No more dropped approach photos (v700+)** — on older firmware, if the animal moved while a photo was already being uploaded, the next approach photo would be silently dropped (`Approach photo dropped at NNNmm - queue full` in serial logs). v700+ defers the dropped photo into a single-slot pending queue and fires it as soon as the camera is free. If multiple approach moments collide, the **nearest** distance wins. You'll see one extra photo per detection cycle that previously would have been lost — especially useful when the animal is moving quickly.
* **Faster image upload (v705+)** — modern-camera chunk-read timeout reduced from 200 ms to 100 ms (legacy cameras kept at 500 ms). Each timeout that previously fired stalled the main loop for the full window; v705 cuts the idle penalty in half during heavy transfers.
* **Cooldown after departure** — once the animal leaves the detection zones, the trap waits about 5 minutes before re-arming the alerts. This prevents the same animal from generating a flood of duplicate notifications as it moves around near the trap.
* **Battery usage** — monitoring uses the same low-power detection mode as armed, so battery life is similar. The 30-second photo cadence draws meaningfully more power while an animal is parked in the trap; if you want to stretch battery life further on a long deployment, ask your fleet admin to lengthen the interval (`monImgInt`) or set it to `0` to disable periodic photos entirely.

## Exiting monitoring mode

You can exit monitoring at any time in two ways:

1. **Tap Unmonitor** in the app. The trap goes back to **Unarmed** with the door still open.
2. **Close the door** from the app. The trap closes the door and goes to **Unarmed** in one step — no need to manually unmonitor first.

After exiting, you can arm the trap normally if you want to start capturing.

## Image quality in monitoring mode

By default, monitoring uses higher-quality photos than armed mode (VGA 640×480 vs QVGA 320×240). The reasoning is that monitor-mode images are for human review while you're scouting, so a sharper photo is worth the slower transmission; armed-mode images are forensic confirmation of a real capture, where speed matters more.

If you want to override the default, ask your installer or fleet admin to set the **`monImg`** value (1–6, where 3 = VGA) in the device settings. Higher values = higher resolution = slower transmission and larger battery cost per image.

> **Note (firmware v672+):** Separate monitor image quality is a v672 feature. On older firmware, monitoring uses the same `imageSize` as armed mode.

## Firmware version requirements

| Feature                                                | Firmware version required                          |
| ------------------------------------------------------ | -------------------------------------------------- |
| Monitoring mode (basic — `monitor` / `unmonitor`)     | **v598 or newer**                                  |
| Close-the-door from monitoring (one-tap exit)          | **v633 or newer**                                  |
| Reliable monitoring cleanup on close (timer/sensor reset) | **v644 or newer**                              |
| Separate `monImg` image-quality setting for monitoring | **v672 or newer**                                  |
| Periodic monitoring photos every ~30 s (`monImgInt`)   | **v675 or newer**                                  |
| Approach photos no longer dropped under cellular pressure (single-slot deferred photo with nearer-wins coalescing) | **v700 or newer** |
| `arm=N pend=N` visible on serial heartbeat for diagnostics | **v700 or newer**                              |
| `pwrOff` always reported in `callback_settings` (no longer hidden when at default) | **v701 or newer** |
| LED off during low-power sleep (no more solid red drain) | **v702 or newer**                                |
| Hibernation retries on sleep-fail; cellular auto-recovers | **v703 or newer**                              |
| Durable `Low battery shutdown` + `low_voltage_shutdown` events at runtime, not just at boot | **v704 or newer** |
| 20%/10% battery alerts use durable cloud queue (survive offline windows + reboot) | **v704 or newer** |
| Faster image transfers — modern cameras 200ms→100ms chunk timeout (legacy unchanged at 500ms) | **v705 or newer** |
| Boot-time emergency-halt loop replaced with main-loop retry (deprecated `System.sleep` API removed) | **v706 or newer** |

> **Most deployed traps run firmware v550** as of April 2026. **v550 firmware does not support monitoring mode at all** — the device will reject the `monitor` command. If your trap doesn't show a Monitor option in the app, or if Monitor commands fail with a generic error, your trap likely needs an over-the-air firmware update before monitoring will work.
>
> See [Updating firmware](../../faqs/updating-firmware.md) for how to bring your trap up to date.

## When monitoring **isn't** what you want

* **You want to capture an animal you're confident about.** Use Armed mode — it's the same detection logic but with the door close.
* **You want a one-off photo.** Use the Camera button in trap controls instead. Monitoring is for ongoing observation; for a single image, the camera command is faster.
* **You're testing the trap door mechanism.** Use the Open / Close buttons in trap controls; monitoring won't move the door.

## Troubleshooting

* **"The Monitor command is failing or unavailable"** — check your firmware version (Settings → Trap Info). v598+ is required. If you're below that, see [Updating firmware](../../faqs/updating-firmware.md).
* **"Monitor was refused with an obstruction error"** — clear the capture zone. The trap won't enter monitoring with something in the line of sight, the same way it won't arm.
* **"Monitor was refused with a door-not-open error"** — open the door from trap controls, then try again. Monitoring requires a fully open door.
* **"I'm getting alerts every few minutes from the same animal"** — the 5-minute reset cooldown should suppress this. If it isn't, the animal is likely cycling in and out of the detection zones faster than the cooldown timer; this is expected behavior.
