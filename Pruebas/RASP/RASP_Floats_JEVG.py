from gpiozero import Button
import time

# Configurar los pines GPIO7 y GPIO8 como entradas pull-down
flotador7 = Button(7, pull_up=False)
flotador8 = Button(8, pull_up=False)

# Definir funciones que se ejecutarán al presionar los botones
def flotador7_pressed():
    print("flotador1 LevelDown ON")

def flotador8_pressed():
    print("flotador2 LevelUp ON")

# Asociar las funciones a los eventos de presionar los botones
flotador7.when_pressed = flotador7_pressed
flotador8.when_pressed = flotador8_pressed

# Función para mostrar el estado de los botones
def print_status():
    while True:
        flotador7_state = "HIGH" if flotador7.is_pressed else "LOW"
        flotador8_state = "HIGH" if flotador8.is_pressed else "LOW"
        print(f"flotador1 LevelDown: {flotador7_state}, flotador1 LevelUp: {flotador8_state}")
        time.sleep(1)

# Ejecutar la función en un bucle infinito
try:
    print_status()
except KeyboardInterrupt:
    print("Script terminado por el usuario")


