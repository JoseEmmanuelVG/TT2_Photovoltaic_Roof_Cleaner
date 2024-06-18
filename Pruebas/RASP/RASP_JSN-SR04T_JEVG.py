#!/usr/bin/python
# encoding:utf-8

from gpiozero import DistanceSensor
import time

# Define los pines para los sensores de distancia
sensor1 = DistanceSensor(echo=4, trigger=18, max_distance=4, threshold_distance=0.05)
sensor2 = DistanceSensor(echo=12, trigger=13, max_distance=4, threshold_distance=0.05)

def calibrate_distance(distance):
    """
    Ajustar la calibración si es necesario
    """
    return round(distance * 100 - 0.5, 2)  # Convertir la distancia de metros a centímetros y ajustar

print("Distance measurement in progress")

while True:
    time.sleep(1)  # Reducir el tiempo de espera para mediciones más frecuentes

    distance1 = sensor1.distance  # Medir la distancia en metros del sensor 1
    distance2 = sensor2.distance  # Medir la distancia en metros del sensor 2

    calibrated_distance1 = calibrate_distance(distance1)
    calibrated_distance2 = calibrate_distance(distance2)
    
    print(f"Sensor 1 Distance: {calibrated_distance1} cm")
    print(f"Sensor 2 Distance: {calibrated_distance2} cm")
