# 1. Создать программный файл в текстовом формате, записать в него построчно данные,
# вводимые пользователем. Об окончании ввода данных будет свидетельствовать пустая строка.

import sys
for line in sys.stdin:
    if not line.rstrip('\n'): break
    with open('text', 'a') as file:
        file.write(input)


# 2. Создать текстовый файл (не программно), сохранить в нём несколько строк,
# выполнить подсчёт строк и слов в каждой строке.

with open('text', 'r') as file:
    for n, line in enumerate(file, 1):
        num_words = len(list(filter(None, line.split(' '))))
        print(f'Количество слов в {n} строке: {num_words}')


# 3. Создать текстовый файл (не программно). Построчно записать фамилии сотрудников
# и величину их окладов (не менее 10 строк). Определить, кто из сотрудников имеет
# оклад менее 20 тысяч, вывести фамилии этих сотрудников. Выполнить подсчёт средней
# величины дохода сотрудников. Пример файла:
# Иванов 23543.12
# Петров 13749.32

with open('text', 'r') as file:
    salaries = {}
    for line in file:
        name, salary = line.split(' ')
        salaries[name] = float(salary)

    mean = round(sum([sal for name, sal in salaries.items()]) / len(salaries))
    names = ', '.join([name for name, sal in salaries.items() if sal < 20000])

    print(f'Средняя величина дохода сотрудников: {mean}')
    print(f'Сотрудники с зарплатой менее 20 000: {names}')


# 4. Создать (не программно) текстовый файл со следующим содержимым:
#
# One — 1
# Two — 2
# Three — 3
# Four — 4
#
# Напишите программу, открывающую файл на чтение и считывающую построчно данные.
# При этом английские числительные должны заменяться на русские. Новый блок строк
# должен записываться в новый текстовый файл.

with open('text_in', 'r') as file_r, open('text_out', 'w') as file_w:
    for n, line in enumerate(file_r, 1):
        line = line.rstrip('\n')
        num, _, salary = line.split(' ')
        if num == 'One': num = 'Один'
        if num == 'Two': num = 'Два'
        if num == 'Three': num = 'Три'
        if num == 'Four': num = 'Четыре'
        print(num, _, salary, file=file_w)


# 5. Создать (программно) текстовый файл, записать в него программно набор чисел,
# разделённых пробелами. Программа должна подсчитывать сумму чисел в файле и выводить
# её на экран.

import json

a = [1, 2, 3, 4, 5]

with open('text', 'w') as file:
    w = ' '.join(str(i) for i in a)
    json.dump(w, file)

with open('text', 'r') as file:
    r = json.load(file)
    r = sum([int(i) for i in r.split()])
    print(f'Сумма чисел в файле: {r}')


# 6. Сформировать (не программно) текстовый файл. В нём каждая строка должна описывать
# учебный предмет и наличие лекционных, практических и лабораторных занятий по предмету.
# Сюда должно входить и количество занятий. Необязательно, чтобы для каждого предмета
# были все типы занятий.
# Сформировать словарь, содержащий название предмета и общее количество занятий по нему.
# Вывести его на экран.
#
# Примеры строк файла:
# Информатика: 100(л) 50(пр) 20(лаб).
# Физика: 30(л) — 10(лаб)
# Физкультура: — 30(пр) —
# Пример словаря: {“Информатика”: 170, “Физика”: 40, “Физкультура”: 30}

with open('text', 'r') as file:
    subj = {}
    for line in file:
        line = line.rstrip('\n')
        name, lections, practice, labs = line.split(' ')

        lections = int(lections.split('(')[0]) if lections != '—' else 0
        practice = int(practice.split('(')[0]) if practice != '—' else 0
        labs = int(labs.split('(')[0]) if labs != '—' else 0

        subj[name.split(':')[0]] = lections + practice + labs

    print(f'Пример словаря: {subj}')


# 7. Создать вручную и заполнить несколькими строками текстовый файл, в котором
# каждая строка будет содержать данные о фирме: название, форма собственности,
# выручка, издержки.
#
# Пример строки файла: firm_1 ООО 10000 5000.
# Необходимо построчно прочитать файл, вычислить прибыль каждой компании, а также
# среднюю прибыль. Если фирма получила убытки, в расчёт средней прибыли её не включать.
# Далее реализовать список. Он должен содержать словарь с фирмами и их прибылями,
# а также словарь со средней прибылью. Если фирма получила убытки, также добавить
# её в словарь (со значением убытков).
#
# Пример списка: [{“firm_1”: 5000, “firm_2”: 3000, “firm_3”: 1000}, {“average_profit”: 2000}].
# Итоговый список сохранить в виде json-объекта в соответствующий файл.
#
# Пример json-объекта:
# [{"firm_1": 5000, "firm_2": 3000, "firm_3": 1000}, {"average_profit": 2000}]
# Подсказка: использовать менеджер контекста.

import json

with open('text', 'w') as file:
    file.write('firm_1 ООО 10000 5000\n')
    file.write('firm_2 ЗАО 20000 6000\n')
    file.write('firm_3 ОАО 30000 7000\n')

with open('text', 'r') as file_r, open('text_out', 'w') as file_w:
    firm = []
    for line in file_r:
        line = line.rstrip('\n')
        name, form, revenue, costs = line.split(' ')
        firm.append({'name': name, # название
                     'form': form, # форма собственности
                     'revenue': float(revenue), # выручка
                     'costs': float(costs), # издержки
                     'net_revenue': float(revenue) - float(costs) # чистая прибыль
                    })

    # прибыль каждой компании
    print('Прибыль каждой компании:')
    for f in firm:
        print(f'{f["form"]} {f["name"]}: {f["net_revenue"]}')

    # средняя прибыль всех
    mean_rev = sum([f['net_revenue'] for f in firm if 0 < f['net_revenue']]) \
                / len([True for f in firm if 0 < f['net_revenue']])
    print(f'Средняя прибыль всех: {mean_rev}')

    # список в файл
    list=[
        {f['name']: f['net_revenue'] for f in firm},
        {'average_profit': mean_rev}
    ]
    print(f'Список: {list}')
    json.dump(list, file_w)
