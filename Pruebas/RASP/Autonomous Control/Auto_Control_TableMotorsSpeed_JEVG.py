import time
import threading
from gpiozero import Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory

# Configuración de los pines
Device.pin_factory = LGPIOFactory()

# Clase para controlar los motores
class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None
        self.delay = 0.001  # Valor por defecto del delay

    def move(self, direction):
        self.DIR.value = direction
        self.ENA.on()
        while self.running:
            self.PUL.on()
            time.sleep(self.delay)
            self.PUL.off()
            time.sleep(self.delay)
        self.ENA.off()

    def start_moving(self, direction):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction,))
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

def test_motor_speed_change():
    # Iniciar los motores en la misma dirección (True para adelante)
    motor1.start_moving(True)
    motor2.start_moving(True)
    motor3.start_moving(True)
    motor4.start_moving(True)

    # Incrementar el valor de 0.0001 a 0.001 para motor1 y motor3
    # Decrementar el valor de 0.001 a 0.0001 para motor2 y motor4
    for i in range(100):
        delay1_3 = 0.0001 + (i * 0.000009)  # Incremento para motor1 y motor3
        delay2_4 = 0.001 - (i * 0.000009)   # Decremento para motor2 y motor4

        motor1.set_speed(delay1_3)
        motor2.set_speed(delay2_4)
        motor3.set_speed(delay1_3)
        motor4.set_speed(delay2_4)

        print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
        time.sleep(0.1)

    # Detener todos los motores
    motor1.stop_moving()
    motor2.stop_moving()
    motor3.stop_moving()
    motor4.stop_moving()

# Ejecutar la prueba
test_motor_speed_change()
