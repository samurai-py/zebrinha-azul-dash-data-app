import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd

from data.query import get_dash_dataframe

dash.register_page(__name__)

df_temp_raw, df_routes_raw  = get_dash_dataframe('trips')
df_temp = df_temp_raw.reset_index(drop=True)
df_routes = df_routes_raw.loc[df_routes_raw['record_id'] == df_routes_raw['record_id'].max()].reset_index(drop=True)

css_dict_h2 = {
    'height': '15%', 
    'textAlign': 'center',
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center',
    'marginTop': '80px'
}

css_dict_h4 = {
    'textAlign': 'center',
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center',
    'marginTop': '0'
}

css_dict_card = {
    'backgroundColor': 'white',
    'height': '100%',
    'width': '100%',
    'margin': '0',
    'padding': '0'
}

def create_location_layout(id_prefix, default_value, css_h2_pattern=None, css_h4_pattern=None,css_card_pattern=None):
    return dbc.Card([
    dcc.Dropdown(
        id=f'{id_prefix}-location-dropdown',
        options=[{'label': origin, 'value': origin} for origin in df_routes['origin'].unique()],
        value=default_value,
        style={'width': '100%'}
    ),
    html.H1(id=f'{id_prefix}-location-name', children=default_value, style={'textAlign': 'center', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2(id=f'{id_prefix}-precip_mm', style=css_h2_pattern),
                html.H4('Precipitação (mm)', style=css_h4_pattern)
            ], body=True, style=css_card_pattern),
        ], style={'flex': '1'}),
        dbc.Col([
            dbc.Card([
                html.H2(id=f'{id_prefix}-humidity', style=css_h2_pattern),
                html.H4('Umidade (%)', style=css_h4_pattern),
            ], body=True, style=css_card_pattern),
        ], style={'flex': '1'}),
    ], style={'flex': '1'}, className='g-0'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2(id=f'{id_prefix}-condition', style=css_h2_pattern),
                html.H4('Condição do Clima', style=css_h4_pattern)
            ], body=True, style=css_card_pattern),
        ], style={'flex': '1'}),
        dbc.Col([
            dbc.Card([
                html.H2(id=f'{id_prefix}-wind_mph', style=css_h2_pattern),
                html.H4('Velocidade do Vento (mph)', style=css_h4_pattern)
            ], body=True, style=css_card_pattern),
        ], style={'flex': '1'}),
    ], style={'flex': '1'}, className='g-0'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2(id=f'{id_prefix}-is_day', style=css_h2_pattern),
                html.H4('Dia ou Noite', style=css_h4_pattern)
            ], body=True, style=css_card_pattern),
        ], style={'flex': '1'}),
    ], style={'flex': '1'}, className='g-0'),
], style={'backgroundColor': 'white', 'height': '100%', 'display': 'flex', 'flexDirection': 'column'})

first_location_layout = create_location_layout('first', df_routes['origin'][0], css_h2_pattern=css_dict_h2, css_h4_pattern=css_dict_h4,css_card_pattern=css_dict_card)
second_location_layout = create_location_layout('second', df_routes['origin'][1] if len(df_routes['origin'].unique()) > 1 else None, css_h2_pattern=css_dict_h2, css_h4_pattern=css_dict_h4,css_card_pattern=css_dict_card)

layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([                   
                    dbc.Col(children=[
                        html.H1([html.Strong("Guia de Viagens")]),
                        dbc.Card([
                            dbc.CardBody([
                                html.H4(html.Strong('Informações da rota:')),
                                html.Br(),
                                html.P('Origem: ', id='new-origin'),
                                html.P('Destino: ', id='new-destination'),
                                html.P('Distância: ', id='new-distance'),
                                html.P('Tempo estimado: ', id='new-trip_long'),
                            ], style={'marginTop': '20px', 'backgroundColor': 'white'})
                        ]),
                        html.Img(id='new-weather-icon',src='/assets/logo.svg', height='100%', className='clickable-logo', style={'margin-top': '20px'}),
                    ])
                ])
            ])
        ], md=2),              
        dbc.Col([
            first_location_layout
        ], md=5),
        dbc.Col([
            second_location_layout
        ], md=5)
    ])
])


# Callback to update the options of the second dropdown
@dash.callback(
    Output('second-location-dropdown', 'options'),
    [Input('first-location-dropdown', 'value')]
)
def update_second_dropdown(selected_location):
    options = [{'label': origin, 'value': origin} for origin in df_routes['origin'].unique() if origin != selected_location]
    return options

@dash.callback(
    Output('first-location-name', 'children'),
    [Input('first-location-dropdown', 'value')]
)
def update_location_name(value):
    return value

@dash.callback(
    Output('second-location-name', 'children'),
    [Input('second-location-dropdown', 'value')]
)
def update_location_name(value):
    return value


@dash.callback(
    [Output('first-precip_mm', 'children'),
     Output('first-humidity', 'children'),
     Output('first-condition', 'children'),
     Output('first-wind_mph', 'children'),
     Output('first-is_day', 'children')],
    [Input('first-location-dropdown', 'value')]
)
def update_first_location_info(selected_location):
    
    selected_row = df_temp[df_temp['name'] == selected_location].sort_values('created_at', ascending=False).iloc[0]
    
    precip_mm = [html.Strong(selected_row['precip_mm'])]
    humidity = [html.Strong(selected_row['humidity'])]
    condition = [html.Strong(selected_row['condition'])]
    wind_mph = [html.Strong(selected_row['wind_mph'])]
    is_day = [html.Strong('Dia' if selected_row['is_day'] else 'Noite')]
    
    return precip_mm, humidity, condition, wind_mph, is_day
    
    
@dash.callback(
    [Output('second-precip_mm', 'children'),
     Output('second-humidity', 'children'),
     Output('second-condition', 'children'),
     Output('second-wind_mph', 'children'),
     Output('second-is_day', 'children')],
    [Input('second-location-dropdown', 'value')]
)
def update_first_location_info(selected_location):
    
    selected_row = df_temp[df_temp['name'] == selected_location].sort_values('created_at', ascending=False).iloc[0]
    
    precip_mm = [html.Strong(selected_row['precip_mm'])]
    humidity = [html.Strong(selected_row['humidity'])]
    condition = [html.Strong(selected_row['condition'])]
    wind_mph = [html.Strong(selected_row['wind_mph'])]
    is_day = [html.Strong('Dia' if selected_row['is_day'] else 'Noite')]
    
    return precip_mm, humidity, condition, wind_mph, is_day
    
    
@dash.callback(
    [Output('new-origin', 'children'),
     Output('new-destination', 'children'),
     Output('new-distance', 'children'),
     Output('new-trip_long', 'children')],
    [Input('first-location-dropdown', 'value'),
     Input('second-location-dropdown', 'value')]
)
def update_trip_info(origin, destination):
    
    if origin == destination:
        return ["Origem: ", "Destino: ", "Distância: ", "Tempo estimado: "]
    
    selected_row = df_routes[(df_routes['origin'] == origin) & (df_routes['destination'] == destination)].sort_values('created_at', ascending=False).iloc[0]
    origin_info = ["Origem: ", html.Strong(selected_row['origin'])]
    destination_info = ["Destino: ", html.Strong(selected_row['destination'])]
    distance_info = ["Distância: ", html.Strong(selected_row['distance'])]
    trip_long_info = ["Tempo estimado: ", html.Strong(selected_row['trip_long'])]
    
    return origin_info, destination_info, distance_info, trip_long_info