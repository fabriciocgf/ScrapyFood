import os
import streamlit as st

# Custom imports
from multipage import MultiPage
from pages import StoreListBuilder, StoreDatabaseBuilder, GeoAnalysis # import your pages here

# Create an instance of the app
app = MultiPage()

# # Title of the main page
# col2 = st.beta_columns(1)
# col2.title("Data Storyteller Application")

# Add all your application here
app.add_page("First Step", StoreListBuilder.app)
app.add_page("Second Step", StoreDatabaseBuilder.app)
app.add_page("GIS Analysis", GeoAnalysis.app)

# The main app
app.run()