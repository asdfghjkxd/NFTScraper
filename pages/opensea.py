import asyncio
import aiohttp
import streamlit as st
import pandas as pd
import pages.config.opensea_config as default

from utils.utils import printDataFrame
from pages.classes.opensea_class import Assets, Events, Collections, Bundles


def app():
    """
    This is the function that runs when Opensea page is activated
    """

    st.title('Opensea Scraper')
    st.markdown('This app allows you to pull data from Opensea.io.')
    st.markdown('## Type of Data Retrieved')
    default.RETRIEVAL_METHOD = st.selectbox('Select Data Retrieval Type',
                                            ('Assets', 'Events', 'Collections', 'Bundles'))

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                   Assets                                                     #
    # ------------------------------------------------------------------------------------------------------------ #
    if default.RETRIEVAL_METHOD == 'Assets':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.GET_ALL = st.checkbox('Scrape Maximum API Returns?', value=True)
        if not default.GET_ALL:
            if st.checkbox('Define owner Parameter', value=False):
                default.OWNER = st.text_input('Key in Address of Owner of Asset')

            if st.checkbox('Define token_ids Parameter', value=False):
                default.TOKEN_IDS = st.text_input('Key in Array of Token IDs to Search')

            if st.checkbox('Define asset_contract_address Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESS = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                               help='Do not use asset_contract_addresses if you '
                                                                    'are using this parameter.')

            if st.checkbox('Define asset_contract_addresses Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESSES = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                                 help='Note that if you wish to key in a list into '
                                                                      'the input box, delimit your addresses with '
                                                                      'commas. Failure to do so or failure to '
                                                                      'delimit properly would result in broken '
                                                                      'queries.')
                if len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                    st.info('Addresses Detected!')
                else:
                    st.warning(
                        'Warning, No Address Detected. Proceeding in this state will result in a None value being '
                        'passed into asset_contract_addresses parameter.')
            if st.checkbox('Define order_by Parameter', value=False):
                default.ORDER_BY = st.selectbox('Select Order', ('token_id', 'sale_date', 'sale_count'))

            if st.checkbox('Define collection Parameter', value=False):
                default.COLLECTION = st.text_input('Limit responses to members of a Collection')

            if st.checkbox('Define API Key', value=False):
                default.API_KEY = st.text_input('API Key')

            default.OFFSET = st.number_input('Offset',
                                             min_value=0,
                                             max_value=10000,
                                             value=0)

            default.LIMIT = st.number_input('Limit',
                                            min_value=1,
                                            max_value=50,
                                            value=20)

            default.ORDER_DIRECTION = st.selectbox('Select Direction', ('asc', 'desc'))

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        # begin the extraction process here
        st.markdown('## Asset Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed with Data Extraction'):
            # process the input addresses
            if default.ASSET_CONTRACT_ADDRESSES is not None and len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                default.ASSET_CONTRACT_ADDRESSES = set(
                    address.strip() for address in default.ASSET_CONTRACT_ADDRESSES.split(sep=','))
                st.info(f'Addresses Loaded: {[address for address in default.ASSET_CONTRACT_ADDRESSES]}')

            try:
                if default.GET_ALL:
                    default.OFFSET = 0
                    default.LIMIT = 50
                    asset = Assets()

                    # this loads up all the urls
                    for i in range(200):
                        asset.setAssetParameters(owner=default.OWNER,
                                                 token_ids=default.TOKEN_IDS,
                                                 asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                                 order_by=default.ORDER_BY,
                                                 order_direction=default.ORDER_DIRECTION,
                                                 offset=default.OFFSET,
                                                 limit=default.LIMIT,
                                                 collection=default.COLLECTION,
                                                 api_key=default.API_KEY)
                        default.OFFSET += default.LIMIT
                    asset.loadAndSendPayload()
                    asset.parseResponse()
                else:
                    asset = Assets()
                    asset.setAssetParameters(owner=default.OWNER,
                                             token_ids=default.TOKEN_IDS,
                                             asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                             order_by=default.ORDER_BY,
                                             order_direction=default.ORDER_DIRECTION,
                                             offset=default.OFFSET,
                                             limit=default.LIMIT,
                                             collection=default.COLLECTION,
                                             api_key=default.API_KEY)
                    asset.loadAndSendPayload()
                    asset.parseResponse()
            except Exception as ex:
                raise ex
            else:
                if default.SAVE:
                    st.markdown('### Save Data')
                    st.download_button('Download CSV',
                                       data=asset.response_frame.to_csv().encode('utf-8'),
                                       file_name='data.csv',
                                       mime='text/csv')
                if default.VERBOSE:
                    st.markdown('### Display Data')
                    printDataFrame(data=asset.response_frame,
                                   verbose_level=default.VERBOSITY,
                                   advanced=default.ADVANCED)

                asset.resetAll()

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                   Events                                                     #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Events':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.GET_ALL = st.checkbox('Scrape Maximum API Returns?', value=True)
        if not default.GET_ALL:
            if st.checkbox('Define asset_contract_addresses Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESS = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                               help='Note that if you wish to key in a list into '
                                                                    'the input box, delimit your addresses with '
                                                                    'commas. Failure to do so or failure to '
                                                                    'delimit properly would result in broken '
                                                                    'queries.')

            if st.checkbox('Define collection_slug Parameter', value=False):
                default.COLLECTION_SLUG = st.text_input('Key in the Collection Slug')

            if st.checkbox('Define token_ids Parameter', value=False):
                default.TOKEN_ID = st.text_input('Key in Token ID to Search For')

            if st.checkbox('Define account_address Parameter', value=False):
                default.ACCOUNT_ADDRESS = st.text_input('Key in Account Address to Search For')

            if st.checkbox('Define event_type Parameter', value=False):
                default.EVENT_TYPE = st.selectbox('Select Relevant event_type Parameter',
                                                  ['created', 'successful', 'cancelled', 'bid_entered',
                                                   'bid_withdrawn', 'transfer', 'approve'])

            if st.checkbox('Define only_opensea Parameter', value=False):
                default.ONLY_OPENSEA = st.checkbox('Input True/False Value')

            if st.checkbox('Define auction_type Parameter', value=False):
                default.AUCTION_TYPE = st.selectbox('Select Relevant auction_type Parameter',
                                                    ['english', 'dutch', 'min-price'])

            if st.checkbox('Define occurred_before Paramter', value=False):
                default.OCCURRED_BEFORE = st.date_input('Key in Date')

            if st.checkbox('Define occurred-after Parameter', value=False):
                default.OCCURRED_AFTER = st.date_input('Key in Date')

            if st.checkbox('Define API Key', value=False):
                default.API_KEY = st.text_input('API Key')

            default.OFFSET = st.number_input('Offset',
                                             min_value=0,
                                             max_value=10000,
                                             value=0)

            default.LIMIT = st.number_input('Limit',
                                            min_value=1,
                                            max_value=50,
                                            value=20)

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        # begin the extraction process here
        st.markdown('## Asset Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed with Data Extraction'):
            try:
                if default.GET_ALL:
                    default.OFFSET = 0
                    default.LIMIT = 50
                    events = Events()

                    # this loads up all the urls
                    for i in range(200):
                        events.setEventsParameters(asset_contract_address=default.ASSET_CONTRACT_ADDRESS,
                                                   collection_slug=default.COLLECTION_SLUG,
                                                   token_id=default.TOKEN_ID,
                                                   account_address=default.ACCOUNT_ADDRESS,
                                                   event_type=default.EVENT_TYPE,
                                                   only_opensea=default.ONLY_OPENSEA,
                                                   auction_type=default.AUCTION_TYPE,
                                                   offset=default.OFFSET,
                                                   limit=default.LIMIT,
                                                   occurred_before=default.OCCURRED_BEFORE,
                                                   occurred_after=default.OCCURRED_AFTER,
                                                   api_key=default.API_KEY)
                        default.OFFSET += default.LIMIT
                    events.loadAndSendPayload()
                    events.parseResponse()
                else:
                    events = Events()
                    events.setEventsParameters(asset_contract_address=default.ASSET_CONTRACT_ADDRESS,
                                               collection_slug=default.COLLECTION_SLUG,
                                               token_id=default.TOKEN_ID,
                                               account_address=default.ACCOUNT_ADDRESS,
                                               event_type=default.EVENT_TYPE,
                                               only_opensea=default.ONLY_OPENSEA,
                                               auction_type=default.AUCTION_TYPE,
                                               offset=default.OFFSET,
                                               limit=default.LIMIT,
                                               occurred_before=default.OCCURRED_BEFORE,
                                               occurred_after=default.OCCURRED_AFTER,
                                               api_key=default.API_KEY)
                    events.loadAndSendPayload()
                    events.parseResponse()
            except Exception as ex:
                raise ex
            else:
                if default.SAVE:
                    st.markdown('### Save Data')
                    st.download_button('Download CSV',
                                       data=events.response_frame.to_csv().encode('utf-8'),
                                       file_name='data.csv',
                                       mime='text/csv')
                if default.VERBOSE:
                    st.markdown('### Display Data')
                    printDataFrame(data=events.response_frame,
                                   verbose_level=default.VERBOSITY,
                                   advanced=default.ADVANCED)

                events.resetAll()

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                Collections                                                   #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Collections':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.GET_ALL = st.checkbox('Scrape Maximum API Returns?', value=True)
        if not default.GET_ALL:
            if st.checkbox('Define asset_owner Parameter', value=False):
                default.ASSET_OWNER = st.text_input('Key in the Owner Name/ID')

            if st.checkbox('Define API Key', value=False):
                default.API_KEY = st.text_input('API Key')

            default.OFFSET = st.number_input('Offset',
                                             min_value=0,
                                             max_value=10000,
                                             value=0)

            default.LIMIT = st.number_input('Limit',
                                            min_value=1,
                                            max_value=50,
                                            value=20)

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        # begin the extraction process here
        st.markdown('## Asset Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed with Data Extraction'):
            try:
                if default.GET_ALL:
                    default.OFFSET = 0
                    default.LIMIT = 50
                    collections = Collections()

                    # this loads up all the urls
                    for i in range(200):
                        collections.setCollectionsParameters(asset_owner=default.ASSET_OWNER,
                                                             offset=default.OFFSET,
                                                             limit=default.LIMIT,
                                                             api_key=default.API_KEY)
                        default.OFFSET += default.LIMIT
                    collections.loadAndSendPayload()
                    collections.parseResponse()
                else:
                    collections = Collections()
                    collections.setCollectionsParameters(asset_owner=default.ASSET_OWNER,
                                                         offset=default.OFFSET,
                                                         limit=default.LIMIT,
                                                         api_key=default.API_KEY)
                    collections.loadAndSendPayload()
                    collections.parseResponse()
            except Exception as ex:
                raise ex
            else:
                if default.SAVE:
                    st.markdown('### Save Data')
                    st.download_button('Download CSV',
                                       data=collections.response_frame.to_csv().encode('utf-8'),
                                       file_name='data.csv',
                                       mime='text/csv')
                if default.VERBOSE:
                    st.markdown('### Display Data')
                    printDataFrame(data=collections.response_frame,
                                   verbose_level=default.VERBOSITY,
                                   advanced=default.ADVANCED)

                collections.resetAll()

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                  Bundles                                                     #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Bundles':
        # define flags
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.GET_ALL = st.checkbox('Scrape Maximum API Returns?', value=True)
        if not default.GET_ALL:
            if st.checkbox('Define on_sale Parameter', value=False):
                default.ON_SALE = st.checkbox('Choose True/False Option')

            if st.checkbox('Define owner Parameter', value=False):
                default.OWNER = st.text_input('Key in Address of Owner of Asset')

            if st.checkbox('Define asset_contract_address Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESS = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                               help='Do not use asset_contract_addresses if you '
                                                                    'are using this parameter.')

            if st.checkbox('Define asset_contract_addresses Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESSES = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                                 help='Note that if you wish to key in a list into '
                                                                      'the input box, delimit your addresses with '
                                                                      'commas. Failure to do so or failure to '
                                                                      'delimit properly would result in broken '
                                                                      'queries.')
                if len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                    st.info('Addresses Detected!')
                else:
                    st.warning(
                        'Warning, No Address Detected. Proceeding in this state will result in a None value being '
                        'passed into asset_contract_addresses parameter.')

            if st.checkbox('Define token_ids Parameter', value=False):
                default.TOKEN_IDS = st.text_input('Key in Array of Token IDs to Search')

            if st.checkbox('Define API Key', value=False):
                default.API_KEY = st.text_input('API Key')

            default.OFFSET = st.number_input('Offset',
                                             min_value=0,
                                             max_value=10000,
                                             value=0)

            default.LIMIT = st.number_input('Limit',
                                            min_value=1,
                                            max_value=50,
                                            value=20)

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        # begin the extraction process here
        st.markdown('## Asset Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed with Data Extraction'):
            # process the input addresses
            if default.ASSET_CONTRACT_ADDRESSES is not None and len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                default.ASSET_CONTRACT_ADDRESSES = set(
                    address.strip() for address in default.ASSET_CONTRACT_ADDRESSES.split(sep=','))
                st.info(f'Addresses Loaded: {[address for address in default.ASSET_CONTRACT_ADDRESSES]}')

            try:
                if default.GET_ALL:
                    default.OFFSET = 0
                    default.LIMIT = 50
                    bundles = Bundles()

                    # this loads up all the urls
                    for i in range(200):
                        bundles.setBundlesParameter(on_sale=default.ON_SALE,
                                                    owner=default.OWNER,
                                                    asset_contract_address=default.ASSET_CONTRACT_ADDRESS,
                                                    asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                                    token_ids=default.TOKEN_IDS,
                                                    offset=default.OFFSET,
                                                    limit=default.LIMIT,
                                                    api_key=default.API_KEY)
                        default.OFFSET += default.LIMIT
                    bundles.loadAndSendPayload()
                    bundles.parseResponse()
                else:
                    bundles = Bundles()
                    bundles.setBundlesParameter(on_sale=default.ON_SALE,
                                                owner=default.OWNER,
                                                asset_contract_address=default.ASSET_CONTRACT_ADDRESS,
                                                asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                                token_ids=default.TOKEN_IDS,
                                                offset=default.OFFSET,
                                                limit=default.LIMIT,
                                                api_key=default.API_KEY)
                    bundles.loadAndSendPayload()
                    bundles.parseResponse()
            except Exception as ex:
                raise ex
            else:
                if default.SAVE:
                    st.markdown('### Save Data')
                    st.download_button('Download CSV',
                                       data=bundles.response_frame.to_csv().encode('utf-8'),
                                       file_name='data.csv',
                                       mime='text/csv')
                if default.VERBOSE:
                    st.markdown('### Display Data')
                    printDataFrame(data=bundles.response_frame,
                                   verbose_level=default.VERBOSITY,
                                   advanced=default.ADVANCED)

                bundles.resetAll()
