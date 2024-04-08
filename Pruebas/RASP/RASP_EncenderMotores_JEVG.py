from gpiozero import OutputDevice
from time import sleep

# Define los pines a utilizar usando gpiozero
PUL = OutputDevice(17)  # Pin para la señal de pulso
DIR = OutputDevice(27)  # Pin para la dirección
EN = OutputDevice(22, initial_value=True)  # Pin para habilitar el motor, inicialmente desactivado

def motor_steps(steps, direction):
    DIR.value = direction  # Establece la dirección
    for i in range(steps):
        PUL.on()
        sleep(0.0004)  # Espera 400 microsegundos
        PUL.off()
        sleep(0.0004)  # Espera 400 microsegundos

try:
    # Habilita el motor
    EN.off()
    
    while True:  # Bucle infinito para repetir los movimientos
        # Mueve el motor hacia adelante 1600 pasos
        motor_steps(1600, False)
        
        # Pausa entre la inversión de dirección
        sleep(0.1)
        
        # Mueve el motor hacia atrás 1600 pasos
        motor_steps(1600, True)
        
        # Pausa antes de repetir el ciclo
        sleep(0.1)

except KeyboardInterrupt:
    # Si el usuario interrumpe la ejecución (Ctrl+C), detiene el motor
    EN.on()
