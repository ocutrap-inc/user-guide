---
description: >-
  GPS startup, location refinement, automatic intervals, manual requests,
  reception and battery use, including firmware compatibility.
---

# GPS

OcuTrap checks its location periodically rather than tracking continuously. You
can also request a location when you need one.

> **Firmware preview:** The extended startup and refinement behavior below is
> included in the tested **v1081 candidate, which has not been released**. It
> applies only to traps running that candidate. Uploading firmware to Particle
> does not install it on your trap. Older firmware behaves as described below.

## Automatic location updates

In the trap's **Settings**, find **GPS Update Interval**. With firmware v1073 or
later and the updated app, choose **Disabled**, **3 hours**, **6 hours (default)**,
**12 hours**, or **24 hours**. There is no four-hour option. Firmware through
v1072 uses a fixed eight-hour interval when GPS is enabled.

**Disabled** stops automatic updates. You can still tap **Location** in Trap
Controls. A saved setting does not confirm that an offline trap has received it.

Later automatic attempts wait the selected interval after the previous session
finishes, including an unsuccessful attempt. The schedule is checked every five
minutes, and photos, captures, sleep or connectivity can delay an attempt further.
Changing the interval starts a new wait; saving the same value does not restart it.

## Startup in the v1081 candidate

When automatic GPS is enabled, the first search becomes eligible about **30
seconds after startup**, once startup tasks and higher-priority work permit.
The receiver then has a fixed **15-minute search and refinement window**, counted
from when it first powers on.

The trap sends the first acceptable location promptly. It does not wait until
15 minutes have passed. It continues looking for better fixes during the
remaining window and can send an improved location at most once per minute.

Photos and captures take priority. They can pause GPS, which resumes only for
the remaining original window. Paused time counts toward the 15 minutes.
Shutdown, low-battery handling and sleep can end the session early. In particular,
armed offline sleep does not guarantee a complete 15-minute startup search.
Routine trap work continues while GPS searches.

Firmware v1073 through v1077 instead waits 15 minutes before its first automatic
attempt. The extended startup behavior was introduced in the v1078 candidate
and is included in the combined v1081 candidate.

## Manual and scheduled refinement in the v1081 candidate

Tap **Location** in Trap Controls to request a GPS update, even when automatic
updates are disabled. Once a fresh valid fix is available, the trap queues it
for sending and continues searching for **two additional minutes**. Later
scheduled updates use the same two-minute refinement period.

During refinement, an update must have an estimated horizontal error at least
**10% smaller** than the last accepted fix. Improved locations are sent at most
once per **30 seconds**. The deadline stays fixed; another request or improved
fix does not extend it. If no better fix arrives, the first one remains valid.

A photo or capture after the first accepted fix ends this refinement so image
work can proceed. It does not replace that successful fix with a failed-location
result. Outside the GPS-enabled startup window, the first search can take up to
three minutes, and later searches up to two minutes, before the additional
refinement period starts. These are search limits, not guaranteed fix times.

## Reception and accuracy

Place the trap outdoors with a clear view of the sky. Buildings, a metal roof,
dense foliage and nearby obstructions can reduce reception. Indoors, a timeout
without a fix is expected and does not by itself mean the GPS is faulty.

The candidate requires fresh, valid position data from at least **five
satellites**, after at least **15 seconds** of receiver operation. A satellite
count alone does not establish a usable fix. Better reception may improve the
position estimate, but neither satellite count nor the receiver's accuracy
estimate guarantees the exact real-world location.

A stationary trap can report slightly different coordinates as estimates improve.
If a search gets no valid fix, the app keeps the last known location. Check when
that location was last updated before relying on it. GPS reception and LTE-M
cellular delivery are separate: a good satellite fix can still take longer to
appear in the app if cellular service is poor or images are queued.

## Battery use and retained GPS state

Six hours is the default, not a measured best interval for every installation.
For a stationary trap, longer intervals reduce the number of automatic searches.
If you do not need automatic tracking, choose **Disabled** and use a manual
Location request when needed. At an indoor or covered site, you can use **Set
location** to place the trap on the map without repeated satellite searches.

The startup window and two-minute refinement use additional receiver time to
seek better estimates. Actual battery use depends on reception, search duration,
photos and cellular activity. More frequent searches are not proven to improve
battery life, and this firmware does not choose an interval automatically.

On the reviewed circuit-board design, the GPS backup clock and saved receiver
state remain powered by the trap's main supply when normal GPS operation stops.
There is no separate backup battery shown. Retention therefore depends on that
main supply remaining powered; there is no verified fixed retention time after
removing the battery. Saved receiver state also does not guarantee a fast fix
six hours later. Other board revisions may differ.

## If the location does not update

1. Place the trap outdoors with a clear sky view and check cellular connectivity.
2. For automatic updates, confirm **GPS Update Interval** is not Disabled and
   allow for the firmware-specific startup and search windows above.
3. Request **Location** in Trap Controls. A photo or capture may take priority.
4. Check the location's last-update time. A failed search preserves the previous
   location; it does not prove that the trap is still at that position.
5. If searches repeatedly fail outdoors, contact support with the trap identifier,
   firmware version and approximate request time.

## Who can see the location

You can view traps you own or that have been shared with you. A trap's location
is not visible to people who have not been given access.
