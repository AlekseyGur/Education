# 1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за четыре квартала для каждого предприятия. Программа должна определить среднюю прибыль (за год для всех предприятий) и отдельно вывести наименования предприятий, чья прибыль выше среднего и ниже среднего.

import sys
from collections import defaultdict
from statistics import mean


def show_size(x, level=0):
    print('\t' * level, f'type= {x.__class__}, size= {sys.getsizeof(x)}, object= {x}')

    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in x.items():
                show_size(xx, level+1)



dict = defaultdict(list)

count = input('Введите количество предприятий: ')
for i in range(int(count)):
    name = input('Введите название предприятия: ')
    income = input('Введите прибыль за четыре квартала: ')
    dict[name] = float(income)

avg = mean(i for i in dict.values())
avg_good = [name for name, income in dict.items() if avg <= income]
avg_bad = [name for name, income in dict.items() if income < avg]

show_size(avg)
# type= <class 'float'>, size= 24, object= 2.0

show_size(avg_good)
# type= <class 'list'>, size= 88, object= ['1', '2']

show_size(avg_bad)
# type= <class 'list'>, size= 56, object= []

if avg_good:
    print(f'Прибыль выше среднего у предприятий: {", ".join(avg_good)}')

if avg_bad:
    print(f'Прибыль ниже среднего у предприятий: {", ".join(avg_bad)}')
