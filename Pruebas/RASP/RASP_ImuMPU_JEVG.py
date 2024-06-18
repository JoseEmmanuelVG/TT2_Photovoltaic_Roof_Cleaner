import smbus2
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

# Dirección I2C del MPU 6050
MPU6050_ADDR = 0x68

# Registros del MPU 6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

def read_word(bus, addr, reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def get_accel_data(bus, addr):
    x = read_word(bus, addr, ACCEL_XOUT_H)
    y = read_word(bus, addr, ACCEL_YOUT_H)
    z = read_word(bus, addr, ACCEL_ZOUT_H)
    return x, y, z

def get_gyro_data(bus, addr):
    x = read_word(bus, addr, GYRO_XOUT_H)
    y = read_word(bus, addr, GYRO_YOUT_H)
    z = read_word(bus, addr, GYRO_ZOUT_H)
    return x, y, z

def calibrate_sensor(bus, addr, num_samples=100):
    accel_offset = [0, 0, 0]
    gyro_offset = [0, 0, 0]
    
    for _ in range(num_samples):
        ax, ay, az = get_accel_data(bus, addr)
        gx, gy, gz = get_gyro_data(bus, addr)
        
        accel_offset[0] += ax
        accel_offset[1] += ay
        accel_offset[2] += az
        gyro_offset[0] += gx
        gyro_offset[1] += gy
        gyro_offset[2] += gz
        
        time.sleep(0.01)
    
    accel_offset = [x / num_samples for x in accel_offset]
    gyro_offset = [x / num_samples for x in gyro_offset]
    
    return accel_offset, gyro_offset

def apply_offset(data, offset):
    return [d - o for d, o in zip(data, offset)]

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def fir_filter(data, numtaps=5):
    taps = np.ones(numtaps) / numtaps
    return lfilter(taps, 1.0, data)

def main():
    try:
        bus = smbus2.SMBus(1)
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
        
        accel_data = {'x': [], 'y': [], 'z': []}
        gyro_data = {'x': [], 'y': [], 'z': []}
        times = []

        print("Calibrating sensor...")
        accel_offset, gyro_offset = calibrate_sensor(bus, MPU6050_ADDR)
        print("Calibration complete")
        
        start_time = time.time()
        
        while True:
            accel_x, accel_y, accel_z = apply_offset(get_accel_data(bus, MPU6050_ADDR), accel_offset)
            gyro_x, gyro_y, gyro_z = apply_offset(get_gyro_data(bus, MPU6050_ADDR), gyro_offset)
            
            current_time = time.time() - start_time
            times.append(current_time)
            
            accel_data['x'].append(accel_x)
            accel_data['y'].append(accel_y)
            accel_data['z'].append(accel_z)
            
            gyro_data['x'].append(gyro_x)
            gyro_data['y'].append(gyro_y)
            gyro_data['z'].append(gyro_z)
            
            print(f"Accelerometer: X={accel_x}, Y={accel_y}, Z={accel_z}")
            print(f"Gyroscope: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
            
            time.sleep(1)
            
            # Stop after collecting data for 20 seconds for demonstration
            if current_time > 20:
                break

        # Convert data to numpy arrays for filtering
        times = np.array(times)
        accel_data['x'] = np.array(accel_data['x'])
        accel_data['y'] = np.array(accel_data['y'])
        accel_data['z'] = np.array(accel_data['z'])
        gyro_data['x'] = np.array(gyro_data['x'])
        gyro_data['y'] = np.array(gyro_data['y'])
        gyro_data['z'] = np.array(gyro_data['z'])
        
        # Apply moving average filter
        window_size = 5
        accel_data['x'] = moving_average(accel_data['x'], window_size)
        accel_data['y'] = moving_average(accel_data['y'], window_size)
        accel_data['z'] = moving_average(accel_data['z'], window_size)
        gyro_data['x'] = moving_average(gyro_data['x'], window_size)
        gyro_data['y'] = moving_average(gyro_data['y'], window_size)
        gyro_data['z'] = moving_average(gyro_data['z'], window_size)

        # Apply FIR filter
        numtaps = 5
        accel_data['x'] = fir_filter(accel_data['x'], numtaps)
        accel_data['y'] = fir_filter(accel_data['y'], numtaps)
        accel_data['z'] = fir_filter(accel_data['z'], numtaps)
        gyro_data['x'] = fir_filter(gyro_data['x'], numtaps)
        gyro_data['y'] = fir_filter(gyro_data['y'], numtaps)
        gyro_data['z'] = fir_filter(gyro_data['z'], numtaps)

        # Plotting the data
        plt.figure()
        plt.plot(times[:len(accel_data['x'])], accel_data['x'], label='Accel X')
        plt.plot(times[:len(accel_data['y'])], accel_data['y'], label='Accel Y')
        plt.plot(times[:len(accel_data['z'])], accel_data['z'], label='Accel Z')
        plt.title('Accelerometer Data')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration')
        plt.legend()
        plt.show()
        
        plt.figure()
        plt.plot(times[:len(gyro_data['x'])], gyro_data['x'], label='Gyro X')
        plt.plot(times[:len(gyro_data['y'])], gyro_data['y'], label='Gyro Y')
        plt.plot(times[:len(gyro_data['z'])], gyro_data['z'], label='Gyro Z')
        plt.title('Gyroscope Data')
        plt.xlabel('Time (s)')
        plt.ylabel('Rotation')
        plt.legend()
        plt.show()
        
    except FileNotFoundError as e:
        print("Error: I2C bus not found. Ensure I2C is enabled and connected properly.")
        print(e)
    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == "__main__":
    main()
