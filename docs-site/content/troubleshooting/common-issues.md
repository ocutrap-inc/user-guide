---
description: Fix common arming, sensor, camera, connectivity, battery, door, GPS, and LED problems with your OcuTrap.
---

# Common Issues

_Applies to: OcuTrap R1 and R2._

Use this guide to fix common OcuTrap problems.

---

## Trap Won't Arm

If you cannot arm your trap, check the following:

### Door Must Be Fully Open

The trap **requires the door to be fully open** before arming. This is a safety feature to ensure proper capture operation.

**Solution:**
1. Open the OcuTrap app
2. Tap the **Open** button and wait for the door to fully open
3. Check that the light shows **blue** (unarmed and open). See the [LED Guide](../getting-started/led-guide.md)
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

The trap uses a **warn-and-arm** approach: if the POD lens looks blocked or dirty, the trap **still arms** but sends a warning so you know to clean it:

- Arm: **`Trap armed. Check camera and clean sensor if blocked.`**
- Scout: **`Scout on. Check camera and clean sensor if blocked.`**

Clean the POD lens and clear the sensor path when you see this. The trap keeps working, but a dirty lens can affect detection. Clean it as soon as you can.

A real object physically blocking the trap interior is different: arming is **blocked** with **`Remove object at <distance> first`**. Remove the object and arm again.

See [Distance Limits, Sensor Alerts & Errors](../getting-started/capture-behavior/distance-safety-and-alerts.md) for capture distance presets and other arming errors.

### Sensor Error (Blocks Arming)

If arming fails with **`Sensor fault. Power-cycle the trap.`**, the distance sensor did not pass its self-check.

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

OcuTrap filters false triggers, but environmental conditions can still cause them.

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
3. Default is **8 in**. Try **6 in** or **7 in** for more selective triggering

---

## GPS Not Updating

GPS updates limit battery use, so they may not happen as often as you expect.

### Understanding GPS Behavior

- **Update interval**: Every 8 hours, fixed (not real-time)
- **First boot delay**: 15 minutes after boot before the first GPS acquisition
- **Captures take priority**: A capture in progress pauses GPS until it finishes; GPS never interrupts a capture

### GPS Shows Old Location

**Solution:**
1. Wait for the next scheduled update (the trap updates every 8 hours)
2. Request a manual update: in the Trap Controls bar, tap **Location**
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
1. Check **Dark Lux Threshold** setting. Night vision and IR activate when light falls **below** this value, so **increase** it to enable them earlier (see [Camera](../faqs/camera.md))
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
4. Wait. High-quality photos can take several minutes to upload, especially on a weak cellular connection

---

## Connectivity Issues

### Trap Shows "Offline"

For a step-by-step field guide to the battery, hibernation, LED patterns, cellular coverage, and what to send Support, see **[Trap Offline or Won't Connect](trap-offline-or-wont-connect.md)**.

**Automatic reconnection:** If the trap loses connection, it will try to reconnect on its own. This can take up to an hour. Leave it powered on in an area with decent cellular coverage and check back later.

If the trap stays offline after the steps in the guide above, contact support.

### Commands Not Reaching Trap

See [Trap Not Sending Commands](trap-not-sending-commands.md) for detailed troubleshooting.

---

## Battery Issues

### Battery Draining Quickly

**Common Causes:**
- Poor cellular signal (device uses more power searching)
- Location (GPS) left on where the trap cannot get a fix
- Camera timelapse interval set too short
- Cold temperatures reduce battery capacity

**Solution:**
1. Deploy in areas with good cellular coverage
2. Turn Location (GPS) off if you do not need location tracking
3. Increase Camera Time Lapse interval (6+ hours recommended)
4. In cold weather, expect reduced battery life
5. Keep firmware updated (includes battery optimizations)

### Trap Keeps Hibernating

If the trap enters hibernation unexpectedly:

1. **Check battery level.** The trap hibernates when the battery is critically low
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
4. Check battery level. Door operation requires adequate power
5. Use the manual door control: press the **User Button** once, then press again and **hold ~5 seconds** (about 7 seconds total before the door moves)
6. Check for a sensor-fault indicator (3 orange flashes)

### Door Not Latching Behind the Locking Bar

If the door comes to rest in front of or on top of the locking bar, a captured animal can push it open.

Full checks and fixes: [Door won't lock behind the locking bar](door-wont-lock.md).

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
2. Charge the battery. The trap may have auto-hibernated due to low power
3. Check battery connections
4. If battery is charged and power button doesn't respond, contact support

### Rapid Red Blinking

Rapid red blinking means the trap is **powering down** because the power button is being held. It is **not** an error code.

**Solution:**
1. If you didn't mean to power off, **release the power button within about 3 seconds** to cancel the shutdown.
2. If it finishes shutting down, the LED goes **solid red** and the trap powers off. Press the power button again to turn it back on.
3. Genuine faults show as brief flash bursts instead: **3 orange flashes** (sensor error; clean the POD lens and power-cycle) or **5 magenta flashes** (data error). If a fault repeats, contact support.

For LED status meanings, see the [LED Guide](../getting-started/led-guide.md).

---

## Trap Placement

Set the trap on level, stable ground so it cannot shift and the door can operate cleanly.

---

## Still Need Help?

If you've tried the solutions above and still have issues:

1. [Contact Support](../support/support.md) with details about your issue
2. Include: trap serial number, battery voltage, LED status, and steps already tried
