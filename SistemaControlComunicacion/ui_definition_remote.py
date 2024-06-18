from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from callbacks_remote import register_callbacks



# Crear el layout de Dash
def create_layout():
    return html.Div([
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
        html.H1("Control Remoto del Robot", className="header-title"),
        
        # Estado del WiFi
        html.Div(id='wifi-status', className='status-div', style={'marginTop': '10px', 'textAlign': 'center'}),

        # Estado de los flotadores
        html.Div(id='flotadores-status', className='sensor-data', style={'textAlign': 'center', 'padding': '10px', 'marginBottom': '20px', 'color': 'white', 'fontWeight': 'bold'}),

        # Controles de la bomba
        html.Div([
            dbc.Button("Activar Bomba", id='activate-pump-btn', className='remote-btn', style={'backgroundColor': 'blue', 'color': 'white', 'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("Desactivar Bomba", id='deactivate-pump-btn', className='remote-btn', style={'backgroundColor': 'red', 'color': 'white', 'width': '30%', 'height': '50px', 'margin': '5px'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px 0'}),

        # Controles de los actuadores
        html.Div([
            dbc.Button("Activar Actuador Adelante", id='activate-act1-btn', className='remote-btn', style={'backgroundColor': 'blue', 'color': 'white', 'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("Activar Actuador Atrás", id='activate-act2-btn', className='remote-btn', style={'backgroundColor': 'blue', 'color': 'white', 'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("Desactivar Actuadores", id='deactivate-act-btn', className='remote-btn', style={'backgroundColor': 'red', 'color': 'white', 'width': '30%', 'height': '50px', 'margin': '5px'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px 0'}),

        # Lecturas de sensores de humedad y temperatura
        html.Div([
            html.Div("Humedad: X %", id='humidity', className='sensor-data', style={'backgroundColor': 'blue', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'margin': '10px'}),
            html.Div("Temperatura: X °C", id='temperature', className='sensor-data', style={'backgroundColor': 'red', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'margin': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'center', 'margin': '20px 0'}),

        # Lectura del nivel de batería
        html.Div("Nivel de batería: X V", id='battery-level', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'marginBottom': '20px'}),

        # Sliders de control de velocidad
        html.Div([
            html.Div([
                html.Label("PWM velocidad del rodillo", style={'textAlign': 'center', 'width': '100%'}),
                dcc.Slider(
                    id='pwm-slider',
                    min=1,
                    max=100,
                    step=1,
                    value=50,
                    marks={i: f'{i}%' for i in range(0, 101, 10)},
                    className='slider',
                    updatemode='drag'
                ),
                html.Label("Velocidad de desplazamiento", style={'textAlign': 'center', 'width': '100%'}),
                dcc.Slider(
                    id='speed-slider',
                    min=0.0001,
                    max=0.001,
                    step=0.0001,
                    value=0.0005,
                    marks={i: f'{i:.4f}' for i in [0.0001, 0.0005, 0.0010]},
                    className='slider',
                    updatemode='drag'
                ),
                html.Div(id='speed-slider-value', style={'textAlign': 'center', 'marginTop': '10px'})
            ], style={'width': '80%', 'margin': 'auto', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px 0'}),

        # Controles del motor principal
        html.Div([
            dbc.Button("ARRANQUE DELANTE", id='start-forward-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("ARRANQUE REVERSA", id='start-reverse-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("PARO", id='stop-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px 0'}),

        # Controles de dirección y sensores
        dbc.Container([
            html.Div([
                html.Div("Delante izquierdo: X cm", id='front-left-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'front-left'}),
                dbc.Button("ADELANTE", id='forward-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'forward'}),
                html.Div("Delante derecho: X cm", id='front-right-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'front-right'}),
                dbc.Button("IZQUIERDA", id='left-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'left'}),
                html.Div("Sensor 1: X cm", id='sensor-1', className='sensor-data', style={'backgroundColor': 'yellow', 'color': 'black', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'left-sensor'}),
                dbc.Button("ROTAR IZQUIERDA", id='rotate-left-btn', className='remote-btn rotate-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'rotate-left'}),
                dbc.Button("ROTAR DERECHA", id='rotate-right-btn', className='remote-btn rotate-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'rotate-right'}),
                dbc.Button("DERECHA", id='right-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'right'}),
                html.Div("Sensor 2: X cm", id='sensor-2', className='sensor-data', style={'backgroundColor': 'yellow', 'color': 'black', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'right-sensor'}),
                html.Div("Atrás izquierdo: X cm", id='back-left-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'back-left'}),
                dbc.Button("ATRÁS", id='backward-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'back'}),
                html.Div("Atrás derecho: X cm", id='back-right-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'back-right'}),
                dbc.Button("PARO DE EMERGENCIA", id='emergency-stop-btn', className='emergency-btn', style={'backgroundColor': 'red', 'color': 'white', 'width': '100%', 'height': '100px', 'gridArea': 'emergency'}),
                dbc.Button("TOMAR FOTO ANTES", id='capture-btn-before', className='capture-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'capture-before'}),
                dbc.Button("TOMAR FOTO DESPUÉS", id='capture-btn-after', className='capture-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'capture-after'}),
            ], style={
                'display': 'grid',
                'gridTemplateColumns': '1fr 1fr 1fr 1fr',
                'gridTemplateRows': 'auto auto auto auto auto',
                'gridTemplateAreas': '''
                    'front-left forward forward front-right'
                    'left rotate-left rotate-right right'
                    'left-sensor . . right-sensor'
                    'back-left back back back-right'
                    'emergency emergency emergency emergency'
                    'capture-before capture-before capture-after capture-after'
                ''',
                'gridGap': '10px',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }),
            dbc.Row([
                dbc.Col(html.Div(id='images-container-before', style={'width': '100%', 'maxWidth': '600px', 'marginTop': '20px'}), width=6),
                dbc.Col(html.Div(id='images-container-after', style={'width': '100%', 'maxWidth': '600px', 'marginTop': '20px'}), width=6)
            ], justify='center', align='center'),
            dbc.Row([
                dbc.Col(html.Div(id='status-div', className='status-div', style={'marginTop': '20px', 'textAlign': 'center'}), width=12),
            ], justify='center', align='center')
        ])
    ], style={'width': '100%', 'maxWidth': '900px', 'margin': '0 auto'})