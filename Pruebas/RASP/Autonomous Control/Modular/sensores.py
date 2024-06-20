
import threading
import serial
import math
from gpiozero import Device, OutputDevice, DistanceSensor
import time

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
    

def start_sensor_thread():
    sensor_thread = threading.Thread(target=read_sensors)
    sensor_thread.daemon = True
    sensor_thread.start()