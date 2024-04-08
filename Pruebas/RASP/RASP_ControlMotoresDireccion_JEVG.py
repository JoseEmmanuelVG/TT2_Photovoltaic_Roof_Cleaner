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
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

# Configuraciones de movimiento
duration = 10000  # Número de pasos para cada dirección
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor

print("Inicio del programa")

# Mover todos los motores hacia adelante y hacia atrás
def move_motors():
    # Mover hacia adelante
    # Llantas lado izquiero
    motor1.move(duration, True, delay) # Llanta frontal izquierda
    motor3.move(duration, True, delay) # Llanta trasera izquiera
    # Llatas lado derecho
    motor2.move(duration, False, delay) # Llanta frontal derecha
    motor4.move(duration, False, delay) # Llanta trasera derecha
    
    sleep(2)  # Pausa entre cambios de dirección

    # Mover hacia atrás
    # Llantas lado izquiero
    motor1.move(duration, False, delay) # Llanta frontal izquierda
    motor3.move(duration, False, delay) # Llanta trasera izquiera
    # Llatas lado derecho
    motor2.move(duration, True, delay) # Llanta frontal derecha
    motor4.move(duration, True, delay) # Llanta trasera derecha 

move_motors()

print('Movimiento de motores completado')
