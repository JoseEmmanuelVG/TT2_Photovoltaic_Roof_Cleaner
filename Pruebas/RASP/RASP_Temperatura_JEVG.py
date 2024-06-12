from gpiozero import CPUTemperature, DigitalOutputDevice, DigitalInputDevice
import time

# Pines GPIO (utiliza la numeración BCM)
pin_data = 18

# Configura el pin inicialmente como salida (para poder enviar la señal de inicio)
dht11_pin = DigitalOutputDevice(pin_data)

# Función para leer el DHT11
# ... (código anterior)

# Función para leer el DHT11
def read_dht11():
    # Envía señal de inicio al sensor
    dht11_pin.on()
    time.sleep(0.02) # Aumentamos un poco el tiempo
    dht11_pin.off()
    time.sleep(0.00002)

    # Cambia el pin a entrada para leer los datos
    dht11_pin.close()
    dht11_data = DigitalInputDevice(pin_data)

    # Espera la respuesta del sensor (agregamos un pequeño retraso)
    time.sleep(0.001)  
    while dht11_data.value == 0:
        pass
    while dht11_data.value == 1:
        pass

    # ... (resto del código de lectura de datos del DHT11)

    return humidity, temperature

# ... (resto del código)


# Bucle principal
while True:
    humidity, temperature = read_dht11()
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature:.1f} C  Humidity: {humidity:.1f}%")
        print("Temperatura CPU: ", CPUTemperature().temperature)
    else:
        print("Failed to get reading. Try again!")
    time.sleep(2.0)
