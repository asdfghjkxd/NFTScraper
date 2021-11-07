# CUSTOM PAGE IMPORTS
import streamlit as st
from multipage import MultiPage
from pages import opensea

# INSTANTIATE THE APP
app = MultiPage()

# DEFINE THE PAGES AND THE APPS THEY CONTAIN
app.add_page('Opensea', opensea.app)

# RUN THE APP
app.run()
