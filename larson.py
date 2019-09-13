import RPi.GPIO as GPIO
import time

time_delay = 0.08

GPIO.setmode(GPIO.BCM)
PIN_DATA = 14
PIN_CLOCK = 15
PIN_LATCH = 18
GPIO.setup(PIN_DATA, GPIO.OUT)
GPIO.setup(PIN_LATCH, GPIO.OUT)
GPIO.setup(PIN_CLOCK, GPIO.OUT)

def shiftout(byte):
    GPIO.output(PIN_LATCH, 0)
    for x in range(8):
        GPIO.output(PIN_DATA, (byte >> x) & 1)
        GPIO.output(PIN_CLOCK, 1)
        GPIO.output(PIN_CLOCK, 0)
    GPIO.output(PIN_LATCH, 1)

b = 1;

while (1):
    for x in range(7):
        shiftout(b)
        b = b << 1
        time.sleep(time_delay)

    for x in range(7):
        shiftout(b)
        b = b >> 1
        time.sleep(time_delay)
