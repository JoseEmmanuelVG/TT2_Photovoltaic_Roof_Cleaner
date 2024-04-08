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


def move_forward():
    print("Moviendo hacia adelante")
    motor1.move(duration, True, delay)  # Llanta frontal izquierda hacia adelante
    motor2.move(duration, False, delay)  # Llanta frontal derecha hacia adelante
    motor3.move(duration, True, delay)  # Llanta trasera izquierda hacia adelante
    motor4.move(duration, False, delay)  # Llanta trasera derecha hacia adelante

def move_backward():
    print("Moviendo hacia atrás")
    motor1.move(duration, False, delay)  # Llanta frontal izquierda hacia atrás
    motor2.move(duration, True, delay)  # Llanta frontal derecha hacia atrás
    motor3.move(duration, False, delay)  # Llanta trasera izquierda hacia atrás
    motor4.move(duration, True, delay)  # Llanta trasera derecha hacia atrás

def move_left():
    print("Girando hacia la izquierda")
    motor1.move(duration, False, delay)  # Llanta frontal izquierda hacia atrás
    motor2.move(duration, True, delay)  # Llanta frontal derecha hacia adelante
    motor3.move(duration, True, delay)  # Llanta trasera izquierda hacia adelante
    motor4.move(duration, False, delay)  # Llanta trasera derecha hacia atrás

def move_right():
    print("Girando hacia la derecha")
    motor1.move(duration, True, delay)  # Llanta frontal izquierda hacia adelante
    motor2.move(duration, False, delay)  # Llanta frontal derecha hacia atrás
    motor3.move(duration, False, delay)  # Llanta trasera izquierda hacia atrás
    motor4.move(duration, True, delay)  # Llanta trasera derecha hacia adelante

def rotate_right():
    print("Rotando hacia la derecha")
    motor1.move(duration, True, delay)  # Llantas lado izquierdo hacia adelante
    motor3.move(duration, True, delay)
    motor2.move(duration, True, delay)  # Llantas lado derecho hacia atrás
    motor4.move(duration, True, delay)

def rotate_left():
    print("Rotando hacia la izquierda")
    motor1.move(duration, False, delay)  # Llantas lado izquierdo hacia atrás
    motor3.move(duration, False, delay)
    motor2.move(duration, False, delay)  # Llantas lado derecho hacia adelante
    motor4.move(duration, False, delay)

# Ejecuta cada movimiento
print("Inicio del programa")
move_forward()
sleep(2)  # Espera 2 segundos entre movimientos
move_backward()
sleep(2)
move_left()
sleep(2)
move_right()
sleep(2)
rotate_right()
sleep(2)
rotate_left()
print('Movimientos completados')
