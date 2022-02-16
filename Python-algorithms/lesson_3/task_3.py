# 3. В массиве случайных целых чисел поменять местами минимальный и максимальный элементы.

from random import randint

a = [randint(0, 10) for _ in range(10)]

min_index = a.index(min(a))
max_index = a.index(max(a))

a[min_index], a[max_index] = a[max_index], a[min_index]
