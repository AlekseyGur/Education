# смотреть задание в файле task_6_7.py
import sys

with open('sales', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if len(sys.argv) == 2 and i < int(sys.argv[1]):
            continue

        if len(sys.argv) == 3 and (i < int(sys.argv[1]) or int(sys.argv[2]) < i):
            continue

        print(line.rstrip())
