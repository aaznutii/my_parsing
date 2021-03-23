from datetime import datetime
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}

url = 'https://samara.cian.ru/kupit-kvartiru/'
response = requests.get(url, headers=headers).text
# print(response)
# Передаем структуру в суп.Ищем те поля, которые необходимо парсить и функцией найти проверяем корректность доступа.
soup = BeautifulSoup(response, "lxml")
# в структуре нашли само объявление (как объект соупа).
articles = soup\
        .find('div', attrs={"data-name" : "Offers"})\
        .find('article', attrs={"data-name" : "CardComponent"}) # в тесте используем файнд, в работе файнд_ол
print(articles.text)
