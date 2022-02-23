import streamlit as st
import pandas as pd
import os
from scrapy.crawler import CrawlerRunner
from ScrapyFood.spiders.Data import DataSpider
from ScrapyFood.spiders.MenuData import MenudataSpider
from crochet import setup, wait_for # use this ti run scrapy more than one time

def app():

    setup() # use this ti run scrapy more than one time

    @wait_for(1000) # use this ti run scrapy more than one time
    def run_Data():
        process = CrawlerRunner({'FEEDS': {
            'Restaurants.csv': {
                'format': 'csv',
                "overwrite": True,
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 0,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                }
            }}})
        d = process.crawl(DataSpider)
        return d

    @wait_for(1000) # use this ti run scrapy more than one time
    def run_Menu():
        process = CrawlerRunner({'FEEDS': {
            'Items.csv': {
                'format': 'csv',
                "overwrite": True,
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 0,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                }
            }}})
        d = process.crawl(MenudataSpider)
        return d

    @st.cache
    def convert_df_to_csv(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    if 'button1' not in st.session_state:
        st.session_state.button1 = False

    if 'button2' not in st.session_state:
        st.session_state.button2 = False

    if 'button3' not in st.session_state:
        st.session_state.button3 = False

    st.markdown("## First lets generate the Database")
    left_column, right_column = st.columns(2)
    with left_column:
        if st.button('Generate Database using first step links'):
            run_Data()
            st.session_state.button1 = True
    with right_column:
        uploaded_file = st.file_uploader('Upload your links')
        if uploaded_file is not None:
            if not st.session_state.button1:
                st.write('Loading your links')
                with open(os.path.join(uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                os.rename(uploaded_file.name, 'stores_list.json')
                run_Data()
                st.session_state.button1 = True

    if st.session_state.button1:
        st.write('Database Ready')
        st.markdown("## Now let's filter this Database")
        df = pd.read_csv("Restaurants.csv", header=0)
        df.drop_duplicates(subset=['uuid'], inplace=True)
        df = df[df["tipo"].str.contains("tipo") == False]
        type = st.multiselect(
            "Select the Categories (Can be more than one):",
            options=df["tipo"].unique(),
            default=df["tipo"].unique()
        )
        if st.button('Save Filtered Database'):
            df_selection = df.query("tipo == @type")
            df_selection.to_csv("Restaurants.csv", index=False)
            st.session_state.button2 = True
    if st.session_state.button2:
        st.write('Filtered Database Saved')
        st.markdown("## Now we can get all the items sold im these stores")
        if st.button('Save items sold in these stores'):
            run_Menu()
            st.write('All store itens were saved')
            st.session_state.button3 = True
    if st.session_state.button3:
        st.markdown("## Now you can download your results")
        left_column, right_column = st.columns(2)
        with left_column:
            restaurants = pd.read_csv('Restaurants.csv')  # This is your 'my_large_df'

            st.download_button(
                label="Download Restaurant database",
                data=convert_df_to_csv(restaurants),
                file_name='Restaurants.csv',
                mime='text/csv',
            )
        with right_column:
            items = pd.read_csv('Items.csv')  # This is your 'my_large_df'

            st.download_button(
                label="Download Items database",
                data=convert_df_to_csv(items),
                file_name='Items.csv',
                mime='text/csv',
            )
