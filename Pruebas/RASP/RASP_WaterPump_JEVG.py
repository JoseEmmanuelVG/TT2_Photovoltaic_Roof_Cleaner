from gpiozero import LED
import time

# Configurar el pin GPIO19 como una salida
relay = LED(19)

try:
    while True:
        # Activar el relé enviando una señal baja (LED apagado)
        relay.off()
        print("Relé activado (señal baja)")
        time.sleep(1)  # Mantener el relé activado por 1 segundo

        # Desactivar el relé enviando una señal alta (LED encendido)
        relay.on()
        print("Relé desactivado (señal alta)")
        time.sleep(1)  # Mantener el relé desactivado por 1 segundo

except KeyboardInterrupt:
    print("Script terminado por el usuario")
    relay.close()  # Asegurarse de liberar el pin GPIO
