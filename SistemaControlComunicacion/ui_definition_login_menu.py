# ui_definition_login_menu.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def login_layout():
    return dbc.Container([
        dbc.Row(dbc.Col(html.H2(
            "TT2 ROBOT MÓVIL CON DESPLAZAMIENTO AUTÓNOMO PARA LA LIMPIEZA DE TECHOS SOLARES FOTOVOLTAICOS", 
            className="robot-title text-center mb-5"), width=12)),
        html.Div([  # Encapsulating the login form for transparency
            dbc.Row(dbc.Col(html.Div(
                "Inicio de Sesión", 
                className="login-title h3 mb-3 font-weight-bold text-center"), width=12)),
            dbc.Row(dbc.Col(dbc.Input(
                type="text", 
                placeholder="Usuario", 
                id="username-login", 
                className="login-input mb-3"), width=12)),
            dbc.Row(dbc.Col(dbc.Input(
                type="password", 
                placeholder="Contraseña", 
                id="password-login", 
                className="login-input mb-3"), width=12)),
            dbc.Row(dbc.Col(dbc.Button(
                "Ingresar", 
                id="login-button", 
                n_clicks=0, 
                className="login-button btn-lg btn-block"), width=12)),
            dbc.Row(dbc.Col(html.Div(
                id="login-status"), width=12))
        ], className="login-container")
    ])

def menu_layout():
    return html.Div([
        html.H3('Seleccione el modo de operación', className="menu-title"),
        html.Div([
            dbc.Button("Desplazamiento Autónomo", href="/automatic", color="primary", className="menu-button btn-lg"),
            html.P('''
                Realiza la limpieza de techos solares mediante configuraciones preestablecidas, incluyendo la opción de limpieza en seco o con agua según sea necesario.
                Monitoreo en tiempo real del estado del robot, niveles de agua y batería, y progreso del proceso de limpieza.
            ''', className="menu-description"),
        ], style={'textAlign': 'center'}),
        html.Div([
            dbc.Button("Control Remoto", href="/remote", color="secondary", className="menu-button btn-lg"),
            html.P('''
                Permite el control manual del robot para operaciones específicas o manejo directo. Incluye visualización de la cámara y sensores; Asi como control manual de movimientos.
            ''', className="menu-description"),
        ], style={'textAlign': 'center'}),
    ], style={'textAlign': 'center', 'marginTop': '50px'})