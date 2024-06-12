
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask_login import login_required, current_user
import ui_definition_remote, ui_definition_login_menu, ui_definition_autonomous
import callbacks_remote, callbacks_auth
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '/home/ttm/TT2_Photovoltaic_Roof_Cleaner/SistemaControlComunicacion/environment_variables.env')
load_dotenv(dotenv_path)

# Intenta imprimir los valores cargados para verificar
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("PASSWORD:", os.getenv('PASSWORD'))

if not os.getenv('SECRET_KEY'):
    raise Exception("No se pudo cargar la clave secreta desde el archivo .env")




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Utiliza la variable de entorno para la clave secreta
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise Exception("No se pudo cargar la clave secreta desde el archivo .env")
app.server.secret_key = secret_key
print("Clave secreta establecida:", secret_key)

from functions_auth import login_manager, login_user, logout_user, User
login_manager.init_app(app.server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])




@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    print("Current user:", current_user)
    print("Authenticated:", current_user.is_authenticated)
    if pathname == '/remote':
        if not current_user.is_authenticated:
            return '/login'
        layout = ui_definition_remote.create_layout()
        callbacks_remote.register_callbacks(app)  # Asegúrate de registrar los callbacks aquí
        return layout
    if pathname in ["/", "/login"]:
        if current_user.is_authenticated:
            return '/menu'
        return ui_definition_login_menu.login_layout()
    elif pathname == '/menu':
        if not current_user.is_authenticated:
            return '/login'
        return ui_definition_login_menu.menu_layout()
    elif pathname == '/remote':
        if not current_user.is_authenticated:
            return '/login'
        return ui_definition_remote.create_layout()
    elif pathname == '/automatic':
        if not current_user.is_authenticated:
            return '/login'
        return ui_definition_autonomous.create_layout()
    else:
        return "404 Page not found. Return to Login", dcc.Link('Go to Login', href='/login')

callbacks_auth.register_auth_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)










