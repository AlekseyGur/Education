-- dag который пересоздает в целевой базе таблицы для хранения данных в модели data vault, однократно

-- схема хранилища https//raw.githubusercontent.com/AlekseyGur/Education/master/ETL/lesson_4/DataVault-model/DataVault.svg

-- Удаляем всё
-- DROP DATABASE IF EXISTS my_database;
-- CREATE DATABASE my_database;

\connect my_database;

-- Удаляем схему и все таблицы из схемы
DROP SCHEMA IF EXISTS core CASCADE;

-- DROP TABLE IF EXISTS core.l_s_order_product;
-- DROP TABLE IF EXISTS core.l_product_supplier;
-- DROP TABLE IF EXISTS core.l_order_product;
-- DROP TABLE IF EXISTS core.h_order;
-- DROP TABLE IF EXISTS core.h_product;
-- DROP TABLE IF EXISTS core.h_supplier;
-- DROP TABLE IF EXISTS core.s_supplier;
-- DROP TABLE IF EXISTS core.s_product;

-- Создаём схему
CREATE SCHEMA core;


-- Сателлиты линков

CREATE TABLE core.l_s_order_product (
   l_order_product_rk INT,
   UnitPrice FLOAT,
   Quantity INT,
   Discount FLOAT,
   OrderDate date,
   RequiredDate date,
   Freight FLOAT,
   ShipAddress VARCHAR(60),
   ShipCity VARCHAR(30),
   ShipRegion VARCHAR(30),
   ShipPostalCode VARCHAR(30),
   ShipCountry VARCHAR(20),
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now(),
   CONSTRAINT l_order_product_fk FOREIGN KEY (l_order_product_rk) REFERENCES core.l_order_product(l_product_supplier_rk)
);

-- Линки

CREATE TABLE core.l_order_product (
   l_order_product_rk SERIAL,
   h_order_rk INT,
   h_product_rk INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now()
   CONSTRAINT h_order_fk FOREIGN KEY (h_order_rk) REFERENCES core.h_order(h_order_rk),
   CONSTRAINT h_product_fk FOREIGN KEY (h_product_rk) REFERENCES core.h_product(h_product_rk)
);

CREATE TABLE core.l_product_supplier (
   l_product_supplier_rk SERIAL,
   h_product_rk INT,
   h_supplier_rk INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now(),
   CONSTRAINT h_product_fk FOREIGN KEY (h_product_rk) REFERENCES core.h_product(h_product_rk),
   CONSTRAINT h_supplier_fk FOREIGN KEY (h_supplier_rk) REFERENCES core.h_supplier(h_supplier_rk)
);

-- Хабы

CREATE TABLE core.h_order (
   h_order_rk int4 SERIAL NOT NULL,
   order_id INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now()
);

CREATE TABLE core.h_product (
   h_product_rk int4 SERIAL NOT NULL,
   product_id INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now()
);

CREATE TABLE core.h_supplier (
   h_supplier_rk int4 SERIAL NOT NULL,
   supplier_id INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now()
);

-- Саттелиты

CREATE TABLE core.s_supplier (
   h_supplier_rk INT,
   CompanyName VARCHAR(40),
   ContactName VARCHAR(40),
   Address VARCHAR(40),
   City VARCHAR(40),
   Region VARCHAR(40),
   PostalCode VARCHAR(40),
   Country VARCHAR(40),
   Phone VARCHAR(40),
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now(),
   valid_from_dttm TIMESTAMP SET DEFAULT now(),
   valid_to_dttm TIMESTAMP,
   CONSTRAINT h_supplier_fk FOREIGN KEY (h_supplier_rk) REFERENCES core.h_supplier(h_supplier_rk)
);

CREATE TABLE core.s_product (
   h_product_rk INT,
   ProductName VARCHAR(40),
   QuantityPerUnit INT,
   UnitPrice FLOAT,
   Discontinued INT,
   source_system VARCHAR(40) SET DEFAULT 'stage',
   processed_dttm TIMESTAMP SET DEFAULT now(),
   valid_from_dttm TIMESTAMP SET DEFAULT now(),
   valid_to_dttm TIMESTAMP,
   CONSTRAINT s_product_fk FOREIGN KEY (h_product_rk) REFERENCES core.h_product(h_product_rk)
);
