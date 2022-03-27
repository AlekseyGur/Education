# 1. Определение количества различных подстрок с использованием хеш-функции. Пусть на вход функции дана строка. Требуется вернуть количество различных подстрок в этой строке.
# Примечания:
# * в сумму не включаем пустую строку и строку целиком;
# * без использования функций для вычисления хэша (hash(), sha1() или любой другой из модуля hashlib задача считается не решённой.


import hashlib


def search_all_substr(s: str) -> dict:
    result = {}
    str_to_calc = []  # какие подстроки искать
    str_to_calc.extend(s.split()) # все целые слова

    for len_sub in range(1, len(s)):
        for i in range(len(s) - len_sub + 1):
            if s[i:i+len_sub] != ' ':
                str_to_calc.append(s[i:i+len_sub])

    str_to_calc = set(str_to_calc)  # убираем дубликаты

    for i in set(str_to_calc):
        result.update({i: result.get(i, 0) + rabin_karp(s, i)})

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    for string, count in result:
        print(f'подстрока "{string}" встречается {count} раз')


def rabin_karp(s: str, subs: str) -> int:
    assert len(s) > 0 and len(subs) > 0, 'Строки не могут быть пустыми'
    assert len(s) >= len(subs), 'Подстрока длинее строки'

    len_sub = len(subs)
    h_subs = hashlib.sha1(subs.encode('utf-8')).hexdigest()

    count = 0
    for i in range(len(s) - len_sub + 1):
        if h_subs == hashlib.sha1(s[i:i+len_sub].encode('utf-8')).hexdigest():
            if s[i:i + len_sub] == subs:
                count += 1
    return count


search_all_substr('hello world')
