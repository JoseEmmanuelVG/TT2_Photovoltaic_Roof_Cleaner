from dash.dependencies import Input, Output, State
import dash
from functions_remote import handle_movement, emergency_stop, capture_image
import base64

from dash import html
import os
import subprocess

from flask_login import current_user, login_required


def register_callbacks(app):

    @app.callback(
        [Output('status-div', 'children')] +
        [Output(f'{btn_id}-btn', 'className') for btn_id in ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']],
        [Input(f'{btn_id}-btn', 'n_clicks_timestamp') for btn_id in ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']] + 
        [Input('emergency-stop-btn', 'n_clicks')],
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

        # Update motors
        handle_movement(action)
        
        # Determine the active button
        btn_ids = ['forward', 'backward', 'left', 'right', 'rotate-right', 'rotate-left']
        active_classes = ['active' if f'{btn}-btn' == button_id else '' for btn in btn_ids]
        
        return [f"{action.replace('_', ' ').capitalize()} iniciado"] + active_classes

   # Cámara

    @app.callback(
        Output('images-container', 'children'),
        [Input('capture-btn', 'n_clicks')],
        [State('images-container', 'children')],
        prevent_initial_call=True
    )
    def handle_capture(n_clicks, children):
        if n_clicks:
            # Asegura que children sea una lista si llega como None
            if children is None:
                children = []

            capture_image()  # Función que toma la foto
            try:
                with open("/home/ttm/TT2_Photovoltaic_Roof_Cleaner/Pruebas/RASP/Camara/current_image.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    new_image = html.Img(src=f"data:image/jpeg;base64,{encoded_string}", style={'width': '100%', 'padding-top': '10px'})
                    children.append(new_image)
                    return children
            except Exception as e:
                print(f"Error al cargar o codificar la imagen: {str(e)}")
                return children
        return dash.no_update
