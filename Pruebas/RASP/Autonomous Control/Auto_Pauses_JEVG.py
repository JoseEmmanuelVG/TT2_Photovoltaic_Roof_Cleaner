from gpiozero import OutputDevice
from time import sleep
import threading

class StepperMotor:
    """
    Clase para controlar un motor paso a paso.
    """

    def __init__(self, pul_pin, dir_pin, ena_pin, steps_per_revolution=6000):
        """
        Inicializa un objeto StepperMotor con los pines de control del motor.

        Args:
            pul_pin (int): Número del pin para el pulso.
            dir_pin (int): Número del pin para la dirección.
            ena_pin (int): Número del pin para la habilitación.
            steps_per_revolution (int): Número de pasos por revolución del motor.
        """
        self.PUL = OutputDevice(pul_pin)
        self.DIR = OutputDevice(dir_pin)
        self.ENA = OutputDevice(ena_pin, initial_value=False)
        self.steps_per_revolution = steps_per_revolution

    def move(self, revolutions, direction, delay):
        """
        Mueve el motor una cantidad específica de revoluciones en una dirección y con un retardo entre pulsos.

        Args:
            revolutions (int): Número de revoluciones a mover el motor.
            direction (bool): Dirección del movimiento (True para adelante, False para atrás).
            delay (float): Retardo entre pulsos en segundos.
        """
        def movement_sequence():
            print(f"Iniciando movimiento: {revolutions} revoluciones, dirección: {'adelante' if direction else 'atrás'}, retardo: {delay}s")
            self.ENA.on()
            sleep(0.1)  # Espera breve para asegurar que el motor esté habilitado
            self.DIR.value = direction

            for revolution in range(revolutions):
                for step in range(self.steps_per_revolution):
                    self.PUL.on()
                    sleep(delay)
                    self.PUL.off()
                    sleep(delay)

                print(f"Revolución completada: {revolution + 1}")
                self.ENA.off()
                sleep(1)  # Pausa de 1 segundo después de cada revolución
                self.ENA.on()

            self.ENA.off()
            print("Movimiento completado")

        thread = threading.Thread(target=movement_sequence)
        thread.start()
        return thread

# Instancia cada motor con sus respectivos pines
motor1 = StepperMotor(23, 24, 25)
motor2 = StepperMotor(16, 20, 21)
motor3 = StepperMotor(17, 27, 22)
motor4 = StepperMotor(5, 6, 26)

revolutions = 5  # Número de revoluciones para cada dirección
delay = 0.0001  # Retardo entre pulsos, controla la velocidad del motor

def move_all_at_once(movements):
    """
    Mueve todos los motores al mismo tiempo.

    Args:
        movements (list): Lista de tuplas (motor, direction) con los movimientos a realizar.
    """
    threads = []
    for move in movements:
        thread = threading.Thread(target=move[0].move, args=(revolutions, move[1], delay))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def move_forward():
    """
    Mueve todos los motores hacia adelante.
    """
    print("Moviendo hacia adelante")
    movements = [
        (motor1, True),
        (motor2, False),
        (motor3, True),
        (motor4, False),
    ]
    move_all_at_once(movements)

if __name__ == "__main__":
    move_forward()
