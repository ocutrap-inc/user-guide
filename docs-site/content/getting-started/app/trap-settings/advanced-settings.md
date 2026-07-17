---
description: >-
  The advanced settings provide additional control over alerts, temperature
  monitoring, and image processing. These options are intended for users who
  want finer control over trap behavior.
---

# Advanced Settings

> **Note:** After changing any advanced settings, a reboot of the trap is recommended to ensure all changes are applied correctly.

***

#### Outdoor Temperature Alerts

Enables or disables alerts when the weather at the trap gets too hot or too cold.

These alerts use the **outdoor weather at the trap's location**, not a reading from the trap's own sensor.

The trap's location can come from either its **GPS fix** or a location you **set manually**. Only a trap that has neither, one that has never reported a location and never had one set, cannot check the weather. If that happens, set the location yourself and the checks begin at the next interval.

The selected interval determines how often the weather is checked.

Until the first check comes back, the card shows **Not checked yet** and no temperature. Checks run on a schedule rather than the moment you switch them on, so give it up to an hour to fill in.

***

#### Temperature Alert Thresholds

Defines the outdoor temperature limits that trigger alerts. These values use the selected unit system, shown as Imperial in the interface.

**Above Upper Limit**

Sets the maximum temperature. An alert is sent if the outdoor temperature at the trap rises above this value.

**Below Lower Limit**

Sets the minimum temperature. An alert is sent if the outdoor temperature at the trap falls below this value.

***

#### Capture Alerts

Controls notifications related to capture events.

**Capture Alerts Interval**

Defines the minimum amount of time between capture alerts. This helps prevent repeated notifications for the same capture event or ongoing activity.

***

#### Image Cropping

Adjusts how images are cropped before being processed or uploaded. Cropping can be used to remove unnecessary areas of the image, reduce file size, or focus on a specific region inside the trap.

**Left Crop**

Removes a portion of the image from the left side.

**Right Crop**

Removes a portion of the image from the right side.

**Top Crop**

Removes a portion of the image from the top.

**Bottom Crop**

Removes a portion of the image from the bottom.

***
