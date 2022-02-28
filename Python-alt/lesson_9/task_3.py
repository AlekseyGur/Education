# ## Задание 3
# Реализовать базовый класс `Worker` (работник):
# * определить атрибуты: `name`, `surname`, `position` (должность), `income` (доход);
# * последний атрибут должен быть защищённым и ссылаться на словарь, содержащий элементы «оклад» и «премия»,
#   например, `{"wage": wage, "bonus": bonus}`;
# * создать класс `Position` (должность) на базе класса `Worker`;
# * в классе `Position` реализовать методы получения полного имени сотрудника (`get_full_name`) и дохода с
#   учётом премии (`get_total_income`);
# * проверить работу примера на реальных данных: создать экземпляры класса `Position`, передать данные,
#   проверить значения атрибутов, вызвать методы экземпляров.
#
# **ВНИМАНИЕ!** Используйте стартовый код для своей реализации:
#
# ```(python)
# class Worker:
#
#     def __init__(self, name: str, surname: str, position: str, income: dict):
#         ...  # Ваш код здесь
#
#
# class Position(Worker):
#
#     def get_full_name(self) -> str:
#         """Возвращает строку по формату 'Имя Фамилия'"""
#         ...  # Ваш код здесь
#
#     def get_total_income(self) -> int:
#         """Возвращает суммарный ежемесячных доход"""
#         ...  # Ваш код здесь
#
#
# if __name__ == '__main__':
#     welder = Position('иван', 'васильев', 'сварщик', {'wage': 50000, 'bonus': 15000})
#     driver = Position('петр', 'николаев', 'водитель', {'wage': 30000, 'bonus': 7500})
#     scientist = Position('геннадий', 'разумов', 'ученый', {'wage': 150000, 'bonus': 25000})
#     print(welder.get_full_name(), welder.get_total_income())  # Иван Васильев 65000
#     print(driver.get_full_name(), driver.get_total_income())  # Петр Николаев 37500
#     print(scientist.get_full_name(), scientist.get_total_income())  # Геннадий Разумов 175000
# ```


class Worker:
    def __init__(self, name: str, surname: str, position: str, income: dict):
        """конструктор класса
        :param name: имя
        :param surname: фамилия
        :param position: должность
        :param income: зарплата и бонусы: {"wage": 10, "bonus": 5}
        """
        self.name = name
        self.surname = surname
        self.position = position
        self.income = income


class Position(Worker):
    def get_full_name(self):
        """Возвращает строку по формату 'Имя Фамилия'"""
        return self.name.capitalize() + ' ' + self.surname.capitalize()

    def get_total_income(self):
        """Возвращает суммарный ежемесячных доход"""
        return self.income["wage"] + self.income["bonus"]


if __name__ == '__main__':
    welder = Position('иван', 'васильев', 'сварщик', {'wage': 50000, 'bonus': 15000})
    driver = Position('петр', 'николаев', 'водитель', {'wage': 30000, 'bonus': 7500})
    scientist = Position('геннадий', 'разумов', 'ученый', {'wage': 150000, 'bonus': 25000})
    print(welder.get_full_name(), welder.get_total_income())  # Иван Васильев 65000
    print(driver.get_full_name(), driver.get_total_income())  # Петр Николаев 37500
    print(scientist.get_full_name(), scientist.get_total_income())  # Геннадий Разумов 175000



###### Реализация через namedtuple ######
from collections import namedtuple

Position = namedtuple('Position', 'name, surname, job, salary')

workers = []
workers.append(Position('иван', 'васильев', 'сварщик', {'wage': 50000, 'bonus': 15000}))
workers.append(Position('петр', 'николаев', 'водитель', {'wage': 30000, 'bonus': 7500}))
workers.append(Position('геннадий', 'разумов', 'ученый', {'wage': 150000, 'bonus': 25000}))

for w in workers:
    print(f'{w.name.capitalize()} {w.surname.capitalize()} {w.salary["wage"] + w.salary["bonus"]}')
