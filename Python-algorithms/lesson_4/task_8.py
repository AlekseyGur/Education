# 8. Матрица 5x4. Программа должна вычислять сумму элементов каждой строки и записывать ее в последнюю ячейку строки. В конце следует вывести полученную матрицу.


from random import randint

matrix = [[randint(0, 10) for _ in range(5)] for _ in range(4)]

# вычисление
for idx, row in enumerate(matrix):
    matrix[idx].append(sum(row))


# вывод
for row in matrix:
    for i in row:
        print(f'{i:>4}', end ='')
    print()
