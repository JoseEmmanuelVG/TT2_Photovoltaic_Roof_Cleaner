from dash import Dash, html, dcc

def create_layout():
    return html.Div([
        html.H1("Control del Robot"),
        html.Div([
            html.Div(id='status-div', style={'grid-area': 'status'}),  # Div para mensajes de estado
            html.Button('Adelante', id='forward-btn', style={'grid-area': 'forward'}),
            html.Button('Atrás', id='backward-btn', style={'grid-area': 'backward'}),
            html.Button('Izquierda', id='left-btn', style={'grid-area': 'left'}),
            html.Button('Derecha', id='right-btn', style={'grid-area': 'right'}),
            html.Button('Rotar Derecha', id='rotate-right-btn', style={'grid-area': 'rotate-right'}),
            html.Button('Rotar Izquierda', id='rotate-left-btn', style={'grid-area': 'rotate-left'}),
        ], style={
            'display': 'grid',
            'grid-template-areas': '''
                " . forward . "
                "left . right"
                "rotate-left . rotate-right"
                " . backward . "
                " . status . "
            ''',
            'grid-gap': '10px',
            'justify-content': 'center',
            'align-items': 'center',
            'padding': '20px'
        })
    ])

