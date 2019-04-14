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
import busio
import adafruit_lis3dh
 
#-------------------------------------------------------------------------------------------
#                                          SETUP
#-------------------------------------------------------------------------------------------
WAV_FILE_NAME       = "test_room.wav"           # name of your wave file in top folder
COLOR_WHITE         = (255, 255, 255)           # white light (or FFFFFF)
COLOR_RED           = (255, 0, 0)               # red light
MOVE_THRESH         = 100                       # threshold for determining if holocron moved
NORM_BRIGHTNESS     = 0.5                       # brightness of LED while sound is off
MAX_BRIGHTNESS      = 1.0                       # maximum brightness of Jewel
MIN_BRIGHTNESS      = 0.1                       # chosen minimum brightness of Jewel

""" Enable power to the Prop-Maker Wing """
WING_PWR = digitalio.DigitalInOut(board.D10)    # Pin D10 must be enabled for Prop-Maker Wing
WING_PWR.direction = digitalio.Direction.OUTPUT
WING_PWR.value = True

""" Built-in LED on the Feather, used for debug status """
status_led = digitalio.DigitalInOut(board.D13)
status_led.direction = digitalio.Direction.OUTPUT
status_led.value = True

""" Set up built-in NeoPixel on Feather M0 Express """
PIX = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1, auto_write=True)
PIX.fill(COLOR_RED)                             # set color to red

""" Set up NeoPixel Jewel """
NUM_PIXELS = 14                                 # NeoPixel length (7 doesn't work for me?)
NEOPIXEL_PIN = board.D5                         # pin where Jewel is connected (D5 for this wing)
JEWEL = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.1, auto_write=True)

JEWEL.fill(COLOR_WHITE)                         # turn on all NeoPixels in the jewel

""" Set up accelerometer """
I2C = busio.I2C(board.SCL, board.SDA)
ACCEL = adafruit_lis3dh.LIS3DH_I2C(I2C, address=0x18)
ACCEL.range = adafruit_lis3dh.RANGE_4_G

#-------------------------------------------------------------------------------------------
#                                       MAIN LOOP
#-------------------------------------------------------------------------------------------
while True:
    """ Toggle status LED on Feather. Comment this part out after debugging. """
    status_led.value = True
    time.sleep(0.5)
    status_led.value = False
    time.sleep(0.5) 
    
    """ Get accelerometer reading and do calculation """
    ACCEL_X, ACCEL_Y, ACCEL_Z = ACCEL.acceleration          # read accelerometer
    ACCEL_SQUARED = ACCEL_X * ACCEL_X + ACCEL_Z * ACCEL_Z + ACCEL_Y * ACCEL_Y
    
    """ Check if holocron movement was above threshold. If it was,
        begin playing sound. This part of the code blocks until
        sound is complete. """
    if (ACCEL_SQUARED > MOVE_THRESH):
        with audioio.AudioOut(board.A0) as AUDIO:           # speaker connected to analog out (pin A0 on Feather m0)
            wave_file = open(WAV_FILE_NAME, "rb")           # open .wav
            wave = audioio.WaveFile(wave_file)
         
            AUDIO.play(wave)                                # start audio
            
            """ While audio plays, animate a breathing effect on the Jewel"""
            i = NORM_BRIGHTNESS * 100                       # convert to number 0-100 instead of fractional number
            
            while AUDIO.playing:
                """ Increase in brightness to max. Break early
                    if the audio finishes playing """
                while i < (MAX_BRIGHTNESS*100) and AUDIO.playing:
                    JEWEL.brightness = (i / 100.0)
                    i += 1
                    
                time.sleep(0.25)
                
                """ Decrease in brightness to min. Break early
                    if the audio finishes playing """                
                while i > (MIN_BRIGHTNESS*100) and AUDIO.playing:
                    JEWEL.brightness = (i / 100.0)  
                    i -= 1
                    time.sleep(0.01)
                
            wave_file.close()                               # close .wav so we can play it again later :)
            
            """ Smoothly return Jewel back to its normal brightness. """
            if i > (NORM_BRIGHTNESS*100):
                while i > (NORM_BRIGHTNESS*100):
                    JEWEL.brightness = (i / 100.0)
                    i -= 1
            elif i < ((NORM_BRIGHTNESS*100)):
                while i < (NORM_BRIGHTNESS*100):
                    JEWEL.brightness = (i / 100.0)
                    i += 1
            else:
                JEWEL.brightness = NORM_BRIGHTNESS