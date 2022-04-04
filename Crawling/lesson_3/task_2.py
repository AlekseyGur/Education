# Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введённой суммы (необходимо анализировать оба поля
# зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для
# поиска продуктов с рейтингом не ниже введенного или качеством не ниже
# введенного (то есть цифра вводится одна, а запрос проверяет оба поля)

import pandas as pd
from task_1_tools import *
from task_1_db import *


min_salary = int(input('Минимальная зарплата: '))

db = DB()
data = pd.DataFrame(list(db.get_list(min_salary=min_salary)))
print(pd.DataFrame(data))
