# Урок 2. HDFS

## Задания

### Реализовать на bash скрипт, который совершает следующие действия

1. Создание 3 пустых файлов файлов test_file_1, test_file_2, test_file_3
2. Запись в каждый из них по 1 значению:
• “Hello,” > test_file_1
• “ hdfs” > test_file_2
• “!” > test_file_3
3. Далее кладём их в домашнюю директорию в hdfs, ставим репликацию 2 и читаем по очереди, записывая аутпут в log.txt
4. Далее на hdfs перемещаем их в папку task_2
5. Печатаем размер кажого файла с учётом репликации (вторая колонка в hdfs dfs -du + http://rus-linux.net/MyLDP/consol/awk.html) записывая аутпут в log.txt.
6. После чего удаляем все созданные файлы как на hdfs (не забываем -skipTrash), так и на локальной машине.
7. Делаем скрипт исполняемым и запускаем его через ./<my_script>
8. Запускаем его и присылаем скриншот, где видно, как мы это запустили и как оно отработало + код самого файла + вывод команды cat log.txt
*ДОП по желанию, но задача "жизненная": сделай так, чтобы при записи в log.txt напротив каждого вывода записывались текущие дата и время; т.е. через табуляцию или 4 пробела.
Пример:
2021-04-23 20:19:13 Hello,
2021-04-23 20:19:15 hdfs


## Решение:

```Bash
### 1. 2.
mkdir ~/lesson_2
cd ~/lesson_2
echo 'Hello,' > test_file_1
echo 'hdfs' > test_file_2
echo '!' > test_file_3
### 3. 
hdfs dfs -put -f test_file_1
hdfs dfs -put -f test_file_2
hdfs dfs -put -f test_file_3
hdfs dfs -setrep 2 test_file_*
hdfs dfs -cat test_file_* | awk '{print strftime("%Y-%m-%d %H:%M:%S"), $0;}' | hadoop fs -appendToFile - log.txt
hdfs dfs -cat log.txt
### 4.
hdfs dfs -mkdir task_2
hdfs dfs -mv test_file_* task_2/
### 5.
hdfs dfs -du task_2/* | awk '{print $2, $3;}'
### 6.
hdfs dfs -rm -r -skipTrash task_2
hdfs dfs -rm -r -skipTrash log.txt
rm -rf ~/lesson_2
```


## Решение

Решение домашних заданий (см.файлы)
