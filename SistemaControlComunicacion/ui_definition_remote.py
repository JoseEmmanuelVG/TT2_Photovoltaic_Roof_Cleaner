
from dash import html, dcc

def create_layout():
    return html.Div([
        html.H1("Control del Robot", style={'textAlign': 'center'}),
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
    ], style={'width': '100%', 'maxWidth': '600px', 'margin': '0 auto'})
