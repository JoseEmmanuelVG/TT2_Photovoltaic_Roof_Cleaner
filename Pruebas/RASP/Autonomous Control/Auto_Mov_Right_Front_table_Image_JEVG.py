import time
import threading
import serial
import math
import os
import base64
import subprocess
from gpiozero import Device, OutputDevice, DistanceSensor
from gpiozero.pins.lgpio import LGPIOFactory
import matplotlib.pyplot as plt

# Configuración de los pines
Device.pin_factory = LGPIOFactory()

# Directorio de almacenamiento de imágenes
IMAGE_DIR = '/home/ttm/TT2_Photovoltaic_Roof_Cleaner/Pruebas/RASP/Autonomous Control/assets'

def save_image(image_data, prefix, index):
    # Asegúrate de que el directorio de imágenes exista
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    file_name = f"{prefix}_{index}.jpg"
    file_path = os.path.join(IMAGE_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image_data.split(",")[1]))
    print(f"Image saved to {file_path}")  # Línea de depuración
    return file_name

def capture_image(image_name):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    file_path = os.path.join(IMAGE_DIR, image_name)
    subprocess.run(['libcamera-still', '-o', file_path])
    with open(file_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded_image}"

# Clase para controlar los motores
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

    def start_moving(self, direction, steps):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, steps))
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

image_index = 0

def control_robot():
    global image_index

    while True:
        datos = leer_datos_serial()
        if datos:
            front_left = float(datos[0])
            front_right = float(datos[1])
            rear_left = float(datos[2])
            rear_right = float(datos[3])
            middle_left = sensor_distances[0]
            middle_right = sensor_distances[1]

            # Almacenar los datos de los sensores
            sensor_data.append([front_left, front_right, middle_left, middle_right, rear_left, rear_right])

            # Imprimir los valores de los sensores en la consola
            print(f"Delante izquierda: {front_left} cm     ---    Delante derecha: {front_right} cm")
            print(f"Medio izquierda: {middle_left} cm     ---    Medio derecha: {middle_right} cm")
            print(f"Atrás izquierda: {rear_left} cm     ---    Atrás derecha: {rear_right} cm")
            print("")

            # Condición para detener el movimiento
            if (front_left > 30 and front_right > 30) or (rear_left > 30 and rear_right > 30):
                stop_all_motors()
                continue

            # Función para mover los motores
            def move_all_motors(direction, steps):
                global image_index
                motor1.start_moving(direction, steps)
                motor2.start_moving(not direction, steps)
                motor3.start_moving(direction, steps)
                motor4.start_moving(not direction, steps)
                motor1.thread.join()  # Espera a que motor1 complete su movimiento
                stop_all_motors()
                time.sleep(4)  # Pausa de 4 segundos
                image_name = f"image_{image_index}.jpg"
                capture_image(image_name)
                print(f"Image captured: {image_name}")
                image_index += 1

            ####### Aplicar PID para corregir la dirección si el robot se va a la izquierda #######
            if (middle_right < 10) and (front_right < 30 and rear_right < 30):
                correction = pid_left.compute(10, middle_right)
                for i in range(10):
                    delay1_3 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor1 y motor3
                    delay2_4 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor2 y motor4

                    motor1.set_speed(delay1_3)
                    motor2.set_speed(delay2_4)
                    motor3.set_speed(delay1_3)
                    motor4.set_speed(delay2_4)

                    print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                    time.sleep(0.1)
                
                move_all_motors(True, 6000)
                print(f"PID Correction Left: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

            # Rectificar ruedas
            elif (middle_right > 10) and (front_right > 30 and rear_right < 30):
                correction = pid_right.compute(10, middle_right)
                for i in range(10):
                    delay1_3 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor1 y motor3
                    delay2_4 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor2 y motor4

                    motor1.set_speed(delay1_3)
                    motor2.set_speed(delay2_4)
                    motor3.set_speed(delay1_3)
                    motor4.set_speed(delay2_4)

                    print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                    time.sleep(0.1)
                
                move_all_motors(True, 6000)
                print(f"PID Correction Right: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

            ####### Aplicar PID para corregir la dirección si el robot se va a la derecha #######
            elif (middle_right > 10) and (front_right > 30 and rear_right > 30):
                correction = pid_right.compute(10, middle_right)
                for i in range(10):
                    delay1_3 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor1 y motor3
                    delay2_4 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor2 y motor4

                    motor1.set_speed(delay1_3)
                    motor2.set_speed(delay2_4)
                    motor3.set_speed(delay1_3)
                    motor4.set_speed(delay2_4)

                    print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                    time.sleep(0.1)
                
                move_all_motors(True, 6000)
                print(f"PID Correction Right: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

            # Aplicar PID para corregir la dirección si el robot se va a la izquierda
            elif (middle_right > 10) and (front_right < 30 and rear_right > 30):
                correction = pid_left.compute(10, middle_right)
                for i in range(10):
                    delay1_3 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor1 y motor3
                    delay2_4 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor2 y motor4

                    motor1.set_speed(delay1_3)
                    motor2.set_speed(delay2_4)
                    motor3.set_speed(delay1_3)
                    motor4.set_speed(delay2_4)

                    print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                    time.sleep(0.1)
                
                move_all_motors(True, 6000)
                print(f"PID Correction Left: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")
            
            else:
                move_all_motors(True, 6000)
            
            time.sleep(1)  # Pausar entre movimientos de 30 cm

control_thread = threading.Thread(target=control_robot)
control_thread.daemon = True
control_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    emergency_stop()
    # Graficar las señales de los sensores
    sensor_data = list(zip(*sensor_data))  # Transponer la lista para obtener los datos por sensor
    time_steps = range(len(sensor_data[0]))  # Crear una lista de pasos de tiempo

    plt.figure(figsize=(12, 8))
    plt.subplot(3, 2, 1)
    plt.plot(time_steps, sensor_data[0])
    plt.title('Delante izquierda')

    plt.subplot(3, 2, 2)
    plt.plot(time_steps, sensor_data[1])
    plt.title('Delante derecha')

    plt.subplot(3, 2, 3)
    plt.plot(time_steps, sensor_data[2])
    plt.title('Medio izquierda')

    plt.subplot(3, 2, 4)
    plt.plot(time_steps, sensor_data[3])
    plt.title('Medio derecha')

    plt.subplot(3, 2, 5)
    plt.plot(time_steps, sensor_data[4])
    plt.title('Atrás izquierda')

    plt.subplot(3, 2, 6)
    plt.plot(time_steps, sensor_data[5])
    plt.title('Atrás derecha')

    plt.tight_layout()
    plt.savefig("sensor_data_plot.png")  # Guarda la gráfica en el mismo directorio
    plt.close()  # Cierra la gráfica
