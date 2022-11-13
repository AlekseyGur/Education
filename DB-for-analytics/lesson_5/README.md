# Урок 5. Системы web-аналитики

## Задания

Даны 2 таблицы:
Таблица клиентов clients, в которой находятся данные по карточному лимиту каждого клиента

clients
id_client (primary key) number,
limit_sum number

transactions
id_transaction (primary key) number,
id_client (foreign key) number,
transaction_date number,
transaction_time number,
transaction_sum number

Написать текст SQL-запроса, выводящего количество транзакций, сумму транзакций, среднюю сумму транзакции и дату и время первой транзакции для каждого клиента

Найти id пользователей, кот использовали более 70% карточного лимита

## Решение
 
Готовим две таблицы:

```SQL

DROP TABLE IF EXISTS clients;

CREATE TABLE clients ( 
    id_client (primary key) number,
    limit_sum number
);

DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions ( 
    id_transaction (primary key) number,
    id_client (foreign key) number,
    transaction_date number,
    transaction_time number,
    transaction_sum number
);
```

### 1. Написать текст SQL-запроса, выводящего количество транзакций, сумму транзакций, среднюю сумму транзакции и дату и время первой транзакции для каждого клиента

```SQL
SELECT
    COUNT(transaction_sum),
    SUM(transaction_sum),
    AVG(transaction_sum),
    MIN(transaction_date)
FROM
    transactions
GROUP BY
    id_client;
```

### 2. Найти id пользователей, кот использовали более 70% карточного лимита

    
```SQL
SELECT
    id_client
FROM (
    SELECT
        cl.id_client as id_client,
        cl.limit_sum AS limit_sum,
        SUM(tr.transaction_sum) AS tr_sum
    FROM
        transactions AS tr 
    INNER JOIN
        clients AS cl
    GROUP BY
        id_client)
WHERE
    tr_sum > limit_sum*0.7;
```
