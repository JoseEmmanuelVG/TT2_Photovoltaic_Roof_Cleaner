import serial
import time
from gpiozero import Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
import threading
import os
import base64
import subprocess

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

def handle_movement(action, pwm_value=50):
    if action == 'forward':
        enviar_comando(f"A_{pwm_value}")
    elif action == 'backward':
        enviar_comando(f"R_{pwm_value}")
    elif action == 'stop':
        enviar_comando("D")

def emergency_stop():
    enviar_comando("D")

def control_new_motor(action, pwm_value):
    if action == 'start_forward':
        enviar_comando(f"A_{pwm_value}")
    elif action == 'start_reverse':
        enviar_comando(f"R_{pwm_value}")
    elif action == 'stop':
        enviar_comando("D")

# Motores desplazamiento 
Device.pin_factory = LGPIOFactory()

class StepperMotor:
    def __init__(self, pul_pin, dir_pin, ena_pin):
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.running = False
        self.thread = None

    def move(self, direction, delay=0.0001):
        self.DIR.value = direction
        self.ENA.on()
        while self.running:
            self.PUL.on()
            time.sleep(delay)
            self.PUL.off()
            time.sleep(delay)
        if not self.running:
            self.ENA.off()

    def start_moving(self, direction, delay=0.0001):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.move, args=(direction, delay))
            self.thread.start()

    def stop_moving(self, hold=False):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        if hold:
            self.ENA.on()
        else:
            self.ENA.off()

motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

current_movement = None

def handle_movement(action, hold=False):
    global current_movement
    movements = {
        'forward': (True, False, True, False),
        'backward': (False, True, False, True),
        'left': (False, False, True, True),
        'right': (True, True, False, False),
        'rotate_right': (True, True, True, True),
        'rotate_left': (False, False, False, False),
    }

    if action == current_movement:
        stop_all_motors(hold=True)  # Stops all motors but holds the torque
        current_movement = None
    else:
        stop_all_motors(hold=True)  # Ensure motors are held with torque when stopped
        direction = movements.get(action)
        if direction:
            motor1.start_moving(direction[0])
            motor2.start_moving(direction[1])
            motor3.start_moving(direction[2])
            motor4.start_moving(direction[3])
            current_movement = action

def stop_all_motors(hold=False):
    motor1.stop_moving(hold)
    motor2.stop_moving(hold)
    motor3.stop_moving(hold)
    motor4.stop_moving(hold)

def emergency_stop():
    stop_all_motors(hold=True)
    global current_movement
    current_movement = None  # Resets the current movement state
    print("Emergency: All motors have been stopped.")

stop_all_motors(hold=True)

# Cámara
import os
import base64
import subprocess

# Directorio de almacenamiento de imágenes
IMAGE_DIR = '/home/ttm/TT2_Photovoltaic_Roof_Cleaner/SistemaControlComunicacion/assets'

def save_image(image_data, prefix, index):
    # Asegúrate de que el directorio de imágenes existe
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








# CONEXION WIFI
import time
import subprocess


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

