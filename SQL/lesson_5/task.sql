/* 
Практическое задание по теме “Операторы, фильтрация,  сортировка и ограничение” 
*/

-- Задание 1
-- заполним created_at и updated_at текущей датой и временем
UPDATE users SET created_at = NOW(), updated_at = NOW();


-- Задание 2
-- преобразуем данные в нужный формат типа
UPDATE users SET created_at = STR_TO_DATE(created_at, '%d.%m.%Y %k:%i'), updated_at = STR_TO_DATE(updated_at, '%d.%m.%Y %k:%i');
-- изменяем тип столбцов
ALTER TABLE users MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;


-- Задание 3
-- вывести складские запасы по возрастаню запасов, но отсутствующие должны быть в конце списка
SELECT *, CASE WHEN value = 0 THEN 0 ELSE 1 END AS exist FROM storehouses_products ORDER BY exist DESC, value;


-- Задание 4
-- из таблицы users необходимо извлечь пользователей, родившихся в августе и мае. Месяцы заданы в виде списка английских названий ('may', 'august')
SELECT *, MONTHNAME(birthday_at) AS month FROM users WHERE MONTHNAME(birthday_at) RLIKE 'may|august';


-- Задание 5
-- Отсортируйте записи в порядке, заданном в списке IN.
SELECT * FROM catalogs WHERE id IN (5, 1, 2) ORDER BY FIELD(id,5,1,2);


/* 
Практическое задание теме “Агрегация данных” 
*/

-- Задание 1
-- средний возраст пользователей в таблице users
SELECT round(AVG(TIMESTAMPDIFF(YEAR, birthday_at, NOW()))) AS AVG_AGE FROM users;


-- Задание 2
-- количество дней рождения, которые приходятся на каждый из дней недели. Необходимы дни недели текущего года, а не года рождения.
SELECT DAYOFWEEK( DATE_FORMAT( birthday_at, CONCAT(YEAR(NOW()), '-%m-%d') ) ) AS day, COUNT(*) AS cnt FROM use
rs GROUP BY day; -- (1 = воскресенье, …, 7 = суббота)


-- Задание 3
-- произведение чисел в столбце таблицы
SELECT ROUND(EXP(SUM(LN(id)))) AS 'RESULT' FROM numbers;
