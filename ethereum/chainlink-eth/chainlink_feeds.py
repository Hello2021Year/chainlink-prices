import math
import os
from web3 import Web3
import configparser
import logging as log
from functools import wraps
from datetime import datetime
import json
import requests
import pandas as pd

def _rpc_url_formatter(func):
    @wraps(func)
    def _conversion_formating(self, *args, **kwargs):
        result_dict = func(self, *args, **kwargs)
        if self.time is not None:
            result_dict['time_stamp'] = datetime.fromtimestamp(
                result_dict['time_stamp']).strftime(self.time)
            result_dict['started_at'] = datetime.fromtimestamp(
                result_dict['started_at']).strftime(self.time)
        return result_dict
    return _conversion_formating


# def _handle_api_call(func):
#     @wrape
class ChainlinkFeeds(object):
    """ Base class where the decorators and base function for the other
    classes of this python wrapper will inherit from.

    TODO: Add The Graph for historical
    """

    def __init__(self, rpc_url=None, output_format='json', proxy=None, rpc_env_var=None, conversion='ether',
                 time='%Y-%m-%d %H:%M:%S'):
        """ Initialize the class
        Keyword Arguments:
            key:  rpc_url: The Ethereum Client node. This can be from node hosting services like infura, fiews, or quiknode.
            output_format:  Either 'json' or 'pandas'
            proxy:  Dictionary mapping protocol or protocol and hostname to the URL of the proxy.
        """
        self.rpc_url = rpc_url
        if rpc_url is not None or rpc_env_var is not None:
            if rpc_env_var is None:
                self.rpc_url = os.getenv('RPC_URL')
            else:
                self.rpc_url = os.getenv(rpc_env_var)
            if not self.rpc_url or not isinstance(self.rpc_url, str):
                raise ValueError(
                    'No value RPC_URL provided. Please set environment variable RPC_URL, ',
                    'provide an rpc_url as a keyword argument, or set your own environment',
                    ' variable name with rpc_env_var.')
            else:
                log.info(
                    'You have chosen the RPC_URL. You will only be able to get specific historical data. ')
        self.abis_config = configparser.ConfigParser()
        self.addresses_config = configparser.ConfigParser()
        self.decimals_config = configparser.ConfigParser()
        self.load_config(os.path.join(os.path.dirname(
            __file__), 'config', 'addresses.cfg'), abi_or_address='address')
        self.load_config(os.path.join(os.path.dirname(
            __file__), 'config', 'abis.cfg'), abi_or_address='abi')
        self.load_config(os.path.join(os.path.dirname(
            __file__), 'config', 'decimals.cfg'), abi_or_address='decimals')
        if self.rpc_url:
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.proxy = proxy or {}
        self.output_format = output_format
        self.conversion = conversion
        self.time = time
        self.base_url = 'https://api.thegraph.com/subgraphs/name/melonproject/chainlink'

    def get_latest_round_data(self, network='mainnet', pair='eth_usd', address=None, abi=None):
        """Pairs that end with ETH have 18 0s. All other pairs only have 10.
        We multiply them by 'bump' so they are all in wei before conversion.
        """
        if self.rpc_url is not None:
            return self.get_latest_round_data_rpc(network=network, pair=pair, address=address, abi=abi)
        else:
            raise ValueError('You must provide an RPC_URL to use this function. ')

    def get_historical_price(self, round_id=None, network='mainnet', pair='eth_usd', address=None, abi=None):
        """Pairs that end with ETH have 18 0s. All other pairs only have 10.
        We multiply them by 'bump' so they are all in wei before conversion.
        """
        if self.rpc_url is not None:
            return self.get_historical_price_rpc(round_id=round_id, network=network, pair=pair, address=address, abi=abi)
        else:
            raise ValueError('You must provide an RPC_URL to use this function. ')

    def _handle_output(self, response, column=None, set_index=None):
        if self.output_format == 'pandas':
            if column:
                df = pd.DataFrame(response['data'][column])
            else:
                df = pd.DataFrame(response['data'])
            if set_index:
                df = df.set_index(set_index)
            return df
        else:
            if column:
                return response['data'][column]
            return response['data']

    @staticmethod
    def convert_pair_format(pair):
        pair = pair.upper()
        if "_" in pair:
            return pair.replace("_", "/")
        return pair

    """
    The functions below are ment specifically for those who want to use the RPC_URL instead of the query from The Graph.
    """

    def load_config(self, config_path, abi_or_address='abi'):
        if abi_or_address.lower() == 'abi':
            self.abis_config.read(config_path)
        elif abi_or_address.lower() == 'address':
            self.addresses_config.read(config_path)
        else:
            self.decimals_config.read(config_path)

    def get_manual_addresses(self):
        return json.loads(json.dumps(self.addresses_config._sections))

    def get_manual_abis(self):
        return json.loads(json.dumps(self.abis_config._sections))

    def get_manual_decimalss(self):
        return json.loads(json.dumps(self.decimals_config._sections))

    @_rpc_url_formatter
    def get_historical_price_rpc(self, round_id, network='mainnet', pair='eth_usd', address=None, abi=None):
        """Pairs that end with ETH have 18 0s. All other pairs only have 10.
        We multiply them by 'bump' so they are all in wei before conversion.
        """
        if address is None:
            address = self.addresses_config[network.lower()][pair]
        if abi is None:
            abi = self.abis_config['default']['aggregatorv3interfaceabi']
        price_feed_contract = self.web3.eth.contract(address=address, abi=abi)
        latest_data = price_feed_contract.functions.getRoundData(
            round_id).call()
        result_dict = {'round_id': latest_data[0], 'price': latest_data[1]/math.pow(10,int(self.decimals_config[network.lower()][pair])),
                       'started_at': latest_data[2], 'time_stamp': latest_data[3], 'answered_in_round': latest_data[4]}
        return result_dict

    @_rpc_url_formatter
    def get_latest_round_data_rpc(self, network='mainnet', pair='eth_usd', address=None, abi=None):
        """Pairs that end with ETH have 18 0s. All other pairs only have 10.
        We multiply them by 'bump' so they are all in wei before conversion.
        """
        if address is None:
            address = self.addresses_config[network.lower()][pair]
        if abi is None:
            abi = self.abis_config['default']['aggregatorv3interfaceabi']
        price_feed_contract = self.web3.eth.contract(address=address, abi=abi)
        latest_data = price_feed_contract.functions.latestRoundData().call()
        result_dict = {'round_id': latest_data[0], 'price': latest_data[1]/math.pow(10,int(self.decimals_config[network.lower()][pair])),
                       'started_at': latest_data[2], 'time_stamp': latest_data[3], 'answered_in_round': latest_data[4]}
        return result_dict
