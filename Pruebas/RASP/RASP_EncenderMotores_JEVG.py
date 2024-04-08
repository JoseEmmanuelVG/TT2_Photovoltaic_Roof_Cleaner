from gpiozero import OutputDevice
from time import sleep

# Define los pines a utilizar usando gpiozero
PUL = OutputDevice(16)  # Stepper Drive Pulses
DIR = OutputDevice(20)  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change)
ENA = OutputDevice(21, initial_value=False)  # Controller Enable Bit (Low to Enable / HIGH to Disable)

durationFwd = 5000  # Duración del giro en una dirección
durationBwd = 5000  # Duración del giro en la dirección opuesta
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor
cycles = 1000  # Número de ciclos a ejecutar
cyclecount = 0  # Contador de ciclos

def forward():
    ENA.on()  # Habilita el controlador
    sleep(.5)  # Pausa por si hay cambio de dirección
    DIR.off()  # Establece dirección hacia adelante
    for x in range(durationFwd):
        PUL.toggle()  # Cambia el estado del pin PUL
        sleep(delay)
    ENA.off()  # Deshabilita el controlador
    sleep(.5)  # Pausa por si hay cambio de dirección

def reverse():
    ENA.on()  # Habilita el controlador
    sleep(.5)  # Pausa por si hay cambio de dirección
    DIR.on()  # Establece dirección hacia atrás
    for y in range(durationBwd):
        PUL.toggle()  # Cambia el estado del pin PUL
        sleep(delay)
    ENA.off()  # Deshabilita el controlador
    sleep(.5)  # Pausa por si hay cambio de dirección

print("Inicio del programa")
print("Ciclos a ejecutar: ", cycles)

while cyclecount < cycles:
    forward()
    reverse()
    cyclecount += 1
    print(f'Ciclos completados: {cyclecount}')

print('Ciclos completados')
