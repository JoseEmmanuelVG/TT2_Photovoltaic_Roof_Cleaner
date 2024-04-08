from gpiozero import OutputDevice
from time import sleep

# Define una clase para controlar cada motor
class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)  # Asumimos que False habilita el motor

    def move(self, steps, direction, delay):
        self.ENA.on()  # Habilita el controlador
        self.DIR.value = direction
        for _ in range(steps):
            self.PUL.toggle()  # Cambia el estado del pin PUL
            sleep(delay)
        self.ENA.off()  # Deshabilita el controlador

# Instancia cada motor con sus respectivos pines
motor1 = StepperMotor(17, 27, 22)
motor2 = StepperMotor(23, 24, 25)
motor3 = StepperMotor(5, 6, 26)
motor4 = StepperMotor(16, 20, 21)

# Configuraciones de movimiento
duration = 10000  # Número de pasos para cada dirección
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor

print("Inicio del programa")

# Mover todos los motores hacia adelante y hacia atrás
def move_motors():
    # Mover hacia adelante
    motor1.move(duration, False, delay)
    motor2.move(duration, False, delay)
    motor3.move(duration, False, delay)
    motor4.move(duration, False, delay)
    
    sleep(0.5)  # Pausa entre cambios de dirección

    # Mover hacia atrás
    motor1.move(duration, True, delay)
    motor2.move(duration, True, delay)
    motor3.move(duration, True, delay)
    motor4.move(duration, True, delay)

move_motors()

print('Movimiento de motores completado')
