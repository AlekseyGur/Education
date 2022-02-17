# Задание 2
#
# В корневой директории урока создать task_4_2.py и написать в нём функцию currency_rates(), принимающую в качестве аргумента код валюты (например, USD, EUR, SGD, ...) и возвращающую курс этой валюты по отношению к рублю.
#
# Использовать библиотеку requests.
#
# В качестве API можно использовать http://www.cbr.ru/scripts/XML_daily.asp.
#
#     Рекомендация: выполнить предварительно запрос к API в обычном браузере, посмотреть содержимое ответа.
#
#     Можно ли, используя только методы класса str, решить поставленную задачу?
#     Функция должна возвращать результат числового типа, например float.
#
# Подумайте:
#
#     есть ли смысл для работы с денежными величинами использовать вместо float тип Decimal?
#     Сильно ли усложняется код функции при этом?
#
# Если в качестве аргумента передали код валюты, которого нет в ответе, вернуть None.
#
# Можно ли сделать работу функции не зависящей от того, в каком регистре был передан аргумент?
# В качестве примера выведите курсы доллара и евро.
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# import requests
#
# def currency_rates(code: str) -> float:
#     """возвращает курс валюты `code` по отношению к рублю"""
#     # ваша реализация здесь
#     result_value = 1.11  ## здесь должно оказаться результирующее значение float
#     return result_value
#
#
# print(currency_rates("USD"))
# print(currency_rates("noname"))

import requests

def currency_rates(code: str) -> float:
    """возвращает курс валюты `code` по отношению к рублю"""
    r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    if r.status_code == 200:
        str = r.text.lower()
        idx = str.find('<charcode>' + code.lower() + '</charcode>') # индекс потомка нужной валюты
        if idx == -1:
            return None

        idx_end_valute = idx + str[idx:].find('</valute>') # индекс конца родителя
        idx_start_valute = str[:idx].rfind('<valute id') # индекс начала родителя
        str_valute = str[idx_start_valute:idx_end_valute] # всё содержимое родителя
        str_value = str_valute[str_valute.find('<value>')+len('<value>'):str_valute.find('</value>')] # значение внутри <value>

        return float(str_value.replace(',', '.'))


print(currency_rates("USD"))
print(currency_rates("noname"))
