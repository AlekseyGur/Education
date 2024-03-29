# Урок 4. Хранение данных и ресурсы

## Задание

https://github.com/adterskov/geekbrains-conteinerization/tree/master/homework/4.resources-and-persistence

# Домашнее задание для к уроку 4 - Хранение данных и ресурсы

Напишите deployment для запуска сервера базы данных Postgresql.

Приложение должно запускаться из образа postgres:10.13

Должен быть описан порт:

- 5432 TCP

В деплойменте должна быть одна реплика, при этом при обновлении образа
НЕ ДОЛЖНО одновременно работать несколько реплик.
(то есть сначала должна удаляться старая реплика и только после этого подниматься новая).

> Это можно сделать или с помощью maxSurge/maxUnavailable или указав стратегию деплоя Recreate.

В базе данных при запуске должен автоматически создаваться пользователь testuser
с паролем testpassword. А также база testdatabase.

> Для этого нужно указать переменные окружения POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB в деплойменте.
> При этом значение переменной POSTGRES_PASSWORD должно браться из секрета.

Так же нужно указать переменную PGDATA со значением /var/lib/postgresql/data/pgdata
См. документацию к образу https://hub.docker.com/_/postgres раздел PGDATA

База данных должна хранить данные в PVC c размером диска в 10Gi, замонтированном в pod по пути /var/lib/postgresql/data


## Проверка

Для проверки работоспособности базы данных:

1. Узнайте IP пода postgresql

```bash
kubectl get pod -o wide
```

2. Запустите рядом тестовый под

```bash
kubectl run -t -i --rm --image postgres:10.13 test bash
```

3. Внутри тестового пода выполните команду для подключения к БД

```bash
psql -h <postgresql pod IP из п.1> -U testuser testdatabase
```

Введите пароль - testpassword

4. Все в том же тестовом поде, после подключения к инстансу БД выполните команду для создания таблицы

```bash
CREATE TABLE testtable (testcolumn VARCHAR (50) );
```

5. Проверьте что таблица создалась. Для этого все в том же тестовом поде выполните команду

```bash
\dt
```

6. Выйдите из тестового пода. Попробуйте удалить под с postgresql.

7. После его пересоздания повторите все с п.1, кроме п.4
Проверьте что созданная ранее таблица никуда не делась.


## Выполенени задания

См. файлы yaml в папке.

Устанавливаем пароль в переменную

```bash
kubectl create secret generic postgres -n postgres --from-literal=postgre-pass=testpassword
```

Загружаем все yaml сценарии

```bash
kubectl create -f ./scripts

Создаём папку в нужной ноде, куда будут записываться данные базы.
Так как в проекте пока есть только одна нода minikube, то писать будем прямо туда, в контейнер.
Но по уму надо бы подключить внешнее хранилище!

```bash
docker exec -it -u root minikube mkdir -p /mnt/local-storage
```

Получаем ip контейнера с postgre:

```bash
kubectl get pod -o wide -n postgres | grep postgre | awk '{print $6}'
```

172.17.0.5

Запускаем тестовый под:

```bash
kubectl run -t -i --rm --image postgres:10.13 test bash
psql -h 172.17.0.5 -U testuser testdatabase # Пароль testpassword
CREATE TABLE testtable (testcolumn VARCHAR (50) );
\dt
```

Вывод:

```sql
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | testtable | table | testuser
(1 row)
```

Выходим и вопторяем шаги без создания таблицы:

```bash
kubectl run -t -i --rm --image postgres:10.13 test bash
psql -h 172.17.0.5 -U testuser testdatabase # Пароль testpassword
\dt
```

Вывод:

```sql
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | testtable | table | testuser
(1 row)
```



