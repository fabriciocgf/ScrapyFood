import streamlit as st
import subprocess
import pandas as pd
import os

def app():
    if 'button1' not in st.session_state:
        st.session_state.button1 = False

    if 'button2' not in st.session_state:
        st.session_state.button2 = False

    st.markdown("## First lets generate the Database")
    left_column, right_column = st.columns(2)
    with left_column:
        if st.button('Generate Database using first step links'):
            scrapy = subprocess.run('scrapy crawl data_spider -O Restaurants.csv -t csv', shell=True)
            st.session_state.button1 = True
    with right_column:
        uploaded_file = st.file_uploader('Upload your links')
        if uploaded_file is not None:
            if not st.session_state.button1:
                st.write('Loading your links')
                with open(os.path.join(uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                scrapy = subprocess.run('scrapy crawl data_spider -O Restaurants.csv -t csv', shell=True)
                st.session_state.button1 = True

    if st.session_state.button1:
        st.write('Database Ready')
        st.markdown("## Now let's filter this Database")
        df = pd.read_csv("Restaurants.csv")
        df.drop_duplicates(subset=['uuid'], inplace=True)
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
            scrapy = subprocess.run('scrapy crawl menudata_spider -O Itens.csv -t csv', shell=True)
            st.write('All store itens were saved')