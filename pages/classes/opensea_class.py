import datetime
import os
import time

import aiohttp
import requests
import pandas as pd
import json
import logging
import asyncio
import pages.config.opensea_config as default

from typing import Optional
from utils.utils import assertType


class Opensea:
    """
    The Parent Class which defines all the params and common function used by all child classes
    """

    def __init__(self):
        """
        Define the static types that will be used in the app
        """

        # scraper params
        self.account_address_type = (str, type(None))
        self.api_key_type = (str, type(None))
        self.asset_contract_address_type = (str, type(None))
        self.asset_contract_addresses_type = (str, type(None))
        self.asset_owner_type = (str, type(None))
        self.auction_type_type = (str, type(None))
        self.auction_type_conditions = ['english', 'dutch', 'min-price', None]
        self.collection_type = (str, type(None))
        self.collection_slug_type = (str, type(None))
        self.event_type_type = (str, type(None))
        self.event_type_conditions = ['created', 'successful', 'cancelled', 'bid_entered', 'bid_withdrawn', 'transfer',
                                      'approve', None]
        self.limit_type = int
        self.limit_type_conditions = range(1, 51)
        self.occurred_after_type = (str, type(None))
        self.occurred_before_type = (str, type(None))
        self.offset_type = int
        self.offset_type_conditions = range(0, 10000)
        self.on_sale_type = (bool, type(None))
        self.only_opensea_type = bool
        self.order_by_type = (str, type(None))
        self.order_by_conditions = ['token_id', 'sale_date', 'sale_count', 'sale_price', None]
        self.order_direction_type = str
        self.order_direction_conditions = ['asc', 'desc']
        self.owner_type = (str, type(None))
        self.token_id_type = (str, type(None))
        self.token_ids_type = (str, type(None))

        # app params
        # self.params shall be a list of dicts, each containing the key-value pair tagged to a particular url loop
        self.temp_url = ''
        self.URLs = []
        self.endpoint = ''
        self.response_frame = pd.DataFrame()
        self.responses = []

    def loadAndSendPayload(self):
        """
        Loads up the requests and prepares them for asynchronous request sending
        """
        os.system(f'python utils/async_requests.py {self.URLs}')

    def resetAll(self):
        """
        Function to quickly reset all the relevant class attributes in the deinit or reset process
        """

        self.temp_url = ''
        self.URLs = []
        self.response_frame = pd.DataFrame()
        self.responses = []


class Assets(Opensea):
    """
    Class to API calls for Opensea Assets
    """

    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/assets'

    def setAssetParameters(self,
                           owner: Optional[str] = None,
                           token_ids: Optional[list] = None,
                           asset_contract_address: Optional[str] = None,
                           asset_contract_addresses: Optional[list] = None,
                           order_by: Optional[str] = None,
                           order_direction: str = 'desc',
                           offset: int = 0,
                           limit: int = 20,
                           collection: Optional[str] = None,
                           api_key: Optional[str] = None
                           ):
        """
        Gets and sets the variables for the OpenseaAsset class; setting parameters are separate from __init__ so that
        users can conduct multiple queries by getting the maximum number of API calls permitted for Opensea.io, which
        requires this function so that the requests can be sent and obtained asynchronously

        Initial call of the class will not set the variables per default as defined in opensea_config. You must set
        the parameters of the function manually through setParameters. This is to ensure that async works perfectly,
        and that your final url list consists of only parameters you want to parse, and not unwanted parameters from
        the initial call to the class

        :param owner:                               The address of the owner of the assets
        :param token_ids:                           An array of token IDs to search for
        :param asset_contract_address:              The NFT contract address for the assets
        :param asset_contract_addresses:            An array of contract addresses to search for
        :param order_by:                            How to order the assets returned, accepts token_id, sale_date,
                                                    sale_count and sale_price as arugments
        :param order_direction:                     Accepts asc or desc as arguments (asc for Ascending and desc for
                                                    Descending)
        :param offset:                              Offset value (refers to the page where you want to extract data
                                                    from)
        :param limit:                               Limit value, defaults to 20 but limited to 50
        :param collection:                          Limit responses to members of a collection
        :param api_key:                             API Key
        """

        param = {}
        temp = ''

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.token_ids_type, token_ids):
            if token_ids is not None:
                param['token_ids'] = token_ids

        if assertType(self.asset_contract_address_type, asset_contract_address):
            if asset_contract_addresses is None:
                if asset_contract_address is not None:
                    param['asset_contract_address'] = asset_contract_address
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if assertType(self.asset_contract_addresses_type, asset_contract_addresses):
            if asset_contract_address is None:
                if asset_contract_addresses is not None:
                    param['asset_contract_addresses'] = asset_contract_addresses
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if assertType(self.order_by_type, order_by, conditions=self.order_by_conditions):
            if order_by is not None:
                param['order_by'] = order_by

        if assertType(self.order_direction_type, order_direction,
                      conditions=self.order_direction_conditions):
            if order_direction is not None:
                param['order_direction'] = order_direction.lower().strip()

        if assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            param['offset'] = offset

        if assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            param['limit'] = limit

        if assertType(self.collection_type, collection):
            if collection is not None:
                param['collection'] = collection

        if assertType(self.api_key_type, api_key):
            if api_key is not None:
                param['X-API-KEY'] = api_key

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseResponse(self, timeout: int = 600):
        """
        This parses the response object obtained from loadAndSendPayload()

        :return:                        Complete Pandas DataFrame
        """

        counter = 0
        base_filepath = os.path.join(os.getcwd(), 'dumps', 'data_dumps.json')

        try:
            if os.path.exists(base_filepath):
                with open(f'{base_filepath}', 'r') as f:
                    data = json.load(f)
                    self.responses = data

                main_list = []

                for dict_item in self.responses:
                    main_list.extend(dict_item['assets'])

                self.response_frame = pd.DataFrame(data=main_list).astype(str)
            else:
                time.sleep(1)
                counter += 1

            if counter > timeout:
                raise TimeoutError('Error: File cannot be created. Try again.')

        except Exception as ex:
            raise ex


class Events(Opensea):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/events'

    def setEventsParameters(self,
                            asset_contract_address: Optional[str] = None,
                            collection_slug: Optional[str] = None,
                            token_id: Optional[int] = None,
                            account_address: Optional[str] = None,
                            event_type: Optional[str] = None,
                            only_opensea: bool = False,
                            auction_type: Optional[str] = None,
                            offset: int = 0,
                            limit: int = 20,
                            occurred_before: Optional[str] = None,
                            occurred_after: Optional[str] = None,
                            api_key: Optional[str] = None):
        """
        Gets and sets the variables for the OpenseaEvents class; setting parameters are separate from __init__ so that
        users can conduct multiple queries by getting the maximum number of API calls permitted for Opensea.io, which
        requires this function so that the requests can be sent and obtained asynchronously

        Initial call of the class will not set the variables per default as defined in opensea_config. You must set
        the parameters of the function manually through setParameters. This is to ensure that async works perfectly,
        and that your final url list consists of only parameters you want to parse, and not unwanted parameters from
        the initial call to the class

        :param asset_contract_address:              The NFT contract address for the assets for which to show events
        :param collection_slug:                     Limit responses to events from a collection
        :param token_id:                            The token's id to optionally filter by
        :param account_address:                     A user account's wallet address to filter for events on an account
        :param event_type:                          The event type to filter
        :param only_opensea:                        Restrict to events on OpenSea auctions
        :param auction_type:                        Filter by an auction type
        :param offset:                              Offset for pagination
        :param limit:                               Limit for pagination
        :param occurred_before:                     Only show events listed before this timestamp; seconds since Unix
                                                   epoch
        :param occurred_after:                      Only show events listed after this timestamp; seconds since Unix
                                                   epoch
        :param api_key:                             API Key
        """

        param = {}
        temp = ''

        if assertType(self.asset_contract_address_type, asset_contract_address):
            if asset_contract_address is not None:
                param['asset_contract_address'] = asset_contract_address

        if assertType(self.collection_slug_type, collection_slug):
            if collection_slug is not None:
                param['collection_slug'] = collection_slug

        if assertType(self.token_id_type, token_id):
            if token_id is not None:
                param['token_id'] = token_id

        if assertType(self.account_address_type, account_address):
            if account_address is not None:
                param['account_address'] = account_address

        if assertType(self.event_type_type, event_type, conditions=self.event_type_conditions):
            if event_type is not None:
                param['event_type'] = event_type

        if assertType(self.only_opensea_type, only_opensea):
            if only_opensea is not None:
                param['only_opensea'] = only_opensea

        if assertType(self.auction_type_type, auction_type, conditions=self.auction_type_conditions):
            if auction_type is not None:
                param['auction_type'] = auction_type

        if assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            if offset is not None:
                param['offset'] = offset

        if assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            if limit is not None:
                param['limit'] = limit

        if assertType(self.occurred_before_type, occurred_before):
            if occurred_before is not None:
                param['occurred_before'] = occurred_before

        if assertType(self.occurred_after_type, occurred_after):
            if occurred_after is not None:
                param['occurred_after'] = occurred_after

        if assertType(self.api_key_type, api_key):
            if api_key is not None:
                param['X-API-KEY'] = api_key

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseResponse(self, timeout: int = 600):
        """
        This parses the response object obtained from loadAndSendPayload()

        :return:                        Complete Pandas DataFrame
        """

        counter = 0
        base_filepath = os.path.join(os.getcwd(), 'dumps', 'data_dumps.json')

        try:
            if os.path.exists(base_filepath):
                with open(f'{base_filepath}', 'r') as f:
                    data = json.load(f)
                    self.responses = data

                main_list = []

                for dict_item in self.responses:
                    main_list.extend(dict_item['asset_events'])

                self.response_frame = pd.DataFrame(data=main_list).astype(str)
            else:
                time.sleep(1)
                counter += 1

            if counter > timeout:
                raise TimeoutError('Error: File cannot be created. Try again.')

        except Exception as ex:
            raise ex


class Collections(Opensea):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/collections'

    def setCollectionsParameters(self,
                                 asset_owner: Optional[str] = None,
                                 offset: int = 0,
                                 limit: int = 20,
                                 api_key: Optional[str] = None):
        """
        Gets and sets the variables for the OpenseaCollections class; setting parameters are separate from __init__ so
        that users can conduct multiple queries by getting the maximum number of API calls permitted for Opensea.io,
        which requires this function so that the requests can be sent and obtained asynchronously

        Initial call of the function will not set the variables per default as defined in opensea_config. You must set
        the parameters of the function manually through setParameters. This is to ensure that async works perfectly,
        and that your final url list consists of only parameters you want to parse, and not unwanted parameters from
        the initial call to the class

        :param asset_owner:                         A wallet address. If specified, will return collections where
                                                    the owner owns at least one asset belonging to smart contracts
                                                    in the collection
        :param offset:                              Number of contracts offset from the beginning of the result list
        :param limit:                               Maximum number of contracts to return.
        :param api_key:                             API Key
        """

        param = {}
        temp = ''

        if assertType(self.asset_owner_type, asset_owner):
            if asset_owner is not None:
                param['asset_owner'] = asset_owner

        if assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            if offset is not None:
                param['offset'] = offset

        if assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            if limit is not None:
                param['limit'] = limit

        if assertType(self.api_key_type, api_key):
            if api_key is not None:
                param['X-API-KEY'] = api_key

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseResponse(self, timeout: int = 600):
        """
        This parses the response object obtained from loadAndSendPayload()

        :return:                        Complete Pandas DataFrame
        """

        counter = 0
        base_filepath = os.path.join(os.getcwd(), 'dumps', 'data_dumps.json')

        try:
            if os.path.exists(base_filepath):
                with open(f'{base_filepath}', 'r') as f:
                    data = json.load(f)
                    self.responses = data

                main_list = []

                for dict_item in self.responses:
                    main_list.extend(dict_item['collections'])

                self.response_frame = pd.DataFrame(data=main_list).astype(str)
            else:
                time.sleep(1)
                counter += 1

            if counter > timeout:
                raise TimeoutError('Error: File cannot be created. Try again.')

        except Exception as ex:
            raise ex


class Bundles(Opensea):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/bundles'

    def setBundlesParameter(self,
                            on_sale: Optional[bool] = None,
                            owner: Optional[str] = None,
                            asset_contract_address: Optional[str] = None,
                            asset_contract_addresses: Optional[list] = None,
                            token_ids: Optional[list] = None,
                            offset: int = 0,
                            limit: int = 20,
                            api_key: Optional[str] = None):
        """
        Gets and sets variables for the OpenseaBundles class; setting parameters are separate from __init__ so that
        users can conduct multiple queries by getting the maximum number of API calls permitted for Opensea.io, which
        requires this function so that the requests can be sent and obtained asynchronously

        Initial call of the function will set the variables per default as defined in opensea_config. This behaviour
        can be overwritten by altering the default values in the config file before calling this Class

        Call this function after __init__ to reset variables according to your own specifications; if no changes were
        made, then the default parameters will run

        :param on_sale:                             If set to true, only show bundles currently on sale. If set to
                                                    false, only show bundles that have been sold or cancelled.
        :param owner:                               Account address of the owner of a bundle
        :param asset_contract_address:              Contract address of all the assets in a bundle
        :param asset_contract_addresses:            An array of contract addresses to search for
        :param token_ids:                           A list of token IDs for showing only bundles with at least one of
                                                    the token IDs in the list
        :param offset:                              Number of contracts offset from the beginning of the result list
        :param limit:                               Maximum number of contracts to return
        :param api_key:                             API Key
        """

        param = {}
        temp = ''

        if assertType(self.on_sale_type, on_sale):
            if on_sale is not None:
                param['on_sale'] = on_sale

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.asset_contract_address_type, asset_contract_address):
            if asset_contract_addresses is None:
                if asset_contract_address is not None:
                    param['asset_contract_address'] = asset_contract_address
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if assertType(self.asset_contract_addresses_type, asset_contract_addresses):
            if asset_contract_address is None:
                if asset_contract_addresses is not None:
                    param['asset_contract_addresses'] = asset_contract_addresses
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if assertType(self.token_id_type, token_ids):
            if token_ids is not None:
                param['token_ids'] = token_ids

        if assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            if offset is not None:
                param['offset'] = offset

        if assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            if limit is not None:
                param['limit'] = limit

        if assertType(self.api_key_type, api_key):
            if api_key is not None:
                param['X-API-KEY'] = api_key

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseResponse(self, timeout: int = 600):
        """
        This parses the response object obtained from loadAndSendPayload()

        :return:                        Complete Pandas DataFrame
        """

        counter = 0
        base_filepath = os.path.join(os.getcwd(), 'dumps', 'data_dumps.json')

        try:
            if os.path.exists(base_filepath):
                with open(f'{base_filepath}', 'r') as f:
                    data = json.load(f)
                    self.responses = data

                main_list = []

                for dict_item in self.responses:
                    main_list.extend(dict_item['bundles'])

                self.response_frame = pd.DataFrame(data=main_list).astype(str)
            else:
                time.sleep(1)
                counter += 1

            if counter > timeout:
                raise TimeoutError('Error: File cannot be created. Try again.')

        except Exception as ex:
            raise ex
