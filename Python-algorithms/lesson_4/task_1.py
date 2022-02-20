# 1. Проанализировать скорость и сложность одного любого алгоритма из разработанных в рамках домашнего задания первых трех уроков.
# Примечание. Идеальным решением будет:
# a. выбрать хорошую задачу, которую имеет смысл оценивать,
# b. написать 3 варианта кода (один у вас уже есть),
# c. проанализировать 3 варианта и выбрать оптимальный,
# d. результаты анализа вставить в виде комментариев в файл с кодом (не забудьте указать, для каких N вы проводили замеры),
# e. написать общий вывод: какой из трёх вариантов лучше и почему.


import timeit
import cProfile

# Задача: Определить, какое число в массиве встречается чаще всего.

def func_v1(m:int = 100, n:int = 1000):
    from random import randint
    from collections import Counter

    a = [randint(0, m) for _ in range(n)]

    res = Counter(a).most_common()[0]

    print(f'Значение {res[0]} повторяется {res[1]} раза, что чаще всего')

def func_v2(m:int = 100, n:int = 1000):
    from random import randint
    b = {}
    a = [randint(0, m) for _ in range(n)]
    for i in a:
        b.update({i: b.get(i, 0) + 1})

    max_val = max([i for _, i in b.items()])
    res = [(idx, val) for idx, val in b.items() if val == max_val][0]

    print(f'Значение {res[0]} повторяется {res[1]} раза, что чаще всего')

# cProfile.run('func_v1(10, 100)')
# 1245 function calls (1210 primitive calls) in 0.002 seconds

# cProfile.run('func_v1(100, 1000)')
# 5954 function calls (5919 primitive calls) in 0.003 seconds

# cProfile.run('func_v1(1000, 10000)')
# 50899 function calls (50864 primitive calls) in 0.016 seconds

# cProfile.run('func_v1(10000, 100000)')
# 564441 function calls (564406 primitive calls) in 0.151 seconds



# cProfile.run('func_v2(10, 100)')
# 1418 function calls (1391 primitive calls) in 0.002 seconds

# cProfile.run('func_v2(100, 1000)')
# 7962 function calls (7935 primitive calls) in 0.003 seconds

# cProfile.run('func_v2(1000, 10000)')
# 70913 function calls (70886 primitive calls) in 0.022 seconds

# cProfile.run('func_v2(10000, 100000)')
# 764331 function calls (764304 primitive calls) in 0.199 seconds
