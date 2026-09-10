---
description: >-
  How OcuTrap's GPS works: automatic update intervals, satellite and fix
  requirements, manual updates, accuracy tips, and battery impact.
---

# GPS

OcuTrap uses an integrated u-blox GPS module for location tracking and mapping. These settings help you get accurate location data for your traps.

---

### How GPS Works on OcuTrap

GPS limits its battery use. Instead of tracking location continuously, OcuTrap checks at set intervals so you can see trap locations without constant power use.

#### Default Behavior
- **Update Interval**: Every 6 hours by default on firmware v1073 or later. Choose Disabled, 3, 6, 12, or 24 hours. Firmware through v1072 uses a fixed 8-hour interval when enabled.
- **First Boot Delay**: 15 minutes after boot before the first GPS acquisition
- **Captures take priority**: Captures take priority and can postpone a GPS attempt
- **Fix Requirements**: Minimum 5 satellites with a 3D fix for valid position

---

### GPS Settings

#### GPS Update Interval

Choose **Disabled**, **3 hours**, **6 hours (default)**, **12 hours**, or **24 hours**. These choices require firmware v1073 or later and the updated app. Older firmware continues to use eight hours when GPS is enabled.

After boot, the first automatic attempt is eligible after 15 minutes. The schedule is checked every five minutes. Later attempts wait the selected interval after the previous attempt finishes, even if it did not get a fix. Changing the interval starts a new wait; saving the same interval does not restart it. Captures, photos, or a disconnected trap can delay an attempt.

**Disabled** stops automatic location updates. You can still request **Location** in Trap Controls. This can save battery on traps that stay in one known location. A saved setting is not confirmation that the trap has received it.

* In the trap’s **Settings**, find **GPS Update Interval** in device configuration.

#### GPS Status Indicators

When viewing trap locations, you'll see key metrics:

* **Satellites Connected**: Number of GPS satellites currently in use (e.g., "8 connected"). More satellites = better accuracy.
* **Last Updated**: How long ago the GPS position was updated (e.g., "6 Hours Ago").
* **Radius**: The trap's last location is within the approximate radius.

### Best Practices

#### Optimal GPS Performance

* Place the OcuTrap outdoors with clear sky view for best results
* **First attempt**: Once the search starts, allow up to 3 minutes for the first GPS acquisition after boot
* **Subsequent fixes**: Typically acquired within 2 minutes
* System will timeout if no fix is acquired within the timeout period
* More satellites generally means better accuracy
* Buildings, dense foliage, and urban canyons can reduce accuracy

#### Manual Updates

* In Trap Controls, tap **Location** to request a GPS update
* Works even when automatic GPS updates are disabled
* Useful for verifying position without waiting for next interval

#### Access Levels

* Anyone with access to a trap can view that trap's location. The owner and any managers the trap is shared with all see the trap on the map tab.
* You only see traps you own or that have been shared with you. A trap's location is not visible to anyone you haven't shared it with.

### Troubleshooting

#### No Fix Available

1. Ensure device is outdoors with clear view of sky
2. Wait up to 3 minutes for initial fix
3. For automatic updates, check **GPS Update Interval** is not Disabled
4. Request **Location** from Trap Controls
5. If problems persist, verify no physical obstructions are blocking GPS antenna

#### Poor Accuracy

* Move device to location with clearer sky view
* Wait for more satellites to be acquired
* Verify Fix type is 3 for best accuracy
* Consider environmental factors (buildings, trees, etc.)

### Battery Considerations

* GPS attempts use battery power
* **6 hours** is the default automatic interval on firmware v1073 or later
* Shorter intervals provide more frequent updates but reduce battery life
* Disable automatic GPS updates when location tracking is not needed
* Sleep and competing work can defer an attempt; a valid clock lets the trap account for elapsed sleep time
* Poor cellular signal in combination with GPS can increase power consumption

### Map Interface

* Toggle between Map and Satellite views
* Terrain overlay available for topographical reference
* Zoom controls for detailed area inspection
