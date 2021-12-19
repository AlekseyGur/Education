/* 
Практическое задание по теме “Сложные запросы” 
*/

-- Составьте список пользователей users, которые осуществили хотя бы один заказ orders в интернет магазине.
   -- Сначала добавляем тестовые данные:
      INSERT INTO orders (user_id) VALUES (1);
      INSERT INTO orders (user_id) VALUES (2);
      INSERT INTO orders (user_id) VALUES (2); 
      /*
         orders:
         +----+---------+
         | id | user_id |
         +----+---------+
         |  1 |       1 |
         |  2 |       2 |
         |  3 |       2 |
         +----+---------+
      */
   
   -- делаем выборку:
      SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
      /*
         +----+------------------+
         | id | name             |
         +----+------------------+
         |  1 | Геннадий         |
         |  2 | Наталья          |
         +----+------------------+
      */



-- Выведите список товаров products и разделов catalogs, который соответствует товару.
   SELECT products.name, catalogs.name FROM products LEFT JOIN catalogs ON products.catalog_id = catalogs.id;
   /*
      +-------------------------+-----------------------------------+
      | name                    | name                              |
      +-------------------------+-----------------------------------+
      | Intel Core i3-8100      | Процессоры                        |
      | Intel Core i5-7400      | Процессоры                        |
      | AMD FX-8320E            | Процессоры                        |
      | AMD FX-8320             | Процессоры                        |
      | ASUS ROG MAXIMUS X HERO | Материнские платы                 |
      | Gigabyte H310M S2H      | Материнские платы                 |
      | MSI B250M GAMING PRO    | Материнские платы                 |
      +-------------------------+-----------------------------------+
   */



-- (по желанию) Пусть имеется таблица рейсов flights (id, from, to) и таблица городов cities (label, name). Поля from, to и label содержат английские названия городов, поле name — русское. Выведите список рейсов flights с русскими названиями городов.
   -- Сначала создадим таблицы и добавляем тестовые данные:
      DROP TABLE IF EXISTS flights;
      CREATE TABLE flights (
         id SERIAL PRIMARY KEY,
         flight_to VARCHAR(50),
         flight_from VARCHAR(50)
      );
      
      DROP TABLE IF EXISTS cities;
      CREATE TABLE cities (
         label VARCHAR(255) PRIMARY KEY,
         name VARCHAR(255)
      );
      
      INSERT INTO flights (flight_from, flight_to) VALUES ('moscow', 'omsk');
      INSERT INTO flights (flight_from, flight_to) VALUES ('novgorod', 'kazan');
      INSERT INTO flights (flight_from, flight_to) VALUES ('irkutsk', 'moscow');
      INSERT INTO flights (flight_from, flight_to) VALUES ('omsk', 'irkutsk');
      INSERT INTO flights (flight_from, flight_to) VALUES ('moscow', 'kazan');
      INSERT INTO cities (label, name) VALUES ('moscow', 'Москва');
      INSERT INTO cities (label, name) VALUES ('irkutsk', 'Иркутск');
      INSERT INTO cities (label, name) VALUES ('novgorod', 'Новгород');
      INSERT INTO cities (label, name) VALUES ('kazan', 'Казань');
      INSERT INTO cities (label, name) VALUES ('omsk', 'Омск');
      /*
         flights:
         +----+-----------+-------------+
         | id | flight_to | flight_from |
         +----+-----------+-------------+
         |  1 | omsk      | moscow      |
         |  2 | kazan     | novgorod    |
         |  3 | moscow    | irkutsk     |
         |  4 | irkutsk   | omsk        |
         |  5 | kazan     | moscow      |
         +----+-----------+-------------+
         
         cities:
         +----------+------------------+
         | label    | name             |
         +----------+------------------+
         | irkutsk  | Иркутск          |
         | kazan    | Казань           |
         | moscow   | Москва           |
         | novgorod | Новгород         |
         | omsk     | Омск             |
         +----------+------------------+
      */

   -- делаем выборку:
      SELECT
         id,
         (SELECT name FROM cities WHERE label = flight_from) AS 'from',
         (SELECT name FROM cities WHERE label = flight_to) AS 'to'
      FROM flights;
      
      -- Результат:
      /*
         +----+------------------+----------------+
         | id | from             | to             |
         +----+------------------+----------------+
         |  1 | Москва           | Омск           |
         |  2 | Новгород         | Казань         |
         |  3 | Иркутск          | Москва         |
         |  4 | Омск             | Иркутск        |
         |  5 | Москва           | Казань         |
         +----+------------------+----------------+
      */
