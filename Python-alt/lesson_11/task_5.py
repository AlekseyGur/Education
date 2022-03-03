# ## Задание 5
# Продолжить работу над заданием 4.
# * Разработать методы, которые отвечают за приём оргтехники на склад и передачу в определённое подразделение компании.
# Для хранения данных о наименовании и количестве единиц оргтехники, а также других данных,
# можно использовать любую подходящую структуру (например, словарь).


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
            self.last_id + 1:{
                'name': kwargs['name'], # наименование
                'count': kwargs['count'] # количество
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


class Equipment():
    """Оргтехника"""
    pass


class Printer(Equipment):
    """принтер"""
    pass


class Scaner(Equipment):
    """сканер"""
    pass


class Xerox(Equipment):
    """ксерокс"""
    pass
