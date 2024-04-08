from gpiozero import PWMOutputDevice
from time import sleep

# Define los pines como salidas PWM
pulso = PWMOutputDevice(pin=17, active_high=True, initial_value=0, frequency=2500) # Ejemplo de frecuencia a 2.5kHz
dir_pin = OutputDevice(27, initial_value=False)
enable_pin = OutputDevice(22, initial_value=True)

try:
    # Habilita el motor
    enable_pin.off()
    
    # Establece la dirección
    dir_pin.off()  # Para adelante
    pulso.value = 0.5  # Ciclo de trabajo al 50% para empezar los pulsos
    sleep(3)  # Mantener el motor en esta configuración por 3 segundos
    
    # Cambia la dirección
    dir_pin.on()  # Para atrás
    pulso.value = 0.5  # Sigue con un ciclo de trabajo al 50%
    sleep(3)  # Mantener el motor en esta configuración por 3 segundos

except KeyboardInterrupt:
    # Apaga el motor antes de salir si se recibe una interrupción (Ctrl+C)
    pulso.close()
    dir_pin.off()
    enable_pin.on()
