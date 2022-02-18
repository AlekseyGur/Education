# Задание 5 *(вместо 4)
#
# Написать скрипт, который выводит статистику для заданной папки в виде словаря, в котором ключи те же, а значения — кортежи вида (<files_quantity>, [<files_extensions_list>]), например:
#
# {
#   100: (15, ['txt']),
#   1000: (3, ['py', 'txt']),
#   10000: (7, ['html', 'css']),
#   100000: (2, ['png', 'jpg'])
# }
#
# Сохраните результаты в файл <folder_name>_summary.json в той же папке, где запустили скрипт.


from os import walk
from os.path import join as path_join, getsize, isdir

key = [] # размеры и расширения каждого файла
for root, dirs, files in walk('.'):
    if not files:
        continue
    key.extend([
        [getsize(path_join(root, name)),
        name.split('.')[-1] if name.count('.') else '']
        for name in files
    ])

sizes, _ = list(zip(*key))

len_max = len(list(str(max(sizes)))) # длина строки максимального значения
bins = [10 ** i for i in range(2, len_max + 1)] # бины размеров

result = {} # словарь результатов подсчёта
for size, ext in key:
    for j in bins:
        if size < j:
            len_saved, ext_saved = result.get(j, (0, []))
            len_saved += 1
            if ext not in ext_saved:
                ext_saved.append(ext)
            result.update({j: (len_saved, ext_saved)})
            break

result = dict(sorted(result.items(), key=lambda x: x))

# вывод распределение по размерам
for max_size, info in result.items():
    print(f'Файлов с размером не более {max_size}: {info[0]} шт. в форматах {info[1]}')
