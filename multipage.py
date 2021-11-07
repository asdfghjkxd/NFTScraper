"""
Generates a helper class to assist with the generation of multiple Streamlit apps through object-oriented programming
"""

# IMPORT STREAMLIT
import numpy as np
import streamlit as st
import pathlib
import pandas as pd


# DEFINE THE MULTIPAGE CLASS TO MANAGE THE APPS
class MultiPage:
    """
    Combines and manages the different modules within the streamlit application
    """

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []

    def add_page(self, title, func) -> None:
        """
        Class Method to add pages to the project

        Arguments
        ----------
        title ([str]):          The title of page which we are adding to the list of apps
        func:                   Python function to render this page in Streamlit
        ----------
        """

        self.pages.append({"title": title,
                           "function": func
                           })

    def run(self):
        """
        Dropdown menu to select the page to run
        """
        with st.sidebar.container():
            st.markdown('# NFT Scraper\n'
                        'This app is used to scrape NFT Prices from popular NFT marketplaces, such as Opensea.io.')

        # PAGE SELECTOR
        page = st.sidebar.selectbox('Marketplace',
                                    self.pages,
                                    format_func=lambda page: page['title'])
        # RUN THE APP
        page['function']()
