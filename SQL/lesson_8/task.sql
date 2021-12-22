/* 
Практическое задание по теме “Сложные запросы” 

Задачи необходимо решить с использованием объединения таблиц (JOIN)
*/

-- Из всех пользователей соц. сети найдите человека, который больше всех общался (написал сообщений) с пользователем user_id = 1
SELECT
   CONCAT(users.firstname, ' ', users.lastname) AS name,
   COUNT(*) AS msg_count
FROM
   messages
INNER JOIN
   users
ON
   messages.from_user_id = users.id
WHERE
   messages.to_user_id = 1
GROUP BY
   users.id
ORDER BY
   msg_count DESC;


-- Подсчитать общее количество лайков, которые получили пользователи младше 10 лет..
SELECT
   COUNT(*) AS likes_count
FROM
   likes
INNER JOIN post ON likes.post_id=post.id
INNER JOIN profiles ON profiles.user_id=post.user_id
WHERE
   10 > TIMESTAMPDIFF(YEAR, profiles.birthday, NOW());


-- Определить кто больше поставил лайков (всего): мужчины или женщины.
SELECT
   COUNT(*) AS likes_count,
   CASE(gender)
      WHEN 'f' THEN 'female'
      WHEN 'm' THEN 'male'
      WHEN 'x' THEN 'not defined'
   END AS gender
FROM
   likes
INNER JOIN
   profiles
ON
   likes.user_id=profiles.user_id
GROUP BY
   gender
ORDER BY
   gender DESC;
