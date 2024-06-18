from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Robot Limpiador de Techos Fotovoltaicos UPIITA", className="autonomous-title"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Control y monitoreo del robot en UPIITA", className="section-title"),
                    html.P([html.Strong("Nivel de Agua:"), " Lleno"], id='water-level', className="status-text"),
                    html.P([html.Strong("Nivel de Batería:"), " 60%"], className="status-text"),
                    html.P([html.Strong("Inclinación:"), " 5 grados"], className="status-text"),
                    html.P([html.Strong("Conexión Wi-Fi:"), html.Span(" Conectado", id="wifi-status", className="wifi-connected")], className="status-text"),
                ], width=6),
                dbc.Col([
                    html.H4("Configuración del Usuario", className="section-title"),
                    dbc.Checklist(
                        options=[{"label": html.Span("Agua", style={"color": "white"}), "value": 1}],
                        value=[],
                        id="watered-toggle",
                        switch=True,
                        className="checklist-item"
                    ),
                    html.P("Velocidad de Ruedas:", style={"color": "white"}),
                    dcc.Input(type="number", value=100, min=50, max=200, step=10, className="input-pink", id='wheel-speed'),
                    html.P("Velocidad de Cepillos:", style={"color": "white"}),
                    dcc.Input(type="number", value=50, min=10, max=100, step=10, className="input-pink", id='brush-speed'),
                    dbc.Button("Encender Rodillo", id="start-roller-button", color="info", className="control-button"),
                    dbc.Button("Parar Rodillo", id="stop-roller-button", color="warning", className="control-button"),
                    dbc.Row([
                        dbc.Col(dbc.Button("Iniciar Limpieza", id="start-cleaning-button", color="primary", className="mt-4 start-cleaning-button"), width=6),
                        dbc.Col(dbc.Button("Parar Limpieza", id="stop-cleaning-button", color="danger", className="mt-4 stop-cleaning-button"), width=6),
                    ]),
                    html.Div(id='status-div', className="status-text"),  # Div para mostrar el estado de limpieza iniciada
                    html.Div(id='status-div-stop', className="status-text"),  # Div para mostrar el estado de limpieza detenida
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H4("Información de Sensores Ultrasónicos", className="section-title"),
                    html.Div(id='sensor-values', children=[
                        dbc.Row([
                            dbc.Col([
                                html.P([html.Strong("Delante Izquierdo:"), " 50 cm"], className="status-text", id='front-left'),
                                html.P([html.Strong("Detrás Izquierdo:"), " 50 cm"], className="status-text", id='rear-left'),
                            ], width=3),
                            dbc.Col([
                                html.P([html.Strong("Delante Derecho:"), " 50 cm"], className="status-text", id='front-right'),
                                html.P([html.Strong("Detrás Derecho:"), " 50 cm"], className="status-text", id='rear-right'),
                            ], width=3),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.P([html.Strong("Medio Izquierdo:"), " 50 cm"], className="status-text", id='middle-left'),
                            ], width=3),
                            dbc.Col([
                                html.P([html.Strong("Medio Derecho:"), " 50 cm"], className="status-text", id='middle-right'),
                            ], width=3),
                        ]),
                        html.H4("Información del sensor de Temperatura y Divisor", className="section-title"),
                        dbc.Row([
                            dbc.Col([
                                html.P([html.Strong("Humedad:"), " 25.10%"], className="status-text", id='sensor-humidity'),
                            ], width=3),
                            dbc.Col([
                                html.P([html.Strong("Temperatura:"), " 34.00°C"], className="status-text", id='sensor-temperature'),
                            ], width=3),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.P([html.Strong("Voltaje:"), " 0.72 V"], className="status-text", id='voltage'),
                            ], width=3),
                        ]),
                    ])
                ]), width=6)
            ]),
            dbc.Row([
                dbc.Col(dbc.Button("Regresar al Menú", href="/menu", color="secondary", className="menu-control left-button"), className="col-1"),
                dbc.Col(dbc.Button("Paro de Emergencia", href="/logout", color="danger", className="menu-control right-button"), className="col-1 offset-10")
            ], className="top-row-buttons"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H4("Última Imagen Capturada", className="image-title"),
                    html.Div(id="image-container", className="image-box")
                ], className="image-section"), width=12)
            ]),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # Actualiza cada segundo
                n_intervals=0
            )
        ], fluid=True)
    ])
