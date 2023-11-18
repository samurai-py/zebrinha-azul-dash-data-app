import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

with open('assets/zebra.md', 'r', encoding='utf-8') as f:
    markdown_text = f.read()
    
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Markdown(markdown_text)
                ])
            ], className='w-100')  # Adiciona a classe w-100 aqui
            
        ], className='d-flex justify-content-center')
    ])
], className='d-flex justify-content-center', fluid=True, style={'width': '80%', 'height': '100%'})
