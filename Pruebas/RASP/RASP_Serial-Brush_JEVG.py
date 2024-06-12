import serial
from time import sleep

# Ajusta el puerto serial según corresponda en tu Raspberry Pi
serial_port = serial.Serial('/dev/ttyUSB0', 9600)

def activar_motor(direccion):
    if direccion == "adelante":
        serial_port.write(b'A')  # Enviar 'A' para activar adelante
    elif direccion == "atras":
        serial_port.write(b'R')  # Enviar 'R' para activar atrás

def desactivar_motor():
    serial_port.write(b'D')  # Enviar 'D' para desactivar

while True:
    command = input("Ingresa un comando (A: adelante, R: atrás, D: detener, S: salir): ")

    if command == 'A':
        activar_motor("adelante")
    elif command == 'R':
        activar_motor("atras")
    elif command == 'D':
        desactivar_motor()
    elif command == 'S':
        break  # Salir del bucle
    else:
        print("Comando inválido. Intenta de nuevo.")

serial_port.close()  # Cerrar el puerto serial al salir
