---
description: >-
  OcuTrap R2 and R1 specifications: dimensions, door speeds, battery and
  runtime, connectivity, sensors, camera, and environmental ratings.
---

# Technical Specifications

This page provides detailed technical specifications for the OcuTrap R2 smart wildlife trap, with R1 values where they differ.

***

## Physical Specifications

| Specification | OcuTrap R2 | OcuTrap R1 |
| ------------- | ---------- | ---------- |
| **Width** | 10" (25.4 cm) | 10" (25.4 cm) |
| **Height** | 12" (30.5 cm) | 12" (30.5 cm) |
| **Length (cage only)** · trap body **without** the POD; door **closed** | 36" (91.4 cm) | 32" (81.3 cm) |
| **POD (adds to length)** | ~5" (~12.7 cm) | ~5" (~12.7 cm) |
| **Door open (adds to length)** | ~4" (~10.2 cm) | ~4" (~10.2 cm) |
| **Approx. total length** · with POD installed and door fully open | ~45" (~114 cm) | ~41" (~104 cm) |
| **Weight** | 19.8 lbs (8.98 kg) with the 56 Wh battery · 19.1 lbs (8.68 kg) without | 24 lbs (10.9 kg) with the 111 Wh battery |
| **Shipping box** | 36.5" × 11" × 15.5" | — see packing slip |
| **Construction** | Weather-resistant enclosure, compatible with Tomahawk trap frames | Weather-resistant enclosure, compatible with Tomahawk trap frames |
| **Target Animals** | 5–25 lbs (cats, raccoons, opossums, similar wildlife) | 5–25 lbs (cats, raccoons, opossums, similar wildlife) |

***

## Door Mechanism

| Specification       | Value                                                             |
| ------------------- | ----------------------------------------------------------------- |
| **Actuator Type**   | Linear motor with DRV8873 motor controller                        |
| **Close Speed**     | About 0.75 seconds                                                |
| **Open Speed**      | < 1 second                                                        |
| **Door States**     | Opening, Closing, Fully Open, Fully Closed, Error, Forced Stopped |
| **Control Methods** | App remote control, physical button sequence                      |

***

## Battery & Power

| Specification                      | Value                                   |
| ---------------------------------- | --------------------------------------- |
| **Battery Type**                   | Rechargeable KBT 12V Lithium-ion (6-cell pack)  |
| **Ships with R2**                  | 5,200 mAh (56 Wh)                       |
| **Shipped with R1 (US)**           | 10,000 mAh (111 Wh)                     |
| **Battery Voltage Range**          | \~9.6 V (power-off) to 12.1 V (full), set by Battery Type |
| **Low Battery Warning (20%)**      | \~10.4V (internal, set by Battery Type; 10.2 V on the 10,000 mAh pack) |
| **Critical Battery Warning (10%)** | 10.2 V (10.0 V on the 10,000 mAh pack)  |
| **Auto Power-Off Threshold**       | \~9.6V (internal, set by Battery Type)  |
| **Runtime (10000 mAh)**            | ~40+ days per charge (typical usage)    |
| **Runtime (5200 mAh)**             | \~21 days per charge (typical usage)    |
| **Charger (10000 mAh)**            | 2A @ 12V, \~5–6 hours full charge       |
| **Charger (5200 mAh)**             | 1A @ 12V, \~5–6 hours full charge       |
| **Trap connector (5200 mAh)**      | Male XT30 on pack; female XT30 on trap PCB |
| **Trap connector (10000 mAh)**   | Female XT30 on pack; male XT30 on trap PCB |
| **Alternate pack / connector**   | Contact support for PCB + holder swap   |

> **Selecting your battery in the app:** The R2 ships with the **5,200 mAh (56 Wh)** 12 V 6-cell pack, which is the app default. R1 units sold in the US shipped with the **10,000 mAh (111 Wh)** pack. Tell the app which one your trap uses under **Settings → Battery Type**. It adjusts the low-battery alert thresholds and level readout to match. R1 owners should check this setting, because the default assumes the 5,200 mAh pack. There are no manual voltage or percentage threshold controls; the app derives them from your Battery Type.

***

## Connectivity

| Specification           | Value                                      |
| ----------------------- | ------------------------------------------ |
| **Connection**          | LTE-M cellular (4G LTE network)            |
| **Coverage**            | Multi-network cellular coverage            |
| **GPS Update Interval** | Every 8 hours (default, battery-optimized) |
| **GPS Accuracy**        | Minimum 5 satellites, 3D fix required      |



## Sensors

### Distance Sensor

| Specification        | Value                                      |
| -------------------- | ------------------------------------------ |
| **Sensor Range**     | Up to 13 ft (4 m) hardware capability       |
| **Active Detection Range** | Up to ~**34 in (875 mm)** — the trap detects, alerts, and photographs only within this distance |
| **Capture Distance** | App presets **6–18 in**; default **8 in**. See [Distance Limits & Alerts](trap-settings/distance-safety-and-alerts.md) |

### Environmental Sensors

| Sensor                     | Function                                 |
| -------------------------- | ---------------------------------------- |
| **Temperature & Humidity** | Environmental monitoring, alerts         |
| **Ambient Light**          | Automatic day/night detection for camera |
| **Accelerometer**          | Orientation and movement sensing         |

### Temperature Thresholds

| Alert                      | Default Value                           |
| -------------------------- | --------------------------------------- |
| **High Temperature Alert** | 45°C (113°F)                            |
| **Low Temperature Alert**  | -10°C (14°F)                            |
| **Alert Interval**         | Every 8 hours (configurable 0–48 hours) |

***

## Camera System

| Specification                | Value                                         |
| ---------------------------- | --------------------------------------------- |
| **Night Vision**             | Integrated IR LED (automatic activation)      |
| **IR Brightness**            | 0–100% (configurable min/max)                 |
| **Image Sizes**              | QVGA to UXGA (6 selectable sizes)             |
| **Rotation Options**         | 0°, 90°, 180°, 270°                           |
| **Color Modes**              | Grayscale (dark conditions), Color (daylight) |
| **Dark Detection Threshold** | 25 lux (default, configurable 1–100 lux)      |
| **Timelapse Interval**       | 0–24 hours (default: 6 hours)                 |

***

## Capture Detection System

OcuTrap uses a two-step detection process to prevent false triggers from rain, debris, or non-target movement.

### Detection Process

1. **Animal enters the detection area** (within ~34 in / 875 mm) → Steady readings required before proceeding
2. **Pre-capture alert sent** (if enabled)
3. **Animal reaches capture distance** (your preset, default ~8 in) → Door closes
4. **Capture photo taken and transmitted**

### False Trigger Prevention

* **Steady-readings check** — Requires consistent presence before closing
* **Rain and debris filtering** — Ignores splashy or erratic movement
* **Dirty-sensor detection** — Blocks arming when the lens is obstructed

***

## What's in the Box

* OcuTrap R2 smart cage, with the door and motor installed
* POD (electronics module)
* 5,200 mAh (56 Wh) 12 V lithium-ion battery
* 1 A battery charger
* Quick start guide

No tools required. Cut the shipping zip tie, mount the POD, insert the battery, and add the trap in the app. See [Set up your OcuTrap R2](setting-up-r2.md).

R1 units shipped with the 10,000 mAh (111 Wh) battery and its 2 A charger, plus the assembly hardware for the door and handle.

***

## Environmental Ratings

| Specification             | Value                                                      |
| ------------------------- | ---------------------------------------------------------- |
| **Operating Temperature** | -10°C to 45°C (14°F to 113°F)                              |
| **Weather Resistance**    | Designed for outdoor field deployment                      |
| **Recommended Placement** | Areas with strong cellular signal for optimal battery life |

***

## Firmware & Software

| Specification  | Value              |
| -------------- | ------------------ |
| **Updates**    | Over-the-air (OTA) |
| **Mobile App** | iOS and Android    |

***

## Regulatory Information

For warranty, safety, and compliance information, see:

* [Safety Information](../support/safety-information.md)
* [Warranty Information](../legal-and-compliance/warranty-information.md)
* [Legal Disclaimers](../legal-and-compliance/legal-disclaimers-and-compliance-information.md)
