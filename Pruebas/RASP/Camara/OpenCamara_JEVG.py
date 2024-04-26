


from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()
picam2.start_preview()
sleep(10)
picam2.capture_file("test.jpg")
