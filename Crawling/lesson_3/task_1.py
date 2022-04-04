# Сборщик информации о вакансиях на вводимую должность с сайтов HH и Superjob.
# Анализирует несколько страниц сайта (input). Список содержит:
#
#     Наименование вакансии.
#     Предлагаемую зарплату (три поля: мин. и макс. и валюта.).
#     Ссылку на саму вакансию.
#     Сайт, откуда собрана вакансия.
#
# Результат сохраняется в csv.
# Результат сохраняется в базу данных.
# Результат выводится с помощью dataFrame через pandas.

import pandas as pd
from task_1_tools import *
from task_1_db import *


# получаем от пользователя название вакансии и нужное кол-во страниц
# для сканирования
text = input('Название вакансии: ')
num_pages = int(input('Кол-во страниц для сканирования: '))

# Список из страниц для сканирования. Увсех ресурсов одновременно
# запрашивается сначала первая страница, вторая и т.д. Так экономим
# на задержке между сканированиями страниц одного ресурса.
# В адресе обязательно должен быть GET параметр page=1 или аналогичный,
# указывающий на то, что это первая страница в постраничной навигации.
urls = [f'https://hh.ru/search/vacancy?text={text}&items_on_page=20&page=1',
        f'https://superjob.ru/vacancy/search/?keywords={text}&page=1']

cr = Crawler()  # сбор информации о вакансиях
vacancies = cr.get_vacancy_search_info(urls, num_pages)

db = DB()
for vacancy in vacancies:  # сохранение данных о вакансии в базу
    db.add_vacancy(vacancy, cr.get_vacancy_id(vacancy['url'], vacancy['site']))

data = pd.DataFrame(vacancies)
data.to_csv('data.csv', sep='\t')  # сохранение данных о вакансиях в файл
print(pd.DataFrame(data))
