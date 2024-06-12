import time
import psutil
from gpiozero import LED

# Configura el LED en el pin GPIO 4
led = LED(4)

def is_vnc_connected():
    """
    Verifica si el proceso VNC tiene conexiones activas.
    """
    vnc_connected = False
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        if 'vnc' in proc.info['name'].lower() and 'vncserverui' in proc.info['name'].lower():
            try:
                for conn in proc.connections(kind='inet'):
                    print(f"Conexión encontrada en el proceso {proc.info['pid']} ({proc.info['name']}): {conn}")
                    if conn.status == 'ESTABLISHED':
                        print(f"Conexión VNC activa encontrada: {conn}")
                        vnc_connected = True
            except psutil.AccessDenied:
                print(f"Acceso denegado al proceso {proc.info['pid']} ({proc.info['name']})")
    return vnc_connected

def blink_led():
    """
    Hace parpadear el LED.
    """
    while True:
        if is_vnc_connected():
            print("VNC está conectado, parpadeando LED")
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        else:
            print("VNC no está conectado, encendiendo LED de manera continua")
            led.on()  # Enciende el LED cuando la conexión VNC se pierde
            time.sleep(1)  # Añadimos una pequeña pausa para evitar el consumo excesivo de CPU

if __name__ == "__main__":
    print("Iniciando el script de monitoreo VNC")
    try:
        blink_led()
    except KeyboardInterrupt:
        print("El script de monitoreo VNC ha sido detenido")
        led.off()  # Apaga el LED cuando se detenga el script
