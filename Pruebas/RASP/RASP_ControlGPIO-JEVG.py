from gpiozero import LED
from time import sleep

# Configura los pines para cada LED
led1 = LED(17)
led2 = LED(27)
led3 = LED(22)

try:
    while True:  # Bucle infinito
        # Enciende el LED conectado al GPIO 17
        led1.on()
        sleep(1)  # Espera 1 segundo
        led1.off()
        
        # Enciende el LED conectado al GPIO 27
        led2.on()
        sleep(1)  # Espera 1 segundo
        led2.off()

        # Enciende el LED conectado al GPIO 22
        led3.on()
        sleep(1)  # Espera 1 segundo
        led3.off()

        # Espera 1 segundo antes de repetir el ciclo
        sleep(1)

except KeyboardInterrupt:
    # Apaga todos los LEDs antes de salir si se recibe una interrupción (Ctrl+C)
    led1.off()
    led2.off()
    led3.off()
    print("Programa interrumpido por el usuario")
