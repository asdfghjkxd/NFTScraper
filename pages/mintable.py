import streamlit as st
import pandas as pd
import pages.config.mintable_config as default

from utils.utils import printDataFrame
from pages.classes.mintable_class import NFT, Auction


def app():
    """
    This is the function that runs when Mintable page is activated
    """

    st.title('Mintable Scraper')
    st.markdown('This app allows you to pull data from Opensea.io regarding the Assets, Events, Collections and '
                'Bundles listed on Mintable.')
    st.markdown('## Type of Data Retrieved')
    default.RETRIEVAL_METHOD = st.selectbox('Select Data Retrieval Type',
                                            ('NFT', 'Auction'))

    # ------------------------------------------------------------------------------------------------------------ #
    #                                                     NFT                                                      #
    # ------------------------------------------------------------------------------------------------------------ #
    if default.RETRIEVAL_METHOD == 'NFT':
        default.DATA_MODE = st.selectbox('Sub-Modes', ('Query Gasless NFTs', 'Query All NFTs', 'Query Single NFT'))

        st.markdown('## Flags\n'
                    '### Scraper Behaviour')
        if default.DATA_MODE == 'Query Gasless NFTs':
            default.USER_ADDRESS = st.text_input('Define User Address')

        elif default.DATA_MODE == 'Query All NFTs':
            default.CATEGORY = st.text_input('Define Category to Query')
            default.ADDRESS = st.text_input('Define Address')
            default.AUCTION = st.selectbox('Define Auction', (None, True, False))
            default.ORDER_BY_DATE = st.selectbox('Define Order By Data', (None, True, False))
            default.SIZE = st.number_input('Define Size',
                                           min_value=1,
                                           max_value=999999,
                                           value=1)
            default.LAST_KEY = st.number_input('Define Last Key',
                                               min_value=1,
                                               max_value=999999,
                                               value=1)
            default.NETWORK = st.number_input('Define Network',
                                              min_value=1,
                                              max_value=999999,
                                              value=1)

        elif default.DATA_MODE == 'Query Single NFT':
            default.ID = st.text_input('Define ID of NFT')
            default.API_KEY = st.text_input('Define API Key')

    elif default.RETRIEVAL_METHOD == 'Auction':
        default.DATA_MODE = st.selectbox('Sub-Modes', ('Ending Soon Auctions', 'Hot Auctions'))

    st.markdown('### App Behaviour')
    default.SAVE = st.checkbox('Save Outputs?', value=True)
    default.VERBOSE = st.checkbox('Display Outputs?', value=False)
    if default.VERBOSE:
        default.VERBOSITY = st.number_input('Number of Datapoints to Display?',
                                            min_value=0,
                                            max_value=10000,
                                            value=20)
        default.ADVANCED = st.checkbox('Show Advanced DataFrame Statistics', value=False)

    st.markdown('## Data Retrieval\n'
                'Ensure that the parameters you wish to pass into the class is loaded successfully.')

    if st.button('Proceed with Data Extraction'):
        if default.RETRIEVAL_METHOD == 'NFT':
            if default.DATA_MODE == 'Query Gasless NFTs':
                try:
                    nft = NFT()
                    nft.setGaslessNFTParameters(user_address=default.USER_ADDRESS)
                    nft.loadAndSendPayload()
                    nft.parseSingleNFT()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=nft.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=nft.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    nft.resetAll()

            elif default.DATA_MODE == 'Query All NFTs':
                try:
                    nft = NFT()
                    nft.setAllNFTParameter(category=default.CATEGORY,
                                           user_address=default.USER_ADDRESS,
                                           auction=default.AUCTION,
                                           order_by_date=default.ORDER_BY_DATE,
                                           size=default.SIZE,
                                           lastkey=default.LAST_KEY,
                                           network=default.NETWORK)
                    nft.loadAndSendPayload()
                    nft.parseAllNFTs()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=nft.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=nft.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    nft.resetAll()

            elif default.DATA_MODE == 'Query Single NFT':
                try:
                    nft = NFT()
                    nft.setSingleNFTParameter(id=default.ID,
                                              api_key=default.API_KEY)
                    nft.loadAndSendPayload()
                    nft.parseSingleNFT()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=nft.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=nft.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    nft.resetAll()

        elif default.DATA_MODE == 'Auction':
            if default.DATA_MODE == 'Ending Soon Auctions':
                try:
                    auction = Auction()
                    auction.setEndingSoonAuctions()
                    auction.loadAndSendPayload()
                    auction.parseEndingSoonAndHotAuctions()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=auction.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=auction.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    auction.resetAll()

            elif default.DATA_MODE == 'Hot Auctions':
                try:
                    auction = Auction()
                    auction.setHotAuctions()
                    auction.loadAndSendPayload()
                    auction.parseEndingSoonAndHotAuctions()
                except Exception as ex:
                    st.error(ex)
                else:
                    if default.SAVE:
                        st.markdown('### Save Data')
                        st.download_button('Download CSV',
                                           data=auction.response_frame.to_csv().encode('utf-8'),
                                           file_name='data.csv',
                                           mime='text/csv')
                    if default.VERBOSE:
                        st.markdown('### Display Data')
                        printDataFrame(data=auction.response_frame,
                                       verbose_level=default.VERBOSITY,
                                       advanced=default.ADVANCED)

                    auction.resetAll()
