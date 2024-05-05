from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Robot Limpiador de Techos Fotovoltaicos UPIITA", className="autonomous-title"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Control y monitoreo del robot en UPIITA", className="section-title"),
                    html.P([html.Strong("Nivel de Agua:"), " 75%"], className="status-text"),
                    html.P([html.Strong("Nivel de Batería:"), " 60%"], className="status-text"),
                    html.P([html.Strong("Inclinación:"), " 5 grados"], className="status-text"),
                    html.P([html.Strong("Status:"), " Operando"], className="status-text"),
                    dbc.Button("Inicio", color="success", className="mr-2 control-button"),
                    dbc.Button("Paro", color="danger", className="control-button")
                ], width=6),
                dbc.Col([
                    html.H4("Configuración del Usuario", className="section-title"),
                    dbc.Checklist(
                        options=[{"label": " Agua", "value": 1}],
                        value=[],
                        id="watered-toggle",
                        switch=True,
                        className="checklist-item"
                    ),
                    html.P("Número de Ciclos:"),
                    dcc.Input(type="number", value=2, min=1, max=10, step=1, className="input-pink"),
                    html.P("Velocidad de Cepillos:"),
                    dcc.Input(type="number", value=100, min=50, max=200, step=10, className="input-pink"),
                    html.P("Velocidad de Ruedas:"),
                    dcc.Input(type="number", value=50, min=10, max=100, step=10, className="input-pink"),
                    dbc.Button("Actualizar", color="pink", className="mt-2 control-button")
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col(dbc.Button("Regresar al Menú", href="/menu", color="secondary", className="menu-control left-button"), className="col-1"),
                dbc.Col(dbc.Button("Cerrar Sesión", href="/logout", color="danger", className="menu-control right-button"), className="col-1 offset-10")
            ], className="top-row-buttons"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H4("Última Imagen Capturada", className="image-title"),
                    html.Div(id="image-container", className="image-box")
                ], className="image-section"), width=12)
            ])
        ], fluid=True)
    ])
