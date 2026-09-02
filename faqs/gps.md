---
description: >-
  How OcuTrap's GPS works: the fixed 8-hour update interval, satellite and fix
  requirements, manual updates, accuracy tips, and battery impact.
---

# GPS

OcuTrap uses an integrated u-blox GPS module to provide location tracking and mapping capabilities. This guide explains the GPS settings and functionality to help you get the most accurate location data for your traps.

---

### How GPS Works on OcuTrap

GPS is **battery-optimized by design**. Rather than continuously tracking location, OcuTrap uses strategic update intervals to maximize battery life while keeping you informed of trap locations.

#### Default Behavior
- **Update Interval**: Every 8 hours (fixed)
- **First Boot Delay**: 15 minutes after boot before the first GPS acquisition
- **Captures take priority**: A capture in progress pauses GPS until it finishes; GPS never interrupts a capture
- **Fix Requirements**: Minimum 5 satellites with a 3D fix for valid position

---

### GPS Settings

#### Location (GPS)

Location (GPS) is on or off. When on, the trap gets a fix 15 minutes after boot and then every 8 hours; the interval is fixed. Turn it off for indoor or covered deployments to save battery.

* Located in **Settings → Location**

#### GPS Status Indicators

When viewing trap locations, you'll see key metrics:

* **Satellites Connected**: Number of GPS satellites currently in use (e.g., "8 connected"). More satellites = better accuracy.
* **Last Updated**: How long ago the GPS position was updated (e.g., "6 Hours Ago").
* **Radius**: The trap's last location is within the approximate radius.

### Best Practices

#### Optimal GPS Performance

* Place the OcuTrap outdoors with clear sky view for best results
* **First fix**: Allow up to 3 minutes for initial GPS acquisition after power-on
* **Subsequent fixes**: Typically acquired within 2 minutes
* System will timeout if no fix is acquired within the timeout period
* More satellites generally means better accuracy
* Buildings, dense foliage, and urban canyons can reduce accuracy

#### Manual Updates

* In controls, click on data button to request a GPS update
* Only works when GPS is not disabled in settings
* Useful for verifying position without waiting for next interval

#### Access Levels

* Anyone with access to a trap can view that trap's location. The owner and any managers the trap is shared with all see the trap on the map tab.
* You only see traps you own or that have been shared with you — a trap's location is not visible to anyone you haven't shared it with.

### Troubleshooting

#### No Fix Available

1. Ensure device is outdoors with clear view of sky
2. Wait up to 3 minutes for initial fix
3. Check that Location (GPS) is on in settings
4. Try manual update by clicking location data
5. If problems persist, verify no physical obstructions are blocking GPS antenna

#### Poor Accuracy

* Move device to location with clearer sky view
* Wait for more satellites to be acquired
* Verify Fix type is 3 for best accuracy
* Consider environmental factors (buildings, trees, etc.)

### Battery Considerations

* GPS usage impacts battery life significantly
* **Default 8-hour interval** is optimized for multi-week deployments
* Shorter intervals provide more frequent updates but reduce battery life
* Disable GPS when location tracking not needed
* GPS is automatically disabled in Low Power mode to conserve battery
* Poor cellular signal in combination with GPS can increase power consumption

### Map Interface

* Toggle between Map and Satellite views
* Terrain overlay available for topographical reference
* Zoom controls for detailed area inspection
