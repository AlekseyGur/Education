from bs4 import BeautifulSoup as bs
from os.path import isfile as file_exist
from itertools import zip_longest
from time import sleep
import requests

# verbose включает вывод дополнительной отладочной информации
verbose = False

# file_save_mode включает сохранение загруженных данных на диск, чтобы не делать
# повторный запрос к сайту
file_save_mode = False


class Crawler():
    def get_vacancy_search_info(self, urls: list, num_pages: int = 1) -> list:
        """Выполняет сканирование страниц и сбор информации о вакансиях. Список
        сканируемых адресов самостоятельно дополняется нужными страницами
        пагинации результата.
        :param urls: URL адреса страниц со списками вакансий
        :param num_pages: желаемое количество страниц
        :return: список вакансий
        """
        vacancies = []  # тут будет список из словарей, содержащих данные о вакансиях

        # После первого запроса, при котором узнаётся макс. значение пагинации (кол-во стр),
        # формируются списки URL для обхода. В списки адресов подставляются нужные
        # значнения параметров пагинации.
        urls_chunks = []

        for url in urls:  # Первый раз сканируем, чтобы получить пагинацию
            site = self.get_site_code(url)  # символьный код сайта
            num_pages_this = num_pages

            dom = self.get_page_dom(url)  # dom BeautifulSoup с данными страницы сайта
            vacancies.extend(self.get_vacancies(dom, site))  # добавляем вакансии в список
            num_pages_max = self.get_page_max_num(dom, site)  # макс. кол-во страниц в выборке

            if num_pages_max < num_pages_this:  # просят больше страниц, чем есть
                num_pages_this = num_pages_max

            if 1 < num_pages_this:  # список для сканирования страниц в пагинации
                chunk = [self.inc_url_page_num(url, num, site) for num in range(1, num_pages_this)]

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

                    site = self.get_site_code(url)  # символьный код сайта
                    dom = self.get_page_dom(url)
                    vacancies.extend(self.get_vacancies(dom, site))

        return vacancies

    def get_site_code(self, site: str = '') -> str:
        """Получение символьного кода сайта"""
        if 'hh' in site:
            return 'hh'

        if 'superjob' in site:
            return 'superjob'

    def get_vacancy_id(self, url: str = '', site: str = '') -> str:
        """Получение уникального кода вакансии из URL адреса
        :param url: URL адрес страницы детального просмотра вакансии
        :param site: символьный код сайта
        :return: уникальный id вакансии
        """
        if not site:
            site = self.get_site_code(url)

        if 'hh' in site:
            # /vacancy/53825215
            return url.split('/')[-1]

        if 'superjob' in site:  # на сайте используется stormwall анти-DDoS
            # /vakansii/programmist-1s-37785388.html
            return url.split('-')[-1].replace('.html', '')

    def get_page_dom(self, url: str = ''):
        """Получение страницы сайта, преобразование в dom BeautifulSoup.
        :return: dom BeautifulSoup или None при ошибке
        """
        global verbose  # флаг дополнительной информации о процессе
        global file_save_mode  # флаг записи страниц сайта на диск, чтобы потом читать

        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
        response = None
        if file_save_mode:  # сохраняем данные и читаем с диска, без запроса к сайту
            safe_file_name = url.replace('/', '_')
            if not file_exist(safe_file_name + '.html'):  # записываем данные в файл
                response = requests.get(url, headers=headers)
                with open(safe_file_name + '.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)

            with open(safe_file_name + '.html', 'r', encoding='utf-8') as f:
                response = requests
                response.text = f.read()
                response.status_code = 200
                if verbose:
                    print(f'Из файла загружены данные для страницы: {url}')
        else:
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print('Ошибка загрузки страницы')
        else:
            if verbose:
                print(f'Загружена страница: {url}')

            try:
                dom = bs(response.text, 'html.parser')

                if 'stormwall' in response.text:
                    print('Сработал анти-DDoS на странице: ' + url)

                return dom
            except:
                print('Ошибка преобразования страницы в dom')

        return None

    def inc_url_page_num(self, url: str = '', num: int = 1, site: str = '') -> str:
        """Увеличение счётчика пагинации в URL адресе страницы
        :param url: URL с GET параметрами
        :param num: количество страниц для добавления
        :param site: символьный код сайта
        :return: url адрес следующей страницы паганации
        """
        if not site:
            site = self.get_site_code(url)

        base, params_str = url.split('?')
        params_vals = params_str.split('&')

        params = {}
        for pair_val in params_vals:
            key, val = pair_val.split('=')
            params[key] = val

        if site == 'hh':
            params['page'] = int(params['page']) + num
        elif site == 'superjob':
            params['page'] = int(params['page']) + num

        return base + '?' + '&'.join(f'{key}={val}' for key, val in params.items())

    def get_page_max_num(self, dom, site: str = '') -> int:
        """Получение максимального количества страниц в поисковой выдаче
        :param: dom страницы от BeautifulSoup
        :param site: символьный код сайта
        """
        if site == 'hh':
            try:
                return int(dom.select('.pager a span')[-2].getText())
            except:
                return 1
        elif site == 'superjob':
            try:
                selector = 'a.f-test-button-1.f-test-button_active.f-test-link-1'
                return int(dom.select(selector)[-1].parent.select('a')[-2].getText())
            except:
                return 1

        return 1

    def get_vacancies(self, dom, site: str = '') -> list:
        """Получение данных о вакансиях. Возвращает список словарей с полями:
        ['name'] - Наименование вакансии
        ['min'] - Минимальная зарплата
        ['max'] - Максимальная зарплата
        ['currency'] - Валюта зарплаты
        ['url'] - Ссылка на саму вакансию
        ['site'] - Сайт, откуда собрана вакансия

        :param: dom страницы от BeautifulSoup
        """
        vacancies = []  # Содержание вакансий

        if site == 'hh':
            vacancies_raw = dom.select('.vacancy-serp-content .vacancy-serp-item')
            for v in vacancies_raw:
                data = {}

                # Наименование вакансии
                name = v.select('h3')
                if name:
                    data['name'] = name[0].getText().replace('\t', ' ')

                if not name:
                    continue

                # Зарплата
                data['min'] = None  # минимальное значение
                data['max'] = None  # максимальное значение
                data['currency'] = None  # валюта
                salary = v.select('.bloko-header-section-3')
                if salary and len(salary) > 1:
                    salary_str = salary[1].getText().replace('\u202f', '')

                    if 'от' in salary_str:  # есть только минимальное значение
                        data['min'] = int(salary_str.split(' ')[1:-1][0].replace(' ', ''))
                    elif 'до' in salary_str:  # есть только максимальное значение
                        data['max'] = int(salary_str.split(' ')[1:-1][0].replace(' ', ''))
                    elif '–' in salary_str:  # диапазон
                        rng = salary_str.split(' ')[:-1]  # удалили валюту
                        rng_ar = ' '.join(rng).split('–')  # разделили запись "мин - макс"
                        data['min'] = int(rng_ar[0].replace(' ', ''))
                        data['max'] = int(rng_ar[1].replace(' ', ''))

                    data['currency'] = salary_str.split(' ')[-1].upper().replace('.', '')

                # Ссылка на саму вакансию
                url = v.select('h3 a')
                if url:
                    data['url'] = url[0]['href'].split('?')[0].split('hh.ru')[1]

                # Сайт, откуда собрана вакансия
                data['site'] = site

                vacancies.append(data)

        if site == 'superjob':
            vacancies_raw = dom.select('.f-test-search-result-item')
            for v in vacancies_raw:
                data = {}

                # Наименование вакансии
                name = v.select('span a[target=_blank]')
                if name:
                    data['name'] = name[0].getText().replace('\t', ' ')

                if not name:
                    continue

                # Зарплата
                data['min'] = None  # минимальное значение
                data['max'] = None  # максимальное значение
                data['currency'] = None  # валюта
                salary = v.select('.f-test-text-company-item-salary span')
                if salary and len(salary) > 0:
                    salary_str = salary[0].getText().replace('\xa0', ' ')

                    if any([char.isdigit() for char in salary_str]):
                        if 'от' in salary_str:  # есть только минимальное значение
                            data['min'] = int(''.join(salary_str.split(' ')[1:-1]))
                        elif 'до' in salary_str:  # есть только максимальное значение
                            data['max'] = int(''.join(salary_str.split(' ')[1:-1]))
                        elif '—' in salary_str:  # диапазон
                            rng = salary_str.split(' ')[:-1]  # удалили валюту
                            rng_ar = ' '.join(rng).split('—')  # разделили запись "мин - макс"
                            data['min'] = int(rng_ar[0].replace(' ', ''))
                            data['max'] = int(rng_ar[1].replace(' ', ''))

                        data['currency'] = salary_str.split(' ')[-1].upper().replace('.', '')

                # Ссылка на саму вакансию
                url = v.select('span a[target=_blank]')
                if url:
                    data['url'] = url[0]['href']

                # Сайт, откуда собрана вакансия
                data['site'] = site

                vacancies.append(data)

        return vacancies
