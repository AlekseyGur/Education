/* 
Практическое задание по теме “Транзакции, переменные, представления” 
*/

-- В базе данных shop и sample присутствуют одни и те же таблицы, учебной базы данных. Переместите запись id = 1 из таблицы shop.users в таблицу sample.users. Используйте транзакции.

   START TRANSACTION;
      
      -- записываем в переменные
      SELECT
         @name := name, @birthday_at := birthday_at
      FROM
         shop.users
      WHERE
         id = 1;
         
      -- вставляем значения
      INSERT INTO
         sample.users (name, birthday_at)
      VALUES
         (@name, @birthday_at);

      -- удаляем старые значения
      DELETE FROM
         shop.users
      WHERE
         id = 1
      LIMIT 1;

   COMMIT;


-- Создайте представление, которое выводит название name товарной позиции из таблицы products и соответствующее название каталога name из таблицы catalogs.

   CREATE OR REPLACE VIEW view_products_catalogs AS
   SELECT
      products.name AS 'product',
      catalogs.name AS 'catalog'
   FROM
      products
   JOIN
      catalogs
   ON
      products.catalog_id = catalogs.id;


-- Пусть имеется таблица с календарным полем created_at. В ней размещены разряженые календарные записи за август 2018 года '2018-08-01', '2016-08-04', '2018-08-16' и 2018-08-17. Составьте запрос, который выводит полный список дат за август, выставляя в соседнем поле значение 1, если дата присутствует в исходном таблице и 0, если она отсутствует.

   -- создаём таблицу и заполняем тестовыми значениями
      DROP TABLE IF EXISTS dates;
      CREATE TABLE dates ( created_at DATE );
      INSERT INTO dates (created_at) VALUES ('2018-08-01'), ('2016-08-04'), ('2018-08-16'), ('2018-08-17');
      
   -- выборка
      SELECT @created := created_at, IF( (SELECT * FROM dates WHERE created_at = @created), 1, 0) FROM dates WHERE created_at LIKE '2018-08%';

      
-- Пусть имеется любая таблица с календарным полем created_at. Создайте запрос, который удаляет устаревшие записи из таблицы, оставляя только 5 самых свежих записей.
   -- создаём таблицу и заполняем тестовыми значениями
      DROP TABLE IF EXISTS dates;
      CREATE TABLE dates ( created_at DATE );
      INSERT INTO dates (created_at) VALUES 
         ( NOW() ),
         ( NOW() - INTERVAL 7 DAY),
         ( NOW() - INTERVAL 21 DAY ),
         ( NOW() - INTERVAL 28 DAY ),
         ( NOW() - INTERVAL 35 DAY ),
         ( NOW() - INTERVAL 42 DAY),
         ( NOW() - INTERVAL 49 DAY ),
         ( NOW() - INTERVAL 56 DAY ),
         ( NOW() - INTERVAL 63 DAY );
      
   -- удаляем данные через переменные / транзакции, потому что так надо по теме
      START TRANSACTION;
         
         SET @lastRowNotToDelete := 0; -- последняя дата, после которой можно удалять
         
         SELECT
            @lastRowNotToDelete := created_at
         FROM
            dates
         ORDER BY
            created_at DESC
         LIMIT 5;
         
         SELECT @lastRowNotToDelete;
         
         DELETE FROM
            dates
         WHERE
            created_at < NOW() - INTERVAL 10 DAY
         AND
            created_at < @lastRowNotToDelete
         ORDER BY
            created_at DESC;

      COMMIT;

/* 
Практическое задание по теме “Администрирование MySQL” 
*/

-- Создайте двух пользователей которые имеют доступ к базе данных shop. Первому пользователю shop_read должны быть доступны только запросы на чтение данных, второму пользователю shop — любые операции в пределах базы данных shop.

   CREATE USER 'shop_read'@'localhost';
   GRANT SELECT ON shop.* TO 'shop_read'@'localhost';

   CREATE USER 'shop'@'localhost';
   GRANT ALL PRIVILEGES ON shop.* TO 'shop'@'localhost';


-- Пусть имеется таблица accounts содержащая три столбца id, name, password, содержащие первичный ключ, имя пользователя и его пароль. Создайте представление username таблицы accounts, предоставляющий доступ к столбца id и name. Создайте пользователя user_read, который бы не имел доступа к таблице accounts, однако, мог бы извлекать записи из представления username.

   -- создаём представление
      CREATE OR REPLACE VIEW view_accounts AS
      SELECT
         id, name
      FROM
         accounts;
   
   -- даём пользователю username разрешение на чтение представления
      REVOKE ALL PRIVILEGES ON shop.view_accounts FROM 'username'@'localhost';
   
   -- удаляем разрешение username на чтение исходной таблицы
      GRANT SELECT ON shop.accounts TO 'username'@'localhost';
   

/* 
Практическое задание по теме “Хранимые процедуры и функции, триггеры” 
*/

-- Создайте хранимую функцию hello(), которая будет возвращать приветствие, в зависимости от текущего времени суток. С 6:00 до 12:00 функция должна возвращать фразу "Доброе утро", с 12:00 до 18:00 функция должна возвращать фразу "Добрый день", с 18:00 до 00:00 — "Добрый вечер", с 00:00 до 6:00 — "Доброй ночи".
   DELIMITER //
   DROP FUNCTION IF EXISTS hello//
   CREATE FUNCTION hello ()
   RETURNS TEXT DETERMINISTIC
   BEGIN
      SET @hour := HOUR( NOW() );
      IF( 6 <= @hour and @hour < 12 ) THEN -- С 6:00 до 12:00
         RETURN 'Доброе утро';
      ELSEIF ( 12 <= @hour and @hour < 18 ) THEN -- 12:00 до 18:00
         RETURN 'Добрый день';
      ELSEIF ( 18 <= @hour and @hour <= 23 ) THEN -- 18:00 до 00:00
         RETURN 'Добрый вечер';
      ELSE -- 00:00 до 6:00
         RETURN 'Доброй ночи';
      END IF;
   END//
   DELIMITER ;
   SELECT hello();

   
--  В таблице products есть два текстовых поля: name с названием товара и description с его описанием. Допустимо присутствие обоих полей или одно из них. Ситуация, когда оба поля принимают неопределенное значение NULL неприемлема. Используя триггеры, добейтесь того, чтобы одно из этих полей или оба поля были заполнены. При попытке присвоить полям NULL-значение необходимо отменить операцию.

   -- триггер для UPDATE
      DELIMITER //
      DROP TRIGGER IF EXISTS check_products_update//
      CREATE TRIGGER check_products_update BEFORE UPDATE ON products
      FOR EACH ROW BEGIN
         IF (NEW.name IS NULL) AND (NEW.description IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Null values!';
         ELSEIF (NEW.name IS NULL) THEN
            SET NEW.name = OLD.name; -- оставляем старое значение
         ELSEIF (NEW.description IS NULL) THEN
            SET NEW.description = OLD.description; -- оставляем старое значение
         END IF;
      END//
      DELIMITER ;
      
   -- триггер для INSERT
      DELIMITER //
      DROP TRIGGER IF EXISTS check_products_insert//
      CREATE TRIGGER check_products_insert BEFORE INSERT ON products
      FOR EACH ROW BEGIN
         IF (NEW.name IS NULL) AND (NEW.description IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Null values!';
         ELSEIF (NEW.name IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'name can`t be Null!';
         ELSEIF (NEW.description IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'description can`t be Null!';
         END IF;
      END//
      DELIMITER ;
      
   -- проверка
      INSERT INTO products (name, description) VALUES ('Intel Core i3-8100', Null);
      INSERT INTO products (name, description) VALUES (Null, 'Процессор для компьютеров');
      INSERT INTO products (name, description) VALUES (Null, Null);
      
      UPDATE products SET name = NULL WHERE id = 1;
      UPDATE products SET description = NULL WHERE id = 1;
      UPDATE products SET name = NULL, description = NULL WHERE id = 1;
      

-- Напишите хранимую функцию для вычисления произвольного числа Фибоначчи. Числами Фибоначчи называется последовательность в которой число равно сумме двух предыдущих чисел. Вызов функции FIBONACCI(10) должен возвращать число 55

   DELIMITER //
   DROP FUNCTION IF EXISTS FIBONACCI//
   CREATE FUNCTION FIBONACCI (num INT)
   RETURNS INT DETERMINISTIC
   BEGIN
      DECLARE i INT DEFAULT 0;
      DECLARE n1 INT DEFAULT 1;
      DECLARE n2 INT DEFAULT 1;
      DECLARE n3 INT DEFAULT 1;
      
      WHILE i < num - 2 DO
         SET n3 := n1 + n2;
         SET n1 := n2;
         SET n2 := n3;
         
         SET i = i + 1;
      END WHILE;
      
      RETURN n3;
      
   END//
   DELIMITER ;
   
   -- проверка: 
      SELECT FIBONACCI(1) AS '1', 
         FIBONACCI(2) AS '2',
         FIBONACCI(3) AS '3',
         FIBONACCI(4) AS '4',
         FIBONACCI(5) AS '5',
         FIBONACCI(6) AS '6',
         FIBONACCI(7) AS '7',
         FIBONACCI(8) AS '8',
         FIBONACCI(9) AS '9',
         FIBONACCI(10) AS '10';
      -- результат: 
         /*
         +------+------+------+------+------+------+------+------+------+------+
         | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   |
         +------+------+------+------+------+------+------+------+------+------+
         |    1 |    1 |    2 |    3 |    5 |    8 |   13 |   21 |   34 |   55 |
         +------+------+------+------+------+------+------+------+------+------+
         */
