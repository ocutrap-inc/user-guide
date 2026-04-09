# Technical Specifications

This page provides detailed technical specifications for the OcuTrap R1 smart wildlife trap.

***

## Physical Specifications

| Specification      | Value                                                             |
| ------------------ | ----------------------------------------------------------------- |
| **Dimensions**     | 10"W × 12"H × 32"L (25.4cm × 30.5cm × 81.3cm)                     |
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
| **Standard Capacity**              | 10,000 mAh (10Ah) — US shipments        |
| **Canadian Variant**               | 5,000 mAh (5Ah) — Canadian shipments    |
| **Operating Voltage Range**        | 7.0V – 15.0V                            |
| **Low Battery Warning (20%)**      | 10.4V (default, configurable)           |
| **Critical Battery Warning (10%)** | \~9.5V                                  |
| **Auto Power-Off Threshold**       | 9.6V (default, configurable 7.0V–12.0V) |
| **Runtime (10Ah)**                 | 4+ weeks per charge (typical usage)     |
| **Runtime (5Ah)**                  | \~21 days per charge (typical usage)    |
| **Charger (10Ah)**                 | 2A @ 12V, \~5–6 hours full charge       |
| **Charger (5Ah)**                  | 1A @ 12V, \~5–6 hours full charge       |

***

## Connectivity

| Specification           | Value                                      |
| ----------------------- | ------------------------------------------ |
| **Connection**          | 4G LTE Cellular                            |
| **Coverage**            | Multi-network cellular coverage            |
| **GPS Update Interval** | Every 8 hours (default, battery-optimized) |
| **GPS Accuracy**        | Minimum 5 satellites, 3D fix required      |



## Sensors

### Time-of-Flight (ToF) Distance Sensor

| Specification        | Value                                      |
| -------------------- | ------------------------------------------ |
| **Model**            | VL53L1X                                    |
| **Maximum Range**    | 0–4 meters                                 |
| **Capture Distance** | Configurable 125mm–1000mm (default: 250mm) |
| **Detection Zone**   | 300–450mm from sensor                      |
| **Capture Zone**     | 0–250mm from sensor                        |

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

OcuTrap uses a sophisticated dual-zone verification system to prevent false triggers from rain, debris, or non-target movement.

### Detection Process

1. **Object enters Detection Zone** (300–450mm) → 3+ consecutive valid readings required
2. **Object verified** → Pre-capture alert sent (if enabled)
3. **Object enters Capture Zone** (0–250mm) → 3+ consecutive readings trigger capture
4. **Door closes** → Capture photo taken and transmitted

### False Trigger Prevention

* **Signal quality filtering** — Validates signal-to-ambient ratio (optimized for outdoor sunlight)
* **Distance consistency checks** — ±20mm tolerance rejects oscillating readings
* **Rain detection** — Oscillation patterns identified and filtered
* **Status validation** — Only Status 0 (valid measurement) readings accepted

***

## What's in the Box

* OcuTrap R1 Smart Cage Unit
* 12V Lithium-ion Battery (10Ah US / 5Ah Canada)
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
