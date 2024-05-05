from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        html.H1("Control Remoto del Robot", className="header-title"),
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Slider(0, 100, 5, value=50, id='motor-speed-slider', tooltip={"placement": "bottom", "always_visible": True}),
                    html.P("Velocidad de los motores", className="control-label")
                ], className="slider-container"), width=6),
                dbc.Col(html.Div([
                    dcc.Slider(0, 100, 5, value=50, id='brush-speed-slider', tooltip={"placement": "bottom", "always_visible": True}),
                    html.P("Velocidad del rodillo", className="control-label")
                ], className="slider-container"), width=6)
            ]),
            dbc.Row([
                dbc.Col(dbc.Button("Encender/Apagar rodillo", id="toggle-brush-btn", color="primary"), width=6),
                dbc.Col(dbc.Button("Expulsar/Parar agua", id="toggle-water-btn", color="primary"), width=6)
            ]),
            dbc.Row([
                dbc.Col(html.Div("Nivel de agua: 75%", id="water-level-display", className="sensor-display"), width=4),
                dbc.Col(html.Div("Nivel de batería: 60%", id="battery-level-display", className="sensor-display"), width=4),
                dbc.Col(html.Div("Inclinación: 5 grados", id="tilt-display", className="sensor-display"), width=4)
            ]),
            dbc.Row([
                dbc.Col(html.Div("Conexión Raspberry Pi: OK", id="pi-connection-status", className="connection-status"), width=6),
                dbc.Col(html.Div("Conexión WiFi: OK", id="wifi-connection-status", className="connection-status"), width=6)
            ]),
            html.Div([
                html.Button('Adelante', id='forward-btn', className='remote-btn', style={'gridArea': 'forward'}),
                html.Button('Atrás', id='backward-btn', className='remote-btn', style={'gridArea': 'backward'}),
                html.Button('Izquierda', id='left-btn', className='remote-btn', style={'gridArea': 'left'}),
                html.Button('Derecha', id='right-btn', className='remote-btn', style={'gridArea': 'right'}),
                html.Button('Rotar Derecha', id='rotate-right-btn', className='remote-btn rotate-btn', style={'gridArea': 'rotate-right'}),
                html.Button('Rotar Izquierda', id='rotate-left-btn', className='remote-btn rotate-btn', style={'gridArea': 'rotate-left'}),
                html.Button('Paro de Emergencia', id='emergency-stop-btn', className='emergency-btn', style={'gridArea': 'stop', 'backgroundColor': 'red', 'color': 'white'}),
                html.Button('Tomar Foto', id='capture-btn', className='capture-btn', style={'gridArea': 'capture', 'marginTop': '20px'}),
                html.Div(id='images-container', style={'gridArea': 'image', 'width': '100%', 'maxWidth': '600px', 'marginTop': '20px'}),
                html.Div(id='status-div', className='status-div', style={'gridArea': 'status', 'marginTop': '20px', 'textAlign': 'center'})
            ], style={
                'display': 'grid',
                'gridTemplateColumns': '1fr 1fr 1fr',
                'gridTemplateRows': 'auto auto auto auto',
                'gridTemplateAreas': '''
                    ". forward ."
                    "left . right"
                    ". backward ."
                    "rotate-left . rotate-right"
                    "capture capture capture"
                    ". stop ."
                    ". status ."
                    ". image ."
                ''',
                'gridGap': '10px',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }),
        ])
    ], style={'width': '100%', 'maxWidth': '900px', 'margin': '0 auto'})
