import dash
from dash.dependencies import Input, Output
from functions import (
    move_forward, move_backward, move_left, move_right, rotate_right, rotate_left
)


def register_callbacks(app):
    from dash.dependencies import Input, Output
    import dash

    @app.callback(
        Output('status-div', 'children'),
        [Input('forward-btn', 'n_clicks_timestamp'),
         Input('backward-btn', 'n_clicks_timestamp'),
         Input('left-btn', 'n_clicks_timestamp'),
         Input('right-btn', 'n_clicks_timestamp'),
         Input('rotate-right-btn', 'n_clicks_timestamp'),
         Input('rotate-left-btn', 'n_clicks_timestamp')],
        prevent_initial_call=True
    )
    def update_output(forward, backward, left, right, rotate_right, rotate_left):
        ctx = dash.callback_context

        if not ctx.triggered:
            return "No buttons yet clicked"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        actions = {
            'forward-btn': 'forward',
            'backward-btn': 'backward',
            'left-btn': 'left',
            'right-btn': 'right',
            'rotate-right-btn': 'rotate_right',
            'rotate-left-btn': 'rotate_left'
        }

        action = actions.get(button_id)
        handle_movement(action)

        return f"{action} initiated"
