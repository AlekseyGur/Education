# Сортировка Хоара
# Сложность: от O(n**2) до O(n*log(n))
# Стабильность: нет (у двух одинаковых элементов  будет изменён порядок)
# Потребление дополнительной памяти: нет

import random
ar = [3, 1, 2]


def hoar_sort(ar, fst, lst):
    print(ar)

    if fst >= lst:
        return

    pivot = ar[random.randint(fst, lst)]
    i, j = fst, lst

    while i <= j:
        while ar[i] < pivot:
            i += 1

        while ar[j] > pivot:
            j -= 1

        if i <= j:
            ar[i], ar[j] = ar[j], ar[i]
            i, j = i + 1, j - 1

    hoar_sort(ar, fst, j)
    hoar_sort(ar, i, lst)



hoar_sort(ar, 0, len(ar) - 1)
print(ar)
