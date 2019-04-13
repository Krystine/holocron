""" Darth Azaryia's Sith Holocron """

""" Designed to be deployed on a Feather M0 Express with the 
    following additional hardware:
        -> Prop-Maker FeatherWing
        -> NeoPixel Jewel 7
        -> Mini Oval Speaker
        -> Power button/switch 
        
    DEPENDENCIES:
        neopixel.mpy
        adafruit_l3gd20.mpy """
        
import digitalio
import board
import audioio
import time
import neopixel
 
WAV_FILE_NAME = "test_room.wav"                 # name of your wave file in top folder
COLOR_WHITE = (255, 255, 255)                   # white light (or FFFFFF)

""" Enable power to the Prop-Maker Wing """
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

""" built-in LED on the Feather, used for debug status """
status = digitalio.DigitalInOut(board.D13)
status.direction = digitalio.Direction.OUTPUT
status.value = True

""" Set up NeoPixel Jewel """
NUM_PIXELS = 14                                 # NeoPixel length (7 doesn't work for me?)
NEOPIXEL_PIN = board.D5                         # pin where Jewel is connected (D5 for this wing)
JEWEL = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.1)

for pixel in range(NUM_PIXELS):                 # turn on NeoPixels in the jewel 
    JEWEL[pixel] = COLOR_WHITE
    JEWEL.show()

with audioio.AudioOut(board.A0) as audio:  # Speaker connector
    wave_file = open(WAV_FILE_NAME, "rb")
    wave = audioio.WaveFile(wave_file)
 
    audio.play(wave)
    while audio.playing:
        pass
        
while True:
    status.value = True
    time.sleep(0.5)
    status.value = False
    time.sleep(0.5) 