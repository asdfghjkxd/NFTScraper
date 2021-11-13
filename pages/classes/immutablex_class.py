import os
import pickle
import pandas as pd
import json

from typing import Optional
from utils.utils import assertType


class ImmutableX:
    def __init__(self):
        """
        This parent class sets the types of inputs the user can input and stores any functions which is used across all
        API calls
        """

        # API parameters
        self.none_type = type(None)
        self.page_size_type = (int, self.none_type)
        self.cursor_type = (str, self.none_type)
        self.order_by_type = (str, self.none_type)
        self.order_by_conditions = [None, 'updated_at', 'name']
        self.direction_type = (str, self.none_type)
        self.direction_type_conditions = [None, 'asc', 'desc']
        self.user_type = (str, self.none_type)
        self.status_type = (str, self.none_type)
        self.name_type = (str, self.none_type)
        self.metadata_type = (str, self.none_type)
        self.sell_orders_type = (bool, self.none_type)
        self.sell_orders_conditions = [None, True, False]
        self.buy_orders_type = (bool, self.none_type)
        self.buy_orders_conditions = [None, True, False]
        self.include_fees_type = (bool, self.none_type)
        self.include_fees_conditions = [None, True, False]
        self.collection_type = (str, self.none_type)
        self.updated_min_timestamp_type = (str, self.none_type)
        self.updated_max_timestamp_type = (str, self.none_type)
        self.token_address_type = str
        self.token_id_type = str
        self.blacklist_type = (str, self.none_type)
        self.address_type = str
        self.address_token_type = (str, self.none_type)
        self.symbol_type = (str, self.none_type)

        # app parameters
        self.URLs = []
        self.endpoint = ''
        self.responses = []
        self.response_frame = pd.DataFrame()

    def loadAndSendPayload(self):
        """
        Loads up the requests and prepares them for asynchronous request sending
        """

        # serialize urls for passing it on to the async component
        try:
            url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')
            with open(url_filepath, 'wb') as output:
                pickle.dump(self.URLs, output)
        except Exception as ex:
            raise
        else:
            os.system('python utils/async_requests.py')

    def resetAll(self):
        """
        Resets all relevant class attributes
        """

        self.URLs = []
        self.response_frame = pd.DataFrame()
        self.responses = []


class Assets(ImmutableX):
    """
    Class to API Calls for ImmutableX Assets
    """

    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.x.immutable.com/v1/assets'

    def setListAssetParameter(self,
                              page_size: Optional[int],
                              cursor: Optional[str],
                              order_by: Optional[str],
                              direction: Optional[str],
                              user: Optional[str],
                              status: Optional[str],
                              name: Optional[str],
                              metadata: Optional[str],
                              sell_orders: Optional[bool],
                              buy_orders: Optional[bool],
                              include_fees: Optional[bool],
                              collection: Optional[str],
                              updated_min_timestamp: Optional[str],
                              updated_max_timestamp: Optional[str]):
        """
        This function gets and sets the query parameters that will be appended behind the endpoint URL to execute the
        the query.

        :param page_size:                       Page size of the result
        :param cursor:                          Cursor
        :param order_by:                        Property to sort by
        :param direction:                       Direction to sort (asc/desc)
        :param user:                            Ethereum address of the user who owns these assets
        :param status:                          Status of these assets
        :param name:                            Name of the asset to search
        :param metadata:                        JSON-encoded metadata filters for these asset
        :param sell_orders:                     Set flag to true to fetch an array of sell order details associated
                                                with the asset
        :param buy_orders:                      Set flag to true to fetch an array of buy order details associated
                                                with the asset
        :param include_fees:                    Set flag to include fees associated with the asset
        :param collection:                      Collection contract address
        :param updated_min_timestamp:           Minimum timestamp for when these assets were last updated
        :param updated_max_timestamp:           Maximum timestamp for when these assets were last updated
        """

        param = {}
        temp = ''

        if assertType(self.page_size_type, page_size):
            if page_size is not None:
                param['page_size'] = page_size

        if assertType(self.cursor_type, cursor):
            if cursor is not None:
                param['cursor'] = cursor

        if assertType(self.order_by_type, order_by, conditions=self.order_by_conditions):
            if order_by is not None:
                param['order_by'] = order_by

        if assertType(self.direction_type, direction):
            if direction is not None:
                param['direction'] = direction

        if assertType(self.user_type, user):
            if user is not None:
                param['user'] = user

        if assertType(self.status_type, status):
            if status is not None:
                param['status'] = status

        if assertType(self.name_type, name):
            if name is not None:
                param['name'] = name

        if assertType(self.metadata_type, metadata):
            if metadata is not None:
                param['metadata'] = metadata

        if assertType(self.sell_orders_type, sell_orders, conditions=self.sell_orders_conditions):
            if sell_orders is not None:
                param['sell_orders'] = sell_orders

        if assertType(self.buy_orders_type, buy_orders, conditions=self.buy_orders_conditions):
            if buy_orders is not None:
                param['buy_orders'] = buy_orders

        if assertType(self.include_fees_type, include_fees, conditions=self.include_fees_conditions):
            if include_fees is not None:
                param['include_fees'] = include_fees

        if assertType(self.collection_type, collection):
            if collection is not None:
                param['collection'] = collection

        if assertType(self.updated_min_timestamp_type, updated_min_timestamp):
            if updated_min_timestamp is not None:
                param['updated_min_timestamp'] = updated_min_timestamp

        if assertType(self.updated_max_timestamp_type, updated_max_timestamp):
            if updated_max_timestamp is not None:
                param['updated_max_timestamp'] = updated_max_timestamp

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setSingleAssetParameter(self,
                                token_address: str,
                                token_id: str,
                                include_fees: Optional[bool]):
        """
        This function gets and sets the query parameters that will be appended behind the endpoint URL to execute the
        the query.

        :param token_address:                   Address of the ERC721 contract
        :param token_id:                        Either ERC721 token ID or internal IMX ID
        :param include_fees:                    Set flag to include fees associated with the asset
        """

        temp = ''

        if assertType(self.token_address_type, token_address):
            if token_address is not None:
                temp = temp + token_address
            else:
                raise ValueError('Error: Token Address must not be empty. Try again.')

        if assertType(self.token_id_type, token_id):
            if token_id is not None:
                temp = temp + f'/{token_id}'
            else:
                raise ValueError('Error: Token ID must not be empty. Try again.')

        if assertType(self.include_fees_type, include_fees, conditions=self.include_fees_conditions):
            if include_fees is not None:
                temp = temp + f'?include_fees={str(include_fees).lower()}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseAllAssets(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            main_list = []
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                if data is not None:
                    for dat in data:
                        if dat is None:
                            pass
                        elif 'result' in dat:
                            main_list.extend(dat['result'])

            self.response_frame = pd.DataFrame(data=main_list).astype(str)
            os.remove(base_filepath)
            os.remove(url_filepath)

    def parseSingleAsset(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

            self.response_frame = pd.DataFrame(data=data).astype(str)

            # clean up temp files
            os.remove(base_filepath)
            os.remove(url_filepath)


class Collections(ImmutableX):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.x.immutable.com/v1/collections'

    def setCollectionListParameters(self,
                                    page_size: Optional[int],
                                    cursor: Optional[str],
                                    order_by: Optional[str],
                                    direction: Optional[str],
                                    blacklist: Optional[str]):
        """
        Gets and sets the parameters to get all the collections from ImmutableX

        :param page_size:                       Page size of the result
        :param cursor:                          Cursor
        :param order_by:                        Property to sort by
        :param direction:                       Direction to sort (asc/desc)
        :param blacklist:                       List of collections not to be displayed, separated by commas
        """

        param = {}
        temp = ''

        if assertType(self.page_size_type, page_size):
            if page_size is not None:
                param['page_size'] = page_size

        if assertType(self.cursor_type, cursor):
            if cursor is not None:
                param['cursor'] = cursor

        if assertType(self.order_by_type, order_by):
            if order_by is not None:
                param['order_by'] = order_by

        if assertType(self.direction_type, direction):
            if direction is not None:
                param['direction'] = direction

        if assertType(self.blacklist_type, blacklist):
            if blacklist is not None:
                param['blacklist'] = blacklist

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setSingleCollectionParameters(self,
                                      address: str):
        """
        Gets and sets the parameters to get details of one collection

        :param address:                         Collection contract address
        """

        self.endpoint = 'https://api.x.immutable.com/v1/collections'
        if assertType(self.address_type, address):
            if address is not None:
                self.URLs.append(f'{self.endpoint}/{address}')
            else:
                raise ValueError('Error: Token Address must not be empty. Try again.')

    def setCollectionFilter(self,
                            address: str,
                            page_size: Optional[int],
                            next_page_token: Optional[str]):
        """
        Gets and sets the parameters for getting the list of collection filters

        :param address:                         Collection contract address
        :param page_size:                       Page size of the result
        :param next_page_token:                 Next page token
        """

        param = {}
        temp = ''

        if assertType(self.address_type, address):
            if address is not None:
                temp = temp + f'/{address}/filters'
            else:
                raise ValueError('Error: Token Address must not be empty. Try again.')

        if assertType(self.address_type, page_size):
            if page_size is not None:
                param['page_size'] = page_size

        if assertType(self.address_type, next_page_token):
            if next_page_token is not None:
                param['next_page_token'] = next_page_token

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseAllCollections(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            main_list = []
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                if data is not None:
                    for dat in data:
                        if dat is None:
                            pass
                        elif 'result' in dat:
                            main_list.extend(dat['result'])

            self.response_frame = pd.DataFrame(data=main_list).astype(str)
            os.remove(base_filepath)
            os.remove(url_filepath)

    def parseSingleCollection(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                self.response_frame = pd.DataFrame(data=data).astype(str)

            # clean up temp files
            os.remove(base_filepath)
            os.remove(url_filepath)


class Tokens(ImmutableX):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.x.immutable.com/v1/tokens'

    def setTokenListParameters(self,
                               address: Optional[str],
                               symbol: Optional[str]):
        """
        Gets and sets the parameters for querying tokens

        :param address:                         Contract address of the token
        :param symbol:                          Token symbols for the token, e.g. ?symbols=IMX,ETH
        """

        param = {}
        temp = ''

        if assertType(self.address_token_type, address):
            if address is not None:
                param['address'] = address

        if assertType(self.symbol_type, symbol):
            if symbol is not None:
                param['symbol'] = symbol

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setSingleTokenParameters(self,
                                 address: str):
        """
        Gets and sets the parameters for querying the details of one token

        :param address:                         Token Contract Address
        """

        if assertType(self.address_type, address):
            if address is not None:
                self.URLs.append(f'{self.endpoint}?address={address}')
            else:
                raise ValueError('Error: Token Address must not be empty. Try again.')

    def parseAllTokens(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            main_list = []
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                if data is not None:
                    for dat in data:
                        if dat is None:
                            pass
                        elif 'result' in dat:
                            main_list.extend(dat['result'])

            self.response_frame = pd.DataFrame(data=main_list).astype(str)
            os.remove(base_filepath)
            os.remove(url_filepath)

    def parseSingleToken(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                self.response_frame = pd.DataFrame(data=data).astype(str)

            # clean up temp files
            os.remove(base_filepath)
            os.remove(url_filepath)
