# Задание 1
#
# Написать тело функцию email_parse(email: str), которая при помощи регулярного выражения извлекает имя пользователя и почтовый домен из email адреса и возвращает их в виде словаря. Если адрес не валиден, выбросить исключение ValueError. Пример:
#
# $ email_parse('someone@geekbrains.ru')
# {'username': 'someone', 'domain': 'geekbrains.ru'}
# $ email_parse('someone@geekbrainsru')
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   ...
#     raise ValueError(msg)
# ValueError: wrong email: someone@geekbrainsru
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# import re
#
#
# def email_parse(email: str) -> dict:
#     """
#     Парсит переданную email-строку на атрибуты и возвращает словарь
#     :param email: строковое входное значение обрабатываемого email
#     :return: {'username': <значение до символа @>, 'domain': <значение за символом @>} | ValueError
#     """
#     RE_MAIL = re.compile(r'ваше регулярное выражение')
#     pass  # пишите реализацию здесь
#
#
# if __name__ == '__main__':
#     email_parse('someone@geekbrains.ru')
#     email_parse('someone@geekbrainsru')


import re


def email_parse(email: str) -> dict:
    """
    Парсит переданную email-строку на атрибуты и возвращает словарь
    :param email: строковое входное значение обрабатываемого email
    :return: {'username': <значение до символа @>, 'domain': <значение за символом @>} | ValueError
    """
    RE_MAIL = re.compile(r'^(\w+)@(\w+\.\w+)$')
    mail_parts = RE_MAIL.findall(email)
    try:
        return {'username': mail_parts[0][0], 'domain': mail_parts[0][1]}
    except:
        pass  # не ставим сюда rise, чтобы не появлялось "During handling of the above exception, another exception occurred"

    raise ValueError('wrong email')


if __name__ == '__main__':
    email_parse('someone@geekbrains.ru')
    email_parse('someone@geekbrainsru')
