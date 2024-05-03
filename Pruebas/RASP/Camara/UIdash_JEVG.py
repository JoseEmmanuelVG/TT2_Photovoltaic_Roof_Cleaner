import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import base64
import cv2
from picamera2 import Picamera2
import time

app = Dash(__name__)


def release_camera():
    # Comandos para terminar cualquier proceso que use la cámara y dispositivos relacionados
    os.system('sudo fuser -k /dev/video0')
    os.system('sudo fuser -k /dev/media1')
    os.system('sudo fuser -k /dev/media2')
    

import atexit

def cleanup_camera():
    if picam2 is not None:
        picam2.stop()
        picam2.close()

atexit.register(cleanup_camera)


import threading
camera_lock = threading.Lock()

def init_camera(retries=5, delay=2):
    global camera_lock
    picam = None
    for i in range(retries):
        if camera_lock.acquire(timeout=10):  # Intenta obtener el lock
            try:
                if picam is not None:
                    picam.close()
                picam = Picamera2()
                picam.start_preview(fullscreen=False, window=(0, 0, 640, 480))
                picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
                picam.start()
                print("Cámara inicializada correctamente.")
                return picam
            except Exception as e:
                print(f"Error al inicializar la cámara, reintento {i+1}/{retries}: {str(e)}")
                if picam is not None:
                    picam.close()
                time.sleep(delay)
            finally:
                camera_lock.release()  # Siempre libera el lock
        else:
            print("No se pudo obtener el lock para la cámara.")
    print("No se pudo inicializar la cámara después de varios intentos.")
    return None


picam2 = init_camera()

app.layout = html.Div([
    html.Img(id='live-image'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # en milisegundos
        n_intervals=0
    )
])

@app.callback(Output('live-image', 'src'),
              Input('interval-component', 'n_intervals'))
def update_image(n):
    if picam2 is not None:
        try:
            frame = picam2.capture_array()
            _, buffer = cv2.imencode('.jpg', frame)
            return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode()}"
        except Exception as e:
            print(f"Error al capturar o codificar la imagen: {str(e)}")
    return None

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
