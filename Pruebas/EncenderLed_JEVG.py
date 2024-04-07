import RPi.GPIO as GPIO
import time

# Configura el modo de numeración de pines a BCM
GPIO.setmode(GPIO.BCM)

# Configura el pin 17 como salida
GPIO.setup(17, GPIO.OUT)

# Enciende el LED
GPIO.output(17, GPIO.HIGH)

# Espera 5 segundos
time.sleep(5)

# Apaga el LED
GPIO.output(17, GPIO.LOW)

# Limpia la configuración de los pines
GPIO.cleanup()