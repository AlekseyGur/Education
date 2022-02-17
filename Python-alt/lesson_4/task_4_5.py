# Задание 5
#
# *(вместо 4) Рядом со скриптом task_4_4.py, создать скрипт task_4_5.py с содержимым аналогичным task_4_4.py, но переработанным так, чтобы новый скрипт теперь срабатывал, как CLI, прямо в консоли/терминале.
#
# Например:
#
# >>> python task_4_5.py USD
# 75.18, 2020-09-05
#
#     Задачи со * предназначены для продвинутых учеников, которым мало сделать обычное задание.

from sys import argv
from utils import currency_rates

currency = argv[1]

if currency:
    print(currency_rates(currency))
