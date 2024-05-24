import serial
import time

# Inicializa el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Asegúrate de seleccionar el puerto correcto

def leer_datos_serial():
    if ser.inWaiting() > 0:
        linea = ser.readline()  # Lee una línea del puerto serial
        datos = linea.decode('utf-8').strip().split(',')  # Decodifica y divide los datos
        return datos
    else:
        return None

while True:
    datos = leer_datos_serial()
    if datos is not None:
        print(f"Delante izquierdo: {datos[0]} cm")
        print(f"Delante derecho: {datos[1]} cm")
        print(f"Atrás izquierda: {datos[2]} cm")
        print(f"Atrás derecha: {datos[3]} cm")
    time.sleep(0.1)  # Espera un poco antes de leer los datos de nuevo
