# ## Задание 4
# Реализуйте базовый класс `Car`:
# * у класса должны быть следующие атрибуты: `speed`, `color`, `name`, `is_police` (булево).
#   А также методы: `go`, `stop`, `turn(direction)`, которые должны сообщать в stdout информацию по формату
#   (формат сообщений смотрите в документации методов исходного задания);
# * значение аргумента `direction`, передаваемого в метод `turn(direction)` может иметь только одно из
#   четырез значений: `направо`, `налево`, `прямо` или `назад` (если передать другое значение, то должно быть
#   возбуждено исключение `ValueError` с сообщением `нераспознанное направление движения`)
# * опишите несколько дочерних классов: `TownCar`, `SportCar`, `WorkCar`, `PoliceCar`;
# * добавьте в базовый класс метод `show_speed`, который должен показывать текущую скорость автомобиля
#   по формату в документации метода, если атрибут `is_police` равен `True`, то при вызове метода выводить
#   в `stdout` дополнительно второе сообщение `Вруби мигалку и забудь про скорость!`;
# * для классов `TownCar` и `WorkCar` переопределите метод `show_speed`.
#   При значении скорости свыше `60 (TownCar)` и `40 (WorkCar)` в `stdout` должно выводиться сообщение о
#   превышении скорости `Alarm!!! Speed!!!`, если превышения нет, то стандартное сообщение из родительского класса.
#
# Создайте экземпляры классов, передайте значения атрибутов. Выполните доступ к атрибутам, выведите результат.
# Вызовите методы и покажите результат.
#
# **ВНИМАНИЕ!** Используйте стартовый код для своей реализации:
#
# ```(python)
# class Car:
#     is_police: bool = False
#
#     def __init__(self, speed: int, color: str, name: str):
#         """
#         Конструктор класса
#         :param speed: текущая скорость автомобиля
#         :param color: цвет автомобиля
#         :param name: название марки автомобиля
#         """
#         pass  # опишите конструктор
#
#     def go(self) -> None:
#         """
#         Увеличивает значение скорости на 15
#         :return: в stdout сообщение по формату
#             'Машина <название марки машины> повысила скорость на 15: <текущая скорость машины>'
#         """
#         pass  # Ваш код здесь
#
#     def stop(self) -> None:
#         """
#         При вызове метода скорость становится равной '0'
#         :return: в stdout сообщение по формату '<название марки машины>: остановилась'
#         """
#         pass  # Ваш код здесь
#
#     def turn(self, direction: str) -> None:
#         """
#         Принимает направление движения автомобиля
#         :param direction: строковое представление направления движения, может принимать только
#             следующие значения: 'направо', 'налево', 'прямо', 'назад'
#         :return: в stdout сообщение по формату
#             '<название марки машины>: движется <direction>'
#         """
#         pass  # Ваш код здесь
#
#     def show_speed(self) -> None:
#         """
#         Проверка текущей скорости автомобиля
#         :return: в stdout выводит сообщение формата
#             '<название марки машины>: текущая скорость <значение текущей скорости> км/час'
#         """
#         pass  # Ваш код здесь
#
#
# # определите классы TownCar, WorkCar, SportCar, PoliceCar согласно условия задания
#
#
# if __name__ == '__main__':
#     town_car = TownCar(41, "red", 'WW_Golf')
#     work_car = WorkCar(41, 'yellow', 'BobCat')
#     police_car = PoliceCar(120, "blue", 'BMW')
#     sport_car = SportCar(300, 'white', 'Ferrari')
#     town_car.go()  # Машина WW_Golf повысила скорость на 15: 56
#     town_car.show_speed()  # WW_Golf: текущая скорость 56 км/час
#     work_car.show_speed()  # Alarm!!! Speed!!!
#     town_car.stop()  # WW_Golf: остановилась
#     police_car.show_speed()
#     # BMW: текущая скорость 120 км/час
#     # Вруби мигалку и забудь про скорость!
#     sport_car.turn('назад')  # Ferrari(SportCar): движется назад
#     sport_car.turn('right')
#     """
#     Traceback (most recent call last):
#       ...
#     ValueError: нераспознанное направление движения
#     """
# ```


class Car:
    def __init__(self, speed: int, color: str, name: str, is_police: bool = False):
        """
        Конструктор класса
        :param speed: текущая скорость автомобиля
        :param color: цвет автомобиля
        :param name: название марки автомобиля
        """
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

        # print(f'\nНазвание автомобиля: {self.name}')
        # print(f'Цвет: {self.color}')
        #
        # self.go()

    def go(self) -> None:
        """
        Увеличивает значение скорости на 15
        :return: в stdout сообщение по формату
            'Машина <название марки машины> повысила скорость на 15: <текущая скорость машины>'
        """
        self.speed += 15
        print(f'Машина {self.name} повысила скорость на 15: {self.speed}')

    def stop(self) -> None:
        """
        При вызове метода скорость становится равной '0'
        :return: в stdout сообщение по формату '<название марки машины>: остановилась'
        """
        self.speed = 0
        print(f'{self.name}: остановилась')

    def turn(self, direction: str) -> None:
        """
        Принимает направление движения автомобиля
        :param direction: строковое представление направления движения, может принимать только
            следующие значения: 'направо', 'налево', 'прямо', 'назад'
        :return: в stdout сообщение по формату
            '<название марки машины>: движется <direction>'
        """
        if direction in ['направо', 'налево', 'прямо', 'назад']:
            print(f'{self.name}: движется {direction}')
        else:
            raise ValueError('нераспознанное направление движения')

    def show_speed(self) -> None:
        """
        Проверка текущей скорости автомобиля
        :return: в stdout выводит сообщение формата
            '<название марки машины>: текущая скорость <значение текущей скорости> км/час'
        """
        print(f'{self.name}: текущая скорость {self.speed} км/час')
        if self.is_police:
            print('Вруби мигалку и забудь про скорость!')


class TownCar(Car):
    def show_speed(self):
        Car.show_speed(self)
        if 60 < self.speed:
            print('Alarm!!! Speed!!!')


class WorkCar(Car):
    def show_speed(self):
        Car.show_speed(self)
        if 40 < self.speed:
            print('Alarm!!! Speed!!!')


class SportCar(Car):
    pass


class PoliceCar(Car):
    def __init__(self, *args):
        Car.__init__(self, *args, is_police=True)


if __name__ == '__main__':
    town_car = TownCar(41, "red", 'WW_Golf')
    work_car = WorkCar(41, 'yellow', 'BobCat')
    police_car = PoliceCar(120, "blue", 'BMW')
    sport_car = SportCar(300, 'white', 'Ferrari')
    town_car.go()  # Машина WW_Golf повысила скорость на 15: 56
    town_car.show_speed()  # WW_Golf: текущая скорость 56 км/час
    work_car.show_speed()  # Alarm!!! Speed!!!
    town_car.stop()  # WW_Golf: остановилась
    police_car.show_speed()
    # BMW: текущая скорость 120 км/час
    # Вруби мигалку и забудь про скорость!
    sport_car.turn('назад')  # Ferrari(SportCar): движется назад
    sport_car.turn('right')
    """
    Traceback (most recent call last):
      ...
    ValueError: нераспознанное направление движения
    """
