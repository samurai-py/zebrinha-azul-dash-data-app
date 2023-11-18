import dash
from dash import dash_table
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from urllib.request import urlopen
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data.query import get_dash_dataframe


dash.register_page(__name__)

load_figure_template('bootstrap')

with urlopen('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-35-mun.json') as response:
    geojson = json.load(response)
    
with open('utils/weather_cols_pt-br.json', encoding='utf-8') as f:
    cols_ptbr = json.load(f)['translations']

df_raw = get_dash_dataframe('forecast')

df = df_raw.loc[df_raw['name'] != 'Recife'].reset_index(drop=True)

df_ptbr_full = df.copy()
df_ptbr = df_ptbr_full.sort_values('created_at', ascending=False)
df_ptbr.drop(columns=['record_id', 'id','lat', 'lon', 'location_id', 'updated_at', 'row_num'], inplace=True)
df_ptbr.rename(columns=cols_ptbr, inplace=True)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1([html.Strong("Previsão do Tempo")]),
                    dcc.Dropdown(
                        id='location-dropdown',
                        options=[{'label': name, 'value': name} for name in df['name'].unique()],
                        value=df['name'][0],
                        style={'width': '100%'}
                    ),
                    dbc.Card([
                        dbc.CardBody([
                            html.P('Precipitação (mm): ', id='precip_mm'),
                            html.P('Umidade (%): ', id='humidity'),
                            html.P('Condição do Clima: ', id='condition'),
                            html.P('Velocidade do Vento (mph): ', id='wind_mph'),
                            html.P('Dia ou Noite: ', id='is_day'),
                        ])
                    ], style={'marginTop': '20px', 'backgroundColor': 'white'}),
                    dbc.Row([
                        html.Img(id='weather-icon',src='/assets/logo.svg', height='100%', className='clickable-logo', style={'margin-top': '20px'})
                    ])
                ])
            ], style={'height': '100%'}),        
        ], md=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='gauge-plot', figure={}),
                ], md=6),
                dbc.Col([
                    dcc.Graph(id='map-plot', figure={}, style={'height': '100%'}),
                ], md=6)
            ]),
            dbc.Row([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_ptbr.columns],
                    page_size=10,
                    sort_action='native',
                    style_table={'overflowX': 'auto'}
                ),
            ], style={'marginTop': '20px'}),
        ], md=10),
    ]),
], fluid=True)

# Callback para o mapa
@dash.callback(
    Output('map-plot', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_map_plot(selected_location):
    selected_row = df[df['name'] == selected_location]
    
    # Verifique se 'temp_c' existe e não contém NaN
    assert 'temp_c' in selected_row.columns
    assert not selected_row['temp_c'].isna().any()
    
    fig = px.choropleth_mapbox(
        selected_row,
        geojson=geojson,
        featureidkey='properties.name',
        title='Mapa de Temperatura',
        locations='name',
        color='temp_c',
        hover_name='name',
        zoom=6.5,
        center=dict(lat=-22.966224, lon=-45.465454),
        opacity=0.5,
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'temp_c':'°C'} 
    )
    fig.update_layout(
        title_x=0.5,
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ]
    )
    return fig

# Callback para o gráfico de gauge
@dash.callback(
    Output('gauge-plot', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_gauge_plot(selected_location):
    selected_row = df[df['name'] == selected_location].sort_values('created_at', ascending=False)
    value = selected_row['temp_c'].values[0]
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': "Termômetro"},
        gauge = {'axis': {'range': [None, 60]}}
    ))
    return fig

# Callback para a tabela
@dash.callback(
    Output('table', 'data'),
    [Input('location-dropdown', 'value')]
)
def update_table(selected_location):
    filtered_df = df_ptbr[df_ptbr['Cidade'] == selected_location]
    return filtered_df.to_dict('records')

@dash.callback(
    [Output('precip_mm', 'children'),
     Output('humidity', 'children'),
     Output('condition', 'children'),
     Output('wind_mph', 'children'),
     Output('is_day', 'children')],
    [Input('location-dropdown', 'value')]
)
def update_card_info(selected_location):
    selected_row = df[df['name'] == selected_location].sort_values('created_at', ascending=False).iloc[0]
    precip_mm = ['Precipitação (mm): ', html.Strong(selected_row['precip_mm'])]
    humidity = ['Umidade (%): ', html.Strong(selected_row['humidity'])]
    condition = ['Condição do Clima: ', html.Strong(selected_row['condition'])]
    wind_mph = ['Velocidade do Vento (mph): ', html.Strong(selected_row['wind_mph'])]
    is_day = ['Dia ou Noite: ', html.Strong('Dia' if selected_row['is_day'] else 'Noite')]
    return precip_mm, humidity, condition, wind_mph, is_day

@dash.callback(
    Output('weather-icon', 'src'),
    [Input('location-dropdown', 'value')]
)
def update_icon(selected_location):
    selected_row = df[df['name'] == selected_location].sort_values('created_at', ascending=False).iloc[0]
    is_day = selected_row['is_day']
    if is_day:
        return '/assets/sol.svg'
    else:
        return '/assets/lua.svg'