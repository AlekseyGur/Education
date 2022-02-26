# 2. Написать программу сложения и умножения двух шестнадцатеричных чисел. При этом каждое число представляется как массив, элементы которого — цифры числа.
# Например, пользователь ввёл A2 и C4F. Нужно сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно. Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].
# Примечание: Если воспользоваться функциями hex() и/или int() для преобразования систем счисления, задача решается в несколько строк. Для прокачки алгоритмического мышления такой вариант не подходит. Поэтому использование встроенных функций для перевода из одной системы счисления в другую в данной задаче под запретом.
# Вспомните начальную школу и попробуйте написать сложение и умножение в столбик.


from collections import defaultdict

a = 'A2'
b = 'C4F'


def hex_to_int(a: list = []) -> int:
    int_num = [*range(16)]
    hex_num = [*(str(i) for i in range(10)), 'A', 'B', 'C', 'D', 'E', 'F']
    d = defaultdict(int, zip(hex_num, int_num))
    sum = 0
    for i, v in enumerate(reversed(list(a)), 0):
        sum += d[v] * 16**i

    return sum


def int_to_hex(a: int = 0) -> list:
    int_num = [*range(16)]
    hex_num = [*(str(i) for i in range(10)), 'A', 'B', 'C', 'D', 'E', 'F']
    d = defaultdict(int, zip(int_num, hex_num))

    s = ''
    while a > 0:
        s = f'{d[a % 16]}{s}'
        a //= 16

    return list(s)


def sum_hex(a: str, b: str) -> str:
    return int_to_hex(hex_to_int(a) + hex_to_int(b))


def mult_hex(a: str, b: str) -> str:
    return int_to_hex(hex_to_int(a) * hex_to_int(b))


print(sum_hex(a, b))
print(mult_hex(a, b))
