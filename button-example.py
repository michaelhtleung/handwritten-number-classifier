import RPi.GPIO as GPIO
import time

pwmPin = 18
ledPin = 23
butPin = 17

dc = 95

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 50)

GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(ledPin, GPIO.LOW)
pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(butPin): # button is released
            pwm.ChangeDutyCycle(dc)
            GPIO.output(ledPin, GPIO.LOW)
        else: # button is pressed
            pwm.ChangeDutyCycle(100-dc)
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(0.075)

except KeyboardInterrupt: # if ctrl+c is pressed, exit program cleanly
    pwm.stop()
    GPIO.cleanup()
except: 
    GPIO.cleanup()

