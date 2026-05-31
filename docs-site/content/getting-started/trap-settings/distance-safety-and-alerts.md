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

### Error — arming blocked

`Sensor blocked or dirty: Reading at 4.02 in` (or `102 mm` in metric mode)

**What to do:** Clean the POD lens, clear anything in front of the sensor, then try arming again.

### Warning — arms anyway (temporary override)

If you try again **within 5 minutes** of the error above, the trap may arm but show a warning:

- Arm: `Armed but sensor may be blocked or dirty`
- Scout: `Scouting but sensor may be blocked or dirty`

You should still clean the lens when you see this warning. After **5 minutes**, the trap blocks arming again until the sensor reads normally.

### Real obstruction

**Error:** `Object at …` — something is blocking the trap interior. Remove it and try again. This error cannot be overridden by retrying.

---

## Other arm errors

| Message | Cause |
|---|---|
| **Sensor error** | Sensor self-check failed — clean the lens, power-cycle, or contact support |
| **Door not open** | Door not fully open |
| **Cannot arm - trap captured** | Trap in captured state — open the door and unarm first |

See [Common Issues — Trap Won't Arm](../../troubleshooting/common-issues.md#trap-wont-arm).
