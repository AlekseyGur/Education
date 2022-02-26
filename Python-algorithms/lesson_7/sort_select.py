# Сортировка выбором
# Сложность: O(n**2)
# Стабильность: да / нет (у двух одинаковых элементов не будет изменён порядок)
# Потребление дополнительной памяти: нет

lst = [3, 1, 2]


def selection_sort(ar):
    for i in range(len(ar)):
        idx_min = i
        for j in range(i + 1, len(ar)):
            if ar[j] < ar[idx_min]:
                idx_min = j

        ar[idx_min], ar[i] = ar[i], ar[idx_min]


selection_sort(lst)
print(lst)
