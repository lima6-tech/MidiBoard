# MidiBoard
A custom midi PCB with touch capacity keys, switches, LEDs and more!
Features hexagon shaped keys.

<img width="642" height="454" alt="Schematics_image" src="https://github.com/user-attachments/assets/58cdaeba-217b-4749-a955-6c81de007bdb" />
<img width="528" height="394" alt="PCB_image" src="https://github.com/user-attachments/assets/0505e24f-da00-4ff2-be06-fff81bd5847c" />

## Components

| Component | Quantity |
| --- | --- |
| LED SK6812MINI-E | 3 |
| Capacity Keys (Capacitive keys) | 1 |
| Potentiometer Bourn Single_Slide | 2 |
| Kailh Choc Low-Profile Switches | 3 |
| RotaryEncoder Alps EC11E-Switch Vertical H20mm | 1 |
| Waveshare ESP32-S3-Zero | 1 |

*Note that BOM total cost for each component because they have to be bought in batches

## Firmware
Done with Circuit python. At the present here is what the different components have been set to do:

Switches: 
- Left: Raises the notes played by an octave
- Center: pause / play (I plan to change this later)
- Right: Lowers the notes played by an octave

Rotary Encoder: volume

Sliders:
- Slider 1: modulation
- Slider 2: resonance
