import board
import analogio
import touchio
import usb_midi

from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.midi import Midi
from kmk.keys import KC, make_key
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes

import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn


# KEYBOARD SET UP

keyboard = KMKKeyboard()

# custom key handler set up:
# key - key object
# keyboard - represents KMKKeyboard instance
def shift_octave_up(key, keyboard, *args):
    global current_octave
    if current_octave < MAX_OCTAVE:
        current_octave += 12  # Shift up by one octave (12 semitones)

def shift_octave_down(key, keyboard, *args):
    global current_octave
    if current_octave > MIN_OCTAVE:
        current_octave -= 12  # Shift down by one octave (12 semitones)

KC_OCT_UP = make_key(shift_octave_up)
KC_OCT_DOWN = make_key(shift_octave_down)

midi = Midi()
keyboard.modules.append(midi)

# initialize usb_midi output
# adafruit_midi.MIDI - initialize the MIDI object
# usb_midi.ports[1] - use the second USB MIDI port for output (the first is for input)
# out_channel=0  - set the output channel to 0 (MIDI channel 1)
midi_device = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# LEDs

rgb = RGB(
    pixel_pin = board.IO5,  
    num_pixels = 3,      # total # of LEDs
    val_default = 80,    # default brightness
    val_limit = 150       # max brightness
    hue_default = 0,      # starting color
    sat_default = 255,
    animation_mode = AnimationModes.STATIC,
)

keyboard.extensions.append(rgb)

# OCTAVE SHIFTING

current_octave = 0
MAX_OCTAVE = 36
MIN_OCTAVE = -36

def shift_octave_up(key, keyboard, *args):
    global current_octave
    if current_octave < MAX_OCTAVE:
        current_octave += 12  # Shift up by one octave (12 semitones)

def shift_octave_down(key, keyboard, *args):
    global current_octave
    if current_octave > MIN_OCTAVE:
        current_octave -= 12  # Shift down by one octave (12 semitones)

KC_OCT_UP = make_key(shift_octave_up)
KC_OCT_DOWN = make_key(shift_octave_down)

# SWITCHS & KEY MAPPINGS

# Key Switches: left to right
keyboard.pins = [
    board.RX,  # SW1, left
    board.TX, # SW2, center
    board.IO3, # SW3, right
]

keyboard.keymap = [
    [
        KC_OCT_DOWN,   
        KC.MPLY,   #pause/play
        KC_OCT_UP,      
    ],
]

# ROTARY ENCODER

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Encoder Pins: Phase A, Phase B, Push Switch (none)
encoder_handler.pins = (
    (board.IO5, board.IO6, None)
)

encoder_handler.map = [
    (
        #cc1 - modulation wheel
        [KC.MIDI(cc=7, val=+5), KC.MIDI(cc=7, val=-5)],
    ),
]

# ANALOG SLIDERS

# pin - set up the analog input pin for slider
# cc_num - set which cc number the slider controls
# last_cc_val - keep track of the last MIDI value sent to avoid sending duplicates
SLIDERS = [
    {
        "pin": analogio.AnalogIn(board.IO1),
        "cc_num": 1,
        "last_cc_val": -1
    },
    {
        "pin": analogio.AnalogIn(board.IO2),
        "cc_num": 71,
        "last_cc_val": -1
    }
]

TOUCH_KEYS = [
    {
        "sensor": touchio.TouchIn(board.IO7),
        "note": 60,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO8),
        "note": 62,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO9),
        "note": 64,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO10),
        "note": 66,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO11),
        "note": 68,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO12),
        "note": 70,  # C4 
        "playing_note": None,
        "is_touched": False
    },
    {
        "sensor": touchio.TouchIn(board.IO13),
        "note": 72,  # C4 
        "playing_note": None,
        "is_touched": False
    },
]

# FUNCTIONS

def process_slider():
    for slider in SLIDERS:

        # Convert 16-bit (0 65,535) analog value to 7-bit (0-127)
        current_cc_val = slider["pin"].value >> 9

        # Only send a new MIDI CC message if the value has changed significantly (to avoid flooding)
        if abs(current_cc_val - slider["last_cc_val"]) > 1:
            midi_device.send(ControlChange(slider["cc_num"], current_cc_val))
            slider["last_cc_val"] = current_cc_val

def process_touch_keys():
    for key in TOUCH_KEYS:
        currently_touched = key["sensor"].value

        if currently_touched and not key["is_touched"]:

            target_note = max(0, min(127, key["note"] + current_octave))

            key["playing_note"] = target_note
            midi_device.send(NoteOn(target_note, 127))  # Note on with velocity 127
            key["is_touched"] = True
        elif not currently_touched and key["is_touched"]:

            if key["playing_note"] is not None:
                midi_device.send(NoteOff(key["playing_note"], 0))  # Note off
                key["playing_note"] = None
                
            key["is_touched"] = False

# MAIN LOOP

if __name__ == '__main__':
    keyboard.update()
    process_slider()
    process_touch_keys()