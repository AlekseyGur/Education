# Урок 4. Типовая аналитика маркетинговой активности

## Задания

Главная задача: сделать RFM-анализ на основе данных по продажам за 2 года (из предыдущего дз).
​
1. Определяем критерии для каждой буквы R, F, M (т.е. к примеру, R – 3 для клиентов, которые покупали <= 30 дней от последней даты в базе, R – 2 для клиентов, которые покупали > 30 и менее 60 дней от последней даты в базе и т.д.)
2. Для каждого пользователя получаем набор из 3 цифр (от 111 до 333, где 333 – самые классные пользователи)
3. Вводим группировку, к примеру, 333 и 233 – это Vip, 1XX – это Lost, остальные Regular ( можете ввести боле глубокую сегментацию)
4. Для каждой группы из п. 3 находим кол-во пользователей, кот. попали в них и % товарооборота, которое они сделали на эти 2 года.
5. Проверяем, что общее кол-во пользователей бьется с суммой кол-во пользователей по группам из п. 3 (если у вас есть логические ошибки в создании групп, у вас не собьются цифры). То же самое делаем и по деньгам.

## Решение

### 1. Определяем критерии для каждой буквы R, F, M (т.е. к примеру, R – 3 для клиентов, которые покупали <= 30 дней от последней даты в базе, R – 2 для клиентов, которые покупали > 30 и менее 60 дней от последней даты в базе и т.д.)

```SQL
SELECT
    COUNT(user_id),
    SUM(price),
    MAX(o_date)
INTO
    @source_users_count,
    @source_sum_price,
    @source_max_date
FROM
    orders_20190822;
```

```SQL
DROP TABLE IF EXISTS FrequencySum;

CREATE TABLE FrequencySum AS
SELECT
    user_id,
    DATEDIFF(@source_max_date, MAX(o_date)) AS count_days,
    COUNT(id_o) AS count_orders,
    SUM(price) AS sum_payments
FROM
    orders_20190822
GROUP BY
    user_id;
```

### 2. Для каждого пользователя получаем набор из 3 цифр (от 111 до 333, где 333 – самые классные пользователи)

```SQL
DROP TABLE IF EXISTS RFM;

CREATE TABLE RFM AS
SELECT
    user_id,
    sum_payments,
    CASE WHEN count_days <= 60 THEN 3
         WHEN count_days <= 30 THEN 2
         ELSE 1 END AS R,
    CASE WHEN count_orders <= 1 THEN 1
         WHEN count_orders <= 2 THEN 2
    ELSE 3 END AS F,
    CASE WHEN sum_payments <= 1000 THEN 1
         WHEN sum_payments <= 5000 THEN 2
    ELSE 3 END AS M
FROM
    FrequencySum;
```

### 3. Вводим группировку, к примеру, 333 и 233 – это Vip, 1XX – это Lost, остальные Regular ( можете ввести боле глубокую сегментацию)
    
```SQL
DROP TABLE IF EXISTS RFM_Rating;

CREATE TABLE RFM_Rating AS
SELECT
    user_id,
    sum_payments,
    CASE  WHEN CONCAT(R, F, M) IN ('333', '233') THEN 'Vip'
          WHEN CONCAT(R, F, M) LIKE '1%' THEN 'Lost'
    ELSE 'Regular' END AS Rating
FROM
    RFM;
```

### 4. Для каждой группы из п. 3 находим кол-во пользователей, кот. попали в них и % товарооборота, которое они сделали на эти 2 года.

```SQL
DROP TABLE IF EXISTS RFM_Stat;
CREATE TABLE RFM_Stat AS
SELECT
    Rating,
    SUM(sum_payments) AS `sum_payments`,
    ROUND(SUM(sum_payments) * 100 / @source_sum_price) AS `sum_payments_prc`,
    COUNT(user_id) AS `user_count`
FROM
    RFM_Rating
GROUP BY
    Rating;

SELECT * FROM RFM_Stat;
```

Вывод:

| Rating  | sum_payments       | sum_payments_prc | user_count |
|---------|--------------------|------------------|------------|
| Lost    | 2972151619.1511216 |               65 |     788069 |
| Regular |  504047881.4005098 |               11 |     185719 |
| Vip     | 1066487940.6999832 |               23 |      41331 |

### 5. Проверяем, что общее кол-во пользователей бьется с суммой кол-во пользователей по группам из п. 3 (если у вас есть логические ошибки в создании групп, у вас не собьются цифры). То же самое делаем и по деньгам.

```SQL
SELECT
    CASE WHEN (u = 1) THEN 'Ok' ELSE 'Error' END AS 'Validate users count', 
    CASE WHEN (s < 1) THEN 'Ok' ELSE 'Error' END AS 'Validate sum payments' 
FROM (
    SELECT
        (SUM(user_count) = @source_user_count) AS u, 
        (SUM(sum_payments) = @source_sum_price) AS s 
    FROM
        RFM_Stat
) as t;

```

Вывод:

| Validate users count | Validate sum payments |
|----------------------|-----------------------|
| Ok                   | Ok                    |
