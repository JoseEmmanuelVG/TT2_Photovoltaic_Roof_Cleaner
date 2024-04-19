from dash import Dash, html, dcc

def create_layout():
    return html.Div([
        html.H1("Control del Robot", style={'text-align': 'center'}),
        html.Div([
            html.Button('Adelante', id='forward-btn', style={'grid-area': 'forward'}),
            html.Button('Atrás', id='backward-btn', style={'grid-area': 'backward'}),
            html.Button('Izquierda', id='left-btn', style={'grid-area': 'left'}),
            html.Button('Derecha', id='right-btn', style={'grid-area': 'right'}),
            html.Button('Rotar Derecha', id='rotate-right-btn', style={'grid-area': 'rotate-right'}),
            html.Button('Rotar Izquierda', id='rotate-left-btn', style={'grid-area': 'rotate-left'}),
            html.Button('Paro de Emergencia', id='emergency-stop-btn', style={'grid-area': 'stop', 'background-color': 'red', 'color': 'white'}),
            html.Div(id='status-div', style={'grid-area': 'status', 'margin-top': '20px', 'text-align': 'center'})
        ], style={
            'display': 'grid',
            'grid-template-columns': '1fr 1fr 1fr',
            'grid-template-rows': 'auto auto auto auto',
            'grid-template-areas': '''
                ". forward ."
                "left . right"
                ". backward ."
                "rotate-left . rotate-right"
                ". stop ."
                ". status ."
            ''',
            'grid-gap': '10px',
            'justify-content': 'center',
            'align-items': 'center',
            'padding': '20px'
        }),
    ], style={'width': '100%', 'max-width': '600px', 'margin': '0 auto'})
