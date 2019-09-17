import RPi.GPIO as GPIO
import time

time_delay = 0.08

GPIO.setmode(GPIO.BCM)
PIN_DATA = 14
PIN_CLOCK = 15
PIN_LATCH = 18
PIN_RESET = 16
#GPIO.setup(PIN_DATA, GPIO.IN)
#GPIO.setup(PIN_LATCH, GPIO.IN)
#GPIO.setup(PIN_CLOCK, GPIO.IN)
#GPIO.setup(PIN_RESET, GPIO.IN)

GPIO.setup(PIN_DATA, GPIO.OUT)
GPIO.setup(PIN_LATCH, GPIO.OUT)
GPIO.setup(PIN_CLOCK, GPIO.OUT)
GPIO.setup(PIN_RESET, GPIO.OUT)

def shiftout(byte):
    GPIO.output(PIN_LATCH, 0)
    for x in range(8):
        GPIO.output(PIN_DATA, (byte >> x) & 1)
        GPIO.output(PIN_CLOCK, 1)
        GPIO.output(PIN_CLOCK, 0)
    GPIO.output(PIN_LATCH, 1)

def run_larson_scanner():
    b = 1;
    for pass_num in range(1):
        for x in range(7):
            shiftout(b)
            b = b << 1
            time.sleep(time_delay)

        for x in range(7):
            shiftout(b)
            b = b >> 1
            time.sleep(time_delay)

run_larson_scanner()
GPIO.output(PIN_RESET, 0)
time.sleep(2)
#GPIO.output(PIN_RESET, 1)
