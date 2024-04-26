from gpiozero import Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
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
        if not self.running:
            self.ENA.off()

    def start_moving(self, direction, delay=0.0001):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, delay))
            self.thread.start()

    def stop_moving(self, hold=False):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        if hold:
            self.ENA.on()
        else:
            self.ENA.off()

motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

current_movement = None

def handle_movement(action, hold=False):
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
        stop_all_motors(hold=True)  # Stops all motors but holds the torque
        current_movement = None
    else:
        stop_all_motors(hold=True)  # Ensure motors are held with torque when stopped
        direction = movements.get(action)
        if direction:
            motor1.start_moving(direction[0])
            motor2.start_moving(direction[1])
            motor3.start_moving(direction[2])
            motor4.start_moving(direction[3])
            current_movement = action

def stop_all_motors(hold=False):
    motor1.stop_moving(hold)
    motor2.stop_moving(hold)
    motor3.stop_moving(hold)
    motor4.stop_moving(hold)

def emergency_stop():
    stop_all_motors(hold=True)
    global current_movement
    current_movement = None  # Resets the current movement state
    print("Emergency: All motors have been stopped.")

stop_all_motors(hold=True)
