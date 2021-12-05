-- ДЗ: Написать cкрипт, добавляющий в БД vk, которую создали на занятии, 3 новые таблицы (с перечнем полей, указанием индексов и внешних ключей) 

/* создание таблиц */

DROP TABLE IF EXISTS post, poll, poll_answer, likes;

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



/* заполнение таблиц тестовыми данными */

-- добавляем публикацию
INSERT INTO post VALUES (
	DEFAULT, -- id SERIAL PRIMARY KEY
	NULL, -- post_id - это не репост
	1, -- user_id автора добавляемого поста
	NULL, -- poll_id голосования
	NULL, -- id группы. NULL = публикация в своём профиле
	1, -- прикреплённый файл
	'Открытое голосование', -- текст публикации
	DEFAULT -- created_at - текущая дата
);

-- опросы в публикациях (содержимое вопросов)
INSERT INTO poll VALUES (
	DEFAULT, -- id
	1, -- id поста, получаем после создания публикации
	'Кошки или собаки?', -- текст вопроса на голосовании
	'["Кошки","Собаки"]' -- данные для опроса
);

-- подвязываем голосование к посту
UPDATE post SET poll_id = 1 WHERE id = 1;

-- ответы пользователей на опросы
INSERT INTO poll_answer VALUES  (
	DEFAULT, -- id,
	1, -- user_id голосовавшего
	1, -- poll_id опроса
	1 -- номер ответа = номер элемента JSON массива (начиная с нуля)
);

-- лайки к постам
INSERT INTO likes VALUES (
	1, -- id автора лайка
	1 -- id публикации
);
