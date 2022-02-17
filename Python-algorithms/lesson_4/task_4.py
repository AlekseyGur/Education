# 4. Определить, какое число в массиве встречается чаще всего.


from random import randint
from collections import Counter

a = [randint(0, 10) for _ in range(100)]

res = Counter(a).most_common()[0]

print(f'Значение {res[0]} повторяется {res[1]} раза, что чаще всего')
