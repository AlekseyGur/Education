-- Социальная сеть

/*
+-------------------+--------------------------------+
| Таблицы           | Описание                       |
+-------------------+--------------------------------+
| users             | пользователи                   |
| post              | публикации (+репосты)          |
| likes             | лайки к постам                 |
| poll              | опросы в публикациях           |
| poll_answer       | ответы пользователей на опросы |
| profiles          | профили пользователей          |
| messages          | приватные сообщения            |
| communities       | группы                         |
| communities_users | подписчики групп               |
| friend_requests   | запрос на добавление в друзья  |
| media             | данные файлов                  |
| media_types       | типы файлов                    |
+-------------------+--------------------------------+
*/


/* создание таблиц */

   -- удаляем таблицы, если существовали ранее
   DROP TABLE IF EXISTS users, post, poll, poll_answer, profiles, messages, likes, communities, communities_users, friend_requests, media, media_types;

   -- данные пользователей
   CREATE TABLE users(
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      firstname VARCHAR(50) NOT NULL,
      lastname VARCHAR(50) NOT NULL,
      phone CHAR(11) NOT NULL,
      email VARCHAR(120) UNIQUE,
      password_hash CHAR(65),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      INDEX (lastname),
      INDEX (phone)
   );

   -- дополнительные данные профилей
   CREATE TABLE profiles(
      user_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
      gender ENUM('f', 'm', 'x') NOT NULL,
      birthday DATE NOT NULL,
      photo_id BIGINT UNSIGNED NOT NULL,
      city VARCHAR(130),
      country VARCHAR(130),
      FOREIGN KEY (user_id) REFERENCES users (id)
   );

   -- приватные сообщения
   CREATE TABLE messages (
      id SERIAL PRIMARY KEY, -- BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE
      from_user_id BIGINT UNSIGNED NOT NULL,
      to_user_id BIGINT UNSIGNED NOT NULL,
      body TEXT,
      created_at DATETIME DEFAULT NOW(),
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      is_delivered BOOLEAN DEFAULT FALSE,
      FOREIGN KEY (from_user_id) REFERENCES users (id),
      FOREIGN KEY (to_user_id) REFERENCES users (id)
   );

   -- запросы в друзья
   CREATE TABLE friend_requests(
      from_user_id BIGINT UNSIGNED NOT NULL,
      to_user_id BIGINT UNSIGNED NOT NULL,
      accepted BOOL DEFAULT FALSE,
      PRIMARY KEY(from_user_id, to_user_id),
      FOREIGN KEY (from_user_id) REFERENCES users (id),
      FOREIGN KEY (to_user_id) REFERENCES users (id)
   );

   -- группы
   CREATE TABLE communities(
      id SERIAL,
      name VARCHAR(145) NOT NULL,
      description VARCHAR(255),
      admin_id BIGINT UNSIGNED NOT NULL,
      PRIMARY KEY(id),
      INDEX communities_name_idx (name),
      CONSTRAINT fk_communities_admin_id FOREIGN KEY (admin_id) REFERENCES users (id)
   );

   -- подписчики в группах
   CREATE TABLE communities_users(
      community_id BIGINT UNSIGNED NOT NULL,
      user_id BIGINT UNSIGNED NOT NULL,
      PRIMARY KEY(community_id, user_id),
      FOREIGN KEY (community_id) REFERENCES communities (id),
      FOREIGN KEY (user_id) REFERENCES users (id)
   );

   -- типы медиа контента
   CREATE TABLE media_types(
      id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(45) NOT NULL UNIQUE
   );

   -- данные медиа файлов
   CREATE TABLE media (
      id SERIAL PRIMARY KEY,
      user_id BIGINT UNSIGNED NOT NULL,
      media_types_id INT UNSIGNED NOT NULL,
      file_name VARCHAR(255),
      file_size BIGINT UNSIGNED,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (media_types_id) REFERENCES media_types (id)
   ); 

   -- публикации в группах (+репосты)
   CREATE TABLE post (
      id SERIAL PRIMARY KEY,
      post_id BIGINT UNSIGNED, -- id поста (для функции репоста). NULL = это не репост
      user_id BIGINT UNSIGNED NOT NULL, -- id автора добавляемого поста
      poll_id BIGINT UNSIGNED, -- id голосования
      community_id BIGINT UNSIGNED, -- id группы. NULL = публикация в своём профиле
      media_id BIGINT UNSIGNED, -- прикреплённый файл
      text VARCHAR(280) NOT NULL, -- текст публикации (как в twitter)
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- время создания. Обновлять нельзя, только создавать (как в twitter)
      FOREIGN KEY (post_id) REFERENCES post (id),
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (poll_id) REFERENCES post (id),
      FOREIGN KEY (community_id) REFERENCES communities (id),
      FOREIGN KEY (media_id) REFERENCES media (id)
   );

   -- опросы в публикациях (содержимое вопросов)
   CREATE TABLE poll (
      id SERIAL PRIMARY KEY,
      post_id BIGINT UNSIGNED, -- id поста
      text VARCHAR(280) NOT NULL, -- текст вопроса на голосовании
      answers JSON NOT NULL, -- данные для опроса (варианты ответов). Не будем выносить в отдельную таблицу. Они не будут изменяться после создания (посты нельзя редактировать). Сохранение результата по порядковым номерам элементов (начиная с 0)
      FOREIGN KEY (post_id) REFERENCES post (id)
   );

   -- ответы пользователей на опросы
   CREATE TABLE poll_answer (
      id SERIAL,
      user_id BIGINT UNSIGNED NOT NULL, -- id голосовавшего
      poll_id BIGINT UNSIGNED NOT NULL, -- id опроса
      answer_id INT UNSIGNED NOT NULL, -- порядковый номер ответа
      PRIMARY KEY(user_id, poll_id), -- голосовать можно только один раз
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (poll_id) REFERENCES poll (id)
   );

   -- лайки к постам
   CREATE TABLE likes (
      user_id BIGINT UNSIGNED NOT NULL, -- id автора лайка
      post_id BIGINT UNSIGNED NOT NULL, -- id публикации
      PRIMARY KEY(user_id, post_id), -- поставить можно только один раз
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (post_id) REFERENCES post (id)
   );


/* триггеры */
         
   -- нельзя ставить лайк на свои публикации
         
      -- триггер для INSERT
         DELIMITER //
         DROP TRIGGER IF EXISTS check_likes_insert//
         CREATE TRIGGER check_likes_insert BEFORE INSERT ON likes
         FOR EACH ROW BEGIN
            DECLARE isSelfLike BOOL DEFAULT 0;
            SELECT if(id, 1, 0) INTO isSelfLike FROM post WHERE id = NEW.post_id AND user_id = NEW.user_id LIMIT 1;
            IF (isSelfLike) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You can`t like your own posts!';
            END IF;
         END//
         DELIMITER ;

   -- у пользователя должно быть имя и фамилия

      -- триггер для UPDATE
         DELIMITER //
         DROP TRIGGER IF EXISTS check_firstname_lastname_update//
         CREATE TRIGGER check_firstname_lastname_update BEFORE UPDATE ON users
         FOR EACH ROW BEGIN
            IF (NEW.firstname IS NULL) AND (NEW.lastname IS NULL) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Name can not be empty!';
            ELSEIF (NEW.firstname IS NULL) THEN
               SET NEW.firstname = OLD.firstname; -- оставляем старое значение
            ELSEIF (NEW.lastname IS NULL) THEN
               SET NEW.lastname = OLD.lastname; -- оставляем старое значение
            END IF;
         END//
         DELIMITER ;
         
      -- триггер для INSERT
         DELIMITER //
         DROP TRIGGER IF EXISTS check_firstname_lastname_insert//
         CREATE TRIGGER check_firstname_lastname_insert BEFORE INSERT ON users
         FOR EACH ROW BEGIN
            IF (NEW.firstname IS NULL) AND (NEW.lastname IS NULL) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'empty values!';
            ELSEIF (NEW.firstname IS NULL) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'firstname can`t be empty!';
            ELSEIF (NEW.lastname IS NULL) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'lastname can`t be empty!';
            END IF;
         END//
         DELIMITER ;
         
         
   -- у публикации должен быть хоть какой-то текст

      -- триггер для UPDATE
         DELIMITER //
         DROP TRIGGER IF EXISTS check_post_update//
         CREATE TRIGGER check_post_update BEFORE UPDATE ON post
         FOR EACH ROW BEGIN
            IF (NEW.text IS NULL) THEN
               SET NEW.text = OLD.text; -- оставляем старое значение
            END IF;
         END//
         DELIMITER ;
         
      -- триггер для INSERT
         DELIMITER //
         DROP TRIGGER IF EXISTS check_post_insert//
         CREATE TRIGGER check_post_insert BEFORE INSERT ON post
         FOR EACH ROW BEGIN
            IF (NEW.text IS NULL) THEN
               SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'text field can`t be empty!';
            END IF;
         END//
         DELIMITER ;

/* заполнение таблиц тестовыми данными (по 10 записей в каждой таблице) */

   -- очистка всех тестовых данных
   SET FOREIGN_KEY_CHECKS = 0;
   TRUNCATE TABLE communities_users;
   TRUNCATE TABLE communities;
   TRUNCATE TABLE friend_requests;
   TRUNCATE TABLE likes;
   TRUNCATE TABLE media;
   TRUNCATE TABLE media_types;
   TRUNCATE TABLE messages;
   TRUNCATE TABLE poll;
   TRUNCATE TABLE poll_answer;
   TRUNCATE TABLE post;
   TRUNCATE TABLE profiles;
   TRUNCATE TABLE users;
   SET FOREIGN_KEY_CHECKS = 1;

   -- пользователи
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Vasya', 'Vasilkov', 'vasya@mail.com', '81dc9bdb52d04d8313ed051c20036dbd', '99999999901');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Masha', 'Ivanova', 'masha@mail.com', 'dbd8313ed05281d04dc20036c9bdb52d', '99999999902');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Misha', 'Petrov', 'misha@mail.com', '04dc20036d81dc13ed0539bdb52dbd83', '99999999903');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Max',   'Sidorov', 'mas@mail.com', '81dc9bdb52d04dc13ed05420036dbd83', '99999999904');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Kate',  'Kuznetsov', 'kate@mail.com', 'd8313ed05581dc9b2d04dc20db036db5', '99999999905');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Paul',  'Kotov', 'paul@mail.com', 'd04dc2081dc9bdd056036db52bd8313e', '99999999906');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Alex',  'Alekseev', 'alex@mail.com', 'dc20036db81d8313ed057dc9bdb52d04', '99999999907');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Sergey', 'Borisov', 'sergey@mail.com', 'b52d04dc81313ed058dc9bd20036dbd8', '99999999908');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Stepan','Lomov', 'stepan@mail.com', '52d04dc2003813ed059dc9bdb6dbd831', '99999999909');
   INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Peter', 'Stepanov', 'peter@mail.com', 'd8313ed01bdb6db052d81dc904dc2003', '99999999910');

   -- профили пользователей
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (1, 'm', '1988-11-01', 2, 'Moscow', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (2, 'f', '1988-11-02', 2, 'Magadan', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (3, 'm', '1988-11-03', 2, 'St.Peter', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (4, 'm', '1988-11-04', 2, 'Sochi', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (5, 'f', '1988-11-05', 2, 'Novgorod', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (6, 'm', '1988-11-06', 2, 'Rostov', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (7, 'm', '1988-11-07', 2, 'Novosibirsk', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (8, 'm', '1988-11-08', 2, 'Saransk', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (9, 'm', '1988-11-09', 2, 'Archangelsk', 'Russia');
   INSERT INTO profiles (user_id, gender, birthday, photo_id, city, country) VALUES (10, 'm', '1988-11-10', 2, 'Volgograd', 'Russia');

   -- сообщества
   INSERT INTO communities (name, description, admin_id) VALUES ("Vasya's group!", 'Vasya made that group', 1);
   INSERT INTO communities (name, description, admin_id) VALUES ("Masha's group!", 'Masha made that group', 2);
   INSERT INTO communities (name, description, admin_id) VALUES ("Misha's group!", 'Misha made that group', 3);
   INSERT INTO communities (name, description, admin_id) VALUES ("Max's group!", 'Max made that group', 4);
   INSERT INTO communities (name, description, admin_id) VALUES ("Kate's group!", 'Kate made that group', 5);
   INSERT INTO communities (name, description, admin_id) VALUES ("Paul's group!", 'Paul made that group', 6);
   INSERT INTO communities (name, description, admin_id) VALUES ("Alex's group!", 'Alex made that group', 7);
   INSERT INTO communities (name, description, admin_id) VALUES ("Sergey's group!", 'Sergey made that group', 8);
   INSERT INTO communities (name, description, admin_id) VALUES ("Stepan's group!", 'Stepan made that group', 9);
   INSERT INTO communities (name, description, admin_id) VALUES ("Peter's group!", 'Peter made that group', 10);

   -- приватные сообщения
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (10, 1, 'Hi, Vasya');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (9, 2, 'Hi, Masha');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (8, 3, 'Hi, Misha');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (7, 4, 'Hi, Max');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (6, 5, 'Hi, Kate');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (5, 6, 'Hi, Paul');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (4, 7, 'Hi, Alex');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (3, 8, 'Hi, Sergey');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (2, 9, 'Hi, Stepan');
   INSERT INTO messages (from_user_id, to_user_id, body) VALUES (1, 10, 'Hi, Peter');

   -- пользователи сообществ
   INSERT INTO communities_users (community_id, user_id) VALUES (10, 1);
   INSERT INTO communities_users (community_id, user_id) VALUES (9, 2);
   INSERT INTO communities_users (community_id, user_id) VALUES (8, 3);
   INSERT INTO communities_users (community_id, user_id) VALUES (7, 4);
   INSERT INTO communities_users (community_id, user_id) VALUES (6, 5);
   INSERT INTO communities_users (community_id, user_id) VALUES (5, 6);
   INSERT INTO communities_users (community_id, user_id) VALUES (4, 7);
   INSERT INTO communities_users (community_id, user_id) VALUES (3, 8);
   INSERT INTO communities_users (community_id, user_id) VALUES (2, 9);
   INSERT INTO communities_users (community_id, user_id) VALUES (1, 10);

   -- запросы в друзья
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (10, 1, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (9, 2, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (8, 3, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (7, 4, 0);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (6, 5, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (4, 6, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (3, 7, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (2, 8, 0);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (1, 9, 1);
   INSERT INTO friend_requests (from_user_id, to_user_id, accepted) VALUES (9, 10, 0);

   -- типы файлов
   INSERT INTO media_types (name) VALUES ('изображение');
   INSERT INTO media_types (name) VALUES ('музыка');
   INSERT INTO media_types (name) VALUES ('документ');
   INSERT INTO media_types (name) VALUES ('видео');
   INSERT INTO media_types (name) VALUES ('презентация');
   INSERT INTO media_types (name) VALUES ('чертёж');
   INSERT INTO media_types (name) VALUES ('модель');
   INSERT INTO media_types (name) VALUES ('осциллограмма');
   INSERT INTO media_types (name) VALUES ('график');
   INSERT INTO media_types (name) VALUES ('диаграмма');

   -- файлы
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (1, 1, 'file.изображение', 100);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (2, 2, 'file.музыка', 200);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (3, 3, 'file.документ', 300);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (4, 4, 'file.видео', 400);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (5, 5, 'file.презентация', 500);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (6, 6, 'file.чертёж', 600);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (7, 7, 'file.модель', 700);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (8, 8, 'file.осциллограмма', 800);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (9, 9, 'file.график', 900);
   INSERT INTO media (user_id, media_types_id, file_name, file_size) VALUES (10, 10, 'file.диаграмма', 1000);

   -- публикации
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 1, 10, 1, 'Текст публикации от Vasya');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 2, NULL, NULL, 'Текст публикации от Masha');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 3, NULL, NULL, 'Текст публикации от Misha');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 4, NULL, NULL, 'Текст публикации от Max');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 5, NULL, NULL, 'Текст публикации от Kate');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 6, NULL, NULL, 'Текст публикации от Paul');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 7, NULL, NULL, 'Текст публикации от Alex');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 8, NULL, NULL, 'Текст публикации от Sergey');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 9, NULL, NULL, 'Текст публикации от Stepan');
   INSERT INTO post (post_id, user_id, community_id, media_id, text) VALUES (NULL, 10, NULL, NULL, 'Текст публикации от Peter');

   -- опросы в публикациях (содержимое вопросов)
   INSERT INTO poll (post_id, text, answers) VALUES (1, 'Опрос от Vasya', '["Кошки","Собаки"]');
   INSERT INTO poll (post_id, text, answers) VALUES (2, 'Опрос от Masha', '["Пельмени","Вареники","Выпечка"]');
   INSERT INTO poll (post_id, text, answers) VALUES (3, 'Опрос от Misha', '["Попугаи","Питоны","Бобры","Коты"]');
   INSERT INTO poll (post_id, text, answers) VALUES (4, 'Опрос от Max', '["Москва","Новосибирск","Сочи"]');
   INSERT INTO poll (post_id, text, answers) VALUES (5, 'Опрос от Kate', '["Белый","Чёрный","Зелёный","Красный"]');
   INSERT INTO poll (post_id, text, answers) VALUES (6, 'Опрос от Paul', '["Яблоко","Вишня"]');
   INSERT INTO poll (post_id, text, answers) VALUES (7, 'Опрос от Alex', '["Отдых","Работа","Досуг"]');
   INSERT INTO poll (post_id, text, answers) VALUES (8, 'Опрос от Sergey', '["Карьера","Семья","Родственники"]');
   INSERT INTO poll (post_id, text, answers) VALUES (9, 'Опрос от Stepan', '["Дом","Квартира","Дача"]');
   INSERT INTO poll (post_id, text, answers) VALUES (10, 'Опрос от Peter', '["Электричество","Вода","Интернет","Отопление"]');

   -- подвязываем голосование к посту
   UPDATE post SET poll_id = 1 WHERE id = 1;
   UPDATE post SET poll_id = 2 WHERE id = 2;
   UPDATE post SET poll_id = 3 WHERE id = 3;
   UPDATE post SET poll_id = 4 WHERE id = 4;
   UPDATE post SET poll_id = 5 WHERE id = 5;
   UPDATE post SET poll_id = 6 WHERE id = 6;
   UPDATE post SET poll_id = 7 WHERE id = 7;
   UPDATE post SET poll_id = 8 WHERE id = 8;
   UPDATE post SET poll_id = 9 WHERE id = 9;
   UPDATE post SET poll_id = 10 WHERE id = 10;

   -- ответы пользователей на опросы (нумерация ответов в JSON с нуля)
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (1, 10, 1);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (2, 9, 0);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (3, 8, 1);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (4, 7, 0);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (5, 6, 1);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (6, 5, 0);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (7, 4, 1);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (8, 3, 0);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (9, 2, 1);
   INSERT INTO poll_answer (user_id, poll_id, answer_id) VALUES (10, 1, 0);

   -- лайки к постам
   INSERT INTO likes (user_id, post_id) VALUES (1, 10);
   INSERT INTO likes (user_id, post_id) VALUES (2, 9);
   INSERT INTO likes (user_id, post_id) VALUES (3, 8);
   INSERT INTO likes (user_id, post_id) VALUES (4, 7);
   INSERT INTO likes (user_id, post_id) VALUES (5, 6);
   INSERT INTO likes (user_id, post_id) VALUES (6, 5);
   INSERT INTO likes (user_id, post_id) VALUES (7, 4);
   INSERT INTO likes (user_id, post_id) VALUES (8, 3);
   INSERT INTO likes (user_id, post_id) VALUES (9, 2);
   INSERT INTO likes (user_id, post_id) VALUES (10, 1);
