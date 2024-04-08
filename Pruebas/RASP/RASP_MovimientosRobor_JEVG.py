from gpiozero import OutputDevice
from time import sleep
import threading

# Define una clase para controlar cada motor
class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)

    def move(self, steps, direction, delay):
        def movement_sequence():
            self.ENA.on()
            self.DIR.value = direction
            for _ in range(steps):
                self.PUL.on()
                sleep(delay)
                self.PUL.off()
                sleep(delay)
            self.ENA.off()

        # Ejecutar la secuencia de movimiento en un hilo
        thread = threading.Thread(target=movement_sequence)
        thread.start()
        return thread  # Devolver el hilo para poder esperar a que termine

# Instancia cada motor con sus respectivos pines
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

# Configuraciones de movimiento
duration = 10000  # Número de pasos para cada dirección
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor

def move_all_at_once(movements):
    # Iniciar todos los movimientos al mismo tiempo
    threads = []
    for move in movements:
        thread = threading.Thread(target=move[0].move, args=(duration, move[1], delay))
        thread.start()
        threads.append(thread)

    # Esperar a que todos los movimientos terminen
    for thread in threads:
        thread.join()

def move_forward():
    print("Moviendo hacia adelante")
    movements = [
        (motor1, True),
        (motor2, False),
        (motor3, True),
        (motor4, False),
    ]
    move_all_at_once(movements)

def move_backward():
    print("Moviendo hacia atrás")
    movements = [
        (motor1, False),
        (motor2, True),
        (motor3, False),
        (motor4, True),
    ]
    move_all_at_once(movements)

def move_left():
    print("Girando hacia la izquierda")
    movements = [
        (motor1, False),
        (motor2, True),
        (motor3, True),
        (motor4, False),
    ]
    move_all_at_once(movements)

def move_right():
    print("Girando hacia la derecha")
    movements = [
        (motor1, True),
        (motor2, False),
        (motor3, False),
        (motor4, True),
    ]
    move_all_at_once(movements)

def rotate_right():
    print("Rotando hacia la derecha")
    movements = [
        (motor1, True),
        (motor2, True),
        (motor3, True),
        (motor4, True),
    ]
    move_all_at_once(movements)

def rotate_left():
    print("Rotando hacia la izquierda")
    movements = [
        (motor1, False),
        (motor2, False),
        (motor3, False),
        (motor4, False),
    ]
    move_all_at_once(movements)

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
