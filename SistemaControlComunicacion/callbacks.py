from dash.dependencies import Input, Output, State
import dash
from functions import handle_movement, emergency_stop

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
