from gpiozero import Device, LED
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero.exc import GPIOPinInUse
from gpiozero import OutputDevice
from time import sleep


Device.pin_factory = LGPIOFactory()

led_pin = 4  # Asegúrate de que este pin no se use en otro lugar simultáneamente

try:
    with LED(led_pin) as led:
        led.on()
        sleep(1)
        led.off()
except GPIOPinInUse:
    print(f"GPIO {led_pin} está actualmente en uso. Intentando liberar y reasignar...")
    # Aquí el manejo adecuado depende de tu lógica de aplicación específica



def test_led():
    try:
        led = LED(4)  # Intenta configurar el LED
        led.on()
        sleep(1)
        led.off()
    except GPIOPinInUse:
        print("GPIO 4 está actualmente en uso. Intentando liberar...")
    finally:
        if 'led' in locals():  # Verifica si 'led' fue exitosamente definido
            led.close()  # Cierra y libera el pin





# Prueba Motores Paso a Paso
from gpiozero.exc import GPIOPinInUse
from time import sleep
import threading

class StepperMotor:
    """
    Clase para controlar un motor paso a paso.
    """

    def __init__(self, pul_pin, dir_pin, ena_pin):
        """
        Inicializa un objeto StepperMotor con los pines de control del motor.

        Args:
            pul_pin (int): Número del pin para el pulso.
            dir_pin (int): Número del pin para la dirección.
            ena_pin (int): Número del pin para la habilitación.
        """
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)

    def move(self, steps, direction, delay):
        """
        Mueve el motor una cantidad específica de pasos en una dirección y con un retardo entre pulsos.

        Args:
            steps (int): Número de pasos a mover el motor.
            direction (bool): Dirección del movimiento (True para adelante, False para atrás).
            delay (float): Retardo entre pulsos en segundos.
        """
        def movement_sequence():
            self.ENA.on()
            self.DIR.value = direction
            for _ in range(steps):
                self.PUL.on()
                sleep(delay)
                self.PUL.off()
                sleep(delay)
            self.ENA.off()

        thread = threading.Thread(target=movement_sequence)
        thread.start()
        return thread

# Instancia cada motor con sus respectivos pines
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

duration = 10000  # Número de pasos para cada dirección
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor

def move_all_at_once(movements):
    """
    Mueve todos los motores al mismo tiempo.

    Args:
        movements (list): Lista de tuplas (motor, direction) con los movimientos a realizar.
    """
    threads = []
    for move in movements:
        thread = threading.Thread(target=move[0].move, args=(duration, move[1], delay))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def move_forward():
    """
    Mueve todos los motores hacia adelante.
    """
    print("Moviendo hacia adelante")
    movements = [
        (motor1, True),
        (motor2, False),
        (motor3, True),
        (motor4, False),
    ]
    move_all_at_once(movements)

def move_backward():
    """
    Mueve todos los motores hacia atrás.
    """
    print("Moviendo hacia atrás")
    movements = [
        (motor1, False),
        (motor2, True),
        (motor3, False),
        (motor4, True),
    ]
    move_all_at_once(movements)

def move_left():
    """
    Gira todos los motores hacia la izquierda.
    """
    print("Girando hacia la izquierda")
    movements = [
        (motor1, False),
        (motor2, False),
        (motor3, True),
        (motor4, True),
    ]
    move_all_at_once(movements)

def move_right():
    """
    Gira todos los motores hacia la derecha.
    """
    print("Girando hacia la derecha")
    movements = [
        (motor1, True),
        (motor2, True),
        (motor3, False),
        (motor4, False),
    ]
    move_all_at_once(movements)

def rotate_right():
    """
    Mueve todos los motores hacia la derecha.
    """
    print("Moviendo hacia la derecha")
    movements = [
        (motor1, True),
        (motor2, True),
        (motor3, True),
        (motor4, True),
    ]
    move_all_at_once(movements)

def rotate_left():
    """
    Mueve todos los motores hacia la izquierda.
    """
    print("Moviendo hacia la izquierda")
    movements = [
        (motor1, False),
        (motor2, False),
        (motor3, False),
        (motor4, False),
    ]
    move_all_at_once(movements)

