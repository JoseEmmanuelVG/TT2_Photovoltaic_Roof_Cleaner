import time
import threading
from gpiozero import Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory

# Configuración de los pines
Device.pin_factory = LGPIOFactory()

class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin, steps_per_revolution=6000):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None
        self.delay = 0.001  # Valor por defecto del delay
        self.steps_per_revolution = steps_per_revolution

    def move(self, direction, steps):
        self.DIR.value = direction
        self.ENA.on()
        for _ in range(steps):
            if not self.running:
                break
            self.PUL.on()
            time.sleep(self.delay)
            self.PUL.off()
            time.sleep(self.delay)
        self.ENA.off()
        self.running = False  # Asegurar que el estado 'running' se restablezca

    def start_moving(self, direction):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, self.steps_per_revolution))
            self.thread.start()

    def stop_moving(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        self.ENA.off()

    def set_speed(self, delay):
        self.delay = delay

# Inicialización de los motores
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

def stop_all_motors():
    motor1.stop_moving()
    motor2.stop_moving()
    motor3.stop_moving()
    motor4.stop_moving()

def emergency_stop():
    stop_all_motors()
    print("Emergency: All motors have been stopped.")
