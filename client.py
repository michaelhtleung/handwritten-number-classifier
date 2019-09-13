import RPi.GPIO as GPIO
from picamera import PiCamera
import threading
from time import sleep
import requests
import os

import libSevenSegDisplay as SSD

unique_portion = "nnis"
addr = "http://mhtl-" + unique_portion + ".localhost.run/"

img_num = 0;
img_base_path = './capture'

response_received = False

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
            sleep(1)
            # sleep for at least 2 seconds so the camera can adjust light levels
            img_path = img_base_path + str(img_num) + ".jpg"
            img_filename = os.path.basename(img_path)
            camera.capture(img_path)
            img_num += 1

            img = open(img_path, 'rb')
            data = img.read() # read in data as bytes
            img.close()

            larson_thread = threading.Thread(target=count_up, args=())
            larson_thread.start()
            response = requests.post(addr, data=data)
            response_received = True
            larson_thread.join()
            print("larson thread joined")

            # display prediction
            character = int(response.text, 10)
            SSD.displayCharacter(character, cathodeToPin)
            sleep(2)
            turnOffPins(ledPin)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
finally:
    camera.stop_preview()
