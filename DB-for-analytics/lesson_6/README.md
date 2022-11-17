# Урок 6. Хранилища данных для анализа

## Задание 1

Создать структуру БД турфирмы (можно в экселе, как я показываю на занятиях).
Что должно содержаться: кто куда летит, когда, какая оплата, может лететь группа, могут быть пересадки на рейсах, какая страна или страны, какие города и отели, звездность отеля, тип питания и комнат, данные о пассажирах, необходимость виз, ограничения, цель поездки, канал привлечения пользователя, бонусы и промокода и т.д.

## Задание 2

По кратинке из матриеалов напистаь запрос "Найти пользователей, у которых был хотя бы один заказ, весом больше 10 кг"

## Решение 1
 
Готовим таблицы:

```SQL

DROP TABLE IF EXISTS clients; -- клиенты турфирмы
CREATE TABLE clients ( 
    id SERIAL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    phone CHAR(11) NOT NULL,
    email VARCHAR(120)
);

DROP TABLE IF EXISTS order; -- заказы туров от клиентов
CREATE TABLE order ( 
    id SERIAL,
    client_id BIGINT UNSIGNED,
    tour_id BIGINT UNSIGNED,
    activity VARCHAR(50), -- цель поездки 
    ad_chennel VARCHAR(50), -- канал привлечения пользователя
    ad_bonus VARCHAR(50), -- использованный бонус пользователя
    ad_promocode VARCHAR(50), -- использованный промокод 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    
    FOREIGN KEY (client_id) REFERENCES users (id), 
    FOREIGN KEY (tour_id) REFERENCES tours (id)
);

DROP TABLE IF EXISTS tours; -- все возможные туры
CREATE TABLE tours ( 
    id SERIAL,
    name VARCHAR(50) NOT NULL, -- название тура
    visa BOOLEAN DEFAULT FALSE, -- нужна ли виза
    start_at DATETIME,
    finish_at DATETIME
);

DROP TABLE IF EXISTS flights; -- авиа полёты до места тура
CREATE TABLE flights ( -- полётовможет быть несколько за один тур!
    id SERIAL,
    tour_id BIGINT UNSIGNED,
    client_id BIGINT UNSIGNED,
    
    -- из какого в какой город
    city_id_from BIGINT UNSIGNED,
    city_id_to BIGINT UNSIGNED,
    
    -- дата и время отправления/посадки рейса
    start_at DATETIME,
    finish_at DATETIME, 
    
    FOREIGN KEY (city_id_from) REFERENCES city (id), 
    FOREIGN KEY (city_id_to) REFERENCES city (id), 
    FOREIGN KEY (client_id) REFERENCES users (id), 
    FOREIGN KEY (tour_id) REFERENCES tours (id)
);

DROP TABLE IF EXISTS city; -- города
CREATE TABLE city ( 
    id SERIAL,
    country_id BIGINT UNSIGNED,
    name VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (country_id) REFERENCES country (id)
);

DROP TABLE IF EXISTS country; -- страны
CREATE TABLE country ( 
    id SERIAL,
    name VARCHAR(50) NOT NULL
);

```

## Решение 2

По кратинке из матриалов напистаь запрос "Найти пользователей, у которых был хотя бы один заказ, весом больше 10 кг"

```SQL
SELECT
    DISTINCT(user_id),
FROM
    orders
WHERE
    id_o in (
        SELECT
            t.id_prod,
            sum(t.w_str)
        FROM (
            SELECT
                b.*,
                b.quantity * p.value AS w_str 
            FROM
                orders o
            JOIN
                basket b ON o.id_o = b.id_o
            JOIN
                props p ON p.id_prod = b.id_o
            WHERE
                p.id_prop = 1
        ) t
        GROUP BY t.id_prod
        HAVING sum(t.w_str)> 10 * 1000
    )
GROUP BY
    user_id
HAVING
    COUNT(id_o) >= 1;
```
