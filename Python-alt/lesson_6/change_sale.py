# смотреть задание в файле task_6_7.py
import sys
if len(sys.argv) < 3:
    print('''Недостаточно аргументов.
             Передайте аргументом номер строки для изменения и новое значение''')
    exit(0)

request_number = int(sys.argv[1])
with open('sales', 'r+', encoding='utf-8') as f:
    start = None
    i = 1
    line = f.readline() # обход ошибки вызова tell() - OSError: telling position disabled by next() call
    if request_number == 1:
        start = 0
    else:
        while line:
            i += 1
            if i == request_number:
                start = f.tell()
                break
            line = f.readline()

    if start != None:
        f.seek(start)
        
        # Делаем сохраняемые строки одинаковой длины. Потому что при изменении
        # одного значения без чтения всего файла приходится заменять байты. Иначе
        # будет перезаписана не одна строка, а несколько
        f.write(sys.argv[2].strip().zfill(10) + '\n')
    else:
        print('Такой строки не существует')
