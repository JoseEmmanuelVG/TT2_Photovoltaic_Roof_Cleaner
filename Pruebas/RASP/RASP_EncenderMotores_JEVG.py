import RPi.GPIO as GPIO
import time

# Configura el modo de los pines
GPIO.setmode(GPIO.BCM)

# Define los pines a utilizar
PUL = 17  # Pin para la señal de pulso
DIR = 27  # Pin para la dirección
EN = 22   # Pin para habilitar el motor

# Configura los pines como salida
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Deshabilita el motor para comenzar
GPIO.output(EN, GPIO.HIGH)

def motor_steps(steps, direction):
    GPIO.output(DIR, direction)  # Establece la dirección
    for i in range(steps):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(0.0004)  # Espera 400 microsegundos
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(0.0004)  # Espera 400 microsegundos

try:
    # Habilita el motor
    GPIO.output(EN, GPIO.LOW)
    
    # Mueve el motor hacia adelante 1600 pasos
    motor_steps(1600, GPIO.LOW)
    
    # Pausa entre la inversión de dirección
    time.sleep(0.1)
    
    # Mueve el motor hacia atrás 1600 pasos
    motor_steps(1600, GPIO.HIGH)
    
finally:
    # Limpia los pines GPIO y deshabilita el motor al finalizar
    GPIO.cleanup()
