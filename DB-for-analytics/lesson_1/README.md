# Урок 1. Аналитика в бизнес-задачах

## Задания

1. Загрузить в свою БД данные по продажам. Исходник: https://drive.google.com/drive/folders/1C3HqIJcABblKM2tz8vPGiXTFT7MisrML? . Интересует orders_20190822 и проверить возможные ошибки
2. Проанализировать период данных выгрузки
3. Посчитать кол-во строк, заказов и уникальных пользователей, которые совершили заказы
4. По годам и месяцам посчитать средний чек, среднее кол-во заказов на пользователя, сделать вывод, как изменялись эти показатели год от года.
5. Найти кол-во пользователей, кот покупали в одном году и перестали покупать в следующем.
6. Найти ID самого активного по кол-ву покупок.
7. Найти коэффициенты сезонности по месяцам.
8. Построить график падения вероятности второй покупки по дням сразу после первой.

## Решение

### 2. Проанализировать период данных выгрузки

```SQL
SELECT 
    YEAR(o_date) AS year,
    COUNT(DISTINCT(o_date)) * 100 / 365 AS `data_fullness_%`
FROM
    orders
GROUP BY
    YEAR(o_date)
ORDER BY
    year;
```

Вывод:

| year | data_fullness_% |
|------|-----------------|
| 2016 |        100.2740 |
| 2017 |        100.0000 |


### 3. Посчитать кол-во строк, заказов и уникальных пользователей, которые совершили заказы

```SQL
SELECT 
    COUNT(*) AS `rows`,
    COUNT(DISTINCT(id_o)) AS `orders`,
    COUNT(DISTINCT(user_id)) AS `users`
FROM
    orders;
```

Вывод:
 
| rows    | orders  | users   |
|---------|---------|---------|
| 2002804 | 2002804 | 1015119 | 


### 4. По годам и месяцам посчитать средний чек, среднее кол-во заказов на пользователя, сделать вывод, как изменялись эти показатели год от года.

```SQL
SELECT 
    YEAR(o_date) AS `year`,
    MONTH(o_date) AS `month`,
    COUNT(id_o) AS `orders`,
    ROUND(AVG(price)) AS `avg_price`
FROM
    orders
GROUP BY
    year, month
ORDER BY
    year, month;
```

| year | month | orders | avg_price |
|------|-------|--------|-----------|
| 2016 |     1 |  46559 |      2079 |
| 2016 |     2 |  45076 |      2117 |
| 2016 |     3 |  59536 |      1936 |
| 2016 |     4 |  67734 |      2057 |
| 2016 |     5 |  54686 |      1986 |
| 2016 |     6 |  59980 |      1945 |
| 2016 |     7 |  57230 |      1978 |
| 2016 |     8 |  67180 |      2077 |
| 2016 |     9 |  70146 |      2180 |
| 2016 |    10 |  89763 |      2358 |
| 2016 |    11 | 115287 |      2226 |
| 2016 |    12 | 128169 |      2020 |
| 2017 |     1 |  76145 |      2327 |
| 2017 |     2 |  70652 |      2288 |
| 2017 |     3 |  90348 |      2377 |
| 2017 |     4 |  85308 |      2317 |
| 2017 |     5 |  91949 |      2361 |
| 2017 |     6 |  77343 |      2391 |
| 2017 |     7 |  77002 |      2431 |
| 2017 |     8 |  84375 |      2440 |
| 2017 |     9 |  80976 |      2618 |
| 2017 |    10 | 106973 |      2619 |
| 2017 |    11 | 131882 |      2477 |
| 2017 |    12 | 168505 |      2210 |

```SQL
SELECT 
    YEAR(o_date) AS `year`,
    COUNT(id_o) AS `orders`,
    ROUND(AVG(price)) AS `avg_price`
FROM
    orders
GROUP BY
    year
ORDER BY
    year;
```

| year | orders  | avg_price |
|------|---------|-----------|
| 2016 |  861346 |      2096 |
| 2017 | 1141458 |      2398 |

Вывод 4: в 2017 году средний чек возрос на 15%, а количество заказов на 32%.


### 5. Найти кол-во пользователей, кто покупали в одном году и перестали покупать в следующем.

```SQL
SELECT 
    COUNT(DISTINCT(user_id)) AS count_users
FROM
    orders
WHERE
    YEAR(o_date) = 2016
AND
    user_id NOT IN (
        SELECT 
            DISTINCT(user_id)
        FROM
            orders
        WHERE
            YEAR(o_date) = 2017
    );
```

| count_users |
|-------------|
|      360225 |


### 6. Найти ID самого активного по кол-ву покупок.

```SQL
SELECT 
    DISTINCT(user_id) AS user_id
FROM
    orders
GROUP BY
    user_id
ORDER BY
    SUM(1) DESC
LIMIT 1;
```

| user_id |
|---------|
|  765861 |


### 7. Найти коэффициенты сезонности по месяцам.

```SQL
SELECT 
    `year`,
    `month`,
    ROUND(sum_month / AVG(sum_month) OVER(PARTITION BY year), 2) AS 'season_coeff' 
FROM (
        SELECT 
            YEAR(o_date) AS year,
            MONTH(o_date) AS month,
            SUM(price) AS `sum_month`
        FROM
            orders
        GROUP BY
            YEAR(o_date),
            MONTH(o_date)
    ) as t
ORDER BY
    year,
    month;
```

| year | month | season_coeff |
|------|-------|--------------|
| 2016 |     1 |         0.64 |
| 2016 |     2 |         0.63 |
| 2016 |     3 |         0.77 |
| 2016 |     4 |         0.93 |
| 2016 |     5 |         0.72 |
| 2016 |     6 |         0.78 |
| 2016 |     7 |         0.75 |
| 2016 |     8 |         0.93 |
| 2016 |     9 |         1.02 |
| 2016 |    10 |         1.41 |
| 2016 |    11 |         1.71 |
| 2016 |    12 |         1.72 |
| 2017 |     1 |         0.78 |
| 2017 |     2 |         0.71 |
| 2017 |     3 |         0.94 |
| 2017 |     4 |         0.87 |
| 2017 |     5 |         0.95 |
| 2017 |     6 |         0.81 |
| 2017 |     7 |         0.82 |
| 2017 |     8 |          0.9 |
| 2017 |     9 |         0.93 |
| 2017 |    10 |         1.23 |
| 2017 |    11 |         1.43 |
| 2017 |    12 |         1.63 |


### 8. Построить график падения вероятности второй покупки по дням сразу после первой.

```SQL
SELECT
    days_diff AS `days_delay`,
    COUNT(days_diff) / SUM(COUNT(days_diff)) OVER () AS `probability`
FROM
    (
        SELECT
            DATEDIFF(o_date, LAG(o_date, 1) OVER(PARTITION BY user_id ORDER BY o_date)) AS 'days_diff'
        FROM
            orders
        ORDER BY
            user_id,
            o_date
    ) as t
WHERE
    days_diff IS NOT NULL
GROUP BY
    days_diff
ORDER BY
    days_diff;
```

| days_delay | probability |
|------------|-------------|
|          0 |      0.1950 |
|          1 |      0.0544 |
|          2 |      0.0303 |
|          3 |      0.0262 |
|          4 |      0.0219 |
|          5 |      0.0207 |
|          6 |      0.0205 |
|          7 |      0.0204 |
|          8 |      0.0181 |
|          9 |      0.0160 |
|        ... |         ... |

Изображение в файле 8.jpg
