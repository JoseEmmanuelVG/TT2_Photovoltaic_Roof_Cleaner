from gpiozero import PWMOutputDevice, OutputDevice
from time import sleep

# Definir los pines de conexión
pinPWM = 15    # Puerto de control de velocidad (PWM)
pinDireccion = 14  # Control de avance y retroceso

# Configurar los pines
pwm = PWMOutputDevice(pinPWM)
direccion = OutputDevice(pinDireccion)

# Establecer la dirección inicial del motor
direccion.off()  # Baja para avance (CW), Alta para retroceso (CCW)

while True:
    # Establecer la velocidad del motor
    # Puedes cambiar el valor '0.5' con cualquier valor entre 0 (motor parado) y 1 (velocidad máxima)
    pwm.value = 0.5

    # Cambiar la dirección después de un tiempo
    sleep(5)  # El motor gira en una dirección por 5 segundos
    direccion.on()  # Cambiar la dirección de rotación
    sleep(5)  # El motor gira en la dirección opuesta por 5 segundos
    direccion.off()  # Volver a la dirección original
