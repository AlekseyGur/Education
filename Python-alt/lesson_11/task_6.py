# ## Задание 6
# Продолжить работу над заданием 5.
# * Реализовать механизм валидации вводимых пользователем данных. Например, для указания количества принтеров,
# отправленных на склад, нельзя использовать строковый тип данных!
#
# > Подсказка: постарайтесь реализовать в проекте «Склад оргтехники» максимум возможностей, изученных на уроках по ООП.


class Warehouse():
    """Склад оргтехники"""
    def __init__(self):
        self.store = {} # данные о содержимом склада
        # Формат хранения данных:
        # {
        #     1: { # id предмета - целое число
        #         'name': 'принтер', # наименование
        #         'count': 1, # количество
        #         'user': '' # департамент, где используется
        #     }
        # }

    def add(self, **kwargs):
        """приём оргтехники на склад"""
        a = {
            self.last_id+1:{
                'name': kwargs['name'], # наименование
                'count': self.clear_int_str(kwargs['count']) # количество
            }
        }
        self.store.update(a)

    def use(self, name, to_department):
        """передача в определённое подразделение компании"""
        for id, val in self.store.items():
            if name == val['name']:
                val['user'] = to_department

    def show(self):
        """показатьт склад"""
        print(self.store)

    @property
    def last_id(self):
        """получить последний id"""
        if not self.store:
            return 0
        else:
            return sorted(self.store.items(), key=lambda x: x[0])[-1][0]

    @staticmethod
    def clear_int_str(str: str = '') -> int:
        """Интерпретирует строку как целое положительное значение (включая ноль). Если не получается это сделать, то возвращает ноль"""
        try:
            i = int(str)
        except:
            return 0
        return i if i > 0 else 0

class Equipment():
    """Оргтехника"""
    def __init__(self):
        pass

class Printer(Equipment):
    """принтер"""
    def __init__(self):
        super().__init__()
        pass

class Scaner(Equipment):
    """сканер"""
    def __init__(self):
        super().__init__()
        pass

class Xerox(Equipment):
    """ксерокс"""
    def __init__(self):
        super().__init__()
        pass


w = Warehouse()
w.add(name = 'принтер', count = 1)
w.use(name = 'принтер', to_department = 'HR')
print(w.last_id)
w.show()
