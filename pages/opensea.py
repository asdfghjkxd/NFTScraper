import streamlit as st
import pandas as pd
from pages.classes.opensea_class import OpeanseaAssets, OpenseaEvents, OpenseaCollections, OpenseaBundles
import pages.config.opensea_config as default


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
    #                                                  App Modes                                                   #
    # ------------------------------------------------------------------------------------------------------------ #
    if default.RETRIEVAL_METHOD == 'Assets':
        # define flags
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.GET_ALL = st.checkbox('Scrape Maximum API Returns?', value=True)
        if not default.GET_ALL:
            if st.checkbox('Define owner Parameter', value=False):
                default.OWNER = st.text_input('Key in Address of Owner of Asset')

            if st.checkbox('Define token_ids Parameter', value=False):
                default.TOKEN_IDS = st.text_input('Key in Array of Token IDs to Search')

            if st.checkbox('Define asset_contract_addresses Parameter', value=False):
                default.ASSET_CONTRACT_ADDRESSES = st.text_input('Key in NFT Contract Address for Assets of Search',
                                                                 help='Note that if you wish to key in a list into the '
                                                                      'input box, delimit your addresses with commas.')
                if len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                    st.info('Addresses Detected!')
                else:
                    st.warning(
                        'Warning, No Address Detected. Proceeding in this state will result in a None value being '
                        'passed into asset_contract_addresses parameter.')
            if st.checkbox('Define order_by Parameter', value=False):
                default.ORDER_BY = st.selectbox('Select Order', ('token_id', 'sale_date', 'sale_count'))

            if st.checkbox('Define offset Parameter', value=True):
                default.OFFSET = st.number_input('Offset',
                                                 min_value=0,
                                                 max_value=10000,
                                                 value=0)

            if st.checkbox('Define limit Parameter', value=True):
                default.LIMIT = st.number_input('Limit',
                                                min_value=1,
                                                max_value=50,
                                                value=20)

            if st.checkbox('Define collection Parameter', value=False):
                default.COLLECTION = st.text_input('Limit responses to members of a Collection')

        if st.checkbox('Define order_direction Parameter', value=True):
            default.ORDER_DIRECTION = st.selectbox('Select Direction', ('asc', 'desc'))

        if st.checkbox('Define API Key', value=False):
            default.API_KEY = st.text_input('API Key')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)

        # start extraction
        st.markdown('## Asset Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed with Data Extraction'):
            # process the input addresses
            if default.ASSET_CONTRACT_ADDRESSES is not None and len(default.ASSET_CONTRACT_ADDRESSES) != 0:
                default.ASSET_CONTRACT_ADDRESSES = set(address.strip() for address in default.ASSET_CONTRACT_ADDRESSES.
                                                       split(sep=','))
                st.info(f'Addresses Loaded: {[address for address in default.ASSET_CONTRACT_ADDRESSES]}')

            try:
                if default.GET_ALL:
                    default.OFFSET = 0
                    default.LIMIT = 50
                    appender = []
                    for i in range(10000):
                        osa = OpeanseaAssets(owner=default.OWNER,
                                             token_ids=default.TOKEN_IDS,
                                             asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                             order_by=default.ORDER_BY,
                                             order_direction=default.ORDER_DIRECTION,
                                             offset=default.OFFSET,
                                             limit=default.LIMIT,
                                             collection=default.COLLECTION,
                                             api_key=default.API_KEY)
                        osa.constructRequest()
                        osa.sendRequest()
                        osa.parseRequest()
                        appender.append(osa.response_frame)
                        default.OFFSET += default.LIMIT
                    df = pd.concat(appender)

                else:
                    osa = OpeanseaAssets(owner=default.OWNER,
                                         token_ids=default.TOKEN_IDS,
                                         asset_contract_addresses=default.ASSET_CONTRACT_ADDRESSES,
                                         order_by=default.ORDER_BY,
                                         order_direction=default.ORDER_DIRECTION,
                                         offset=default.OFFSET,
                                         limit=default.LIMIT,
                                         collection=default.COLLECTION,
                                         api_key=default.API_KEY)
                    osa.constructRequest()
                    osa.sendRequest()
                    osa.parseRequest()
                    df = osa.response_frame
            except Exception as ex:
                st.error(f'Error: {ex}')
            else:
                if default.SAVE:
                    st.markdown('### Save Data')
                    st.download_button('Download CSV',
                                       data=df.to_csv().encode('utf-8'),
                                       file_name='data.csv',
                                       mime='text/csv')
                if default.VERBOSE:
                    st.markdown('### Display Data')
                    if default.VERBOSITY != 0:
                        st.dataframe(df.head(default.VERBOSITY))
                    else:
                        st.dataframe(df)

    elif default.RETRIEVAL_METHOD == 'Events':
        pass

    elif default.RETRIEVAL_METHOD == 'Collections':
        pass

    elif default.RETRIEVAL_METHOD == 'Bundles':
        pass
