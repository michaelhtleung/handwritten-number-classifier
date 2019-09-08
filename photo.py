from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1000, 1000)

camera.start_preview(alpha=200)
for i in range(5):
    sleep(5)
    # sleep for at least 2 seconds so the camera can adjust light levels
    camera.capture('/home/pi/Projects/rpi-number-classifier/image%s.jpg' % i)
camera.stop_preview()
