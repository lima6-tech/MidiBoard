# MidiBoard
A custom midi board PCB. Features hexagon shaped touch capacity keys, switches with LEDs and rotary encoders + potentiometer sliders. 

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


## Firmware
Done with Circuit python. The capacity keys play notes (A-G). The different midi board components have been set to do different note adjustment functions (controlling midi cc values). I might later change the middle (2nd) key to change key layers. 

| Component | Function |
| --- | --- |
| Left switch | Raises the notes played by an octave |
| Center switch | pause / play |
| Right switch | Lowers the notes played by an octave |
| Rotary Encoder | controls volume |
| Slider 1 | note modulation |
| Slider  | note resonance
