# 1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за четыре квартала для каждого предприятия. Программа должна определить среднюю прибыль (за год для всех предприятий) и отдельно вывести наименования предприятий, чья прибыль выше среднего и ниже среднего.


from collections import defaultdict
from statistics import mean

dict = defaultdict(list)

count = input('Введите количество предприятий: ')
for i in range(int(count)):
    name = input('Введите название предприятия: ')
    income = input('Введите прибыль за четыре квартала: ')
    dict[name] = float(income)

avg = mean(i for i in dict.values())
avg_good = [name for name, income in dict.items() if avg <= income]
avg_bad = [name for name, income in dict.items() if income < avg]

if avg_good:
    print(f'Прибыль выше среднего у предприятий: {", ".join(avg_good)}')

if avg_bad:
    print(f'Прибыль ниже среднего у предприятий: {", ".join(avg_bad)}')
