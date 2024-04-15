from dash import Dash
import ui_definition
import callbacks

app = Dash(__name__)
app.layout = ui_definition.create_layout()

callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
