-- dag который пересоздает (drop if exists) в целевой базе нужные таблицы (копирует схему из source).

\connect my_database;

-- Удаляем схему и все таблицы из схемы
DROP SCHEMA IF EXISTS stage CASCADE;

-- Создаём схему
CREATE SCHEMA stage;

-- Создаём таблицы по типу старых (типы колонок будут совпадать, но данных не будет)
-- (не будут перенесены FK!)
CREATE TABLE stage.OrderDetails  (LIKE public.OrderDetails INCLUDING ALL);
CREATE TABLE stage.Products      (LIKE public.Products INCLUDING ALL);
CREATE TABLE stage.Suppliers     (LIKE public.Suppliers INCLUDING ALL);
CREATE TABLE stage.Orders        (LIKE public.Orders INCLUDING ALL);
