# Задание 4
#
# Написать скрипт, который выводит статистику для заданной папки в виде словаря, в котором ключи — верхняя граница размера файла (пусть будет кратна 10), а значения — общее количество файлов (в том числе и в подпапках), размер которых не превышает этой границы, но больше предыдущей (начинаем с 0), например:
#
# {
#   100: 15,
#   1000: 3,
#   10000: 7,
#   100000: 2
# }
#
# Тут 15 файлов размером не более 100 байт; 3 файла больше 100 и не больше 1000 байт...


from os import walk
from os.path import join as path_join, getsize

key = [] # размеры каждого файла
for root, dirs, files in walk('.'):
    if not files:
        continue
    key.extend((getsize(path_join(root, name)) for name in files))

len_max = len(list(str(max(key)))) # длина строки максимального значения
bins = [10 ** i for i in range(2, len_max + 1)] # бины размеров

result = {} # словарь результатов подсчёта
for i in key:
    for j in bins:
        if i < j:
            result.update({j: result.get(j, 0) + 1})
            break

result = dict(sorted(result.items(), key=lambda x: x))

# вывод распределение по размерам
for max_size, count in result.items():
    print(f'Файлов с размером не более {max_size}: {count} шт.')
