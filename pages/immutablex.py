import streamlit as st

from utils.utils import printDataFrame
from pages.classes.immutablex_class import Assets, Collections, Tokens
import pages.config.immutablex_config as default


def app():
    """
    This is the function that runs when ImmutableX page is activated
    """

    st.title('ImmutableX Scraper')
    st.markdown('This module allows you to pull data from ImmutableX regarding Assets, Collections and Tokens listed '
                'the Marketplace.')
    st.markdown('## Type of Data Retrieved')
    default.RETRIEVAL_METHOD = st.selectbox('Select Data Retrieval Type', ('Assets', 'Collections', 'Tokens'))

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                   Assets                                                     #
    # ------------------------------------------------------------------------------------------------------------ #
    if default.RETRIEVAL_METHOD == 'Assets':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.QUERY_MODE = st.selectbox('Select Type of Query to Execute', ('Get List of Assets',
                                                                              'Get Details of Single Asset'))
        if default.QUERY_MODE == 'Get List of Assets':
            st.info('**Get List of Assets** Mode Selected!')
            default.QUERY_PARAMS = st.multiselect('Select Parameters to Define',
                                                  ('page_size', 'cursor', 'order_by', 'direction', 'user', 'status',
                                                   'name', 'metadata', 'sell_orders', 'buy_orders', 'includes_fee',
                                                   'collection', 'updated_min_timestamp', 'updated_max_timestamp'))

            if 'page_size' in default.QUERY_PARAMS:
                default.PAGE_SIZE = st.number_input('Key in the page size of the result',
                                                    min_value=0,
                                                    max_value=999999,
                                                    value=1)
            if 'cursor' in default.QUERY_PARAMS:
                default.CURSOR = st.text_input('Define Cursor for your query', help='Use this to define the number of '
                                                                                    'results to return per query.')
            if 'order_by' in default.QUERY_PARAMS:
                default.ORDER_BY = st.selectbox('Select Property to sort by in result', (None, 'updated_at', 'name'))
            if 'direction' in default.QUERY_PARAMS:
                default.DIRECTION = st.selectbox('Select direction to sort results by', (None, 'asc', 'desc'))
            if 'user' in default.QUERY_PARAMS:
                default.USER = st.text_input('Define Ethereum address of owner of asset of query')
            if 'status' in default.QUERY_PARAMS:
                default.STATUS = st.text_input('Define status of asset of query')
            if 'name' in default.QUERY_PARAMS:
                default.NAME = st.text_input('Define name of asset of query')
            if 'metadata' in default.QUERY_PARAMS:
                default.METADATA = st.text_area('Define JSON-encoded metadata filters for asset of query')
            if 'sell_orders' in default.QUERY_PARAMS:
                default.SELL_ORDERS = st.selectbox('Select Flag to fetch array of sell order details for asset of '
                                                   'query', (None, True, False))
            if 'buy_orders' in default.QUERY_PARAMS:
                default.SELL_ORDERS = st.selectbox('Select Flag to fetch array of buy order details for asset of '
                                                   'query', (None, True, False))
            if 'includes_fee' in default.QUERY_PARAMS:
                default.INCLUDE_FEES = st.selectbox('Select Flag to fetch array of fees for asset of query',
                                                    (None, True, False))
            if 'collection' in default.QUERY_PARAMS:
                default.COLLECTION = st.text_input('Define Collection contract address for asset of query')
            if 'updated_min_timestamp' in default.QUERY_PARAMS:
                default.UPDATED_MIN_TIMESTAMP = str(st.date_input('Define minimum timestamp for when asset of query '
                                                                  'was last updated'))
            if 'updated_max_timestamp' in default.QUERY_PARAMS:
                default.UPDATED_MAX_TIMESTAMP = str(st.date_input('Define maximum timestamp for when asset of query '
                                                                  'was last updated'))
        elif default.QUERY_MODE == 'Get Details of Single Asset':
            st.info('**Get Details of Single Asset** Mode Selected!')
            default.TOKEN_ADDRESS = st.text_input('Define address of ERC721 contract')
            default.TOKEN_ID = st.text_input('Define ERC721 token ID or Internal IMX ID')
            if default.TOKEN_ADDRESS != '' and default.TOKEN_ID != '':
                default.ASSERT_INPUTS = True
            else:
                default.ASSERT_INPUTS = False
            if st.checkbox('Define other Query Parameters'):
                default.INCLUDE_FEES = st.selectbox('Select Flag to fetch array of fees for asset of query',
                                                    (None, True, False))

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Query Assets')
        # check if required params are inputted
        if default.QUERY_MODE == 'Get Details of Single Asset':
            if default.ASSERT_INPUTS is False:
                st.warning('Warning: One or more of the required parameters are not defined properly. '
                           'Proceeding in this state will raise exceptions.')

        if st.button('Proceed', key='assets'):
            if default.QUERY_MODE == 'Get List of Assets':
                try:
                    asset = Assets()
                    asset.setListAssetParameter(page_size=default.PAGE_SIZE,
                                                cursor=default.CURSOR,
                                                order_by=default.ORDER_BY,
                                                direction=default.DIRECTION,
                                                user=default.USER,
                                                status=default.STATUS,
                                                name=default.NAME,
                                                metadata=default.METADATA,
                                                sell_orders=default.SELL_ORDERS,
                                                buy_orders=default.BUY_ORDERS,
                                                include_fees=default.INCLUDE_FEES,
                                                collection=default.COLLECTION,
                                                updated_min_timestamp=default.UPDATED_MIN_TIMESTAMP,
                                                updated_max_timestamp=default.UPDATED_MAX_TIMESTAMP)
                    asset.loadAndSendPayload()
                    asset.parseAllAssets()
                except Exception as ex:
                    st.error(ex)
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

            elif default.QUERY_MODE == 'Get Details of Single Asset':
                if default.QUERY_MODE == 'Get Details of Single Asset':
                    if not default.ASSERT_INPUTS:
                        st.error('Error: One or more of the required parameters are not defined properly.')
                    else:
                        st.success('Parameters Accepted!')

                        try:
                            asset = Assets()
                            asset.setSingleAssetParameter(token_address=default.TOKEN_ADDRESS,
                                                          token_id=default.TOKEN_ID,
                                                          include_fees=default.INCLUDE_FEES)
                            asset.loadAndSendPayload()
                            asset.parseSingleAsset()
                        except Exception as ex:
                            st.error(ex)
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
    #                                                  Collections                                                 #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Collections':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.QUERY_MODE = st.selectbox('Select Type of Query to Execute',
                                          ('Get List of Collections', 'Get Details of Single Collection',
                                           'Get Collection Filters'))
        if default.QUERY_MODE == 'Get List of Collections':
            st.info('**Get List of Collections** Mode Selected!')
            default.QUERY_PARAMS = st.multiselect('Select Parameters to Define',
                                                  ('page_size', 'cursor', 'order_by', 'direction', 'blacklist'))

            if 'page_size' in default.QUERY_PARAMS:
                default.PAGE_SIZE = st.number_input('Key in the page size of the result',
                                                    min_value=0,
                                                    max_value=999999,
                                                    value=1)
            if 'cursor' in default.QUERY_PARAMS:
                default.CURSOR = st.text_input('Define Cursor for your query', help='Use this to define the number of '
                                                                                    'results to return per query.')
            if 'order_by' in default.QUERY_PARAMS:
                default.ORDER_BY = st.selectbox('Select Property to sort by in result', (None, 'updated_at', 'name'))
            if 'direction' in default.QUERY_PARAMS:
                default.DIRECTION = st.selectbox('Select direction to sort results by', (None, 'asc', 'desc'))
            if 'blacklist' in default.QUERY_PARAMS:
                default.BLACKLIST = st.text_input('Define collections to not display',
                                                  help='Separate collections by collection name')

        elif default.QUERY_MODE == 'Get Details of Single Collection':
            st.info('**Get Details of Single Collection** Mode Selected!')
            default.ADDRESS = st.text_input('Define Collection contract address')

            if default.ADDRESS != '':
                default.ASSERT_INPUTS = True
            else:
                default.ASSERT_INPUTS = False

        elif default.QUERY_MODE == 'Get Collection Filters':
            st.info('**Get Collection Filters** Mode Selected!')
            default.ADDRESS = st.text_input('Define Collection contract address')

            if default.ADDRESS != '':
                default.ASSERT_INPUTS = True
            else:
                default.ASSERT_INPUTS = False

            if st.checkbox('Define Other Paramters'):
                default.QUERY_PARAMS = st.multiselect('Select Parameters to Define',
                                                      ('page_size', 'next_page_token'))
                if 'page_size' in default.QUERY_PARAMS:
                    default.PAGE_SIZE = st.number_input('Key in the page size of the result',
                                                        min_value=0,
                                                        max_value=999999,
                                                        default=1)
                if 'next_page_token' in default.QUERY_PARAMS:
                    default.NEXT_PAGE_TOKEN = st.text_input('Define the next page token')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Collections Query')
        if default.QUERY_MODE == 'Get Details of Single Collection' or default.QUERY_MODE == 'Get Collection Filters':
            if not default.ASSERT_INPUTS:
                st.warning('Warning: One or more of the required parameters are not defined properly. '
                           'Proceeding in this state will raise exceptions.')

        if st.button('Proceed', key='collections'):
            if default.QUERY_MODE == 'Get List of Collections':
                try:
                    collection = Collections()
                    collection.setCollectionListParameters(page_size=default.PAGE_SIZE,
                                                           cursor=default.CURSOR,
                                                           order_by=default.ORDER_BY,
                                                           direction=default.DIRECTION,
                                                           blacklist=default.BLACKLIST)
                    collection.loadAndSendPayload()
                    collection.parseAllCollections()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=collection.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=collection.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    collection.resetAll()

            elif default.QUERY_MODE == 'Get Details of Single Collection':
                if not default.ASSERT_INPUTS:
                    st.error('Error: One or more of the required parameters are not defined properly.')
                else:
                    try:
                        collection = Collections()
                        collection.setSingleCollectionParameters(address=default.ADDRESS)
                        collection.loadAndSendPayload()
                        collection.parseSingleCollection()
                    except Exception as ex:
                        st.error(ex)
                    else:
                        if default.SAVE:
                            st.markdown('### Save Data')
                            st.download_button('Download CSV',
                                               data=collection.response_frame.to_csv().encode('utf-8'),
                                               file_name='data.csv',
                                               mime='text/csv')
                        if default.VERBOSE:
                            st.markdown('### Display Data')
                            printDataFrame(data=collection.response_frame,
                                           verbose_level=default.VERBOSITY,
                                           advanced=default.ADVANCED)

                        collection.resetAll()

            elif default.QUERY_MODE == 'Get Collection Filters':
                if not default.ASSERT_INPUTS:
                    st.error('Error: One or more of the required parameters are not defined properly.')
                else:
                    try:
                        collection = Collections()
                        collection.setCollectionFilter(address=default.ADDRESS,
                                                       page_size=default.PAGE_SIZE,
                                                       next_page_token=default.NEXT_PAGE_TOKEN)
                        collection.loadAndSendPayload()
                        collection.parseSingleCollection()
                    except Exception as ex:
                        st.error(ex)
                    else:
                        if default.SAVE:
                            st.markdown('### Save Data')
                            st.download_button('Download CSV',
                                               data=collection.response_frame.to_csv().encode('utf-8'),
                                               file_name='data.csv',
                                               mime='text/csv')
                        if default.VERBOSE:
                            st.markdown('### Display Data')
                            printDataFrame(data=collection.response_frame,
                                           verbose_level=default.VERBOSITY,
                                           advanced=default.ADVANCED)

                        collection.resetAll()

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                     Tokens                                                   #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Tokens':
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        default.QUERY_MODE = st.selectbox('Select Type of Query to Execute',
                                          ('Get List of Tokens', 'Get Details of Single Token'))

        if default.QUERY_MODE == 'Get List of Tokens':
            default.QUERY_PARAMS = st.multiselect('Select Parameters to Define',
                                                  ('page_size', 'next_page_token'))

            if 'page_size' in default.QUERY_PARAMS:
                default.PAGE_SIZE = st.number_input('Key in the page size of the result',
                                                    min_value=0,
                                                    max_value=999999,
                                                    value=1)
            if 'next_page_token' in default.QUERY_PARAMS:
                default.NEXT_PAGE_TOKEN = st.text_input('Define the next page token')

        elif default.QUERY_MODE == 'Get Details of Single Token':
            default.ADDRESS = st.text_input('Define Collection contract address')

            if default.ADDRESS != '':
                default.ASSERT_INPUTS = True
            else:
                default.ASSERT_INPUTS = False

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Token Query')
        if default.QUERY_MODE == 'Get Details of Single Token':
            if not default.ASSERT_INPUTS:
                st.warning('Warning: One or more of the required parameters are not defined properly. '
                           'Proceeding in this state will raise exceptions.')

        if st.button('Proceed', key='token'):
            if default.QUERY_MODE == 'Get List of Tokens':
                try:
                    token = Tokens()
                    token.setTokenListParameters(address=default.ADDRESS,
                                                 symbol=default.SYMBOL)
                    token.loadAndSendPayload()
                    token.parseAllTokens()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=token.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=token.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    token.resetAll()

            elif default.QUERY_MODE == 'Get Details of Single Token':
                if not default.ASSERT_INPUTS:
                    st.error('Error: One or more of the required parameters are not defined properly.')
                else:
                    try:
                        token = Tokens()
                        token.setSingleTokenParameters(address=default.ADDRESS)
                        token.loadAndSendPayload()
                        token.parseSingleToken()
                    except Exception as ex:
                        st.error(ex)
                    else:
                        if default.SAVE:
                            st.markdown('### Save Data')
                            st.download_button('Download CSV',
                                               data=token.response_frame.to_csv().encode('utf-8'),
                                               file_name='data.csv',
                                               mime='text/csv')
                        if default.VERBOSE:
                            st.markdown('### Display Data')
                            printDataFrame(data=token.response_frame,
                                           verbose_level=default.VERBOSITY,
                                           advanced=default.ADVANCED)
