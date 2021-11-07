import datetime
from typing import Optional
import requests as r
import pandas as pd
import json
import logging


class Opensea:
    """
    The Parent Class which defines all the params and common function used by all child classes
    """
    def __init__(self):
        """
        Define the static types that will be used in the app
        """
        # scraper params
        self.account_address_type = Optional[str]
        self.api_key_type = Optional[str]
        self.asset_contract_address_type = Optional[str]
        self.asset_contract_addresses_type = Optional[list]
        self.asset_owner_type = Optional[str]
        self.auction_type_type = Optional[str]
        self.auction_type_conditions = ['english', 'dutch', 'min-price']
        self.collection_type = Optional[str]
        self.collection_slug_type = Optional[str]
        self.event_type_type = Optional[str]
        self.event_type_conditions = ['created', 'successful', 'cancelled', 'bid_entered', 'bid_withdrawn', 'transfer',
                                      'approve']
        self.limit_type = int
        self.limit_type_conditions = range(1, 50)
        self.occurred_after_type = datetime.datetime
        self.occurred_before_type = datetime.datetime
        self.offset_type = int
        self.offset_type_conditions = range(0, 10000)
        self.on_sale_type = Optional[bool]
        self.only_opensea_type = bool
        self.order_by_type = Optional[str]
        self.order_by_conditions = ['token_id', 'sale_date', 'sale_count', 'sale_price']
        self.order_direction_type = str
        self.order_direction_conditions = ['asc', 'desc']
        self.owner_type = Optional[str]
        self.token_id_type = Optional[int]
        self.token_ids_type = Optional[list]

        # app params
        self.finalised = dict()
        self.param_counter = 0
        self.response = None
        self.response_text = None
        self.response_frame = pd.DataFrame

    def assertType(self, default, test, conditions=None):
        if isinstance(type(default), type(test)):
            if conditions is not None:
                if test in conditions:
                    return True
                else:
                    raise AssertionError(f'Error: {test} is not one of the accepted parameter {conditions}')
            else:
                return True
        # else:
        #     raise AssertionError(f'Error: {type(test)} is not the same as {type(default)}. Try again.')

    def constructRequest(self):
        for k, v in self.finalised.items():
            self.param_counter += 1
            if v is not None:
                if self.param_counter == 1:
                    self.endpoint = f'{self.endpoint}?{k}={v}'
                if self.param_counter > 1:
                    self.endpoint = f'{self.endpoint}&{k}={v}'

    def sendRequest(self):
        self.response = r.request('GET', self.endpoint)
        if self.response.status_code == 400:
            logging.error('Crawl Not Successful')

    def parseRequest(self):
        self.response_text = json.loads(self.response.text)
        for k, v in self.response_text.items():
            self.response_frame = pd.DataFrame.from_dict(data=v,
                                                         orient='columns').astype(str)


class OpeanseaAssets(Opensea):
    """
    This class manages the pulling of assets from Opensea
    """

    def __init__(self,
                 owner: Optional[str] = None,
                 token_ids: Optional[list] = None,
                 asset_contract_address: Optional[str] = None,
                 asset_contract_addresses: Optional[list] = None,
                 order_by: Optional[str] = None,
                 order_direction: str = 'desc',
                 offset: int = 0,
                 limit: int = 20,
                 collection: Optional[str] = None,
                 api_key: Optional[str] = None):
        """
        Gets and sets the variables for the OpenseaAsset class

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

        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/assets'
        self.finalised = {}
        self.param_counter = 0

        if self.assertType(self.owner_type, owner):
            self.finalised['owner'] = owner

        if self.assertType(self.token_ids_type, token_ids):
            self.finalised['token_ids'] = token_ids

        if self.assertType(self.asset_contract_address_type, asset_contract_address):
            if asset_contract_addresses is None:
                self.finalised['asset_contract_address'] = asset_contract_address
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if self.assertType(self.asset_contract_addresses_type, asset_contract_addresses):
            if asset_contract_address is None:
                self.finalised['asset_contract_addresses'] = asset_contract_addresses
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if self.assertType(self.order_by_type, order_by, conditions=self.order_by_conditions):
            if type(order_by) is not None:
                self.finalised['order_by'] = order_by.lower().strip()

        if self.assertType(self.order_direction_type, order_direction.lower().strip(),
                           conditions=self.order_direction_conditions):
            self.finalised['order_direction'] = order_direction.lower().strip()

        if self.assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            self.finalised['offset'] = offset

        if self.assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            self.finalised['limit'] = limit

        if self.assertType(self.collection_type, collection):
            self.finalised['collection'] = collection

        if self.assertType(self.api_key_type, api_key):
            self.finalised['X-API-KEY'] = api_key


class OpenseaEvents(Opensea):
    """
    This class manages the pulling of assets from Opensea
    """
    def __init__(self,
                 asset_contract_address: Optional[str] = None,
                 collection_slug: Optional[str] = None,
                 token_id: Optional[int] = None,
                 account_address: Optional[str] = None,
                 event_type: Optional[str] = None,
                 only_opensea: bool = False,
                 auction_type: Optional[str] = None,
                 offset: int = 0,
                 limit: int = 20,
                 occurred_before: Optional[datetime.datetime] = None,
                 occurred_after: Optional[datetime.datetime] = None,
                 api_key: Optional[str] = None):
        """
        Gets and sets variables for the OpenseaEvents class

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

        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/events'
        self.finalised = {}
        self.param_counter = 0

        if self.assertType(self.asset_contract_address_type, asset_contract_address):
            self.finalised['asset_contract_address'] = asset_contract_address

        if self.assertType(self.collection_slug_type, collection_slug):
            self.finalised['collection_slug'] = collection_slug

        if self.assertType(self.token_id_type, token_id):
            self.finalised['token_id'] = token_id

        if self.assertType(self.account_address_type, account_address):
            self.finalised['account_address'] = account_address

        if self.assertType(self.event_type_type, event_type, conditions=self.event_type_conditions):
            self.finalised['event_type'] = event_type

        if self.assertType(self.only_opensea_type, only_opensea):
            self.finalised['only_opensea'] = only_opensea

        if self.assertType(self.auction_type_type, auction_type, conditions=self.auction_type_conditions):
            self.finalised['auction_type'] = auction_type

        if self.assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            self.finalised['offset'] = offset

        if self.assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            self.finalised['limit'] = limit

        if self.assertType(self.occurred_before_type, occurred_before):
            self.finalised['occurred_before'] = occurred_before

        if self.assertType(self.occurred_after_type, occurred_after):
            self.finalised['occurred_after'] = occurred_after

        if self.assertType(self.api_key_type, api_key):
            self.finalised['X-API-KEY'] = api_key


class OpenseaCollections(Opensea):
    """
    This class manages the pulling of collections from Opensea
    """
    def __init__(self,
                 asset_owner: Optional[str] = None,
                 offset: int = 0,
                 limit: int = 20,
                 api_key: Optional[str] = None):
        """
        Gets and sets variables for the OpenseaCollections class

        :param asset_owner:                         A wallet address. If specified, will return collections where
                                                    the owner owns at least one asset belonging to smart contracts
                                                    in the collection
        :param offset:                              Number of contracts offset from the beginning of the result list
        :param limit:                               Maximum number of contracts to return.
        :param api_key:                             API Key
        """

        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/events'
        self.finalised = {}
        self.param_counter = 0

        if self.assertType(self.asset_owner_type, asset_owner):
            self.finalised['asset_owner'] = asset_owner

        if self.assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            self.finalised['offset'] = offset

        if self.assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            self.finalised['limit'] = limit

        if self.assertType(self.api_key_type, api_key):
            self.finalised['X-API-KEY'] = api_key


class OpenseaBundles(Opensea):
    """
    This class manages the pulling of bundles from Opensea
    """
    def __init__(self,
                 on_sale: Optional[bool] = None,
                 owner: Optional[str] = None,
                 asset_contract_address: Optional[str] = None,
                 asset_contract_addresses: Optional[list] = None,
                 token_ids: Optional[list] = None,
                 offset: int = 0,
                 limit: int = 20,
                 api_key: Optional[str] = None):
        """
        Gets and sets variables for the OpenseaBundles class

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

        super().__init__()
        self.endpoint = 'https://api.opensea.io/api/v1/bundles'
        self.finalised = {}
        self.param_counter = 0

        if self.assertType(self.on_sale_type, on_sale):
            self.finalised['on_sale'] = on_sale

        if self.assertType(self.owner_type, owner):
            self.finalised['owner'] = owner

        if self.assertType(self.asset_contract_address_type, asset_contract_address):
            if asset_contract_addresses is None:
                self.finalised['asset_contract_address'] = asset_contract_address
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if self.assertType(self.asset_contract_addresses_type, asset_contract_addresses):
            if asset_contract_address is None:
                self.finalised['asset_contract_addresses'] = asset_contract_addresses
            else:
                raise AssertionError('Error: Cannot define two separate queries for Asset Contract Address.')

        if self.assertType(self.token_id_type, token_ids):
            self.finalised['token_ids'] = token_ids

        if self.assertType(self.offset_type, offset, conditions=self.offset_type_conditions):
            self.finalised['offset'] = offset

        if self.assertType(self.limit_type, limit, conditions=self.limit_type_conditions):
            self.finalised['limit'] = limit

        if self.assertType(self.api_key_type, api_key):
            self.finalised['X-API-KEY'] = api_key
