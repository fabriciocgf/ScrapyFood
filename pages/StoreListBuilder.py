import streamlit as st
import os
from scrapy.crawler import CrawlerRunner
from ScrapyFood.spiders.Stores import StoresSpider
from crochet import setup, wait_for # use this ti run scrapy more than one time

def app():

    setup() # use this ti run scrapy more than one time

    @wait_for(1000) # use this ti run scrapy more than one time
    def run_spider(address,search):
        process = CrawlerRunner({'FEEDS': {
            'stores_list.json': {
                'format': 'jsonlines',
                "overwrite": False,
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 0,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                }
            }}})
        d = process.crawl(StoresSpider, address=address, search=search)
        return d

    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    st.markdown("## Build your list of iFood stores")
    st.markdown("Enter the Address and Search term that you want to find in the ifood site")
    st.markdown(
        "Repeat this as many times you want, do it for diferent edresses but keep the same Search term to augment your list of stores")
    with st.form("my_form"):
        address_text = st.text_input("Address")
        search_text = st.text_input("Search Term")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Address:", address_text, "Search Term: ", search_text)
            st.write("Processing your query")
            if st.session_state.first_run:
                try:
                    os.remove('stores_list.json')
                except:
                    pass
                run_spider(address_text, search_text)
            else:
                run_spider(address_text, search_text)

            st.write("You can run your next search")
            st.session_state.first_run = False
