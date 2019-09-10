import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import requests
import os

import libSevenSegDisplay as SSD

def setupPins(pinArray, setting):
    for pin in pinArray:
        if (setting is "OUT"):
            GPIO.setup(pin, GPIO.OUT)
        elif (setting is "IN"):
            GPIO.setup(pin, GPIO.IN)

def turnOffPins(pinArray):
    for pin in pinArray:
        GPIO.output(pin, GPIO.LOW)

img_num = 0;
img_base_path = './capture'

addr = "http://mhtl-kl4k.localhost.run/"

# configure GPIO
GPIO.setmode(GPIO.BCM)

# RPI BCM pin -> cathode character -> string of cathodes -> 7 segment character
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

butPin = 4
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
setupPins(ledPin, "IN")
setupPins(ledPin, "OUT")
turnOffPins(ledPin)

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
            sleep(2)
            # sleep for at least 2 seconds so the camera can adjust light levels
            img_path = img_base_path + str(img_num) + ".jpg"
            img_filename = os.path.basename(img_path)
            camera.capture(img_path)
            img_num += 1

            img = open(img_path, 'rb')
            data = img.read() # read in data as bytes
            response = requests.post(addr, data=data)
            img.close()

            # display prediction
            character = int(response.text, 10)
            SSD.displayCharacter(character, cathodeToPin)
            sleep(2)
            turnOffPins(ledPin)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
finally:
    camera.stop_preview()
