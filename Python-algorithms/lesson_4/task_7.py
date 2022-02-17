# 7. В одномерном массиве целых чисел определить два наименьших элемента. Они могут быть как равны между собой (оба минимальны), так и различаться.


from random import randint
from collections import Counter

a = [randint(-5, 5) for _ in range(10)]

print(f'Два наименьших элемента: {sorted(a)[:2]}')
