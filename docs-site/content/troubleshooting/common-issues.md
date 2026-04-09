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
3. Check that the LED shows **Solid Blue** (unarmed and open)
4. Try arming again

### Obstruction Detected

Before arming, the trap performs an **obstruction check** to ensure the capture zone is clear. If something is blocking the sensor, arming will fail.

**Solution:**
1. Check that nothing is in front of the sensor inside the trap
2. Clear any debris, leaves, or objects from the trap interior
3. Ensure the sensor window is clean
4. Wait for 5+ distance readings to confirm the zone is clear
5. Try arming again

### Motor Connectivity Issue

The trap tests motor connectivity before arming. If the motor doesn't respond, arming will fail.

**Solution:**
1. Check the motor connector is securely attached
2. See [Motor Connector Tightness Check](motor-connector-tightness-check.md)
3. Verify the motor cable isn't damaged
4. Contact support if the issue persists

---

## False Triggers / Unwanted Captures

OcuTrap has sophisticated false-trigger prevention, but environmental factors can sometimes cause issues.

### Rain or Debris Triggering

Heavy rain or debris falling through the trap can sometimes trigger captures.

**How OcuTrap Prevents This:**
- Requires **3+ consecutive valid readings** before triggering
- **Oscillation detection** identifies rain patterns (rapidly changing distances)
- **Signal quality filtering** rejects weak or noisy readings

**If you're still getting false triggers:**
1. Increase the **Capture Distance** setting (move trigger point further from sensor)
2. Ensure the trap is positioned to minimize rain entry
3. Check that the sensor window is clean and undamaged
4. Consider repositioning the trap to a more sheltered location

### Capture Distance Too Sensitive

If the trap triggers before animals are fully inside:

**Solution:**
1. Go to **Settings → More Settings**
2. Decrease the **Capture Distance** value (smaller = animal must be closer)
3. Default is 250mm (10 inches) — try 200mm or 150mm for more selective triggering

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
5. If problems persist, try a factory reset of the GPS module (contact support)

---

## Camera Issues

### Dark or Black Images

**Possible Causes:**
- Camera not detecting darkness correctly
- IR LEDs not activating

**Solution:**
1. Check **Dark Lux Threshold** setting — lower value = IR activates at higher light levels
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
4. Wait — images transfer in 8KB chunks and may take time on slow connections

---

## Connectivity Issues

### Trap Shows "Offline"

**OcuTrap's Auto-Recovery:**
The trap has automatic stuck-offline detection. After 20 minutes offline, it will:
1. Disconnect from the network
2. Power cycle the cellular modem
3. Attempt to reconnect
4. Retry with increasing intervals (10, 20, 30... up to 60 minutes)
5. Reset the system after 5 failed attempts

**If the trap stays offline:**
1. Check battery level — low battery can affect connectivity
2. Verify cellular coverage in the deployment area
3. Press the power button to wake the device
4. Contact support if the trap remains offline for extended periods

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

1. **Check battery voltage** — hibernation occurs below 9.6V (default)
2. **Charge or replace the battery**
3. **Verify the correct Battery Type** is selected in settings
4. If the battery is charged but hibernation persists, the battery may be damaged

---

## Door Issues

### Door Won't Open or Close

**Solution:**
1. Check motor connector is securely attached
2. Verify no physical obstruction is blocking the door
3. Check battery level — door operation requires adequate power
4. Use the manual door control: Double-press User Button + hold for 5 seconds
5. Check for motor fault indicator (orange LED)

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

This indicates a firmware crash.

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
3. Include: trap serial number, battery voltage, LED status, and steps already tried
