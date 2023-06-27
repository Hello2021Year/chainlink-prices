import pytest
from web3 import Web3
import math
# Change this to use your own Infura ID

aggregatorv3interfaceabi = [{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
# USDT/USD
usdt_addr = '0x3E7d1eAB13ad0104d2750B8863b489D65364e32D'

# USDC/USD
usdc_addr = '0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6'

# ETH/USD
eth_addr = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'



@pytest.mark.parametrize(
    "address, abi",
    [
        (usdt_addr,aggregatorv3interfaceabi),
        (usdc_addr,aggregatorv3interfaceabi),
        (eth_addr,aggregatorv3interfaceabi),
    ]
)
def test_decode(address, abi):
    w3 = Web3(Web3.HTTPProvider('https://still-virulent-dew.quiknode.pro/921d07e9c4bc2c5dc3689daacc5da9083875f9a6/'))
    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    historicalData = contract.functions.latestRoundData().call()
    print(historicalData)
    assert len(historicalData) == 5