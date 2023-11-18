from data.bd import get_data
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

schema = os.environ.get('REDSHIFT_SCHEMA')

def get_dash_dataframe(page=None):
    
    location_df = get_data(f'{schema}.location')
    weather_df = get_data(f'{schema}.weather')
    temp_df = pd.merge(location_df, weather_df, left_on='id', right_on='location_id').drop('id_x', axis=1).rename(columns={'id_y': 'id'})
    
    if page == 'forecast':
        return temp_df
    
    elif page == 'trips':
        directions_df = get_data(f'{schema}.directions')
        # Merge on origin_id
        merged_df = pd.merge(directions_df, location_df, left_on='origin_id', right_on='id')
        merged_df = merged_df.rename(columns={'name': 'origin'})

        # Merge on destination_id
        routes_df = pd.merge(merged_df, location_df, left_on='destination_id', right_on='id', suffixes=('', '_destination'))
        routes_df = routes_df.rename(columns={'name': 'destination'})
        return temp_df, routes_df
    else:
        pass