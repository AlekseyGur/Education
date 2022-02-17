# Задание 3
#
# *(вместо 2) В task_4_3.py создать функцию currency_rates_adv() аналогичную currency_rates() прошлого задания, только теперь она должна возвращать кроме курса ещё и дату, которая передаётся в ответе сервера.
#
#     Дата должна быть в виде объекта date. Т.е. функция должна возвращать кортеж из двух элементов следующих типов float и datetime.date
#
# Подумайте, как извлечь дату из ответа, какой тип данных лучше использовать в ответе функции?
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# import datetime
#
# def currency_rates_adv(code: str):
#     # ваша реализация здесь
#     ...
#
# kurs, date_value = currency_rates_adv("USD")
#
# empty = bool(not kurs and not date_value)
# if not empty and not isinstance(kurs, float):
#     raise TypeError("Неверный тип данных у курса")
# if not empty and not isinstance(date_value, datetime.date):
#     raise TypeError("Неверный тип данных у даты")
# print(kurs, date_value)

import requests
import datetime


def currency_rates_adv(code: str):
    """возвращает курс валюты `code` по отношению к рублю"""
    r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    if r.status_code == 200:
        str = r.text.lower()

        # получение курса
        idx = str.find('<charcode>' + code.lower() + '</charcode>') # индекс потомка нужной валюты
        if idx == -1:
            return None
        idx_end_valute = idx + str[idx:].find('</valute>') # индекс конца родителя
        idx_start_valute = str[:idx].rfind('<valute id') # индекс начала родителя
        str_valute = str[idx_start_valute:idx_end_valute] # всё содержимое родителя
        str_value = str_valute[str_valute.find('<value>')+len('<value>'):str_valute.find('</value>')] # значение внутри <value>

        # получение даты
        idx_start_date = str.find('<valcurs') # индекс начала контейнера с датой
        idx_end_date = idx_start_date + str[idx_start_date:].find('>') # индекс конца контейнера с датой
        str_date_container = str[idx_start_date:idx_end_date] # кодержимое контейнера с датой
        str_date = str_date_container[str_date_container.find('date="') + len('date="'):].split('"')[0] #  дата

        return float(str_value.replace(',', '.')), datetime.datetime.strptime(str_date, '%d.%m.%Y')


kurs, date_value = currency_rates_adv("USD")

empty = bool(not kurs and not date_value)
if not empty and not isinstance(kurs, float):
    raise TypeError("Неверный тип данных у курса")
if not empty and not isinstance(date_value, datetime.date):
    raise TypeError("Неверный тип данных у даты")
print(kurs, date_value)
