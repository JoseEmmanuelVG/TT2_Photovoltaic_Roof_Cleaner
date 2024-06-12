import serial
import time

# Inicializa el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Asegúrate de usar el puerto correcto

def leer_datos_serial():
    if ser.inWaiting() > 0:
        linea = ser.readline()
        datos = linea.decode('utf-8').strip().split(',')

        # Verifica si hay datos de temperatura y humedad
        if len(datos) == 6:  # 4 distancias + 2 datos DHT11
            return datos
        else:
            return None  # Si no hay datos DHT11, devuelve None
    else:
        return None

while True:
    datos = leer_datos_serial()
    if datos is not None:
        print(f"Delante izquierdo: {datos[0]} cm")
        print(f"Delante derecho: {datos[1]} cm")
        print(f"Atrás izquierda: {datos[2]} cm")
        print(f"Atrás derecha: {datos[3]} cm")
        print(f"Humedad: {datos[4]} %")
        print(f"Temperatura: {datos[5]} *C")

    time.sleep(0.1)  # Espera un poco antes de leer de nuevo
