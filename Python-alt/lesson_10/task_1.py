# Задание 1
#
# Реализовать класс Matrix (матрица).
#
#     Обеспечить перегрузку конструктора класса (метод __init__()), который должен принимать данные (список списков) для формирования матрицы. В случае если список списков некорректный - возбуждать исключение ValueError с сообщением fail initialization matrix.
#
#     Подсказка: матрица — система некоторых математических величин, расположенных в виде прямоугольной схемы.
#
# Примеры матриц: 3 на 2, 3 на 3, 2 на 4.
#
# | 31 43 |
# | 22 51 |
# | 37 86 |
#
# | 3 5 32 |
# | 2 4 6 |
# | -1 64 -8 |
#
# | 3 5 8 3 |
# | 8 3 7 1 |
#
#     Следующий шаг — реализовать перегрузку метода __str__() для вывода матрицы в привычном виде (как показано выше).
#     Далее реализовать перегрузку метода __add__() для сложения двух объектов класса Matrix (двух матриц). Результатом сложения должна быть новая матрица.
#
#     Подсказка: сложение элементов матриц выполнять поэлементно. Первый элемент первой строки первой матрицы складываем с первым элементом первой строки второй матрицы и пр.
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# from typing import List
#
#
# class Matrix:
#     def __init__(self, matrix: List[List[int]]):
#         ...
#
#
# if __name__ == '__main__':
#     first_matrix = Matrix([[1, 2], [3, 4], [5, 6]])
#     second_matrix = Matrix([[6, 5], [4, 3], [2, 1]])
#     print(first_matrix)
#     """
#     | 1 2 |
#     | 3 4 |
#     | 5 6 |
#     """
#     print(first_matrix + second_matrix)
#     """
#     | 7 7 |
#     | 7 7 |
#     | 7 7 |
#     """
#     fail_matrix = Matrix([[1, 2], [3, 4, 7], [5, 6]])
#     """
#     Traceback (most recent call last):
#       ...
#     ValueError: fail initialization matrix
#     """


from typing import List


class Matrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix

        check_len = [len(row) for row in matrix]
        if max(check_len) != min(check_len):
            raise ValueError('fail initialization matrix')

    def __str__(self):
        a = ''
        for row in self.matrix:
            a += '|'
            for el in row:
                a += ' ' + str(el)
            a += ' |\n'
        return a

    def __add__(self, other):
        if isinstance(other, Matrix):
            a = self.matrix.copy()
            for i, row in enumerate(self.matrix):
                for j, val in enumerate(row):
                    a[i][j] = val + other.matrix[i][j]

            return Matrix(a)


if __name__ == '__main__':
    first_matrix = Matrix([[1, 2], [3, 4], [5, 6]])
    second_matrix = Matrix([[6, 5], [4, 3], [2, 1]])
    print(first_matrix)
    """
    | 1 2 |
    | 3 4 |
    | 5 6 |
    """
    print(first_matrix + second_matrix)
    """
    | 7 7 |
    | 7 7 |
    | 7 7 |
    """
    fail_matrix = Matrix([[1, 2], [3, 4, 7], [5, 6]])
    """
    Traceback (most recent call last):
      ...
    ValueError: fail initialization matrix
    """
