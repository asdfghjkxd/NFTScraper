import os
import pickle
import pandas as pd
import json

from utils.utils import assertType


class Mintable:
    def __init__(self):
        self.none_type = None
        self.user_address_type = (str, self.none_type)
        self.category_type = str
        self.category_conditions = ['_all', 'art', 'collectibles', 'videos', 'music', 'domains', 'templates']
        self.auction_type = bool
        self.auction_conditions = [None, True, False]
        self.order_by_date_type = [str, self.none_type]
        self.order_by_type = bool
        self.order_by_conditions = [None, True, False]
        self.size_type = int
        self.last_key_type = int
        self.network_type = int
        self.network_conditions = [1, 4]
        self.id_type = str
        self.api_key = ''
        self.api_key_type = str

        self.URLs = []
        self.responses = []
        self.response_frame = pd.DataFrame()
        self.endpoint = ''

    def loadAndSendPayload(self):
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


class NFT(Mintable):
    def __init__(self):
        super().__init__()

    def setGaslessNFTParameters(self,
                                user_address: str):
        """
        Gets and sets the user address to get all gasless NFTs

        :param user_address:                        Ethereum wallet address to look up NFTs for
        """

        self.endpoint = 'https://api.mintable.app/gasless-by-address?address='

        if assertType(self.user_address_type, user_address):
            if user_address is not None:
                self.endpoint = f'{self.endpoint}{user_address}'

    def setAllNFTParameter(self,
                           category: str,
                           user_address: str,
                           auction: bool,
                           order_by_date: bool,
                           size: int,
                           lastkey: int,
                           network: int):
        """
        Gets and sets the parameters for querying all NFTs

        :param category:                            The catergory of NFT to fetch
        :param user_address:                        Smart contract address to search for
        :param auction:                             Fetch auctions only
        :param order_by_date:                       Order by date item was listed in descending order
        :param size:                                Number of results to return
        :param lastkey:                             Pagination value - 25 means return items after the first 25
        :param network:                             Either 1 for mainnet ethereum or 4 for rinkeby testnet
        """

        temp = ''
        param = {}

        if assertType(self.category_type, category, conditions=self.category_conditions):
            if category is not None:
                param['category'] = category

        if assertType(self.user_address_type, user_address):
            if user_address is not None:
                param['address'] = user_address

        if assertType(self.auction_type, auction, conditions=self.auction_conditions):
            if auction is not None:
                param['auction'] = auction

        if assertType(self.order_by_date_type, order_by_date):
            if order_by_date is not None:
                param['order_by_date'] = order_by_date

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.last_key_type, lastkey):
            if lastkey is not None:
                param['lastKey'] = lastkey

        if assertType(self.network_type, network, conditions=self.network_conditions):
            if network is not None:
                param['network'] = network

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setSingleNFTParameter(self,
                              id: str,
                              api_key: str):
        """
        Gets and sets the parameters for querying one NFT

        :param id:                                  The id of the item to fetch
        :param api_key:                             API Key
        """

        self.endpoint = 'https://api.mintable.app/assets/'

        if assertType(self.id_type, id):
            if id is not None:
                self.endpoint = f'{self.endpoint}{id}'

        # this is going into headers
        if assertType(self.api_key, api_key):
            if api_key is not None:
                self.api_key = api_key

        with open('headers_temp.pkl', 'wb') as f:
            pickle.dump(self.api_key, f)

    def parseAllNFTs(self):
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

    def parseSingleNFT(self):
        base_filepath = os.path.join(os.getcwd(), 'data_dumps.json')
        url_filepath = os.path.join(os.getcwd(), 'url_dumps.pkl')

        if os.path.exists(base_filepath):
            with open(f'{base_filepath}', 'rb') as f:
                data = json.load(f)

                self.response_frame = pd.DataFrame(data=data).astype(str)

            # clean up temp files
            os.remove(base_filepath)
            os.remove(url_filepath)


class Auction(Mintable):
    def __init__(self):
        super().__init__()

    def setEndingSoonAuctions(self):
        self.endpoint = 'https://api.mintable.app/auctions-ending-soon'

    def setHotAuctions(self):
        self.endpoint = 'https://api.mintable.app/hot-auctions'

    def parseEndingSoonAndHotAuctions(self):
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
