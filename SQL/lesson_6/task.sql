/* 
Практическое задание по теме “Операторы, фильтрация, сортировка и ограничение. Агрегация данных” 
*/

-- Из всех пользователей соц. сети найдите человека, который больше всех общался (написал сообщений) с пользователем user_id = 1
SELECT from_user_id FROM messages WHERE to_user_id = 1 GROUP BY from_user_id ORDER BY COUNT(*) DESC LIMIT 1;


-- Подсчитать общее количество лайков, которые получили пользователи младше 10 лет..
SELECT COUNT(*) AS likes FROM likes WHERE post_id IN ( -- сумма лайков к публикациям, которые сделаны пользователями < 10 лет
   SELECT id FROM post WHERE user_id IN ( -- id публикаций, которые сделаны пользователями < 10 лет
      SELECT user_id FROM profiles WHERE 10 > TIMESTAMPDIFF(YEAR, birthday, NOW()) -- id пользователей < 10 лет
   )
);


-- Определить кто больше поставил лайков (всего): мужчины или женщины.
SELECT COUNT(*) AS likes, CASE(gender)
    WHEN 'f' THEN 'female'
    WHEN 'm' THEN 'male'
    WHEN 'x' THEN 'not defined'
  END AS gender
FROM profiles WHERE user_id IN (SELECT user_id FROM likes) GROUP BY gender;
