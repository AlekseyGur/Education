# ## Задание 1
# Реализовать класс `Дата`, функция-конструктор которого должна принимать дату в виде строки формата `день-месяц-год`.
# В рамках класса реализовать два метода:
# * Первый — с декоратором `@classmethod`, должен извлекать число, месяц, год и преобразовывать их тип к типу «Число».
# * Второй — с декоратором `@staticmethod`, должен проводить валидацию числа, месяца и года
#   (например, `месяц — от 1 до 12`). Проверить работу полученной структуры на реальных данных.


class Date():
    def __init__(self, str_DMY: str = ''):
        self.str_DMY = str_DMY

    def __str__(self):
        return self.str_DMY

    @classmethod
    def parce(cls, date = ''):
        """Преобразует дату в формате «день-месяц-год» в кортеж «день, месяц, год»"""
        ar = date.split('-')
        return Date.validate(ar[0], ar[1], ar[2])

    @staticmethod
    def validate(day: int = 0, month: int = 0, year: int = 0) -> list:
        """Проверяет дату на достоверность (только в диапазонах значений!)"""
        day = Date.clear_int_str(day)
        month = Date.clear_int_str(month)
        year = Date.clear_int_str(year)

        return (day if 0 < day and day <= 31 else 1,
                month if 0 < day and day <= 12 else 1,
                year if 1900 < day and day <= 2100 else 1900)

    @staticmethod
    def clear_int_str(str: str = '') -> int:
        """Интерпретирует строку как целое положительное значение (включая ноль). Если не получается это сделать, то возвращает ноль"""
        try:
            i = int(str)
        except:
            return 0
        return i if i > 0 else 0


print(Date('5-10-2002'))
print(Date.validate(5, 10, 2002))
print(Date.parce('5-10-2002'))
