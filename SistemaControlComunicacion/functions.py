from gpiozero import Device, OutputDevice, LED
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero.exc import GPIOPinInUse
import threading
import time

Device.pin_factory = LGPIOFactory()

class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None

    def move(self, direction, delay=0.0001):
        self.DIR.value = direction
        self.ENA.on()
        while self.running:
            self.PUL.on()
            time.sleep(delay)
            self.PUL.off()
            time.sleep(delay)
        self.ENA.off()

    def start_moving(self, direction, delay=0.0001):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, delay))
            self.thread.start()

    def stop_moving(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()


# Instanciar los motores una sola vez
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)


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
        motor1.stop_moving()
        motor2.stop_moving()
        motor3.stop_moving()
        motor4.stop_moving()
        current_movement = None
    else:
        motor1.stop_moving()
        motor2.stop_moving()
        motor3.stop_moving()
        motor4.stop_moving()
        direction = movements.get(action)
        if direction:
            motor1.start_moving(direction[0])
            motor2.start_moving(direction[1])
            motor3.start_moving(direction[2])
            motor4.start_moving(direction[3])
            current_movement = action


def emergency_stop():
    motor1.stop_moving()
    motor2.stop_moving()
    motor3.stop_moving()
    motor4.stop_moving()
    global current_movement
    current_movement = None  # Resetear el estado de movimiento actual
    print("Emergencia: Todos los motores se han detenido.")
