# Задание 1
#
# Не используя библиотеки для парсинга, распарсить (получить определённые данные) файл логов web-сервера nginx_logs.txt — получить список кортежей вида: (<remote_addr>, <request_type>, <requested_resource>) . Например:
#
# [
#     ...
#     ('141.138.90.60', 'GET', '/downloads/product_2'),
#     ('141.138.90.60', 'GET', '/downloads/product_2'),
#     ('173.255.199.22', 'GET', '/downloads/product_2'),
#     ...
# ]
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# from pprint import pprint
#
#
# def get_parse_attrs(line: str) -> tuple:
#     """Парсит строку на атрибуты и возвращает кортеж атрибутов (<remote_addr>, <request_type>, <requested_resource>)"""
#     pass  # Ваша реализация здесь
#     return  # верните кортеж значений <remote_addr>, <request_type>, <requested_resource>
#
#
# list_out = list()
# with open('nginx_logs.txt', 'r', encoding='utf-8') as fr:
#     pass  # передавайте данные в функцию и наполняйте список list_out кортежами
#
# pprint(list_out)


from pprint import pprint


def get_parse_attrs(line: str) -> tuple:
    """Парсит строку на атрибуты и возвращает кортеж атрибутов (<remote_addr>, <request_type>, <requested_resource>)"""
    lineAr = line.split()
    return  lineAr[0], lineAr[5].lstrip('"'), lineAr[6]


list_out = list()
with open('nginx_logs.txt', 'r', encoding='utf-8') as fr:
    for line in fr:
        list_out.append(get_parse_attrs(line))

pprint(list_out)
