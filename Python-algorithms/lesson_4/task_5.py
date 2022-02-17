# 5. В массиве найти максимальный отрицательный элемент. Вывести на экран его значение и позицию в массиве.


from random import randint
from collections import Counter

a = [randint(-100, 100) for _ in range(10)]

print(f'Минимальный отрицательный {max(i for i in a if i < 0)}')
print(f'Максимальный отрицательный {min(i for i in a if i < 0)}')
