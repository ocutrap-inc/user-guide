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
- Set your **capture distance** so the animal is fully inside before the door closes — the sensor is fixed in the POD, so there's nothing to position (see [Deploying Your Trap in the Field](deploying-in-the-field.md))
- Place bait **behind the sensor**, near the back of the cage, so animals must pass through the detection zone
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

The **distance sensor** in the POD watches the inside of the trap for movement.

### Detection Process
1. **Animal enters the detection area** (out to ~34 in / 875 mm from the sensor) — You may get a pre-capture alert
2. **Steady presence confirmed** — The trap waits for several consistent readings to avoid false triggers
3. **Animal reaches your capture distance** (default ~8 in) — The door closes
4. **Capture complete** — Photo taken and alert sent

### Why This Matters
Unlike traditional traps that use a mechanical trip pan, OcuTrap uses a **distance sensor** to detect the animal's position. This method:
- Improves accuracy
- Minimizes false triggers from rain, debris, or vibration
- Allows remote monitoring without physical trigger mechanisms

---

## Testing the Trap

This video shows how your OcuTrap works once it's set up and ready to catch animals.

{% embed url="https://hjxx5i3c7zgkvqye.public.blob.vercel-storage.com/videos/my-movie-13-DRM3GWu9pZ7fmKIA1sFAksHQ2Qcuqq.mp4" %}

### Test Before Deploying
1. **Arm the trap** using the app
2. **Wave your hand** through the detection zone
3. **Verify** the door closes and you receive an alert
4. **Disarm** and reset for deployment

---

## Trigger Settings

### Capture Distance
- **Default**: ~8 inches
- **Adjustable range**: 6–18 inches (app presets)
- **Tip**: Smaller values = animal must be closer before triggering

### Timing
- The sensor must register **continuous presence** before activating
- This timing **reduces false triggers** while ensuring the animal is fully enclosed
- Timing is automatic and cannot be manually adjusted

---

## Reducing False Triggers

If you're getting unwanted captures:

1. **Decrease capture distance** — Requires the animal to be closer before the door closes (reduces false triggers from rain, debris, or distant movement)
2. **Check sensor window** — Clean any dirt, debris, or condensation
3. **Reposition the trap** — Avoid areas with blowing debris or heavy rain entry
4. **Review pre-capture photos** — See what's triggering the trap

The trap uses a **two-step check** to filter out most false triggers from rain and debris automatically.

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
- Great alongside [Scouting Mode](app/scouting-mode.md) when you want photos and alerts without animal captures

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
- Consider the 10,000 mAh battery for extended cold-weather deployments

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
