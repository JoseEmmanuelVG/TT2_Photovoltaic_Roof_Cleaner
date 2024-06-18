import time
import threading
import serial
import matplotlib.pyplot as plt
from gpiozero import Device, OutputDevice, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

# Configuración de los pines
Device.pin_factory = PiGPIOFactory()

# Clase para controlar los motores
class StepperMotor:
    shared_delay = 0.0003  # Variable compartida para el delay

    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None

    def move(self, direction):
        self.DIR.value = direction
        self.ENA.on()
        while self.running:
            self.PUL.on()
            time.sleep(StepperMotor.shared_delay)
            self.PUL.off()
            time.sleep(StepperMotor.shared_delay)
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

# Sensores de distancia
sensor1 = DistanceSensor(echo=4, trigger=18, max_distance=4, threshold_distance=0.05)
sensor2 = DistanceSensor(echo=12, trigger=13, max_distance=4, threshold_distance=0.05)

# Contenedor mutable para las distancias de los sensores
sensor_distances = [0, 0]  # Index 0 for sensor1, index 1 for sensor2
sensor_data = []

def calibrate_distance(distance):
    return round(distance * 100 - 0.5, 2)

def read_sensors():
    while True:
        try:
            sensor_distances[0] = calibrate_distance(sensor1.distance)
            sensor_distances[1] = calibrate_distance(sensor2.distance)
        except Exception as e:
            print(f"Error reading sensors: {e}")
        time.sleep(1)

sensor_thread = threading.Thread(target=read_sensors)
sensor_thread.daemon = True
sensor_thread.start()

# Inicializa el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

def leer_datos_serial():
    if ser.inWaiting() > 0:
        linea = ser.readline().decode('utf-8').strip()
        datos = linea.split(',')
        if len(datos) == 7:
            return datos
        else:
            return None
    else:
        return None

class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.previous_error = 0

    def compute(self, setpoint, measured_value):
        error = setpoint - measured_value
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

pid_left = PIDController(0.1, 0.01, 0.05)
pid_right = PIDController(0.1, 0.01, 0.05)

def control_robot():
    while True:
        datos = leer_datos_serial()
        if datos:
            front_left = float(datos[0])
            front_right = float(datos[1])
            rear_left = float(datos[2])
            rear_right = float(datos[3])

            # Almacenar los datos de los sensores
            sensor_data.append([front_left, front_right, sensor_distances[0], sensor_distances[1], rear_left, rear_right])

            # Imprimir los valores de los sensores en la consola
            print(f"Delante izquierda: {front_left} cm     ---    Delante derecha: {front_right} cm")
            print(f"Medio izquierda: {sensor_distances[0]} cm     ---    Medio derecha: {sensor_distances[1]} cm")
            print(f"Atrás izquierda: {rear_left} cm     ---    Atrás derecha: {rear_right} cm")
            print("")

            right_middle = sensor_distances[1]
            left_middle = sensor_distances[0]

            if right_middle > 10 and front_right < 30 and rear_right < 30:
                # El robot está siguiendo la línea
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)
            elif front_right > 30 and rear_right > 30:
                # El robot se está yendo hacia la derecha
                correction = pid_right.compute(10, right_middle)
                motor1.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor2.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor3.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor4.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                print(f"PID Correction Right: {correction}, Motor Delays: {motor1.shared_delay}, {motor2.shared_delay}, {motor3.shared_delay}, {motor4.shared_delay}")
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)
            elif right_middle < 10:
                # El robot se está yendo hacia la izquierda
                correction = pid_left.compute(10, right_middle)
                motor1.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor2.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor3.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor4.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                print(f"PID Correction Left: {correction}, Motor Delays: {motor1.shared_delay}, {motor2.shared_delay}, {motor3.shared_delay}, {motor4.shared_delay}")
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)
            elif left_middle > 10 and front_left < 30 and rear_left < 30:
                # El robot está siguiendo la línea
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)
            elif front_left > 30 and rear_left > 30:
                # El robot se está yendo hacia la izquierda
                correction = pid_left.compute(10, left_middle)
                motor1.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor2.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor3.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor4.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                print(f"PID Correction Left: {correction}, Motor Delays: {motor1.shared_delay}, {motor2.shared_delay}, {motor3.shared_delay}, {motor4.shared_delay}")
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)
            elif left_middle < 10:
                # El robot se está yendo hacia la derecha
                correction = pid_right.compute(10, left_middle)
                motor1.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor2.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                motor3.shared_delay = max(0.001, min(0.0001, 0.0005 - correction))
                motor4.shared_delay = max(0.001, min(0.0001, 0.0005 + correction))
                print(f"PID Correction Right: {correction}, Motor Delays: {motor1.shared_delay}, {motor2.shared_delay}, {motor3.shared_delay}, {motor4.shared_delay}")
                motor1.start_moving(True)
                motor2.start_moving(True)
                motor3.start_moving(True)
                motor4.start_moving(True)

        time.sleep(0.1)
