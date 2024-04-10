# pip install dash flask-login  Flask-Bcrypt


from dash import Dash, html, dcc

def create_layout():
    return html.Div([
        html.H1("Control del Robot"),
        html.Button('Adelante', id='forward-btn'),
        html.Button('Atrás', id='backward-btn'),
        html.Button('Izquierda', id='left-btn'),
        html.Button('Derecha', id='right-btn'),
        html.Button('Rotar Derecha', id='rotate-right-btn'),
        html.Button('Rotar Izquierda', id='rotate-left-btn'),
        # Espacio para mensajes de estado
        html.Div(id='status-div')
    ])
