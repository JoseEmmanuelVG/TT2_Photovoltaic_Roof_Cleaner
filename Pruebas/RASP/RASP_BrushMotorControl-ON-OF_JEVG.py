from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep

# Definir los pines de conexión
pinPWM = 15           # Puerto de control de velocidad (PWM)
pinDireccion = 14     # Control de avance y retroceso

# Configurar los dispositivos
motor_pwm = PWMOutputDevice(pinPWM, frequency=1000, initial_value=0)  # Inicializa el PWM en apagado
motor_dir = OutputDevice(pinDireccion, initial_value=False)  # Inicializa dirección en falso (avance)

def iniciar_motor():
    motor_pwm.value = 0.5  # Establecer PWM al 50% de ciclo de trabajo
    print("Motor iniciado.")

def parar_motor():
    motor_pwm.value = 0  # Apagar el motor
    print("Motor parado.")

try:
    while True:
        comando = input("Introduce 'i' para iniciar el motor, 'p' para pararlo, 'q' para salir: ").strip().lower()
        
        if comando == 'i':
            iniciar_motor()
            # Motor en una dirección a velocidad media
            motor_dir.off()  # Avance (CW)
            sleep(5)  # Esperar 5 segundos

            # Cambiar la dirección del motor
            motor_dir.on()  # Retroceso (CCW)
            sleep(5)  # Esperar 5 segundos

            # Volver a la dirección original
            motor_dir.off()  # Avance (CW)
        elif comando == 'p':
            parar_motor()
        elif comando == 'qi':
            parar_motor()
            break
        else:
            print("Comando no reconocido. Por favor, introduce 'i' para iniciar, 'p' para parar, 'q' para salir.")
        
except KeyboardInterrupt:
    print("\nInterrupción por teclado. Apagando el motor.")
    parar_motor()
finally:
    # Asegurarse de apagar el motor antes de salir
    motor_pwm.close()
    motor_dir.close()
    print("Recursos liberados. Programa terminado.")
