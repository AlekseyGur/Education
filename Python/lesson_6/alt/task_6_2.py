# Задание 2 *(вместо 1)
#
# Найти IP адрес спамера и количество отправленных им запросов по данным файла логов из предыдущего задания.
#
#     Примечание: спамер — это клиент, отправивший больше всех запросов; код должен работать даже с файлами, размер которых превышает объем ОЗУ компьютера.
#
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
    """Парсит строку на атрибуты и возвращает кортеж атрибутов (<remote_addr>,
     <request_type>, <requested_resource>)"""
    lineAr = line.split()
    return  lineAr[0], lineAr[5].lstrip('"'), lineAr[6]

list_out = list()
with open('nginx_logs.txt', 'r', encoding='utf-8') as fr:
    for line in fr:
        list_out.append(get_parse_attrs(line))



def get_spammer(list_in: list, num_request: list = 1000) -> list:
    """Возвращает список кортежей "ip, кол-во обращений" из наиболее активных ip
    адресов, у которых количество обращений больше, чем num_request"""
    tmp = {}
    return sorted({
        i: tmp.get(i)
        for i in list(zip(*list_in))[0]
        if not tmp.update({i: tmp.get(i, 0) + 1}) and tmp.get(i) > num_request
    }.items(), key = lambda x: x[1])


pprint(get_spammer(list_out))
