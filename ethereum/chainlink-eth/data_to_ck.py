import os
from chainlink_feeds import ChainlinkFeeds
from .db.clickhouse import insert_data_table


def insert_data_to_ck(pair,network='mainnet'):

    cf = ChainlinkFeeds(rpc_env_var="RPC_URL")

    # Act
    data = cf.get_latest_round_data(network=network, pair=pair)
    table = os.environ.get('CLICKHOUSE_TABLE')
    insert_data_table(table,data)

