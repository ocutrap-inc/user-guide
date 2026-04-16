# Trap Tests

{% hint style="info" %}
**Firmware requirement:** v565 or later
{% endhint %}

A safe, audio-only demo of your trap's detection pipeline — no door movement.

***

### Before You Start

Confirm all four before running Trap Test:

1. Trap door is **open**
2. Trap is **unarmed**
3. Trap is **clear** of obstructions
4. Open the back pod door so the beeps can be clearly heard

### Finding Trap Test Button

From your trap, tap **Settings → More Settings → Trap Test** button at the top of the settings page.

### What the Button Does

Tapping **Trap Test** sends a test command to your device. The trap enters a safe demo mode — audio feedback only, no door movement. There is no visible response in the app; listen for audio from the trap to confirm the test is running.

### Running the Test

Wave your hand (or any object) toward the sensor. You'll hear the trap react through four phases:

| Phase         | What You Hear       | What It Means                                                |
| ------------- | ------------------- | ------------------------------------------------------------ |
| **Waiting**   | Silent              | Ready — move something toward the sensor                     |
| **Detecting** | Beeps, speeding up  | Object seen within \~39 in (1000 mm)                         |
| **Verified**  | Confirmation cue    | Reading is stable — move into the capture zone               |
| **Capture!**  | Solid 3-second tone | Crossed the trigger distance — door would close in real mode |
