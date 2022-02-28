# # Урок 9. Объектно-ориентированное программирование. Введение
#
# ## Задание 1
# Создать класс `TrafficLight` (светофор):
# * определить у него один атрибут `color` (цвет) и метод `running` (запуск);
# * атрибут реализовать как приватный;
# * в рамках метода реализовать переключение светофора в режимы: красный, жёлтый, зелёный;
# * продолжительность первого состояния (`red`) составляет `4 секунды`, второго (`yellow`) — `2 секунды`,
#   третьего (`green`) — `3 секунды`;
# * переключение между режимами должно осуществляться только в указанном порядке (красный, жёлтый, зелёный) и
#   в `stdout` каждый цвет должен принтоваться ТОЛЬКО ОДИН раз в момент переключения с указанием исходного
#   кол-ва секунд, т.е. формат строки вывода `<текущий цвет> <значение секунд> сек`;
# * проверить работу примера, создав экземпляр и вызвав описанный метод.
#
# Пример, `stdout` при обращении к методу `running`:
#
# ```
# $ traffic = TrafficLight()
# $ traffic.running()
# red 4 сек
# yellow 2 сек
# green 3 сек
# ```
#
# > Задачу можно усложнить, реализовав проверку порядка режимов.
# > При его нарушении выводить соответствующее сообщение и завершать скрипт.
#
# **ВНИМАНИЕ!** Используйте стартовый код для своей реализации:
#
# ```(python)
# class TrafficLight:
#     ...
#
#     def running(self):
#         ...
#
#
# if __name__ == '__main__':
#     traffic = TrafficLight()
#     traffic.running()
# ```


from time import sleep


class TrafficLight:
    def __init__(self):
        self.__color = ''

    def running(self):
        while True:
            self.__color = 'red'
            print(f'{self.__color} 4 сек')
            sleep(4)

            self.__color = 'yellow'
            print(f'{self.__color} 2 сек')
            sleep(2)

            self.__color = 'green'
            print(f'{self.__color} 3 сек')
            sleep(3)


if __name__ == '__main__':
    traffic = TrafficLight()
    traffic.running()
