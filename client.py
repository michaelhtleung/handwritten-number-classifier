import RPi.GPIO as GPIO
from picamera import PiCamera
import threading
import time 
import requests
import os

import libSevenSegDisplay as SSD
#import larson

unique_portion = "nnis"
addr = "http://mhtl-" + unique_portion + ".localhost.run/"

img_num = 0;
img_base_path = './capture'

response_received = False
larson_time_delay = 0.08

def setupPins(pinArray, setting):
    for pin in pinArray:
        if (setting is "OUT"):
            GPIO.setup(pin, GPIO.OUT)
        elif (setting is "IN"):
            GPIO.setup(pin, GPIO.IN)

def turnOffPins(pinArray):
    for pin in pinArray:
        GPIO.output(pin, GPIO.LOW)

def count_up():
    count = 0
    while (response_received is False):
        print(count)
        count += 1

def shiftout(byte):
    GPIO.output(PIN_LATCH, 0)
    for x in range(8):
        GPIO.output(PIN_DATA, (byte >> x) & 1)
        GPIO.output(PIN_CLOCK, 1)
        GPIO.output(PIN_CLOCK, 0)
    GPIO.output(PIN_LATCH, 1)

def run_larson_scanner(b):
    while (response_received is False):
        for x in range(7):
            shiftout(b)
            b = b << 1
            time.sleep(larson_time_delay)

        for x in range(7):
            shiftout(b)
            b = b >> 1
            time.sleep(larson_time_delay)
        
def clear_larson_scanner():
    for x in range(7):
        shiftout(0)

# configure GPIO
GPIO.setmode(GPIO.BCM)

# pins responsible only for larson scanner
PIN_DATA = 14
PIN_CLOCK = 15
PIN_LATCH = 18
larson_pins = [PIN_DATA, PIN_CLOCK, PIN_LATCH]

# RPI BCM pin -> cathode character -> string of cathodes -> 7 segment character
# pins responsible for only the 7 segment display LEDs
ledPin = [
        17, 
        27, 
        22, 23,
        5,
        6,
        26
]

cathodeToPin = {
        "A": 17,
        "B": 27, 
        "C": 22, 
        "D": 23,
        "E": 5,
        "F": 6,
        "G": 26
}

all_output_pins = ledPin + larson_pins

butPin = 4
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
setupPins(all_output_pins, "IN")
setupPins(all_output_pins, "OUT")
turnOffPins(all_output_pins)

#configure camera
camera = PiCamera()
camera.rotation = 180
camera.resolution = (2000, 2000)

print("Press the button to capture photo. Press CTRL+C to exit")
camera.start_preview(alpha=200)
try:
    while 1:
        if GPIO.input(butPin): # button is released
            pass
        else: # button is pressed
            turnOffPins(ledPin)
            response_received = False
            # sleep for at least 2 seconds so the camera can adjust light levels
            img_path = img_base_path + str(img_num) + ".jpg"
            img_filename = os.path.basename(img_path)
            camera.capture(img_path)
            img_num += 1

            img = open(img_path, 'rb')
            data = img.read() # read in data as bytes
            img.close()

            #larson_thread = threading.Thread(target=count_up, args=())
            larson_thread = threading.Thread(target=run_larson_scanner, args=(1,))
            larson_thread.start()
            response = requests.post(addr, data=data)
            response_received = True
            larson_thread.join()
            clear_larson_scanner()

            # display prediction
            character = int(response.text, 10)
            SSD.displayCharacter(character, cathodeToPin)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
finally:
    camera.stop_preview()
