# Сортировка Шелла
# Сложность: от O(n**2) / O(n*(log(n))**2) до O(n**3/2)
# Стабильность: нет (у двух одинаковых элементов  будет изменён порядок)
# Потребление дополнительной памяти: нет

lst = [3, 1, 2]


def shell_sort(ar):

    assert len(ar) < 4000, 'Массив слишком большой. Используйте другую сортировку' # для такого размера выбраны значения шага:


    def new_inc(ar):
        inc = [1, 4, 10, 23, 57, 132, 301, 701, 1750]

        while len(ar) <= inc[-1]:
            inc.pop()

        while len(inc) > 0:
            yield inc.pop()


    for inc in new_inc(ar):
        for i in range(inc, len(ar)):
            for j in range(i, inc-1, -inc):
                if ar[j-inc] <= ar[j]:
                    break
                ar[j], ar[j-inc] = ar[j-inc], ar[j]


shell_sort(lst)
print(lst)
