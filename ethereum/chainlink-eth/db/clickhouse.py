import clickhouse_connect
import os
import pandas as pd

def init_clickhouse_client():
    # Retrieve the values from os.environ if available, otherwise fallback to config.get()
    clickhouse_config = {
        'host': os.environ.get('CLICKHOUSE_HOST'),
        'port': int(os.environ.get('CLICKHOUSE_PORT')),
        'user': os.environ.get('CLICKHOUSE_USER'),
        'password': os.environ.get('CLICKHOUSE_PASSWORD'),
        'database': os.environ.get('CLICKHOUSE_DATABASE'),
    }

    client = clickhouse_connect.get_client(**clickhouse_config)
    return client

def insert_data_table(table,data):
    client = init_clickhouse_client()


    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    try:
        client.insert_df(table,df)
    except Exception as e:
        print(e)
        raise ValueError("Insertion failed")


