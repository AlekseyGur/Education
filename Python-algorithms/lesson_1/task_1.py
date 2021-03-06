# 1. Выполнить логические побитовые операции «И», «ИЛИ» и др. над числами 5 и 6. Выполнить над числом 5 побитовый сдвиг вправо и влево на два знака.
# 
# Попытайтесь решить задания без использования циклов и собственных функций (они будут рассматриваться на уроке 2), а также без массивов (они будут рассматриваться на уроке 3).
#
# Для простоты понимания зарезервированные слова forи while считаются циклом, def - функцией, любые квадратные скобки [ и ] - массивами. Их наличие в коде расценивается как неверное решение.
#
# Договариваемся об идеальном пользователе, который вводит только верные данные, которые требует программа. Проверка ввода не обязательна. Уделите это время в первую очередь построению графического алгоритма, а затем написанию кода по этому алгоритму. Не наоборот.

a = 5
b = 6

# конвертация в двоичную систему
a = '{0:03b}'.format(a)
b = '{0:03b}'.format(b)

# побитовый сдвиг влево на 2
a = a + '00'

# побитовый сдвиг вправо на 2
a = int(a) // 100
a = '{0:03b}'.format(a)

# операция логическое "И"
ans1 = ''
ans2 = ''
ans3 = ''
if a[-1] == b[-1] == 0:
    ans1 = '1'
else:
    ans1 = '0'

if a[-2] == b[-2] == 0:
    ans2 = '1'
else:
    ans2 = '0'

if a[-3] == b[-3] == 0:
    ans3 = '1'
else:
    ans3 = '0'

ans = ans3 + ans2 + ans2

# операция логическое "ИЛИ"
ans1 = ''
ans2 = ''
ans3 = ''
if a[-1] == b[-1] == 1:
    ans1 = '1'
else:
    ans1 = '0'

if a[-2] == b[-2] == 1:
    ans2 = '1'
else:
    ans2 = '0'

if a[-3] == b[-3] == 1:
    ans3 = '1'
else:
    ans3 = '0'

ans = ans3 + ans2 + ans2

# конвертация в десятичную систему
a = int(a, 2)
b = int(b, 2)
