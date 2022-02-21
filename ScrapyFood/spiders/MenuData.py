import scrapy
import csv
import json

class MenudataSpider(scrapy.Spider):
    name = 'menudata_spider'
    allowed_domains = ['www.ifood.com.br']
    try:
        with open("Restaurants.csv", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            start_urls = [x["Link"] for x in reader]
    except:
        start_urls = []

    def parse(self, response):
        jsondata = response.xpath('/html/body/script[1]').get()[51:-9]
        newDictionary = json.loads(str(jsondata))
        if newDictionary['props']['initialState']['restaurant']['details']["name"] != "iFood":
            try:
                nome = newDictionary['props']['initialState']['restaurant']['details']['name']
            except KeyError as error:
                nome = "-"

            try:
                menu = newDictionary['props']['initialState']['restaurant']['menu']
            except KeyError as error:
                menu = []

            for type in menu:
                for item in type['itens']:
                    try:
                        item_name = item['description'].replace('\n', ' ')
                    except KeyError as error:
                        item_name = None

                    try:
                        item_description = item['details'].replace('\n', ' ')
                    except KeyError as error:
                        item_description = None

                    try:
                        item_price = item['unitMinPrice']
                    except KeyError as error:
                        item_price = None

                    try:
                        item_uuid = item['id']
                    except KeyError as error:
                        item_uuid = None

                    yield {"Name":nome, "uuid":newDictionary['query']['uuid'], "Item_uuid":item_uuid, "Item_name":item_name, "item_description":item_description, "item_price":item_price}