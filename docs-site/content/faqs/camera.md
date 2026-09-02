---
description: >-
  This guide explains how to adjust key camera settings, including time-lapse
  frequency, image quality, and night vision parameters.
---

# Camera

The **OcuTrap camera** provides **daytime and night vision capabilities**, allowing users to configure image capture settings based on lighting conditions.

***

### Camera Time-Lapse Mode

OcuTrap can **automatically capture images** at set intervals in **every mode**: unarmed, armed, scouting, and after a capture.

#### Configurable Option

* **Photo Capture Frequency** – Defines how often the camera captures an image, in every mode (unarmed, armed, scouting, and after a capture).

{% hint style="info" %}
If images are too frequent, **reduce the frequency** to conserve battery and data. If you need more monitoring, **increase the frequency** to capture more activity.
{% endhint %}

***

### Camera Image Settings

These settings control **image quality, resolution, and night vision brightness**.

* **Image Quality** – Adjusts resolution and compression. Higher quality means clearer images but **increased data usage**.
* **Image Size** – Defines the resolution of captured images.
* **Maximum IR Brightness** – Adjusts infrared light intensity in **night vision mode** to **prevent overexposure or underexposure**.

{% hint style="info" %}
If **daytime images look fine but nighttime images are too dark**, **increase** _Max IR Brightness_.
{% endhint %}

{% hint style="info" %}
If **nighttime images are washed out or too bright**, **lower** _Max IR Brightness_.
{% endhint %}

#### Limits for IR Brightness

| **Setting**           | **Min Value** | **Default Value** | **Max Value** |
| --------------------- | ------------- | ----------------- | ------------- |
| **Max IR Brightness** | `0`           | `100`             | `100`         |
| **Min IR Brightness** | `0`           | `10`              | `100`         |

***

### Night Vision & Light Adaptation

{% hint style="warning" %}
**Most users do not need to adjust light settings**, as the camera is designed to work automatically. However, users can fine-tune these settings for optimal image clarity in specific environments.
{% endhint %}

<figure><img src="../.gitbook/assets/Untitled (Flat Greeting Card - Landscape (7 in x 5 in)).png" alt=""><figcaption></figcaption></figure>

The camera **automatically adjusts** between **color mode** (daytime) and **night vision (greyscale)** based on ambient light levels.

#### Automatic Light Switching

* **Dark Lux Threshold**
  * If ambient light **falls below this value**, the camera activates **night vision mode** (greyscale) and **enables IR**.
* **Dynamic Light Adaptation**
  * There is one lux threshold. **Below it**, IR brightness ramps between _Min IR Brightness_ and _Max IR Brightness_ as light drops. **Above it**, the camera shoots color with IR off.

#### Limits for Light Thresholds

| **Setting**              | **Min Value** | **Default Value** | **Max Value** |
| ------------------------ | ------------- | ----------------- | ------------- |
| _**Dark Lux Threshold**_ | `1.0`         | `25.0`            | `100.0`       |

{% hint style="info" %}
If **daytime images are still in greyscale**, **lower** _Dark Lux Threshold_ so the camera switches to color mode sooner.

If **nighttime images are still in color and too dark**, **increase** _Dark Lux Threshold_ to enable greyscale mode earlier.
{% endhint %}

***

### Understanding and Adjusting Image Quality

If you experience **image quality issues**, use the guide below to fine-tune your settings:

| **Issue**                                         | **Cause**                        | **Solution**                                                            |
| ------------------------------------------------- | -------------------------------- | ----------------------------------------------------------------------- |
| **Daytime images appear too dark**                | _Dark Lux Threshold_ is too high | Lower _Dark Lux Threshold_ so the camera switches to color mode sooner. |
| **Daytime images are blurry**                     | Low image quality setting        | Increase **Image Quality** in settings.                                 |
| **Nighttime images are too dark**                 | IR brightness is too low         | Increase _Max IR Brightness_ to enhance night vision.                   |
| **Nighttime images are too bright or washed out** | IR brightness is too high        | Lower _Max IR Brightness_ to prevent overexposure.                      |
| **Images have too much glare**                    | Reflections from IR light        | Adjust trap positioning or lower _Max IR Brightness_.                   |
| **Images are too pixelated**                      | Low resolution setting           | Increase **Image Size** or **Image Quality**.                           |

***

### How OcuTrap Adapts to Different Light Conditions

| **Light Condition**                              | **Camera Mode**              | **IR Brightness**                       |
| ------------------------------------------------ | ---------------------------- | --------------------------------------- |
| **Bright daylight** (above the _dark lux threshold_) | **Color**                | **Off**                                 |
| **Low light/Night** (below the _dark lux threshold_) | **Greyscale (night vision)** | _**Ramps between Min and Max IR Brightness as light drops**_ |

***

### Summary of Best Practices

**For Most Users:**

* No need to adjust light settings—the camera adapts automatically.

**If Adjustments Are Needed:**

* **Improve night images** → Increase `maxIrBrightness`.
* **Fix overexposed IR images** → Lower `maxIrBrightness`.
* **Make daytime images clearer** → Increase **Image Quality**.
