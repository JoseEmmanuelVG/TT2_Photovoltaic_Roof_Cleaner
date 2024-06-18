from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from functions_auth import handle_movement, emergency_stop, leer_datos_serial, control_new_motor, capture_image, save_image, is_wifi_connected, sensor_distances, relay, actuadorPin1, actuadorPin2, flotador7, flotador8, StepperMotor
import threading
import time

def register_autonomous_callbacks(app):

    sensor_values = {
        'front-left': 50,
        'front-right': 50,
        'rear-left': 50,
        'rear-right': 50,
        'middle-left': 50,
        'middle-right': 50,
    }

    @app.callback(
        [
            Output('front-left', 'children'),
            Output('front-right', 'children'),
            Output('rear-left', 'children'),
            Output('rear-right', 'children'),
            Output('middle-left', 'children'),
            Output('middle-right', 'children'),
            Output('sensor-humidity', 'children'),
            Output('sensor-temperature', 'children'),
            Output('voltage', 'children')
        ],
        [Input('interval-component', 'n_intervals')]
    )
    def update_sensor_values(n):
        datos = leer_datos_serial()
        if datos:
            global sensor_values
            sensor_values = {
                'front-left': float(datos[0]),
                'front-right': float(datos[1]),
                'rear-left': float(datos[2]),
                'rear-right': float(datos[3]),
                'middle-left': sensor_distances[0],  # Ajustado basado en el mapeo del sensor
                'middle-right': sensor_distances[1]  # Ajustado basado en el mapeo del sensor
            }
            return (
                f"Delante Izquierdo: {sensor_values['front-left']} cm",
                f"Delante Derecho: {sensor_values['front-right']} cm",
                f"Detrás Izquierdo: {sensor_values['rear-left']} cm",
                f"Detrás Derecho: {sensor_values['rear-right']} cm",
                f"Medio Izquierdo: {sensor_values['middle-left']} cm",
                f"Medio Derecho: {sensor_values['middle-right']} cm",
                f"Humedad: {datos[4]}%",
                f"Temperatura: {datos[5]}°C",
                f"Voltaje: {datos[6]} V"
            )
        return (
            "Delante Izquierdo: Waiting",
            "Delante Derecho: Waiting",
            "Detrás Izquierdo: Waiting",
            "Detrás Derecho: Waiting",
            "Medio Izquierdo: Waiting",
            "Medio Derecho: Waiting",
            "Humedad: Waiting",
            "Temperatura: Waiting",
            "Voltaje: Waiting"
        )

    @app.callback(
        Output('status-div', 'children'),
        [Input('start-cleaning-button', 'n_clicks')],
        [State('wheel-speed', 'value'), State('brush-speed', 'value')]
    )
    def start_cleaning(n_clicks, wheel_speed, brush_speed):
        if n_clicks:
            StepperMotor.shared_delay = 0.0001 / (wheel_speed / 100)
            
            def move_robot():
                while True:
                    front_left = sensor_values['front-left']
                    front_right = sensor_values['front-right']
                    rear_left = sensor_values['rear-left']
                    rear_right = sensor_values['rear-right']
                    middle_left = sensor_values['middle-left']
                    middle_right = sensor_values['middle-right']

                    if ((front_left > 30 and front_right > 30) or
                        (rear_left > 30 and rear_right > 30) or
                        (front_left > 30 and rear_left > 30) or
                        (front_right > 30 and rear_right > 30)):
                        stop_all_motors(hold=True)
                        break

                    if (middle_left < 6.2 and front_left > 30 and rear_left < 27):
                        handle_movement('left')
                    elif (middle_left > 6.2 and front_left < 30 and rear_left > 27):
                        handle_movement('right')
                    elif (middle_right < 6.2 and front_right > 30 and rear_right < 27):
                        handle_movement('right')
                    elif (middle_right > 6.2 and front_right < 30 and rear_right > 27):
                        handle_movement('left')
                    else:
                        handle_movement('forward')

                    time.sleep(0.1)

            cleaning_thread = threading.Thread(target=move_robot)
            cleaning_thread.start()
            
            return "Limpieza iniciada"

        return "Esperando acción"

    @app.callback(
        Output('status-div-stop', 'children'),
        [Input('stop-cleaning-button', 'n_clicks')]
    )
    def stop_cleaning(n_clicks):
        if n_clicks:
            emergency_stop()
            return "Limpieza detenida"
        return "Esperando acción"

    @app.callback(
        Output('wifi-status', 'children'),
        Output('wifi-status', 'className'),
        Input('url', 'pathname'),
        prevent_initial_call=True
    )
    def update_wifi_status(pathname):
        if is_wifi_connected():
            return " Conectado", "wifi-connected"
        else:
            return " Desconectado", "wifi-disconnected"

    @app.callback(
        Output('image-container', 'children'),
        [Input('start-cleaning-button', 'n_clicks'),
         Input('stop-cleaning-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def control_cleaning(start_n_clicks, stop_n_clicks):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'start-cleaning-button':
            handle_movement('forward', 100)
            image_data = capture_image("cleaning_start.jpg")
            return html.Img(src=image_data, className="image-box")

        elif button_id == 'stop-cleaning-button':
            emergency_stop()
            image_data = capture_image("cleaning_stop.jpg")
            return html.Img(src=image_data, className="image-box")

        raise PreventUpdate

    @app.callback(
        [Output('start-roller-button', 'disabled'),
         Output('stop-roller-button', 'disabled')],
        [Input('start-roller-button', 'n_clicks'),
         Input('stop-roller-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def control_roller(start_n_clicks, stop_n_clicks):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'start-roller-button':
            control_new_motor('start_forward', 100)
            return False, True

        elif button_id == 'stop-roller-button':
            control_new_motor('stop', 0)
            return True, False

        raise PreventUpdate

    @app.callback(
        Output('water-level', 'children'),
        [Input('watered-toggle', 'value')]
    )
    def update_water_level(toggle_value):
        if 1 in toggle_value:
            if flotador8.is_pressed:
                return "Lleno"
            elif flotador7.is_pressed:
                return "Vacío"
            else:
                return "Medio"
        else:
            return "Desactivado"
