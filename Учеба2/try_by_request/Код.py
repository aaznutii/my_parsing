import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
# import parser
import time
import random

# Шаг 1. ПОДГОТОВКА: проверяем ответ сайта  и определяем тип ответа.
# Создаем заголовок запроса
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
#
# url = 'https://samara.cian.ru/kupit-kvartiru/'
# response = requests.get(url, headers=headers).text
# print(response)
# Передаем структуру в суп.Ищем те поля, которые необходимо парсить и функцией найти проверяем корректность доступа.
# soup = BeautifulSoup(response, "lxml")
# в структуре нашли само объявление (как объект соупа).
# articles = soup\
#         .find('div', attrs={"data-name" : "Offers"})\
#         .find_all('article', attrs={"data-name" : "CardComponent"}) # в тесте используем файнд, в работе файнд_ол
# print(articles)
# Проверяем доступность искомых данных (ссылки) через цикл.-вернет две строки. Каждая ссылка - страница с квартирой
# links = []
# for row in articles[0:2]:
#         a = row.find('a').get('href')
#         links.append(data)
# print(links)
# ШАГ 2. Превращаем работающий код в функции.
def get_html(url):
    req = requests.get(url, headers=headers)
    return req.text

# def try_except (argument):
# def count_pages(html):
    # soup = BeautifulSoup(html, "lxml")
    # all_pages = soup.find('ul', attrs={"class" : "HEGFW"}).find_all('href')
    # return all_pages

# url = 'https://samara.cian.ru/kupit-kvartiru/'
# print(len(count_pages(get_html(url))))

def get_all_links(html):
    soup = BeautifulSoup(html, "lxml")
    articles = soup\
        .find('div', attrs={"data-name" : "Offers"})\
        .find_all('article', attrs={"data-name": "CardComponent"})
    links = []
    for row in articles:                                  # на этапе теста ограничим выборку 2мя ссылками articles[2]
        a = row.find('a').get('href')
        links.append(a)
    return links

def get_article_data(html):
    data = []
    soup = BeautifulSoup(html, "lxml")
    title = soup.find('h1').text
    price = soup.find('span', attrs={"itemprop": "price"}).text
    geo = soup.find('div', attrs={"data-name": "Geo"}).text
    # article_info = [title,'|'+price, '|'+geo]
    article_info = {'title': title,
                    'price': price,
                    'geo': geo}
    data.append(article_info)
    return data

def main():
    url = 'https://samara.cian.ru/kupit-kvartiru/'
    # count_pages(get_html(url))
    all_links = get_all_links(get_html(url))
    columns = ['link', 'data', 'time']
    rend_time = random.randrange(1, 4, 1)
    all_date = []
    for i in all_links:
        time.sleep(rend_time)
        start = datetime.now()
        html = get_html(i)
        data = get_article_data(html)
        line = [i, data, start]
        all_date.append(line)
        print(i, 'parsed', start)
    df = pd.DataFrame(all_date, columns=columns)
    df.to_csv('G:\DataA/writer_test_2.csv', sep='|')

if __name__ == '__main__':
        main()



