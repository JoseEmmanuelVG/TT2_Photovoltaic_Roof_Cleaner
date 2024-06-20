import time
import threading
from motores import motor1, motor2, motor3, motor4, stop_all_motors, emergency_stop
from sensores import start_sensor_thread, sensor_distances, sensor_data
from correcciones import realizar_correcciones

def main():
    start_sensor_thread()
    try:
        while True:
            resultado = realizar_correcciones(sensor_distances, sensor_data)

            if not sensor_data:
                continue  # Si sensor_data está vacío, saltar la iteración

            front_left, front_right, middle_left, middle_right, rear_left, rear_right = sensor_data[-1]

            if (front_left > 30 and front_right > 30) or (rear_left > 30 and rear_right > 30):
                stop_all_motors()
                print("Condición cumplida: Motores detenidos definitivamente.")
                break

            if any(motor.steps_per_revolution == 36000 for motor in [motor1, motor2, motor3, motor4]):
                stop_all_motors()
                print("Motores detenidos por 4 segundos debido a 6000 pasos completados.")
                time.sleep(4)
                print("Reiniciando correcciones.")

    except KeyboardInterrupt:
        emergency_stop()

if __name__ == "__main__":
    main()
