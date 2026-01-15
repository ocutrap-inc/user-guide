# Tips and Tricks

Get the most out of your OcuTrap with these best practices and pro tips.

---

## Powering Off the Trap

When you're not using the trap, **power it down properly**:
1. Hold the **power button for 3 seconds** until the device powers off
2. The trap will send a final status update before shutting down
3. This ensures a clean disconnection and protects the electronics

Proper shutdown prevents unnecessary battery drain and extends the trap's lifespan.

---

## Maximizing Battery Life

### Deployment Tips
- **Strong cellular signal** — Poor signal causes the trap to work harder to stay connected, draining battery faster
- **GPS interval** — Keep at 8 hours (default) or disable if you don't need location tracking
- **Camera timelapse** — Set to 6+ hours or disable if you only need capture photos
- **Firmware updates** — Keep updated for the latest battery optimizations

### What Drains Battery Fastest
1. Poor cellular coverage (constant reconnection attempts)
2. Frequent GPS updates
3. Short camera timelapse intervals
4. Cold temperatures (reduces battery capacity)

---

## Optimal Trap Placement

### For Best Captures
- Position trigger sensor **6-10 inches inside the cage** to ensure the animal is fully inside before the door closes
- Place bait **behind the sensor** so animals must pass through the detection zone
- Level ground helps prevent tilt alerts when armed

### For Best Connectivity
- Avoid metal buildings or dense structures that block cellular signal
- Test signal strength before leaving the trap — check for cyan breathing LED
- Clear sky view improves GPS accuracy

---

## Animal Sensor

<figure><img src="../.gitbook/assets/Untitled (40 x 30 in).png" alt=""><figcaption></figcaption></figure>

---

## How Detection Works

### Sensor Field of View
The Time-of-Flight sensor projects a **20-degree field of view** from the center of the pod into the trap, constantly monitoring for movement.

### Detection Process
1. **Object enters detection zone** (300-450mm) — Sensor starts tracking
2. **Verification** — System confirms 3+ consecutive readings to avoid false triggers
3. **Object enters capture zone** (0-250mm) — Trigger confirmed
4. **Door closes** — Capture photo taken and alert sent

### Why This Matters
Unlike traditional traps that use a mechanical trip pan, OcuTrap uses a **distance sensor** to detect the animal's position. This method:
- Improves accuracy
- Minimizes false triggers from rain, debris, or vibration
- Allows remote monitoring without physical trigger mechanisms

---

## Testing the Trap

This video shows how your OcuTrap works once it's set up and ready to catch animals.

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MTaWOrEK9jx-3w2Vwjy%2Fuploads%2FKcVJMcGseQJcDhSsYFAA%2FMy%20Movie%2013.mp4?alt=media&token=52ed0618-e462-4221-b591-5166f5294074" %}

### Test Before Deploying
1. **Arm the trap** using the app
2. **Wave your hand** through the detection zone
3. **Verify** the door closes and you receive an alert
4. **Disarm** and reset for deployment

---

## Trigger Settings

### Capture Distance
- **Default**: 250mm (about 10 inches)
- **Adjustable range**: 125mm–1000mm
- **Tip**: Smaller values = animal must be closer before triggering

### Timing
- The sensor must register **continuous presence** before activating
- This timing **reduces false triggers** while ensuring the animal is fully enclosed
- Timing is optimized in firmware and cannot be manually adjusted

---

## Reducing False Triggers

If you're getting unwanted captures:

1. **Increase capture distance** — Makes the trigger less sensitive
2. **Check sensor window** — Clean any dirt, debris, or condensation
3. **Reposition the trap** — Avoid areas with blowing debris or heavy rain entry
4. **Review pre-capture photos** — See what's triggering the trap

The dual-zone verification system filters out most false triggers from rain and debris automatically.

---

## Getting Better Images

### In Daylight
- Images are automatically color
- Adjust **image rotation** if the camera view is upside down
- Use higher **camera quality** settings (3-6) for more detail

### At Night
- IR LEDs activate automatically below the dark lux threshold
- If images are too dark: Lower the **dark lux threshold** or increase **minimum IR brightness**
- If images are washed out: Decrease **maximum IR brightness**

### General Tips
- Keep the camera lens clean
- Use **image cropping** to remove cage mesh from the frame if needed
- Higher quality = larger files = longer transfer times

---

## Using Pre-Capture Alerts

Enable **Pre-Capture Alerts** to get notified when an animal is approaching:

- Sends alert when object enters detection zone (before capture)
- Includes a photo of what's approaching
- 2-minute cooldown between alerts to prevent spam
- Great for monitoring activity without captures

**Use cases:**
- See if non-target animals are visiting
- Monitor animal behavior patterns
- Verify trap placement is attracting targets

---

## Button Shortcuts

Learn the physical button controls:

| Action | How To |
|--------|--------|
| **View status** | Single press User button (5 second display) |
| **Open/close door** | Double-press User button + hold 5 seconds |
| **Arm/disarm** | Press User button, then Power button |
| **Power off** | Hold Power button for 3 seconds |
| **Wake from hibernation** | Press Power button |

---

## Seasonal Considerations

### Cold Weather
- Battery capacity decreases in cold temperatures
- Expect shorter runtime in winter
- Consider the 10Ah battery for extended cold-weather deployments

### Hot Weather
- Temperature alerts will notify you if internal temps exceed 45°C
- Shade the trap if possible in extreme heat
- Electronics are rated to 45°C operating temperature

### Wet Conditions
- The enclosure is weather-resistant but not waterproof
- Avoid submerging or prolonged heavy rain exposure
- Condensation on camera lens can occur — see [Condensation on the Camera](../troubleshooting/condensation-on-the-camera.md)

---

## Multi-Trap Management

If you're managing multiple traps:

- **Name your traps** clearly in the app for easy identification
- **Use the map view** to see all trap locations at once
- **Share traps** with team members using appropriate permission levels
- **Stagger GPS intervals** if deploying many traps to spread data usage

---

## Before You Leave the Field

Checklist before leaving your trap:

- [ ] LED shows breathing cyan (connected)
- [ ] Battery level is sufficient for deployment length
- [ ] Door opens and closes properly
- [ ] Trap is armed (yellow LED)
- [ ] GPS location is updated
- [ ] Bait is positioned behind sensor
- [ ] Trap is level and stable
