# Remoto Funcionando
from dash import Dash
import ui_definition_remote
import callbacks_remote

app = Dash(__name__)
app.layout = ui_definition_remote.create_layout()

callbacks_remote.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)