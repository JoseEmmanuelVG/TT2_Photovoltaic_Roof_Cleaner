from dash import Dash
import ui_definition_autonomous
import callbacks_auth
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = ui_definition_autonomous.create_layout()

callbacks_auth.register_autonomous_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
