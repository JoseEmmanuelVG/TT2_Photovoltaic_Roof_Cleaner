#!/usr/bin/python
# encoding:utf-8

from gpiozero import DistanceSensor
import time

# Define los pines para el sensor de distancia
sensor = DistanceSensor(echo=14, trigger=15)

print("Distance measurement in progress")

while True:
    time.sleep(2)  # Espera para que el sensor se estabilice
    distance = sensor.distance * 100  # Convertir la distancia de metros a centímetros
    distance = round(distance, 2)     # Redondear a dos decimales

    if 20 < distance < 400:  # Comprobar si la distancia está dentro del rango deseado
        print(f"Distance: {distance - 0.5} cm")  # Ajustar la calibración si es necesario
    else:
        print("Out Of Range")
