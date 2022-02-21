import streamlit as st
import subprocess
import os

def app():
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    st.markdown("## Build your list of iFood stores")
    st.markdown("Enter the Address and Search term that you want to find in the ifood site")
    st.markdown("Repeat this as many times you want, do it for diferent edresses but keep the same Search term to augment your list of stores")
    with st.form("my_form"):
        address_text = st.text_input("Address")
        search_text = st.text_input("Search Term")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Address:", address_text, "Search Term: ", search_text)
            st.write("Processing your query")
            if st.session_state.first_run:
                try:
                    os.remove('stores_list.json')
                except:
                    pass
                scrapy = subprocess.run('scrapy crawl stores_spider -O stores_list.json -a address="' + address_text +  '" -a search="' + search_text+ '" -t jsonlines', shell=True)
            else:
                scrapy = subprocess.run('scrapy crawl stores_spider -o stores_list.json -a address="' + address_text + '" -a search="' + search_text + '" -t jsonlines', shell=True)
            st.write("You can run your next search")
            st.session_state.first_run = False
