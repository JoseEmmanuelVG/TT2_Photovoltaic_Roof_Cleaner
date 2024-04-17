from gpiozero import Device, LED
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero.exc import GPIOPinInUse
from gpiozero import OutputDevice
from time import sleep
import gpiozero

Device.pin_factory = LGPIOFactory()

def reset_all_pins():
    for pin in Device.pin_factory.pins.values():
        pin.close()

reset_all_pins()  # Llama a esta función al inicio para asegurarte de que todos los pines están libres


# Prueba Motores Paso a Paso
import threading
class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None

    def move(self, direction, delay=0.01):
        self.DIR.value = direction
        self.ENA.on()
        while self.running:
            self.PUL.on()
            time.sleep(delay)
            self.PUL.off()
            time.sleep(delay)
        self.ENA.off()

    def start_moving(self, direction, delay=0.01):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, delay))
            self.thread.start()

    def stop_moving(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()


            current_movement = None

def handle_movement(action):
    global current_movement

    movements = {
        'forward': (True, False, True, False),
        'backward': (False, True, False, True),
        'left': (False, False, True, True),
        'right': (True, True, False, False),
        'rotate_right': (True, True, True, True),
        'rotate_left': (False, False, False, False),
    }

    if action == current_movement:
        # Detener todos los motores si se presiona el mismo botón de nuevo
        motor1.stop_moving()
        motor2.stop_moving()
        motor3.stop_moving()
        motor4.stop_moving()
        current_movement = None
    else:
        # Detener todos los motores antes de iniciar un nuevo movimiento
        motor1.stop_moving()
        motor2.stop_moving()
        motor3.stop_moving()
        motor4.stop_moving()

        # Iniciar el nuevo movimiento
        direction = movements.get(action)
        if direction:
            motor1.start_moving(direction[0])
            motor2.start_moving(direction[1])
            motor3.start_moving(direction[2])
            motor4.start_moving(direction[3])
            current_movement = action
