import time
from motores import motor1, motor2, motor3, motor4
from pid_controller import PIDController
from sensores import leer_datos_serial

pid_left = PIDController(0.1, 0.01, 0.05)
pid_right = PIDController(0.1, 0.01, 0.05)

def realizar_correcciones(sensor_distances, sensor_data):
    # Aquí deberías leer los datos del puerto serial
    datos = leer_datos_serial()
    if datos:
        front_left = float(datos[0])
        front_right = float(datos[1])
        rear_left = float(datos[2])
        rear_right = float(datos[3])
        middle_left = sensor_distances[0]
        middle_right = sensor_distances[1]

        # Almacenar los datos de los sensores
        sensor_data.append([front_left, front_right, middle_left, middle_right, rear_left, rear_right])

        # Imprimir los valores de los sensores en la consola
        print(f"Delante izquierda: {front_left} cm     ---    Delante derecha: {front_right} cm")
        print(f"Medio izquierda: {middle_left} cm     ---    Medio derecha: {middle_right} cm")
        print(f"Atrás izquierda: {rear_left} cm     ---    Atrás derecha: {rear_right} cm")
        print("")

        # Aplicar PID para corregir la dirección si el robot se va a la izquierda
        if (middle_right < 10) and (front_right < 30 and rear_right < 30):
            correction = pid_left.compute(10, middle_right)
            for i in range(5):
                delay1_3 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor1 y motor3
                delay2_4 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor2 y motor4

                motor1.set_speed(delay1_3)
                motor2.set_speed(delay2_4)
                motor3.set_speed(delay1_3)
                motor4.set_speed(delay2_4)

                print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                time.sleep(0.1)
            
            motor1.start_moving(True)
            motor2.start_moving(False)
            motor3.start_moving(True)
            motor4.start_moving(False)
            print(f"PID Correction Left: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

        # Rectificar ruedas
        elif (middle_right > 10) and (front_right > 30 and rear_right < 30):
            correction = pid_right.compute(10, middle_right)
            for i in range(5):
                delay1_3 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor1 y motor3
                delay2_4 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor2 y motor4

                motor1.set_speed(delay1_3)
                motor2.set_speed(delay2_4)
                motor3.set_speed(delay1_3)
                motor4.set_speed(delay2_4)

                print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                time.sleep(0.1)
            
            motor1.start_moving(True)
            motor2.start_moving(False)
            motor3.start_moving(True)
            motor4.start_moving(False)
            print(f"PID Correction Right: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

        # Aplicar PID para corregir la dirección si el robot se va a la derecha
        elif (middle_right > 10) and (front_right > 30 and rear_right > 30):
            correction = pid_right.compute(10, middle_right)
            for i in range(5):
                delay1_3 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor1 y motor3
                delay2_4 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor2 y motor4

                motor1.set_speed(delay1_3)
                motor2.set_speed(delay2_4)
                motor3.set_speed(delay1_3)
                motor4.set_speed(delay2_4)

                print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                time.sleep(0.1)
            
            motor1.start_moving(True)
            motor2.start_moving(False)
            motor3.start_moving(True)
            motor4.start_moving(False)
            print(f"PID Correction Right: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

        # Aplicar PID para corregir la dirección si el robot se va a la izquierda
        elif (middle_right > 10) and (front_right < 30 and rear_right > 30):
            correction = pid_left.compute(10, middle_right)
            for i in range(5):
                delay1_3 = max(0.0005, min(0.001, 0.0005 - (i * 0.00009)))  # Incremento para motor1 y motor3
                delay2_4 = max(0.0005, min(0.001, 0.001 + (i * 0.00009)))   # Decremento para motor2 y motor4

                motor1.set_speed(delay1_3)
                motor2.set_speed(delay2_4)
                motor3.set_speed(delay1_3)
                motor4.set_speed(delay2_4)

                print(f"Step {i+1}: motor1 and motor3 delay = {delay1_3:.6f}, motor2 and motor4 delay = {delay2_4:.6f}")
                time.sleep(0.1)
            
            motor1.start_moving(True)
            motor2.start_moving(False)
            motor3.start_moving(True)
            motor4.start_moving(False)
            print(f"PID Correction Left: {correction}, Motor Delays: {motor1.delay}, {motor2.delay}, {motor3.delay}, {motor4.delay}")

        else:
            motor1.start_moving(True)
            motor2.start_moving(False)
            motor3.start_moving(True)
            motor4.start_moving(False)

        time.sleep(1)  # Pausar entre movimientos de 30 cm
