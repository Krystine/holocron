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
WAV_FILE_NAME = "test_room.wav"                 # name of your wave file in top folder
COLOR_WHITE = (255, 255, 255)                   # white light (or FFFFFF)
COLOR_RED   = (255, 0, 0)                       # red light
MOVE_THRESH = 100                               # threshold for determining if holocron moved

""" Enable power to the Prop-Maker Wing """
WING_PWR = digitalio.DigitalInOut(board.D10)
WING_PWR.direction = digitalio.Direction.OUTPUT
WING_PWR.value = True

""" built-in LED on the Feather, used for debug status """
status = digitalio.DigitalInOut(board.D13)
status.direction = digitalio.Direction.OUTPUT
status.value = True

""" Set up NeoPixel Jewel """
NUM_PIXELS = 14                                 # NeoPixel length (7 doesn't work for me?)
NEOPIXEL_PIN = board.D5                         # pin where Jewel is connected (D5 for this wing)
JEWEL = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.1)

JEWEL.fill(COLOR_WHITE)                         # turn on all NeoPixels in the jewel
JEWEL.show()

""" Set up accelerometer """
I2C = busio.I2C(board.SCL, board.SDA)
ACCEL = adafruit_lis3dh.LIS3DH_I2C(I2C, address=0x18)
ACCEL.range = adafruit_lis3dh.RANGE_4_G

#-------------------------------------------------------------------------------------------
#                                        FUNCTIONS
#-------------------------------------------------------------------------------------------
def play_wav(wav_name):
    """
    Play a .wav file from the top directory (the same directory as the main.py file).
    
    @param wav_name : Name of .wav file defined above. must include ".wav" extension.
    @param loop     : If True, sound will repeat indefinitely. Default is false.
    """
    try:
        wave_file = open(wav_name, "rb")
        wave = audioio.WaveFile(wave_file)
        AUDIO.play(wave, loop=False)
    except:
        return
 
#-------------------------------------------------------------------------------------------
#                                       MAIN LOOP
#-------------------------------------------------------------------------------------------
while True:
    status.value = True
    time.sleep(0.5)
    status.value = False
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
         
            AUDIO.play(wave)
            JEWEL.fill(COLOR_RED)                           # set red color
            JEWEL.show()
            while AUDIO.playing:
                pass
                
        wave_file.close()                                   # close .wav so we can play it again later :)
        JEWEL.fill(COLOR_WHITE)                             # set color back to solid white