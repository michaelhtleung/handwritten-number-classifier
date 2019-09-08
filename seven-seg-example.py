import RPi.GPIO as GPIO
import time

import libSevenSegDisplay as SSD

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


def setupPins(pinArray, setting):
    for pin in pinArray:
        if (setting is "OUT"):
            GPIO.setup(pin, GPIO.OUT)
        elif (setting is "IN"):
            GPIO.setup(pin, GPIO.IN)

def turnOffPins(pinArray):
    for pin in pinArray:
        GPIO.output(pin, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
setupPins(ledPin, "IN")
setupPins(ledPin, "OUT")
turnOffPins(ledPin)

try:
    while 1:
        for character in range(0, 10):
            SSD.displayCharacter(character, cathodeToPin)
            time.sleep(0.3)
            turnOffPins(ledPin)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
#except: 
#    GPIO.cleanup()
