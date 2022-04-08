# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД


from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient


# собираем данные новостей с сайта
url = 'https://lenta.ru/parts/news/'
header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
news_list = dom.xpath("(//li[contains(@class,'parts-page__item')])[position() < last()]")

news = []
for el in news_list:
    info = {}

    name = el.xpath(".//h3//text()")
    link = el.xpath(".//a/@href")

    info['source'] = 'lenta'  # название источника;
    info['name'] = name[0]  # наименование новости;
    info['link'] = link[0]  # ссылку на новость;
    _, _, year, month, day, *_ = link[0].split('/')  # дата публикации (из ссылки)
    info['date'] = f'{year}-{month}-{day}'

    news.append(info)

# сохраняем результаты в базу
client = MongoClient('127.0.0.1', 27017)  # соединение
mongodb = client['news']  # база
newsdb = mongodb.newsdb  # коллекция

for el in news:
    try:
        el['_id'] = el['link']
        newsdb.insert_one(el)
    except Exception as e:
        print('Ошибка при сохранении новости в базу:')
        print(e)
