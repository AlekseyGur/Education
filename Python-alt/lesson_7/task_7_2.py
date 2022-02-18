# Задание 2 *(вместо 1)
#
# Написать скрипт, создающий из config.yaml стартер для проекта со следующей структурой:
#
# |--my_project
#    |--settings
#    |  |--__init__.py
#    |  |--dev.py
#    |  |--prod.py
#    |--mainapp
#    |  |--__init__.py
#    |  |--models.py
#    |  |--views.py
#    |  |--templates
#    |     |--mainapp
#    |        |--base.html
#    |        |--index.html
#    |--authapp
#    |  |--__init__.py
#    |  |--models.py
#    |  |--views.py
#    |  |--templates
#    |     |--authapp
#    |        |--base.html
#    |        |--index.html
#
#     Примечание: структуру файла config.yaml придумайте сами, его можно создать в любом текстовом редакторе «руками» (не программно); предусмотреть возможные исключительные ситуации, библиотеки использовать нельзя.

from os import mkdir, sep
from os.path import exists, join as path_join

paths = [] # список путей всех файлов и папок

# читаем config.yaml и заполняем список paths путями к файлам и папкам
with open('config.yaml') as file:
    gap_last = 0 # уровень - это кол-во пробелов в начале строки
    path_last = '' # адрес предыдущей папки
    for line in file:
        line = line.rstrip('\n ')
        path = ''
        gap = len(line) - len(line.lstrip())

        if not gap: # верхний уровень
            path_last = ''
            path = line
        else:
            if path_last and gap < gap_last: # выходим на уровень выше
                a = gap_last - gap
                path_last = path_join(*path_last.split(sep)[:(-1)*a])

            path = path_join(path_last, line[gap:]) # собираем полный путь
            gap_last = gap

        paths.append(path)

        if not line.count('.'): # это была папка
            path_last = path


# создаём все файлы и папки по полученным путям
for path in paths:
    if path.count('.'): # файл
        if not exists(path):
            open(path, 'a').close()
            print('Файл создан: ', path)

    else: # папка
        if not exists(path):
            mkdir(path)
            print('Папка создана: ', path)
