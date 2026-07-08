# Common Issues

This guide covers frequently encountered issues and their solutions based on how OcuTrap operates.

---

## Trap Won't Arm

If you're unable to arm your trap, check the following:

### Door Must Be Fully Open

The trap **requires the door to be fully open** before arming. This is a safety feature to ensure proper capture operation.

**Solution:**
1. Open the OcuTrap app
2. Tap the **Open** button and wait for the door to fully open
3. Check that the light shows **blue** (unarmed and open) — see the [LED Light Guide](led-light-guide.md)
4. Try arming again

### Obstruction Detected

Before arming, the trap performs an **obstruction check** to ensure the capture zone is clear. If something is blocking the sensor, arming will fail.

**Solution:**
1. Check that nothing is in front of the sensor inside the trap
2. Clear any debris, leaves, or objects from the trap interior
3. Ensure the sensor window is clean
4. Wait for 5+ distance readings to confirm the zone is clear
5. Try arming again

### Sensor blocked or dirty

**First attempt:** **`Sensor blocked or dirty: Reading at …`** — does **not** arm. Clean the lens and clear the sensor path.

**Retry within 5 minutes:** The trap **will arm** (or enter scout) and sends **`Armed but sensor may be blocked or dirty`** (or the scouting variant). After 5 minutes, the blocking error returns.

A dirty lens with nothing in the trap often reads about **4 in**; that triggers this flow, **not** “Object at 4 in.”

See [Distance Limits, Sensor Alerts & Errors](../getting-started/trap-settings/distance-safety-and-alerts.md) for capture distance presets and other arming errors.

### Sensor Error (Blocks Arming)

If arming fails with **“Sensor error”**, the distance sensor did not pass its self-check.

**Solution:**
1. Clean the POD lens
2. Power-cycle the trap
3. Contact support if the error persists after cleaning

### Motor Connectivity Issue

The trap tests motor connectivity before arming. If the motor doesn't respond, arming will fail.

**Solution:**
1. Check the motor connector is securely attached
2. See [Motor Connector Tightness Check](motor-connector-tightness-check.md)
3. Verify the motor cable isn't damaged
4. If red and black internal wires are visible at the connector, see [Wire Exposed](wire-exposed.md)
5. Contact support if the issue persists

---

## False Triggers / Unwanted Captures

OcuTrap has sophisticated false-trigger prevention, but environmental factors can sometimes cause issues.

### Rain or Debris Triggering

Heavy rain or debris falling through the trap can sometimes trigger captures.

**How OcuTrap Prevents This:**
- Requires **several steady readings in a row** before closing the door
- **Ignores splashy or erratic movement** (such as rain or blowing debris)
- **Ignores weak or unreliable readings** from a dirty or obstructed sensor window

**If you're still getting false triggers:**
1. **Decrease** the **Capture Distance** setting (smaller = animal must be closer before the door closes)
2. Ensure the trap is positioned to minimize rain entry
3. Check that the sensor window is clean and undamaged
4. Consider repositioning the trap to a more sheltered location

### Capture Distance Too Sensitive

If the trap triggers before animals are fully inside:

**Solution:**
1. Go to **Settings → More Settings**
2. Decrease the **Capture Distance** value (smaller = animal must be closer)
3. Default is **8 in** — try **6 in** or **7 in** for more selective triggering

---

## GPS Not Updating

GPS updates are battery-optimized and may not update as frequently as expected.

### Understanding GPS Behavior

- **Default interval**: Every 8 hours (not real-time)
- **First boot delay**: 5-minute delay before first GPS acquisition
- **Capture updates**: GPS automatically updates when a capture occurs

### GPS Shows Old Location

**Solution:**
1. Wait for the next scheduled update (check your GPS Interval setting)
2. Request a manual update: Go to Controls → tap the Data button
3. Ensure GPS is not disabled in settings

### No GPS Fix Available

**Solution:**
1. Ensure the trap is outdoors with a clear view of the sky
2. Move away from buildings, dense tree cover, or metal structures
3. Allow up to 3 minutes for the first fix after power-on
4. Check that GPS is enabled in settings
5. If problems persist, contact support for GPS troubleshooting

---

## Camera Issues

### Dark or Black Images

**Possible Causes:**
- Camera not detecting darkness correctly
- IR LEDs not activating

**Solution:**
1. Check **Dark Lux Threshold** setting — night vision and IR activate when light falls **below** this value, so **increase** it to enable them earlier (see [Camera](../faqs/camera.md))
2. Increase **Minimum IR Brightness** setting
3. Ensure the IR LED window is clean
4. Verify the camera lens is not blocked or dirty

### Overexposed / Washed Out Images

**Solution:**
1. Decrease **Maximum IR Brightness** setting
2. Adjust image cropping to remove reflective areas
3. Reposition the trap to reduce direct reflections

### Images Not Sending

**Possible Causes:**
- Poor cellular signal
- Large image size taking too long to transfer

**Solution:**
1. Check cellular connectivity (LED should be breathing cyan when connected)
2. Reduce **Camera Quality** setting (1-2 for faster transfer)
3. Move trap to an area with better cellular coverage
4. Wait — high-quality photos can take several minutes to upload, especially on a weak cellular connection

---

## Connectivity Issues

### Trap Shows "Offline"

For a step-by-step field guide — battery, hibernation, LED patterns, cellular coverage, and what to send Support — see **[Trap Offline or Won't Connect](trap-offline-or-wont-connect.md)**.

**Automatic reconnection:** If the trap loses connection, it will try to reconnect on its own. This can take up to an hour. Leave it powered on in an area with decent cellular coverage and check back later.

If the trap stays offline after the steps in the guide above, contact support.

### Commands Not Reaching Trap

See [Trap Not Sending Commands](trap-not-sending-commands.md) for detailed troubleshooting.

---

## Battery Issues

### Battery Draining Quickly

**Common Causes:**
- Poor cellular signal (device uses more power searching)
- GPS interval set too frequently
- Camera timelapse interval set too short
- Cold temperatures reduce battery capacity

**Solution:**
1. Deploy in areas with good cellular coverage
2. Increase GPS Interval (8+ hours recommended)
3. Increase Camera Time Lapse interval (6+ hours recommended)
4. In cold weather, expect reduced battery life
5. Keep firmware updated (includes battery optimizations)

### Trap Keeps Hibernating

If the trap enters hibernation unexpectedly:

1. **Check battery level** — the trap hibernates when the battery is critically low
2. **Charge or replace the battery**
3. **Verify the correct Battery Type** is selected in settings
4. If the battery is charged but hibernation persists, the battery may be damaged

---

## Door Issues

### Door Won't Open or Close

**Solution:**
1. Check motor connector is securely attached
2. If red and black internal wires are visible at the connector, see [Wire Exposed](wire-exposed.md)
3. Verify no physical obstruction is blocking the door
4. Check battery level — door operation requires adequate power
5. Use the manual door control: Double-press User Button + hold for 5 seconds
6. Check for motor fault indicator (orange LED)

### Door Not Latching Behind the Locking Bar

When the door closes correctly, it sits **behind and underneath the locking bar**, with the actuator extended to its full length. If the door comes to rest *in front of* the locking bar, the bar cannot hold the door down — a captured animal can push from the inside and bend the door upward, creating enough gap to escape.

**What "fully closed and locked" looks like:**

![Door fully closed and locked — door sits behind and underneath the locking bar, actuator at full length](../.gitbook/assets/door-fully-closed-locked.png)

- **Actuator** is at its **full length** (fully extended).
- **Door** is **behind and underneath the locking bar** along its entire width — not resting on top of or in front of the bar.
- The locking bar runs across the door opening and physically blocks the door from lifting.

**How to verify (every trapping session):**

1. From the app, tap **Close** and wait for the door to fully close.
2. Look at the door from the front of the trap.
3. Confirm the door edge is *tucked under* the locking bar across the full width — not pinched on top of it or sitting outside it.
4. Gently try to lift the door by hand. It should not move; the locking bar should stop it within a small fraction of an inch.

**If the door is on top of or in front of the locking bar:**

1. Tap **Open**, wait for the door to fully retract, then tap **Close** again.
2. If the issue repeats, enable **Enhanced Door Closing** (Settings → More Settings) — it re-cycles the door to clear obstructions and seat the latch.
3. Inspect the door track and locking bar area for debris (dirt, vegetation, ice).
4. Check that the door is not bent. A previously bent door may not seat correctly even when the mechanism works. Contact support if the door edge is deformed.

> **Why it matters:** A door that is not behind the locking bar may not prevent an animal from escaping.

### Door Opens/Closes Slowly

**Possible Causes:**
- Low battery
- Motor wear
- Mechanical obstruction

**Solution:**
1. Charge the battery fully
2. Check for debris in the door track
3. Contact support if the issue persists

---

## LED Indicators

### No LED / Trap Appears Dead

**Solution:**
1. Press the power button to wake from hibernation
2. Charge the battery — the trap may have auto-hibernated due to low power
3. Check battery connections
4. If battery is charged and power button doesn't respond, contact support

### Rapid Red Blinking (SOS)

This indicates a **system error**.

**Solution:**
1. If fewer than 10 blinks, the trap may recover automatically
2. If more than 10 blinks, contact support
3. Note any patterns or counts to share with support

For LED status meanings, see the [LED Guide](../getting-started/led-guide.md).

---

## Tilt / Movement Alerts

### Unexpected Tilt Alerts

The trap sends tilt alerts when not level during armed mode.

**Solution:**
1. Ensure the trap is placed on level ground
2. Check that the trap is stable and not shifting
3. Only one tilt alert is sent per arming session to prevent spam

---

## Still Need Help?

If you've tried the solutions above and still have issues:

1. [Contact Support](../support/support.md) with details about your issue
2. Include: trap serial number, battery voltage, LED status, and steps already tried
