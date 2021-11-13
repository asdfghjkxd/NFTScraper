# CUSTOM PAGE IMPORTS
import streamlit as st
from multipage import MultiPage
from pages import opensea, immutablex

# INSTANTIATE THE APP
app = MultiPage()

# DEFINE THE PAGES AND THE APPS THEY CONTAIN
app.add_page('Opensea', opensea.app)
app.add_page('ImmutableX', immutablex.app)

# RUN THE APP
app.run()
