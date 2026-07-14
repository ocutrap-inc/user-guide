# LED Light Guide

The light on your OcuTrap tells you what the trap is doing. This guide explains what each color and pattern means — including why the light looks **off** most of the time when the trap runs on battery (that's normal and expected).

---

## "The light is off when the trap is idle" — is that a problem?

**No — that's normal battery‑saving behavior.** When the trap is idle and running on **battery**, it keeps the light **off between brief check‑in flashes**. Roughly every **10 seconds** you'll see one **quick flash** (a fraction of a second), then it goes dark again. The trap is fully awake and working — it just isn't lighting the LED continuously, because a steady light would drain the battery.

- On **external/USB power** (or for a few seconds right after you send a command), the light stays on — a slow **breathing cyan** glow when the trap is connected.
- On **battery**, expect the brief flash every ~10 seconds. To confirm the trap is alive, send any command from the app — the light will brighten immediately.

Only be concerned if, when the trap should be sitting idle, the light stays **solid** on one color that never changes, or stays **red**. See [Red light](#red-light) below.

---

## Color meanings

The flash (or steady color) shows the trap's current state:

| Color | Meaning |
|---|---|
| **Blue** | Unarmed, door open |
| **Green** | Unarmed, door closed |
| **Yellow** | Armed — ready to capture |
| **Magenta / pink** | Animal captured |
| **Breathing cyan** | Idle on power, connected to the cloud |
| **Red** | Error or shutting down — see [Red light](#red-light) |

## Connection status

When idle on power, the light also shows its connection state:

| Pattern | Meaning | What to do |
|---|---|---|
| Breathing cyan | Connected and online | Normal — nothing to do |
| Fast blinking cyan | Connecting to the cloud | Wait a few minutes |
| Blinking green | Looking for cellular signal | Move the trap to better coverage |
| Blinking magenta | Firmware update in progress | Leave it powered on and wait |

## When you send a command

The light briefly confirms your action, then returns to its idle pattern:

| You do | Light |
|---|---|
| Open the door | Blue for ~5 seconds |
| Close the door | Green for ~5 seconds |
| Arm the trap | Yellow while it checks the capture zone (~3 seconds), then yellow once armed |
| **Arm is blocked** — something is in the way, the sensor needs cleaning, or an update is pending | **Solid red for ~2 seconds**, then back to idle. The trap did **not** arm. Clear the obstruction or clean the sensor window and try again. |

## Red light

| Pattern | Meaning |
|---|---|
| Brief solid red (~2 seconds) after a command | The action was blocked (for example, arming failed) — see the row above |
| Rapid red blinking | The trap is **powering down** because the power button is being held. Release within ~3 seconds to cancel; otherwise it finishes shutting down. This is **not** an error code. |
| Solid red (staying red) | Hibernating or shut down — including after a low‑battery shutdown. Charge or replace the battery and press the power button to wake it. |

---

**Related:** [Common Issues](common-issues.md) · [Trap Offline or Won't Connect](trap-offline-or-wont-connect.md)
