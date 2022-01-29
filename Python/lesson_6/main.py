# 1. Создать класс TrafficLight (светофор).
# определить у него один атрибут color (цвет) и метод running (запуск);
# в рамках метода реализовать переключение светофора в режимы: красный,
# жёлтый, зелёный;
# продолжительность первого состояния (красный) составляет 7 секунд, второго
# (жёлтый) — 2 секунды, третьего (зелёный) — на ваше усмотрение;
# переключение между режимами должно осуществляться только в указанном порядке
# (красный, жёлтый, зелёный);
# проверить работу примера, создав экземпляр и вызвав описанный метод.
# Задачу можно усложнить, реализовав проверку порядка режимов. При его нарушении
# выводить соответствующее сообщение и завершать скрипт.

from time import sleep
class TrafficLight:
    color = ''
    def running(self):
        while True:
            self.color = 'красный'
            print(self.color)
            sleep(7)

            self.color = 'жёлтый'
            print(self.color)
            sleep(2)

            self.color = 'зелёный'
            print(self.color)
            sleep(3)

tl = TrafficLight()
tl.running()


# 2. Реализовать класс Road (дорога).
# определить атрибуты: length (длина), width (ширина);
# значения атрибутов должны передаваться при создании экземпляра класса;
# атрибуты сделать защищёнными;
# определить метод расчёта массы асфальта, необходимого для покрытия всей дороги;
# использовать формулу: длина*ширина*масса асфальта для покрытия одного кв.
# метра дороги асфальтом, толщиной в 1 см*число см толщины полотна;
# проверить работу метода.
# Например: 20 м*5000 м*25 кг*5 см = 12500 т.

class Road:
    _length = 0 # м
    _width = 0 # м
    _height = 0.05 # = 5 см
    _weight_per_sq_meter = 2500 # кг в 1 куб. метре

    def __init__(self, **kwargs):
        self._length = kwargs['length']
        self._width = kwargs['width']

    def size(self):
        return self._length * self._width * self._height

    def weight(self):
        return round(self._weight_per_sq_meter * self.size() / 1000)

rd = Road(length=5000, width=20)
print(f'Вес: {rd.weight()} т.')

# 3. Реализовать базовый класс Worker (работник).
# определить атрибуты: name, surname, position (должность), income (доход);
# последний атрибут должен быть защищённым и ссылаться на словарь, содержащий
# элементы: оклад и премия, например, {"wage": wage, "bonus": bonus};
# создать класс Position (должность) на базе класса Worker;
# в классе Position реализовать методы получения полного имени сотрудника
# (get_full_name) и дохода с учётом премии (get_total_income);
# проверить работу примера на реальных данных: создать экземпляры класса
# Position, передать данные, проверить значения атрибутов, вызвать методы
# экземпляров.

class Worker:
    name = 'Иван'
    surname = 'Иванов'
    position = 'Должность'
    _income = {"wage": 10, "bonus": 5}

    def get_income(self):
        return self._income

class Position(Worker):

    def get_full_name(self):
        return self.name + ' ' + self.surname

    def get_total_income(self):
        return self.get_income()["wage"] + self.get_income()["bonus"]

p = Position()
print('Полное имя: ' + str(p.get_full_name()))
print('Зарплата: ' + str(p.get_total_income()))


# 4. Реализуйте базовый класс Car.
# у класса должны быть следующие атрибуты: speed, color, name, is_police (булево).
# А также методы: go, stop, turn(direction), которые должны сообщать, что машина
# поехала, остановилась, повернула (куда);
# опишите несколько дочерних классов: TownCar, SportCar, WorkCar, PoliceCar;
# добавьте в базовый класс метод show_speed, который должен показывать текущую
# скорость автомобиля;
# для классов TownCar и WorkCar переопределите метод show_speed. При значении
# скорости свыше 60 (TownCar) и 40 (WorkCar) должно выводиться сообщение о
# превышении скорости.
# Создайте экземпляры классов, передайте значения атрибутов. Выполните доступ
# к атрибутам, выведите результат. Вызовите методы и покажите результат.

import random
class Car:
    speed = 0
    color = ''
    name = ''
    is_police = False

    def __init__(self, **kwargs):
        if 'speed' in kwargs: self.speed = kwargs['speed']
        if 'color' in kwargs: self.color = kwargs['color']
        if 'name' in kwargs: self.name = kwargs['name']
        if 'is_police' in kwargs: self.is_police = kwargs['is_police']

        print(f'\nНазвание автомобиля: {self.name}')
        print(f'Цвет: {self.color}')

        self.go()

    def go(self):
        self.speed = 30 + random.randint(0, 50)

    def stop(self):
        self.speed = 0

    def turn(self, direction=''):
        print(f'Поворот') # = изменение скорости
        self.go()

    def show_speed(self):
        print(f'Скорость: {self.speed} км/ч')

class TownCar(Car):
    def __init__(self, **kwargs):
        Car.__init__(self, **kwargs)

    def show_speed(self):
        Car.show_speed(self)
        if 60 < self.speed: print(f'Превышение скорости!')

class WorkCar(Car):
    def __init__(self, **kwargs):
        Car.__init__(self, **kwargs)

    def show_speed(self):
        Car.show_speed(self)
        if 40 < self.speed: print(f'Превышение скорости!')

class SportCar(Car):
    def __init__(self, **kwargs):
        Car.__init__(self, **kwargs)

class PoliceCar(Car):
    def __init__(self, **kwargs):
        Car.__init__(self, is_police = True, **kwargs)


Town = TownCar(color = 'black', name = 'Town')
Town.show_speed()
Town.turn()
Town.show_speed()

Work = WorkCar(color = 'green', name = 'Work')
Work.show_speed()

Sport = SportCar(color = 'red', name = 'Sport')
Sport.show_speed()

Police = PoliceCar(color = 'white', name = 'Police')
Police.show_speed()



# 5. Реализовать класс Stationery (канцелярская принадлежность).
# определить в нём атрибут title (название) и метод draw (отрисовка). Метод
# выводит сообщение «Запуск отрисовки»;
# создать три дочерних класса Pen (ручка), Pencil (карандаш), Handle (маркер);
# в каждом классе реализовать переопределение метода draw. Для каждого класса
# метод должен выводить уникальное сообщение;
# создать экземпляры классов и проверить, что выведет описанный метод для каждого
# экземпляра.

class Stationery:
    title = ''
    def draw(self):
        print(f'Запуск отрисовки')

class Pen(Stationery):
    def draw(self):
        print(f'Запуск отрисовки (инструмент: ручка)')

class Pencil(Stationery):
    def draw(self):
        print(f'Запуск отрисовки (инструмент: карандаш)')

class Handle(Stationery):
    def draw(self):
        print(f'Запуск отрисовки (инструмент: маркер)')

newPen = Pen()
newPen.draw()

newPencil = Pencil()
newPencil.draw()

newHandle = Handle()
newHandle.draw()
