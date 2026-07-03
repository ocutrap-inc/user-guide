# Technical Specifications

This page provides detailed technical specifications for the OcuTrap R1 smart wildlife trap.

***

## Physical Specifications

| Specification      | Value                                                             |
| ------------------ | ----------------------------------------------------------------- |
| **Width**          | 10" (25.4 cm)                                                     |
| **Height**         | 12" (30.5 cm)                                                     |
| **Length (cage only)** | 32" (81.3 cm) — trap body **without** the POD; door **closed** |
| **POD (adds to length)** | ~5" (~12.7 cm)                                                |
| **Door open (adds to length)** | ~4" (~10.2 cm)                                          |
| **Approx. total length** | ~41" (~104 cm) with POD installed and door fully open       |
| **Weight**         | 24 lbs (10.9 kg)                                                  |
| **Construction**   | Weather-resistant enclosure, compatible with Tomahawk trap frames |
| **Target Animals** | 5–25 lbs (cats, raccoons, opossums, similar wildlife)             |

***

## Door Mechanism

| Specification       | Value                                                             |
| ------------------- | ----------------------------------------------------------------- |
| **Actuator Type**   | Linear motor with DRV8873 motor controller                        |
| **Close Speed**     | < 0.5 seconds                                                     |
| **Open Speed**      | < 1 second                                                        |
| **Door States**     | Opening, Closing, Fully Open, Fully Closed, Error, Forced Stopped |
| **Control Methods** | App remote control, physical button sequence                      |

***

## Battery & Power

| Specification                      | Value                                   |
| ---------------------------------- | --------------------------------------- |
| **Battery Type**                   | Rechargeable KBT 12V Lithium-ion        |
| **Standard Capacity**              | 10,000 mAh (111 Wh) — new traps / US shipments |
| **Canadian Variant**               | 5,200 mAh — Canadian shipments          |
| **Operating Voltage Range**        | 7.0V – 15.0V                            |
| **Low Battery Warning (20%)**      | 10.4V (default, configurable)           |
| **Critical Battery Warning (10%)** | \~9.5V                                  |
| **Auto Power-Off Threshold**       | 9.6V (default, configurable 7.0V–12.0V) |
| **Runtime (10000 mAh)**            | ~40+ days per charge (typical usage)    |
| **Runtime (5200 mAh)**             | \~21 days per charge (typical usage)    |
| **Charger (10000 mAh)**            | 2A @ 12V, \~5–6 hours full charge       |
| **Charger (5200 mAh)**             | 1A @ 12V, \~5–6 hours full charge       |
| **Trap connector (5200 mAh)**      | Male XT30 on pack; female XT30 on trap PCB |
| **Trap connector (10000 mAh)**   | Female XT30 on pack; male XT30 on trap PCB |
| **Alternate pack / connector**   | Contact support for PCB + holder swap   |

***

## Connectivity

| Specification           | Value                                      |
| ----------------------- | ------------------------------------------ |
| **Connection**          | 4G LTE Cellular                            |
| **Coverage**            | Multi-network cellular coverage            |
| **GPS Update Interval** | Every 8 hours (default, battery-optimized) |
| **GPS Accuracy**        | Minimum 5 satellites, 3D fix required      |



## Sensors

### Distance Sensor

| Specification        | Value                                      |
| -------------------- | ------------------------------------------ |
| **Maximum Range**    | Up to 13 ft (4 m)                          |
| **Capture Distance** | App presets **6–18 in**; default **8 in**. See [Distance Limits & Alerts](trap-settings/distance-safety-and-alerts.md) |

### Environmental Sensors

| Sensor                     | Function                                 |
| -------------------------- | ---------------------------------------- |
| **Temperature & Humidity** | Environmental monitoring, alerts         |
| **Ambient Light**          | Automatic day/night detection for camera |
| **Accelerometer**          | Tilt detection, movement alerts          |

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

1. **Animal enters alert zone** (~12–18 in) → Steady readings required before proceeding
2. **Pre-capture alert sent** (if enabled)
3. **Animal reaches capture distance** (your preset, default ~8 in) → Door closes
4. **Capture photo taken and transmitted**

### False Trigger Prevention

* **Steady-readings check** — Requires consistent presence before closing
* **Rain and debris filtering** — Ignores splashy or erratic movement
* **Dirty-sensor detection** — Blocks arming when the lens is obstructed

***

## What's in the Box

* OcuTrap R1 Smart Cage Unit
* 12V Lithium-ion Battery (10000 mAh US / 5200 mAh Canada)
* Battery Charger (2A or 1A depending on battery)
* Quick-Start Guide
* Assembly hardware

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
