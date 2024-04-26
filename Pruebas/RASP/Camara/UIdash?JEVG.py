import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import base64
import cv2
from picamera2 import Picamera2
import time

app = Dash(__name__)

def release_camera():
    # Comando para terminar cualquier proceso que use la cámara
    os.system('sudo fuser -k /dev/video0')


def init_camera(retries=5, delay=2):
    picam = None
    for i in range(retries):
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
