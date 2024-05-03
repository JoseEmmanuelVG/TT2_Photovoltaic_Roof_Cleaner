import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import base64
import subprocess

app = Dash(__name__)

# Función para capturar la imagen usando libcamera-still
def capture_image():
    # Asegúrate de que el directorio de trabajo actual es donde deseas guardar las imágenes
    os.chdir('/home/ttm/TT2_Photovoltaic_Roof_Cleaner/Pruebas/RASP/Camara/')
    # Guarda la imagen en un archivo temporal
    subprocess.run(['libcamera-still', '-o', 'current_image.jpg'])

# Función para mostrar la imagen en la aplicación Dash
@app.callback(Output('live-image', 'src'),
              Input('interval-component', 'n_intervals'))
def update_image(n):
    capture_image()  # Captura una nueva imagen
    try:
        with open("current_image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error al cargar o codificar la imagen: {str(e)}")
    return None

# Layout de la aplicación Dash
app.layout = html.Div([
    html.H1("Live Camera Feed"),
    html.Img(id='live-image'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # en milisegundos
        n_intervals=0
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
