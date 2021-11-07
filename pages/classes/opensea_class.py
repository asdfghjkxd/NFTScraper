from typing import Union
import requests as r
import pandas as pd
import streamlit as st
import json
import logging


class OpeanseaAssets:
    """
    This class manages the pulling of assets from Opensea
    """

    def __init__(self,
                 owner: Union[str, None] = None,
                 token_ids: Union[list, None] = None,
                 asset_contract_addresses: Union[str, list] = None,
                 order_by: Union[str, None] = None,
                 order_direction: str = 'desc',
                 offset: int = 0,
                 limit: int = 20,
                 collection: Union[str, None] = None,
                 api_key: Union[str, None] = None):
        """
        Gets and sets the variables for the OpenseaAsset class

        :param owner:                               The address of the owner of the assets
        :param token_ids:                           An array of token IDs to search for
        :param asset_contract_addresses:            The NFT contract address for the assets
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

        self.endpoint = 'https://api.opensea.io/api/v1/assets'
        self.finalised = {}
        self.param_counter = 0

        if isinstance(owner, str or None):
            self.finalised['owner'] = owner

        if isinstance(token_ids, list or None):
            self.finalised['token_ids'] = token_ids

        if isinstance(asset_contract_addresses, str or list or None):
            self.finalised['asset_contract_addresses'] = asset_contract_addresses

        if isinstance(order_by, str or None):
            order_by = order_by.lower().strip()
            if order_by in ['token_id', 'sale_date', 'sale_count', 'sale_price']:
                self.finalised['order_by'] = order_by
            else:
                raise AssertionError('Error: Parameter Invalid. Only token_id, sale_date, sale_count, '
                                     'sale_price are accepted.')

        if isinstance(order_direction, str or None):
            order_direction = order_direction.lower().strip()
            if order_direction in ['asc', 'desc']:
                self.finalised['order_direction'] = order_direction
            else:
                raise AssertionError('Error: Parameter Invalid. Only asc and desc is accepted')

        if isinstance(offset, int or None):
            if offset <= 10000:
                self.finalised['offset'] = offset

        if isinstance(limit, int or None):
            if 0 < limit <= 50:
                self.finalised['limit'] = limit
            else:
                ValueError('Error: Bounds for limit exceeded. Bound accepted: 0 < Limit <= 50')

        if isinstance(collection, str or None):
            self.finalised['collection'] = collection

        if isinstance(api_key, str or None):
            self.finalised['X-API-KEY'] = api_key
            self.api_key = api_key

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
