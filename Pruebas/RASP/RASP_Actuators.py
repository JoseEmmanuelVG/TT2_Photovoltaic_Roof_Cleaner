from gpiozero import LED
import time

# Configurar los pines GPIO2 y GPIO3 como salidas
actuadorPin1 = LED(9)
actuadorPin2 = LED(11)

try:
    while True:
        # Gira el actuador en una dirección
        actuadorPin1.on()
        actuadorPin2.off()
        print("actuador en dirección 1: GPIO2: ALTA, GPIO3: BAJA")
        time.sleep(5)  # Esperar 2 segundos

        # Detiene el actuador brevemente
        actuadorPin1.off()
        actuadorPin2.off()
        print("actuador detenido brevemente")
        time.sleep(3)  # Esperar 0.5 segundos

        # Gira el actuador en la dirección opuesta
        actuadorPin1.off()
        actuadorPin2.on()
        print("actuador en dirección opuesta: GPIO2: BAJA, GPIO3: ALTA")
        time.sleep(5)  # Esperar 2 segundos

        # Detiene el actuador brevemente
        actuadorPin1.off()
        actuadorPin2.off()
        print("actuador detenido brevemente")
        time.sleep(0.5)  # Esperar 0.5 segundos

except KeyboardInterrupt:
    print("Script terminado por el usuario")
    actuadorPin1.close()  # Asegurarse de liberar el pin GPIO2
    actuadorPin2.close()  # Asegurarse de liberar el pin GPIO3
