import streamlit as st
import pandas as pd
import pages.config.rarible_config as default

from utils.utils import printDataFrame
from pages.classes.rarible_class import Collection, Item, Ownership, OrderActivity, OrderCollection, OrderItem, \
    OrderOwnership


def app():
    """
    This is the function that runs when Rarible page is activated
    """

    st.title('Rarible Scraper')
    st.markdown('This app allows you to pull data from Rarible regarding the Collections, Items, Ownership, '
                'Order Activity, Order Collections, Order Items and Order Ownership of NFT assets found on Rarible.')
    st.markdown('## Type of Data Retrieved')
    default.RETRIEVAL_METHOD = st.selectbox('Select Data Retrieval Type',
                                            ('Collections', 'Items', 'Ownership', 'Order Activity',
                                             'Order Collections', 'Order Items', 'Order Ownership'))

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                  Collections                                                 #
    # ------------------------------------------------------------------------------------------------------------ #
    if default.RETRIEVAL_METHOD == 'Collections':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Generate NFT ID', 'Query NFT Collection by ID',
                                                                       'Query Collections by Owner',
                                                                       'Query all Collections'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Collections Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                     Items                                                    #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Items':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Query NFT Metadata by ID',
                                                                       'Lazy Query NFT by ID', 'Query NFT by ID',
                                                                       'Query NFT by Owner', 'Query NFT by Creator',
                                                                       'Query NFT by Collection', 'Query all NFT'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Items Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                   Ownership                                                  #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Ownership':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Query NFT by ID', 'Query NFT by Item',
                                                                       'Query All NFT'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Ownership Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                Order Activity                                                #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Order Activity':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Query Order Activity by User',
                                                                       'Query Order Activity by Item',
                                                                       'Query Order Activity by Collection',
                                                                       'Query All Order Activity'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Order Activity Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                               Order Collections                                              #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Order Collections':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Generate NFT Order Token',
                                                                       'Query Order Collection by ID',
                                                                       'Query Order Collection by Owner',
                                                                       'Query All Order Collections'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Order Collections Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                  Order Items                                                 #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Order Items':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Query Order Items by ID',
                                                                       'Query Order Items Metadata by ID',
                                                                       'Lazy Query Order Items by ID',
                                                                       'Query Order Items by Owner',
                                                                       'Query Order Items by Creator',
                                                                       'Query Order Items by Collection',
                                                                       'Query Order All Order Items'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Order Items Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                 Order Ownership                                              #
    # ------------------------------------------------------------------------------------------------------------ #
    elif default.RETRIEVAL_METHOD == 'Order Ownership':
        default.QUERY_MODE = st.selectbox('Select Sub-Mode of Query', ('Query Order Ownership by Ownership ID',
                                                                       'Query Order Ownership by Item',
                                                                       'Query All Order Ownership'))
        st.markdown('## Flags\n'
                    '### Scraper Behaviour')

        st.markdown('### App Behaviour')
        default.SAVE = st.checkbox('Save Outputs?', value=True)
        default.VERBOSE = st.checkbox('Display Outputs?', value=False)
        if default.VERBOSE:
            default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                                min_value=0,
                                                max_value=10000,
                                                value=20)
            default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

        st.markdown('## Order Ownership Retrieval\n'
                    'Ensure that the parameters you wish to pass into the class is loaded successfully.')

        if st.button('Proceed'):
            pass
