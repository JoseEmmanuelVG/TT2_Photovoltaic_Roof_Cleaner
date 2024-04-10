from dash.dependencies import Input, Output
# Suponiendo que functions.py contiene todas las funciones de movimiento como move_forward(), etc.
from functions import move_forward, move_backward, move_left, move_right, rotate_right, rotate_left

def register_callbacks(app):
    @app.callback(
        Output('status-div', 'children'),
        [Input('forward-btn', 'n_clicks'),
         Input('backward-btn', 'n_clicks'),
         Input('left-btn', 'n_clicks'),
         Input('right-btn', 'n_clicks'),
         Input('rotate-right-btn', 'n_clicks'),
         Input('rotate-left-btn', 'n_clicks')]
    )
    def update_output(forward, backward, left, right, rotate_right_btn, rotate_left_btn):
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No buttons yet clicked'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'forward-btn':
            move_forward()
            return "Moviendo hacia adelante"
        elif button_id == 'backward-btn':
            move_backward()
            return "Moviendo hacia atrás"
        # Continúa para los demás botones...