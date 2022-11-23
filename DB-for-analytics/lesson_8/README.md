# Урок 8. Прочие типовые структуры БД

## Задания

ДЗ делаем по бд orders

В качестве ДЗ сделаем карту поведения пользователей. Мы обсуждали, что всех пользователей можно разделить, к примеру, на New (совершили только 1 покупку), Regular (совершили 2 или более на сумму не более стольки-то), Vip (совершили дорогие покупки и достаточно часто), Lost (раньше покупали хотя бы раз и с даты последней покупки прошло больше 3 месяцев). Вся база должна войти в эти гурппы (т.е. каждый пользователь должен попадать только в одну из этих групп).

Задачи:

1. Уточнить критерии групп New,Regular,Vip,Lost
2. По состоянию на 1.01.2017 понимаем, кто попадает в какую группу, подсчитываем кол-во пользователей в каждой.
3. По состоянию на 1.02.2017 понимаем, кто вышел из каждой из групп, а кто вошел.
4. Аналогично смотрим состояние на 1.03.2017, понимаем кто вышел из каждой из групп, а кто вошел.
5. В итоге делаем вывод, какая группа уменьшается, какая увеличивается и продумываем, в чем может быть причина.

## Решение

### Берём запросы из ДЗ №4 и модифицируем, чтобы было компактно.

```SQL
DELIMITER $$
-- Процедура создаёт таблицу RFM статистики за определённый год и месяц.
DROP PROCEDURE IF EXISTS RFM_Stat $$
CREATE PROCEDURE
    RFM_Stat(
        IN month INT, -- месяц для подсчёта статистики
        IN year INT,  -- год для подсчёта статистики
        IN table_result_name VARCHAR(100)  -- название таблицы-результата
    ) 
BEGIN
    DECLARE source_users_count VARCHAR(100);
    DECLARE source_sum_price VARCHAR(100);
    DECLARE source_max_date VARCHAR(100);
    
    -- создаём таблицу-выборку из основной
    DROP TABLE IF EXISTS tmp_table_slice;
    CREATE TABLE tmp_table_slice AS
    SELECT
        *
    FROM
        orders_20190822
    WHERE
        MONTH(o_date) = month
    AND
        YEAR(o_date) = year;
        
        
    -- определяем значение переменных на таблице-срезе
    SELECT
        COUNT(user_id),
        SUM(price),
        MAX(o_date)
    INTO
        @source_users_count,
        @source_sum_price,
        @source_max_date
    FROM
        tmp_table_slice;

        
    -- Определяем критерии для каждой буквы R, F, M (т.е. к примеру, R – 3 для клиентов, которые покупали <= 30 дней от последней даты в базе, R – 2 для клиентов, которые покупали > 30 и менее 60 дней от последней даты в базе и т.д.)
    DROP TABLE IF EXISTS tmp_FrequencySum;
    CREATE TABLE tmp_FrequencySum AS
    SELECT
        user_id,
        DATEDIFF(@source_max_date, MAX(o_date)) AS count_days,
        COUNT(id_o) AS count_orders,
        SUM(price) AS sum_payments
    FROM
        tmp_table_slice
    GROUP BY
        user_id;

        
    -- Для каждого пользователя получаем набор из 3 цифр (от 111 до 333, где 333 – самые классные пользователи)
    DROP TABLE IF EXISTS tmp_RFM;
    CREATE TABLE tmp_RFM AS
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
        tmp_FrequencySum;
        
        
    -- Вводим группировку, к примеру, 333 и 233 – это Vip, 1XX – это Lost, остальные Regular ( можете ввести боле глубокую сегментацию)
    DROP TABLE IF EXISTS tmp_RFM_Rating;
    CREATE TABLE tmp_RFM_Rating AS
    SELECT
        user_id,
        sum_payments,
        CASE  WHEN CONCAT(R, F, M) IN ('333', '233') THEN 'Vip'
            WHEN CONCAT(R, F, M) LIKE '1%' THEN 'Lost'
        ELSE 'Regular' END AS Rating
    FROM
        tmp_RFM;
        
        
    -- Для каждой группы из п. 3 находим кол-во пользователей, кот. попали в них и % товарооборота, которое они сделали на эти 2 года.
    DROP TABLE IF EXISTS tmp_RFM_Stat;
    CREATE TABLE tmp_RFM_Stat AS
    SELECT
        Rating,
        SUM(sum_payments) AS `sum_payments`,
        ROUND(SUM(sum_payments) * 100 / @source_sum_price) AS `sum_payments_prc`,
        COUNT(user_id) AS `user_count`
    FROM
        tmp_RFM_Rating
    GROUP BY
        Rating;
    
    -- удалим таблицу результатов, если уже она есть
    SET @b = concat('DROP TABLE IF EXISTS ', table_result_name);
    PREPARE stmt FROM @b;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;  
    
    -- переименуем таблицу результатов
    SET @b = concat('RENAME TABLE tmp_RFM_Stat TO ', table_result_name);
    PREPARE stmt FROM @b;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;  
    
    -- удаляем временные таблицы
    DROP TABLE IF EXISTS table_slice;
    DROP TABLE IF EXISTS tmp_FrequencySum;
    DROP TABLE IF EXISTS tmp_RFM;
    DROP TABLE IF EXISTS tmp_RFM_Rating;
    DROP TABLE IF EXISTS tmp_RFM_Stat;
END $$


-- Процедура вычисляет изменения между двуя таблицами RFM
DROP PROCEDURE IF EXISTS RFM_Stat_compare $$
CREATE PROCEDURE
    RFM_Stat_compare(
        IN RFM_Stat_1 VARCHAR(100), -- название первой таблицы
        IN RFM_Stat_2 VARCHAR(100) -- название второй таблицы (из её значений вычитается первая)
    ) 
BEGIN
    SET @b = concat('
        SELECT
            t1.Rating AS Rating,
            t2.sum_payments - t1.sum_payments AS sum_payments_changes,
            t2.sum_payments_prc - t1.sum_payments_prc AS sum_payments_prc_changes,
            t2.user_count - t1.user_count AS user_count_changes
        FROM
            ', RFM_Stat_1, ' AS t1
        JOIN
            ', RFM_Stat_2, ' AS t2
        ON
            t1.Rating = t2.Rating
    ');
    PREPARE stmt FROM @b;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;  
END $$

-- Процедура-обёртка для RFM_Stat_calc и RFM_Stat_compare.
DROP PROCEDURE IF EXISTS RFM_Stat_diff $$
CREATE PROCEDURE
    RFM_Stat_diff(
        IN month_start INT, -- месяц для подсчёта начальной статистики
        IN year_start INT,  -- год для подсчёта начальной статистики
        IN month_finish INT, -- месяц для подсчёта начальной статистики
        IN year_finish INT  -- год для подсчёта начальной статистики
    ) 
BEGIN
    CALL RFM_Stat(month_start, year_start, 'tmp_RFM_Stat_diff_1');
    CALL RFM_Stat(month_finish, year_finish, 'tmp_RFM_Stat_diff_2');
    CALL RFM_Stat_compare('tmp_RFM_Stat_diff_1', 'tmp_RFM_Stat_diff_2');
    DROP TABLE IF EXISTS tmp_RFM_Stat_diff_1;
    DROP TABLE IF EXISTS tmp_RFM_Stat_diff_2;
END $$
DELIMITER ;


CALL RFM_Stat_diff(1, 2017, 2, 2017);
```

Вывод:

| Rating  | sum_payments_changes | sum_payments_prc_changes | user_count_changes |
|---------|----------------------|--------------------------|--------------------|
| Regular |  -11483934.700009197 |                        1 |              -3141 |
| Vip     |   -4089799.000000041 |                       -1 |               -359 |

```SQL
CALL RFM_Stat_diff(2, 2017, 3, 2017);
```

Вывод:

| Rating  | sum_payments_changes | sum_payments_prc_changes | user_count_changes |
|---------|----------------------|--------------------------|--------------------|
| Regular |    38630391.10002512 |                       -3 |              12076 |
| Vip     |   14541258.900000043 |                        3 |                921 |
