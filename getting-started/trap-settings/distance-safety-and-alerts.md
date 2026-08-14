---
description: >-
  Capture distance presets from 6 to 18 inches, plus the sensor warnings and
  arming errors the app shows and what each one means.
---

# Distance Limits, Sensor Alerts & Errors

Quick reference for capture distance settings and arming errors you may see in the app.

---

## Capture distance setting

Choose how far inside the trap an animal must be before the door closes. In the app, pick a preset from **6 in to 18 in**.

| Preset | When to use it |
|---|---|
| **8 in (default)** | Good starting point for most setups |
| **6–7 in** | Animal must be closer — helps reduce false triggers from rain or debris |
| **10 in and above** | Animal can trigger from farther inside the cage |

Smaller values mean the animal must be deeper in the trap before the door closes.

---

## Sensor blocked or dirty

### Warning — arms anyway

If the POD lens looks blocked or dirty when you arm, the trap **still arms** but sends a warning so you know to clean it:

- Arm: `Trap armed. Check camera and clean sensor if blocked.`
- Scout: `Scout on. Check camera and clean sensor if blocked.`

**What to do:** Clean the POD lens and clear anything in front of the sensor. The trap keeps working, but a dirty lens can affect detection, so clean it as soon as you can.

### Real obstruction — arming blocked

**Error:** `Remove object at <distance> first` (for example, `Remove object at 4.0 in first`) — something is physically blocking the trap interior. Remove it and arm again.

---

## Other arm errors

| Message | Cause |
|---|---|
| **`Sensor blocked or dirty. Clean sensor window, then try again.`** | Sensor can't see through the POD lens (usually condensation or grime) — clean the lens, then arm again |
| **`Sensor fault. Power-cycle the trap.`** | Sensor self-check failed — power-cycle the trap, and contact support if it persists. Firmware v1061 and earlier also shows this when the lens is blocked or dirty |
| **`Open the door first`** | Door is not fully open — open it all the way, then arm |
| **`Release animal first (open door)`** | Trap is in the captured state — open the door to release, then arm |
| **`Cannot disarm`** | A capture is triggering right now — wait a moment and try again |

See [Common Issues — Trap Won't Arm](../../troubleshooting/common-issues.md#trap-wont-arm).
