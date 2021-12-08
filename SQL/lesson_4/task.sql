-- Заполнить все таблицы БД vk данными (по 10 записей в каждой таблице)

/*
Текущие таблицы:

+-------------------+
| Tables_in_vk      |
+-------------------+
| communities       |
| communities_users |
| friend_requests   |
| likes             |
| media             |
| media_types       |
| messages          |
| poll              |
| poll_answer       |
| post              |
| profiles          |
| users             |
+-------------------+
*/

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
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Vasya', 'Vasilkov', 'vasya@mail.com', '81dc9bdb52d04dc20036dbd8313ed051', '99999999901');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Masha', 'Ivanova', 'masha@mail.com', '81dc9bdb52d04dc20036dbd8313ed052', '99999999902');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Misha', 'Petrov', 'misha@mail.com', '81dc9bdb52d04dc20036dbd8313ed053', '99999999903');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Max',   'Sidorov', 'mas@mail.com', '81dc9bdb52d04dc20036dbd8313ed054', '99999999904');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Kate',  'Kuznetsov', 'kate@mail.com', '81dc9bdb52d04dc20036dbd8313ed055', '99999999905');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Paul',  'Kotov', 'paul@mail.com', '81dc9bdb52d04dc20036dbd8313ed056', '99999999906');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Alex',  'Alekseev', 'alex@mail.com', '81dc9bdb52d04dc20036dbd8313ed057', '99999999907');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Sergey', 'Borisov', 'sergey@mail.com', '81dc9bdb52d04dc20036dbd8313ed058', '99999999908');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Stepan','Lomov', 'stepan@mail.com', '81dc9bdb52d04dc20036dbd8313ed059', '99999999909');
INSERT INTO users (firstname, lastname, email, password_hash, phone) VALUES ('Peter', 'Stepanov', 'peter@mail.com', '81dc9bdb52d04dc20036dbd8313ed010', '99999999910');

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
INSERT INTO poll (post_id, text, answers) VALUES (2, 'Опрос от Masha', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (3, 'Опрос от Misha', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (4, 'Опрос от Max', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (5, 'Опрос от Kate', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (6, 'Опрос от Paul', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (7, 'Опрос от Alex', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (8, 'Опрос от Sergey', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (9, 'Опрос от Stepan', '["Кошки","Собаки"]');
INSERT INTO poll (post_id, text, answers) VALUES (10, 'Опрос от Peter', '["Кошки","Собаки"]');

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



-- скрипт, возвращающий список имен (только firstname) пользователей без повторений в алфавитном порядке
SELECT DISTINCT firstname FROM users ORDER BY firstname ASC;

-- Написать скрипт, отмечающий несовершеннолетних пользователей как неактивных (поле is_active = false). Предварительно добавить такое поле в таблицу profiles со значением по умолчанию = true (или 1)
ALTER TABLE profiles ADD COLUMN birthday DATE NOT NULL DEFAULT NOW();
ALTER TABLE profiles ADD COLUMN is_active BOOLEAN DEFAULT true;
   -- добавляем совершеннолетних
      UPDATE profiles SET birthday = '2001-12-08' WHERE user_id = 1;
      UPDATE profiles SET birthday = '2002-10-08' WHERE user_id = 2;
      UPDATE profiles SET birthday = '2018-03-08' WHERE user_id = 3; -- несовершеннолетний
      UPDATE profiles SET birthday = '2000-09-08' WHERE user_id = 4;
      UPDATE profiles SET birthday = '2001-12-08' WHERE user_id = 5;
      UPDATE profiles SET birthday = '2002-10-08' WHERE user_id = 6;
      UPDATE profiles SET birthday = '2024-03-08' WHERE user_id = 7; -- несовершеннолетний
      UPDATE profiles SET birthday = '2000-09-08' WHERE user_id = 8;
      UPDATE profiles SET birthday = '2020-09-08' WHERE user_id = 9; -- несовершеннолетний
      UPDATE profiles SET birthday = '2020-09-08' WHERE user_id = 10; -- несовершеннолетний
   -- ставим is_active = false для несовершеннолетних
      UPDATE profiles SET is_active = false WHERE birthday < NOW() - INTERVAL 18 YEAR;



-- Написать скрипт, удаляющий сообщения «из будущего» (дата больше сегодняшней)
DELETE FROM messages WHERE created_at > NOW();


-- Написать название темы курсового проекта (в комментарии)
Создание базы данных с частью функционала социальной сети twitter
