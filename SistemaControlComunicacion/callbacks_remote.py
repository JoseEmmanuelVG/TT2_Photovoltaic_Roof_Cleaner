from dash.dependencies import Input, Output, State
import dash
from functions_remote import handle_movement, emergency_stop, leer_datos_serial, control_new_motor, capture_image, save_image, is_wifi_connected
from dash import html

# Variables para almacenar las imágenes
images_before = []
images_after = []

def register_callbacks(app):
    @app.callback(
        [Output('status-div', 'children')] +
        [Output(f'{btn_id}-btn', 'className') for btn_id in ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']],
        [Input(f'{btn_id}-btn', 'n_clicks_timestamp') for btn_id in ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']] + 
        [Input('emergency-stop-btn', 'n_clicks'),
         Input('start-forward-btn', 'n_clicks'),
         Input('start-reverse-btn', 'n_clicks'),
         Input('stop-btn', 'n_clicks'),
         Input('pwm-slider', 'value')],
        prevent_initial_call=True
    )
    def update_output(*args):
        ctx = dash.callback_context

        if not ctx.triggered:
            return ["No buttons yet clicked"] + [""] * 6
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        action = button_id.replace('-btn', '').replace('rotate-right', 'rotate_right').replace('rotate-left', 'rotate_left')
        
        if button_id == 'emergency-stop-btn':
            emergency_stop()
            return ["EMERGENCY STOP ACTIVATED!"] + [""] * 6

        pwm_value = args[-1]  # The last argument is the PWM slider value

        if button_id == 'start-forward-btn':
            control_new_motor('start_forward', pwm_value)
            return [f"Motor arrancado adelante al {pwm_value}% PWM"] + [""] * 6
        elif button_id == 'start-reverse-btn':
            control_new_motor('start_reverse', pwm_value)
            return [f"Motor arrancado en reversa al {pwm_value}% PWM"] + [""] * 6
        elif button_id == 'stop-btn':
            control_new_motor('stop', 0)
            return ["Motor detenido"] + [""] * 6

        # Update motors
        handle_movement(action)
        
        # Determine the active button
        btn_ids = ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']
        active_classes = ['active' if f'{btn}-btn' == button_id else '' for btn in btn_ids]
        
        return [f"{action.replace('_', ' ').capitalize()} iniciado"] + active_classes

    @app.callback(
        [Output('images-container-before', 'children'),
         Output('images-container-after', 'children')],
        [Input('capture-btn-before', 'n_clicks'),
         Input('capture-btn-after', 'n_clicks')],
        [State('images-container-before', 'children'),
         State('images-container-after', 'children')]
    )
    def handle_capture(before_clicks, after_clicks, children_before, children_after):
        global images_before, images_after

        ctx = dash.callback_context
        if not ctx.triggered:
            return children_before, children_after

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'capture-btn-before':
            images_list = images_before
            prefix = "REMOTE_ANTES"
        else:
            images_list = images_after
            prefix = "REMOTE_DESPUES"

        # Capturar imagen y actualizar la lista
        image_index = len(images_list) + 1
        if image_index > 17:
            image_index = 1
        image_name = f"{prefix}_{image_index}.jpg"
        new_image_data = capture_image(image_name)
        file_name = save_image(new_image_data, prefix, image_index)
        images_list.append(file_name)

        if button_id == 'capture-btn-before':
            images_before = images_list
            children_before = [html.Img(src=f'assets/{file_name}', style={'width': '100%', 'padding-top': '10px'}) for file_name in images_before]
            return children_before, children_after
        else:
            images_after = images_list
            children_after = [html.Img(src=f'assets/{file_name}', style={'width': '100%', 'padding-top': '10px'}) for file_name in images_after]
            return children_before, children_after





    @app.callback(
        [Output('front-left-sensor', 'children'),
         Output('front-right-sensor', 'children'),
         Output('back-left-sensor', 'children'),
         Output('back-right-sensor', 'children'),
         Output('humidity', 'children'),
         Output('temperature', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_sensors(n):
        datos = leer_datos_serial()
        if datos:
            return [
                html.Div(f"Delante izquierdo: {datos[0]} cm", style={'color': 'white'}),
                html.Div(f"Delante derecho: {datos[1]} cm", style={'color': 'white'}),
                html.Div(f"Atrás izquierdo: {datos[2]} cm", style={'color': 'white'}),
                html.Div(f"Atrás derecho: {datos[3]} cm", style={'color': 'white'}),
                html.Div(f"Humedad: {datos[4]} %", style={'color': 'white'}),
                html.Div(f"Temperatura: {datos[5]} °C", style={'color': 'white'})
            ]
        else:
            return ["Esperando datos...", "Esperando datos...", "Esperando datos...", "Esperando datos...", "Esperando datos...", "Esperando datos..."]




####### WIFI
    @app.callback(
        Output('wifi-status', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_wifi_status(n):
        if is_wifi_connected():
            return html.Span("Conectado a WiFi", style={'color': 'green'})
        else:
            return html.Span("No Conectado a WiFi", style={'color': 'red'})