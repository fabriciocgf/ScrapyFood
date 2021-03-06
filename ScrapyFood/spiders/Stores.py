import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time

class StoresSpider(scrapy.Spider):
    name = "stores_spider"

    def start_requests(self):
        # Using a dummy website to start scrapy request
        url = "https://www.ifood.com.br/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        address = self.address
        search = self.search
        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        firefoxOptions.add_argument("--width=1920");
        firefoxOptions.add_argument("--height=1080");
        service = Service(GeckoDriverManager().install())
        wd = webdriver.Firefox(
            options=firefoxOptions,
            service=service,
        )
        wd.get("https://www.ifood.com.br/restaurantes")  # Site para começar o processo
        print("Abrindo Ifood")
        time.sleep(2)
        el = wd.find_element(By.CLASS_NAME, "address-search-input__button")  # seleciona que o endereço sera inputado
        el.click()
        time.sleep(1)
        el = wd.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[2]/div/div[1]/div[2]/input")  # seleciona a caixa de endereço
        el.click()
        el.send_keys(address)  # entra com o endereço
        print("Entrando com endereço: " + address)
        time.sleep(2)
        el = wd.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[2]/div/div[1]/div[3]/ul/li[1]")  # seleciona o primeiro endereço da lista
        el.click()
        time.sleep(2)
        el = wd.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[3]/div[2]/button")  # confirma o endereço no mapa
        el.click()
        print("Confirmando endereço")
        time.sleep(2)
        el = wd.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[3]/div[1]/div[2]/form/div[4]/button")  # ultima confirmação do endereço
        el.click()
        time.sleep(2)
        el = wd.find_element(By.XPATH, '//*[@id="__next"]/div/header/div/div[2]/form/div/input')  # Seleciona a caixa de busca do site
        el.click()
        el.send_keys(search)  # inputa o que deve ser buscado
        el.send_keys(Keys.ENTER)
        print("Buscando no site por: " + search)
        time.sleep(5)
        while len(wd.find_elements(By.CLASS_NAME, "search__load-more")) != 0:  # checa se existe o botao de carregar mais itens
            el = wd.find_element(By.CLASS_NAME, "search__load-more")  # seleciona o botão de carregar itens
            el.click()
            print("Verificando itens da página")
            time.sleep(1)
        time.sleep(2)
        source = wd.page_source  # resultado
        wd.close()
        soup = BeautifulSoup(source, 'html.parser')
        li = soup.find_all('li', {"class": "restaurants-list__item-wrapper"})
        hrefs = []
        for iten in li:
            a = iten.find('a', href=True).get('href')
            hrefs.append(a)
        hrefs = ["https://www.ifood.com.br" + href for href in hrefs]
        print("Foram achados " + str(len(hrefs)) + " restaurante")
        for link in hrefs:
            yield {
                "Link": link,
            }
