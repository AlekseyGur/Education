# Урок 4. Hive & HUE

## Задачи

### Задание 1 
Подключиться к серверу, ввести команду hive (либо истользуя DBeaver), по очереди выполнить все команды из HSQL_1.sql, заменив student1_1 на своего пользователя. Сказать, какие действия мы выполняем в каждом из запросов/команд (на insert не забываем про TABLEsample). + ответить на вопросы, содержащиеся в HSQL_1.sql.

### Задание 2 
Сказать какие особенности, касающиеся синтаксиса HiveQL надо учитывать, создавая таблицу с партиционированием и при инсерте в неё. Зачем нам нужно партиционирование?

### Задание 3
Переписать «SELECT …» в команде «CREATE TEMPORARY TABLE» используя CTE (“with”: https://www.sqlservertutorial.net/sql-server-basics/sql-server-cte/ ) для объявления t2; пример:
Hive WITH clause example with the SELECT statement
```sql
WITH t1 as (SELECT 1),
t2 as (SELECT 2),
t3 as (SELECT 3)
SELECT * from t1
UNION ALL
SELECT * from t2
UNION ALL
SELECT * from t3;
```

### Задание *
Создать таблицу airport_codes_part_2 c партиционированием по 2 колонкам: type и iso_country. Вставить в неё 1000 строк, запросом SELECT вывести самую популярную связку type iso_country используя оконную функцию row_number https://www.revisitclass.com/hadoop/how-to-use-row-number-function-in-hive/.


Задачи со * предназначены для продвинутых учеников, которым мало сделать обычное ДЗ.

## Решения

### Решение задания 1
*--зачем используем use?*
Чтобы потом не указывать базу через префикс ("student42_19.") в некоторых запросах. Например, вместо "drop TABLE student42_19.airport_codes;" писать коротко "drop TABLE airport_codes;". Если базу не указать и не использовать префикс, то будет использована база "default".

*-- зачем нам эта опция? "skip.header.line.count"="1"*
Чтобы при операциях SELECT пропускалась первая строка, потому что в ней названия столбцов

*--почему пишем лимит? SELECT  FROM airportcodes LIMIT 10; *
Чтобы не выводить всю таблицу в консоль.

*--что делаем в этих запросах?*
SELECT COUNT(DISTINCT type) FROM airport_codes; - Получаем количество уникальных значений поля type
SELECT DISTINCT type FROM airport_codes; - Получаем список уникальных значений поля type

*-- теперь посмотри в hivetestloc через hdfs dfs -ls/-du и скажи, что заметил и почему там всё так*
Произошло (партиционирование) разделение базы данных на несколько файлов по количеству уникальных значений поля type. База разделилась на файлы в отдельных папках с именами в виде:
hive_test_loc/type=%22closed%22
hive_test_loc/type=%22heliport%22
hive_test_loc/type=%22seaplane_base%22
hive_test_loc/type=%22small_airport%22

*--что такое TEMPORARY TABLE и когда лучше использовать?*
"TEMPORARY TABLE":
1. Используется для хранения данных в течение сессии.
2. Удаляются сами после завершения сессии. 
2. Хранятся в /tmp/hive/user/*
3. Нельзя создать несколько  TEMPORARY TABLE с одинаковыми именами, они перезапишут друг друга.
4. В такие таблицы нельзя зайти из другой сессии hive.
5. В них нельзя создавать индексы.
6. Не поддерживают разбиение на части (партиции).


*-- что будет с содержимым таблицы, если колонки, по которым партиционируем, будут стоять не последними в селекте?*
Если написать type не в конце, то Hive не сможет определить колонку, которая является динамической. Поэтому всем данным будет присвоено значение __HIVE_DEFAULT_PARTITION__ в столбце type. И папка с партицией будет находиться по адресу:
hive_test_loc/type=__HIVE_DEFAULT_PARTITION__
В папке будет всё содержимое базы без колонки type. 
По правилам надо ставить динамические колонки всегда в конец списка в SELECT выражениях. И только в том порядке, который прописан в PARTITION()

*-- чем insert overwrite отличается от insert into?*
С "overwrite" база сначала будет очищена, а потом в неё будет записана информация. Без этой приставки информация будет добавлена в конец файла. "overwrite" также действует и на партиции.

*-- выполни в баше это и скажи, что мы тут делаем:*
*-- -- seq 0 9 > col1 && seq 10 19 > col2
-- -- paste -d '|' col1 col2 | hdfs dfs -appendToFile - testtab/testtab.csv*
В первой команде записали два файла col_1 и col_2 с последовательностями чисел от 0 до 9 и от 10 до 19.
Во второй команде соединили строчки файлов col_1 и col_2 через разделитель '|' и записали в конец файла test_tab.csv внутри hadoop.
В конце создаём базу, записывая в неё данные из файла.

*-- что тут произошло и как это можно использовать ещё? SELECT transform(col1, col2) using "awk '{print $1+$2}'" as mysum from mytesttab;*
Получается одна колонка, которая содержит сумму из значений колонок col_1 и col_2. Можно использовать в любом виде, который позволяет awk и другие команды консоли (sed, xargs и т.п.)

### Решение задания 2
Какие особенности, касающиеся синтаксиса HiveQL надо учитывать, создавая таблицу с партиционированием и при инсерте в неё. Зачем нам нужно партиционирование?
1. При инсерте в такую таблицу надо ставить динамические параметры последними в SELECT выражении.
2. И только в том порядке, который указан в PARTITION().
3. Можно указать одновременно статические и динамические партиции. Например: PARTITION(country=‘RU’, state). Но статические должны идти первыми.
4. При создании таблицы с партиционированием надо писать имя колонки, по которой идёт разделение, после PARTITION BY. А не в списке всех колонок. А вот при создании выборок, при помощи SELECT, можно писать название колонок партиционирования в списке выбираемых.
5. Стоит экранировать слово type, потому что часто является системным.

### Решение задания 3
```sql
WITH
t1 AS (SELECT
            ident, name, elevation_ft, continent,iso_region, municipality, gps_code, iata_code, local_code, iso_country, type
       FROM
            student42_19.airport_codes),
t2 AS (SELECT
            distinct type AS type_2
       FROM student42_19.airport_codes_part)
SELECT
    *
FROM
    t1
LEFT JOIN
    t2 
ON
    t1.type = t2.type_2
WHERE
    t2.type_2 is null
LIMIT 10;
```
### Решение задания *
```sql
CREATE TABLE student42_19.airport_codes_part_2 (
    id int,
    ident string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
PARTITIONED BY (type string, iso_country string)
STORED AS TEXTFILE
LOCATION '/user/student42_19/airport_codes_part_2';

SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE airport_codes_part_2 
PARTITION(type, iso_country)
SELECT 
    id,ident,name,latitude_deg,longitude_deg,elevation_ft,
    iso_country,iso_region,municipality,scheduled_service,
    gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,type,iso_country
FROM airport_codes LIMIT 1000;
```
-- запрос с обычным GROUP BY выполняется 4.05 секунды
```sql
SELECT
    type,
    iso_country,
    count(*) as count
FROM
    airport_codes_part_2
GROUP BY type, iso_country
SORT BY count DESC
LIMIT 1;
```
-- запрос с ROW_NUMBER выполняется 4.66 секунды
```sql
SELECT
    type,
    iso_country,
    ROW_NUMBER() OVER (PARTITION BY type ORDER BY iso_country DESC) as rank
FROM
    airport_codes_part_2
SORT BY rank DESC
LIMIT 1;
```
-- 4.66 секунды > 4.05 секунды. Зачем ждать дольше?
