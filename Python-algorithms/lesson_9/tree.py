
# 1. Определение количества различных подстрок с использованием хеш-функции. Пусть на вход функции дана строка. Требуется вернуть количество различных подстрок в этой строке.
# Примечания:
# * в сумму не включаем пустую строку и строку целиком;
# * без использования функций для вычисления хэша (hash(), sha1() или любой другой из модуля hashlib задача считается не решённой.



from binarytree import tree, bst, Node, build


class MyNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


a = tree(height=4, is_perfect=False)  # произвольное дерево
print(a)

b = bst(height=4, is_perfect=True)  # бинарное дерево поиска
print(b)

c = Node(7)  # создание дерева вручную
c.left = Node(3)
c.right = Node(11)
c.left.left = Node(1)
c.left.right = Node(5)
c.right.left = Node(9)
c.right.right = Node(13)
print(c)

d = build([7, 3, 11, 1, 5, 9, 13, None, 2, None, 6])  # дерево на основе списка
print(d)
