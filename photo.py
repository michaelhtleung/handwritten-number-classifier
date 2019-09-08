import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

# configure GPIO
butPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    GPIO.cleanup()
except: 
    GPIO.cleanup()
finally:
    camera.stop_preview()
