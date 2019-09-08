import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

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
camera.resolution = (1000, 1000)

print("Press the button to capture photo. Press CTRL+C to exit")
camera.start_preview(alpha=200)
try:
    while 1:
        if GPIO.input(butPin): # button is released
            pass
        else: # button is pressed
            sleep(2)
            # sleep for at least 2 seconds so the camera can adjust light levels
            camera.capture('/home/pi/Projects/rpi-number-classifier/capture.jpg')
            for character in range(0, 10):
                SSD.displayCharacter(character, cathodeToPin)
                sleep(0.3)
                turnOffPins(ledPin)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
except: 
    GPIO.cleanup()
finally:
    camera.stop_preview()
