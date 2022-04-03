# Сборщик информации о вакансиях на вводимую должность с сайтов HH и Superjob.
# Анализирует несколько страниц сайта (input). Список содержит:
#
#     Наименование вакансии.
#     Предлагаемую зарплату (три поля: мин. и макс. и валюта.).
#     Ссылку на саму вакансию.
#     Сайт, откуда собрана вакансия.
#
# Результат сохраняется в csv.
# Результат выводится с помощью dataFrame через pandas.


from time import sleep
from itertools import zip_longest
# from pprint import pprint as print
import pandas as pd
from task_1_tools import *


# получаем от пользователя название вакансии и нужное кол-во страниц
# для сканирования
text = input('Название вакансии: ')
num_pages = int(input('Кол-во страниц для сканирования: '))

# Список из страниц для сканирования. Увсех ресурсов одновременно
# запрашивается сначала первая страница, вторая и т.д. Так экономим
# на задержке между сканированиями страниц одного ресурса.
# В адресе обязательно должен быть GET параметр page=1 или аналогичный,
# указывающий на то, что это первая страница в постраничной навигации.
urls = [
        # f'https://hh.ru/search/vacancy?text={text}&items_on_page=20&page=1',
        f'https://superjob.ru/vacancy/search/?keywords={text}&page=1'
        ]

vacancies = []  # тут будет список из словарей, содержащих данные о вакансиях

# После первого запроса, при котором узнаётся макс. значение пагинации (кол-во стр),
# формируются списки URL для обхода. В списки адресов подставляются нужные
# значнения параметров пагинации.
urls_chunks = []

for url in urls:  # Первый раз сканируем, чтобы получить пагинацию
    site = get_site_code(url)  # символьный код сайта
    num_pages_this = num_pages

    dom = get_page_dom(url)  # dom BeautifulSoup с данными страницы сайта
    vacancies.extend(get_vacancies(dom, site))  # добавляем вакансии в список
    num_pages_max = get_page_max_num(dom, site)  # макс. кол-во страниц в выборке

    if num_pages_max < num_pages_this:  # просят больше страниц, чем есть
        num_pages_this = num_pages_max

    if 1 < num_pages_this:  # список для сканирования страниц в пагинации
        chunk = [inc_url_page_num(url, num, site) for num in range(1, num_pages_this)]

        if chunk:
            urls_chunks.append(chunk)


if urls_chunks:  # адреса для будущего сканирования
    urls_chunks = list(zip_longest(*urls_chunks))

    # Если запрашивается больше одной страницы и есть пагинация, то повторяем
    # сканирование для нужного количества страниц
    for chunk in urls_chunks:
        sleep(5)  # задержка между запросами к всем сайтам

        for url in chunk:
            if not url:  # в chunk могут быть None из-за zip_longest
                continue

            site = get_site_code(url)  # символьный код сайта
            dom = get_page_dom(url)
            vacancies.extend(get_vacancies(dom, site))


# print(vacancies)

data = pd.DataFrame(vacancies)
print(pd.DataFrame(data))

# сохранение данных о вакансиях в файл
data.to_csv('data.csv', sep='\t')
