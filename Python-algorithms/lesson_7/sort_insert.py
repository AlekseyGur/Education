# Сортировка вставкой
# Сложность: от O(n) до O(n**2)
# Стабильность: да (у двух одинаковых элементов не будет изменён порядок)
# Потребление дополнительной памяти: нет

lst = [3, 1, 2]


def insert_sort(ar):
    for i in range(1, len(ar)):
        val = ar[i]
        j = i

        while ar[j-1] > val and j > 0:
            ar[j] = ar[j-1]
            j -= 1

        ar[j] = val


insert_sort(lst)
print(lst)
