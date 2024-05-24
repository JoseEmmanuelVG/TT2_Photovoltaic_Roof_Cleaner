from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep

# Definir los pines de conexión
pinPWM = 15           # Puerto de control de velocidad (PWM)
pinDireccion = 14     # Control de avance y retroceso

# Configurar los dispositivos
motor_pwm = PWMOutputDevice(pinPWM, frequency=1000, initial_value=0.5)  # Inicializa el PWM al 50% (128 de 255 aprox.)
motor_dir = OutputDevice(pinDireccion, initial_value=False)  # Inicializa dirección en falso (avance)

try:
    while True:
        # Motor en una dirección a velocidad media
        motor_dir.off()  # Avance (CW)
        motor_pwm.value = 0.5  # Establecer PWM al 50% de ciclo de trabajo
        sleep(5)  # Esperar 5 segundos

        # Cambiar la dirección del motor
        motor_dir.on()  # Retroceso (CCW)
        sleep(5)  # Esperar 5 segundos

        # Volver a la dirección original
        motor_dir.off()  # Avance (CW)
        
except KeyboardInterrupt:
    # Asegurarse de apagar el motor antes de salir
    motor_pwm.close()
    motor_dir.close()
