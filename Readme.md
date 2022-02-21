# Scrapy WebCrawler for iFood

## Stores Spider
```shell
scrapy crawl stores_spider -O stores_list.json -a address="R. João Cachoeira, 442 - Vila Nova Conceição" -a search="Mexicana"  -t jsonlines
```

## Restaurant data Spider
```shell
scrapy crawl data_spider -O Restaurants.csv -t csv 
```

## Restaurant Itens Spider
```shell
scrapy crawl menudata_spider -O Items.csv -t csv  
```