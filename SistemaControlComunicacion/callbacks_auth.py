from dash import dcc, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
from flask_login import login_user, current_user
import functions_auth

def register_auth_callbacks(app):
    @app.callback(
        Output('url', 'pathname'),
        [Input('login-button', 'n_clicks')],
        [State('username-login', 'value'), State('password-login', 'value')],
        prevent_initial_call=True  # Asegúrate de que el callback no se llame al cargar la página
    )
    def handle_login(n_clicks, username, password):
        if n_clicks is None:
            raise PreventUpdate
        
        if functions_auth.login(username, password):
            return '/menu'
        return '/login'
