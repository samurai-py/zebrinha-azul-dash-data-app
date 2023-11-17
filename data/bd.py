import os
from dotenv import load_dotenv
import redshift_connector
import pandas as pd

load_dotenv()

def get_data(table_name):
    try:
        conn = redshift_connector.connect(
            host=os.environ.get('REDSHIFT_HOST'),
            database=os.environ.get('REDSHIFT_DBNAME'),
            user=os.environ.get('REDSHIFT_USER'),
            password=os.environ.get('REDSHIFT_PASSWORD'),
            port=int(os.environ.get('REDSHIFT_PORT'))
        )

        cursor = conn.cursor()

        # Utilize placeholders para evitar SQL injection
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)

        # Fetch DataFrame
        table_data = cursor.fetch_dataframe()

        return table_data

    except Exception as e:
        print(f"Erro ao conectar ou executar consulta no banco de dados Redshift: {str(e)}")
        return None

    finally:
        cursor.close()
        conn.close()
        
