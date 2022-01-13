/*
Практическое задание по теме “Оптимизация запросов”

1. Создайте таблицу logs типа Archive. Пусть при каждом создании записи в таблицах users,
catalogs и products в таблицу logs помещается время и дата создания записи, название
таблицы, идентификатор первичного ключа и содержимое поля name.
*/

   CREATE TABLE logs(
      id BIGINT UNSIGNED,
      `table` VARCHAR(50) NOT NULL,
      `name` VARCHAR(50) NOT NULL,
      `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
   ) ENGINE=Archive CHARACTER SET utf8;


   DELIMITER //
   -- триггер для INSERT users
      DROP TRIGGER IF EXISTS archive_users_insert//
      CREATE TRIGGER archive_users_insert BEFORE INSERT ON users
      FOR EACH ROW BEGIN
         INSERT INTO logs (`id`, `table`, `name`) VALUES (NEW.id, 'users', NEW.name);
      END//

   -- триггер для INSERT catalogs
      DROP TRIGGER IF EXISTS archive_catalogs_insert//
      CREATE TRIGGER archive_catalogs_insert BEFORE INSERT ON catalogs
      FOR EACH ROW BEGIN
         INSERT INTO logs (`id`, `table`, `name`) VALUES (NEW.id, 'catalogs', NEW.name);
      END//

   -- триггер для INSERT products
      DROP TRIGGER IF EXISTS archive_products_insert//
      CREATE TRIGGER archive_products_insert BEFORE INSERT ON products
      FOR EACH ROW BEGIN
         INSERT INTO logs (`id`, `table`, `name`) VALUES (NEW.id, 'products', NEW.name);
      END//
   DELIMITER ;


/*
2. (по желанию) Создайте SQL-запрос, который помещает в таблицу users миллион записей.
*/

   DELIMITER //
   DROP PROCEDURE IF EXISTS add_1_mln_logs//
   CREATE PROCEDURE add_1_mln_logs ()
   BEGIN
      DECLARE counter INT DEFAULT 1;

      WHILE counter <= 1000000 DO
         INSERT INTO logs (`id`, `table`, `name`) VALUES (5, 'any', 'name');
         SET counter = counter + 1;
      END WHILE;
   END//
   DELIMITER ;
   
   -- вызов 
   CALL add_1_mln_logs();
   
   -- проверка поличества 
   SELECT COUNT(*) FROM logs;
   

/*
## Практическое задание по теме “NoSQL”

1. В базе данных Redis подберите коллекцию для подсчета посещений с определенных IP-адресов.
*/

   -- создаём множество (ip - дата посещения)
      SADD 192.168.1.1 '2022-01-11'
      SADD 192.168.1.1 '2022-01-12'
      SADD 192.168.1.1 '2022-01-13'
      
   -- считаем кол-во элементов для определённого ip
      SCARD 192.168.1.1

/*
2. При помощи базы данных Redis решите задачу поиска имени пользователя по электронному адресу и наоборот, поиск электронного адреса пользователя по его имени.
*/

   -- Redis не умеет делать поиск ключа по значению. Поэтому придётся делать две базы для "имя - мэйл" и "мэйл - имя".
   
   -- в первой базе храним значения "имя - мэйл"
      SELECT 0
      
      -- добавляем данные
         SET 'Alex' 'alex@mail.ru'

      -- читаем данные (вернёт мэйл)
         GET 'Alex'
      
   -- во второй базе храним значения "мэйл - имя"
      SELECT 1
      
      -- добавляем данные
         SET 'alex@mail.ru' 'Alex' 

      -- читаем данные (вернёт мэйл)
         GET 'alex@mail.ru'
      
      
/*
3. Организуйте хранение категорий и товарных позиций учебной базы данных shop в СУБД MongoDB.
*/

   db.runCommand(
      {
         insert: "shop",
         documents: [
            {
               name: "Процессоры",
               items: [
                  {
                     name: 'Intel Core i3-8100',
                     description: 'Процессор для настольных персональных компьютеров, основанных на платформе Intel.',
                     price: 7890
                  },
                  {
                     name: 'Intel Core i5-7400',
                     description: 'Процессор для настольных персональных компьютеров, основанных на платформе Intel.',
                     price: 12700
                  },
                  {
                     name: 'AMD FX-8320E',
                     description: 'Процессор для настольных персональных компьютеров, основанных на платформе AMD.',
                     price: 4780
                  }
               ]
            },
            {
               name: "Материнские платы",
               items: [
                  {
                     name: 'ASUS ROG MAXIMUS X HERO',
                     description: 'Материнская плата ASUS ROG MAXIMUS X HERO, Z370, Socket 1151-V2, DDR4, ATX',
                     price: 19310
                  },
                  {
                     name: 'Gigabyte H310M S2H',
                     description: 'Материнская плата Gigabyte H310M S2H, H310, Socket 1151-V2, DDR4, mATX',
                     price: 4790
                  }
               ]
            },
            { name: "Видеокарты" },
            { name: "Жесткие диски" },
            { name: "Оперативная память" },
         ]
      }
   )
