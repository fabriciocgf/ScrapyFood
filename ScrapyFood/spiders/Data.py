import scrapy
import json

class DataSpider(scrapy.Spider):
    name = "data_spider"
    try:
        temp_list = []
        with open("stores_list.json", "r") as f:
            for line in f:
                temp_list.append(json.loads(line))

        start_urls = list(map(lambda x: x["Link"], temp_list))
    except:
        start_urls =[]

    def parse(self, response):
        jsondata = response.xpath('/html/body/script[1]').get()[51:-9]
        newDictionary = json.loads(str(jsondata))
        try:
            if newDictionary['props']['initialState']['restaurant']['details']["name"] != "iFood":
                try:
                    telefone = newDictionary['props']['initialState']['restaurant']['details']["telephone"]  # getting the telephone and so on..
                except KeyError as error:
                    telefone = "-"

                try:
                    nome = newDictionary['props']['initialState']['restaurant']['details']['name']
                except KeyError as error:
                    nome = "-"

                try:
                    tipo = newDictionary['props']['initialState']['restaurant']['details']['mainCategory']['friendlyName']
                except KeyError as error:
                    tipo = "-"

                try:
                    nomerua = newDictionary['props']['initialState']['restaurant']['details']['address']['streetName']
                except KeyError as error:
                    nomerua = "-"

                try:
                    bairro = newDictionary['props']['initialState']['restaurant']['details']['address']['district']
                except KeyError as error:
                    bairro = "-"

                try:
                    CEP = newDictionary['props']['initialState']['restaurant']['details']['address']['zipCode']
                except KeyError as error:
                    CEP = "-"

                try:
                    Latitude = newDictionary['props']['initialState']['restaurant']['details']['address']['latitude']
                except KeyError as error:
                    Latitude = "-"

                try:
                    Longitude = newDictionary['props']['initialState']['restaurant']['details']['address']['longitude']
                except KeyError as error:
                    Longitude = "-"


                newDictionary_BM = json.loads(str(jsondata))  # here is the same thing as before, but the info is allocated in a different part os the web site
                try:
                    KA = newDictionary_BM['props']['initialState']['restaurant']['details']['tags']
                except KeyError as error:
                    KA = "-"
                categoria = []
                if "KEY_ACCOUNT" in KA:
                    categoria = "Key Account"
                elif "CONTA_ESTRATEGICA" in KA:
                    categoria = "City Key Account"
                else:
                    categoria = "Normal"

                if "SO_TEM_NO_IFOOD" in KA:
                    contrato = "Exclusivo"
                else:
                    contrato = "Não Exclusivo"

                try:
                    data = newDictionary_BM['props']['initialState']['restaurant']['details']['groups']
                except KeyError as error:
                    data = "-"
                bm = []
                for i in data:
                    if i['type'] == 'BUSINESS_MODEL':
                        bm = i['name']
                try:
                    sr = newDictionary_BM['props']['initialState']['restaurant']['details']['superRestaurant']
                except KeyError as error:
                    sr = "-"

                try:
                    numrating = newDictionary_BM['props']['initialState']['restaurant']['details'][
                        'userRatingCount']
                except KeyError as error:
                    numrating = "-"

                try:
                    rating = newDictionary_BM['props']['initialState']['restaurant']['details']['evaluationAverage']
                except KeyError as error:
                    rating = "-"


            else:
                nome = "Link inválido"
                telefone = ""
                tipo = ""
                nomerua = ""
                bairro = ""
                CEP = ""
                Latitude = ""
                Longitude = ""
                bm = ""
                categoria = ""
                contrato = ""
                sr = ""
                rating = ""
                numrating = ""
        except KeyError as error:
            nome = "Link inválido"
            telefone = ""
            tipo = ""
            nomerua = ""
            bairro = ""
            CEP = ""
            Latitude = ""
            Longitude = ""
            bm = ""
            categoria = ""
            contrato = ""
            sr = ""
            rating = ""
            numrating = ""

        out = [nome, telefone, tipo, nomerua, bairro, CEP, Latitude, Longitude, bm, categoria, contrato, sr, rating, numrating, newDictionary['query']['uuid'], response.request.url]
        label = ['Nome', 'Tel', 'tipo', 'Endereço', 'Bairro', 'CEP', 'Lat', 'Long', 'Business Model', 'Categoria', 'Contrato', 'SuperRs', 'rating', 'numrating', 'uuid', 'Link']
        yield dict(zip(label,out))