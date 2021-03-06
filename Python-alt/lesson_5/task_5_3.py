# Задание 3
#
# Есть два списка:
#
# tutors = [
#     'Иван', 'Анастасия', 'Петр', 'Сергей',
#     'Дмитрий', 'Борис', 'Елена'
# ]
# klasses = [
#     '9А', '7В', '9Б', '9В', '8Б', '10А', '10Б', '9А'
# ]
#
# Необходимо реализовать генератор, возвращающий кортежи вида (<tutor>, <klass>), например:
#
# ('Иван', '9А')
# ('Анастасия', '7В')
# ...
#
# Количество генерируемых кортежей не должно быть больше длины списка tutors. Если в списке klasses меньше элементов, чем в списке tutors, необходимо вывести последние кортежи в виде: (<tutor>, None), например:
#
# ('Станислав', None)
#
# Доказать, что вы создали именно генератор. Проверить его работу вплоть до истощения. Подумать, в каких ситуациях генератор даст эффект.
#
# ВНИМАНИЕ! Используйте стартовый код для своей реализации:
#
# tutors = ['Иван', 'Анастасия', 'Петр', 'Сергей', 'Дмитрий', 'Борис', 'Елена']
# klasses = ['9А', '7В', '9Б', '9В', '8Б', '10А', '10Б', '9А']
#
#
# def check_gen(tutors: list, klasses: list):
#     pass
#
#
# generator = check_gen(tutors, klasses)
# # добавьте здесь доказательство, что создали именно генератор
# for _ in range(len(tutors)):
#     print(next(generator))
# # next(generator)  # если раскомментировать, то должно падать в traceback по StopIteration


import typing

tutors = ['Иван', 'Анастасия', 'Петр', 'Сергей', 'Дмитрий', 'Борис', 'Елена']
klasses = ['9А', '7В', '9Б', '9В', '8Б', '10А', '10Б', '9А']

def check_gen(tutors: list, klasses: list) -> typing.Generator:
    """Генератор, возвращающий кортежи из элементов (tutors[i], klasses[i]). Количество возвратов равно длине tutors. Если в klasses не хватает элементов, то на их месте возвращается None"""
    m = len(tutors) - len(klasses)
    if m:
        klasses.extend([None] * m)
    return (l for l in zip(tutors, klasses))


generator = check_gen(tutors, klasses)
print(type(generator)) # доказательство, что создали именно генератор
for _ in range(len(tutors)):
    print(next(generator))
# next(generator)  # если раскомментировать, то должно падать в traceback по StopIteration
