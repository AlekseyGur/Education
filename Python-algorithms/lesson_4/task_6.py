# 6. В одномерном массиве найти сумму элементов, находящихся между минимальным и максимальным элементами. Сами минимальный и максимальный элементы в сумму не включать.


from random import randint

a = [randint(-100, 100) for _ in range(10)]

min_el = min(a)
max_el = max(a)

sum = sum(i for i in a if min_el < i and i < max_el)

print(f'Сумма элементов {sum}')
