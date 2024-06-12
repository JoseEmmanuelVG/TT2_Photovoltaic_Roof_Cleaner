
import time
import subprocess
from gpiozero import LED

# Configura el LED en el pin GPIO 4
led = LED(4)

def is_wifi_connected():
    """
    Verifica si hay una conexión WiFi activa.
    """
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        print("Salida de nmcli:", output)  # Imprime la salida de nmcli para depuración
        active_connections = output.split('\n')
        for connection in active_connections:
            print("Revisando conexión:", connection)  # Imprime cada línea para depuración
            if 'sí' in connection:
                return True
    except Exception as e:
        print(f"Error verificando la conexión WiFi: {e}")
    return False

def blink_led():
    """
    Hace parpadear el LED cuando hay conexión WiFi, y lo enciende continuamente cuando no hay conexión.
    """
    while True:
        if is_wifi_connected():
            print("WiFi está conectado, parpadeando LED")
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        else:
            print("WiFi no está conectado, encendiendo LED de manera continua")
            led.on()  # Enciende el LED cuando la conexión WiFi se pierde
            time.sleep(1)  # Añadimos una pequeña pausa para evitar el consumo excesivo de CPU

if __name__ == "__main__":
    print("Iniciando el script de monitoreo de WiFi")
    try:
        blink_led()
    except KeyboardInterrupt:
        print("El script de monitoreo de WiFi ha sido detenido")
        led.off()  # Apaga el LED cuando se detenga el script
