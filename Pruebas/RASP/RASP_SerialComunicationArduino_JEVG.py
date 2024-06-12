import serial
import time

# Inicializa el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Asegúrate de usar el puerto correcto

def leer_datos_serial():
    if ser.inWaiting() > 0:
        linea = ser.readline().decode('utf-8').strip()
        datos = linea.split(',')

        # Verifica si hay datos de sensores
        if len(datos) == 6:  # 4 distancias + 2 datos DHT11
            return datos
        else:
            return None
    else:
        return None

def enviar_comando(comando):
    ser.write(f"{comando}\n".encode('utf-8'))

while True:
    datos = leer_datos_serial()
    if datos is not None:
        print(f"Delante izquierdo: {datos[0]} cm")
        print(f"Delante derecho: {datos[1]} cm")
        print(f"Atrás izquierda: {datos[2]} cm")
        print(f"Atrás derecha: {datos[3]} cm")
        print(f"Humedad: {datos[4]} %")
        print(f"Temperatura: {datos[5]} *C")

    command = input("Ingresa un comando (A_xx: adelante xx% PWM, R_xx: atrás xx% PWM, D: detener, S: salir): ")

    if command.startswith('A_') or command.startswith('R_') or command == 'D':
        enviar_comando(command)
    elif command == 'S':
        break  # Salir del bucle
    else:
        print("Comando inválido. Intenta de nuevo.")

ser.close()  # Cerrar el puerto serial al salir
