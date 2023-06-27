# content of conftest.py
import pytest
from chainlink_feeds import ChainlinkFeeds

RPC_URL = 'https://still-virulent-dew.quiknode.pro/921d07e9c4bc2c5dc3689daacc5da9083875f9a6/'

@pytest.fixture
def get_test_abi():
    return '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'  # noqa


@pytest.fixture
def get_test_address():
    return '0x9326BFA02ADD2366b30bacB125260Af641031331'


def test_get_latest_round_data():
    # Arrange
    network = 'mainnet'
    pair = 'eth_usd'
    cf = ChainlinkFeeds(rpc_env_var="RPC_URL")

    # Act
    result = cf.get_latest_round_data(network=network, pair=pair)

    # Assert
    assert isinstance(result, dict)


def test_get_historical_price():
    # Arrange
    network = 'mainnet'
    pair = 'eth_usd'
    round_id = 18446744073709556747
    cf = ChainlinkFeeds(rpc_env_var="RPC_URL")

    # Act
    result = cf.get_historical_price(round_id, network=network, pair=pair)
    print(result)

    # Assert
    assert isinstance(result, dict)

