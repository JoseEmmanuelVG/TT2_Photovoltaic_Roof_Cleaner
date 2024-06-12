from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
        html.H1("Control Remoto del Robot", className="header-title"),
        html.Div(id='wifi-status', className='status-div', style={'marginTop': '10px', 'textAlign': 'center'}),
        html.Div([
            html.Div("Humedad: X %", id='humidity', className='sensor-data', style={'backgroundColor': 'blue', 'color': 'white', 'textAlign': 'center', 'padding': '10px'}),
            html.Div("Temperatura: X °C", id='temperature', className='sensor-data', style={'backgroundColor': 'red', 'color': 'white', 'textAlign': 'center', 'padding': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'center', 'margin': '20px 0'}),
        html.Div([
            html.Label("Control de PWM", style={'textAlign': 'center', 'width': '100%'}),
            html.Div([
                dcc.Slider(
                    id='pwm-slider',
                    min=1,
                    max=100,
                    step=1,
                    value=50,
                    marks={i: f'{i}%' for i in range(0, 101, 10)},
                    className='slider',
                    updatemode='drag'
                )
            ], style={'width': '80%', 'margin': 'auto'})
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'margin': '20px 0'}),
        html.Div([
            dbc.Button("ARRANQUE DELANTE", id='start-forward-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("ARRANQUE REVERSA", id='start-reverse-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
            dbc.Button("PARO", id='stop-btn', className='remote-btn', style={'width': '30%', 'height': '50px', 'margin': '5px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '10px 0'}),
        dbc.Container([
            html.Div([
                html.Div("Delante izquierdo: X cm", id='front-left-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'front-left'}),
                dbc.Button("ADELANTE", id='forward-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'forward'}),
                html.Div("Delante derecho: X cm", id='front-right-sensor', className='sensor-data', style={'backgroundColor': 'green', 'color': 'white', 'textAlign': 'center', 'padding': '10px', 'gridArea': 'front-right'}),
                dbc.Button("IZQUIERDA", id='left-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'left'}),
                dbc.Button("ROTAR IZQUIERDA", id='rotate-left-btn', className='remote-btn rotate-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'rotate-left'}),
                dbc.Button("ROTAR DERECHA", id='rotate-right-btn', className='remote-btn rotate-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'rotate-right'}),
                dbc.Button("DERECHA", id='right-btn', className='remote-btn', style={'width': '100%', 'height': '100px', 'gridArea': 'right'}),
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
