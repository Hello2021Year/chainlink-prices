import pytest
import os
import clickhouse_connect
import pandas as pd
from ..db.clickhouse import init_clickhouse_client

table = 'base_block_serials'
start = 10
end = 100
label = '{}_{}'.format(start, end)


@pytest.mark.parametrize(
    "table,label,start,end",
    [
        (table, label,start, end),
    ]
)



def test_insert_db(table,label,start,end):
    client = init_clickhouse_client()

    # Assuming you have a list of dictionaries or a dictionary with the data
    data = [
        {'label': label, 'start': start, 'end': end},
    ]

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    result = client.insert_df(table,df)
    assert result == None
