from gpiozero import LED
from time import sleep

# Reemplazar '17' con un número de pin que estés utilizando.
led = LED(4)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
