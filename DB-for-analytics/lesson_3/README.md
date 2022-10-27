# Урок 3. Типовые методы анализа данных

## Задания

Делаем прогноз ТО на 05.2017. Считаем сколько денег тратят группы клиентов в день.

1. Группа часто покупающих (3 и более покупок) и которые последний раз покупали не так давно. Считаем сколько денег оформленного заказа приходится на 1 день. Умножаем на 30.
2. Группа часто покупающих, но которые не покупали уже значительное время. Так же можем сделать вывод, из такой группы за следующий месяц сколько купят и на какую сумму. (постараться продумать логику).
3. Отдельно разобрать пользователей с 1 и 2 покупками за всё время, прогнозируем их.
4. В итогу у вас будет прогноз ТО и вы сможете его сравнить с фактом и оценить грубо разлёт по данным. 

Как источник данных используем данные по продажам за 2 года.

## Решение

### 1. Группа часто покупающих (3 и более покупок) и которые последний раз покупали не так давно. Считаем сколько денег оформленного заказа приходится на 1 день. Умножаем на 30.

```SQL
SELECT
    o_date,
    AVG(price) * 30
FROM
    orders
WHERE
    -- o_date > DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    EXTRACT(year FROM o_date) = 2017
AND
    user_id IN ( 
        -- клиенты, которые сделали 3 и более покупок за 30 последних дней
        SELECT
            user_id AS user
        FROM
            orders
        WHERE
            -- o_date > DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            EXTRACT(year FROM o_date) = 2017
        GROUP BY
            user_id
        HAVING 
            COUNT(id_o) > 3
    )
GROUP BY
    o_date;
```

Вывод:

| o_date     | AVG(price) * 30    |
|------------|--------------------|
| 2017-01-01 |  61924.07416732223 |
| 2017-01-02 |  72006.41548265729 |
| 2017-01-03 |  76770.13598539244 |
| 2017-01-04 |  82211.83548959035 |
| 2017-01-05 |  66875.10584801894 |
| 2017-01-06 |  66559.00934838803 |
| 2017-01-07 |  71543.43855877369 |
| 2017-01-08 |  66739.98400785202 |
| 2017-01-09 |  67262.58930827702 |
|        ... |                ... |



### 2. Группа часто покупающих, но которые не покупали уже значительное время. Так же можем сделать вывод, из такой группы за следующий месяц сколько купят и на какую сумму. (постараться продумать логику).

```SQL
WITH res AS (
    -- статистика продаж по месяцам среди клиентов с разницей между последними суммами, чтобы сделать прогноз
    SELECT
        EXTRACT(month FROM o_date) AS date,
        AVG(price) as avg_price,
        AVG(price) - LAG(AVG(price)) OVER () AS last_month_delta
    FROM
        orders
    WHERE
        o_date < DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  --  AND
   --     o_date > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    AND
        user_id IN ( 
            -- клиенты, которые сделали 3 и более покупок, но не за последние 30 дней
            SELECT
                user_id AS user
            FROM
                orders
            WHERE
                o_date < DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            -- AND
           --     o_date > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
            GROUP BY
                user_id
            HAVING 
                COUNT(id_o) > 3
        )
    GROUP BY
        EXTRACT(month FROM o_date)
    ORDER BY
        date DESC
)
SELECT -- предсказание продаж следующего месяца, используя разницу между двумя предыдущими. Предполагаем, что тренд сохранится как по нарпавлению, так и по силе.
    avg_price + last_month_delta AS next_month_sells_prediction
FROM
    res
ORDER BY
    date DESC
LIMIT 1;
```

Вывод:

| next_month_sells_prediction |
|-----------------------------|
|          1978.4190891409753 |

### 3.1 Отдельно разобрать пользователей с 1 и 2 покупками за все время, прогнозируем их.

```SQL
SELECT
    DISTINCT o_date,
    COUNT(id_o) AS orders_count,
    SUM(price) AS orders_count,
    user_id
FROM
    orders 
GROUP BY
    o_date,
    user_id 
HAVING
    COUNT(id_o)=1
ORDER BY 
    o_date 
DESC;
```

### 3.2

```SQL
SELECT
    DISTINCT o_date,
    COUNT(id_o) AS orders_count,
    SUM(price) AS orders_count,
    user_id
FROM
    orders 
GROUP BY
    o_date,
    user_id 
HAVING
    COUNT(id_o)=2
ORDER BY 
    o_date 
DESC;
```
