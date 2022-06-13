-- создание STG базу (она живёт только один день, постоянно обновляется и служит только для копирования данных из OLTP в ODS)
DROP DATABASE IF EXISTS adventureworks_stg;
CREATE DATABASE IF NOT EXISTS adventureworks_stg;
USE adventureworks_stg;

-- создание таблиц
CREATE TABLE adventureworks_stg.FctSales (
   ProductID INT,
   SalesOrderID INT,
   OrderQty INT,
   ModifiedDate DATETIME,
   UnitPrice FLOAT,
   PRIMARY KEY (ProductID, SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_stg.DmnOrder (
   SalesOrderID INT,
   SalesOrderNumber VARCHAR(25),
   AccountNumber VARCHAR(15),
   CreditCardID INT,
   CONSTRAINT adventureworks_stg_DmnOrder_fk FOREIGN KEY (SalesOrderID) REFERENCES adventureworks.salesorderheader(SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_stg.DmnDate (
   SalesOrderID INT,
   OrderDate TIMESTAMP,
   ModifiedDate DATETIME,
   ShipDate DATETIME,
   DueDate DATETIME,
   CONSTRAINT adventureworks_stg_DmnDate_fk FOREIGN KEY (SalesOrderID) REFERENCES adventureworks.salesorderheader(SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_stg.DmnProduct (
   ProductID INT,
   Name VARCHAR(50),
   Color VARCHAR(15),
   Size VARCHAR(5),
   Weight DECIMAL(8,2),
   CONSTRAINT adventureworks_stg_DmnProduct_fk FOREIGN KEY (ProductID) REFERENCES adventureworks.product(ProductID)
) ENGINE=InnoDB;


-- заполнение таблиц свежими данными
INSERT INTO adventureworks_stg.FctSales(ProductID, SalesOrderID,
                     OrderQty, ModifiedDate, 
                     UnitPrice)
SELECT ProductID, SalesOrderID, 
       OrderQty, ModifiedDate,
       UnitPrice
FROM adventureworks.salesorderdetail;


INSERT INTO adventureworks_stg.DmnOrder(SalesOrderID, SalesOrderNumber,
                     AccountNumber, CreditCardID)
SELECT SalesOrderID, SalesOrderNumber,
       AccountNumber, CreditCardID
FROM adventureworks.salesorderheader;


INSERT INTO adventureworks_stg.DmnDate(SalesOrderID, OrderDate, ModifiedDate,
                    ShipDate, DueDate)
SELECT SalesOrderID, OrderDate, ModifiedDate,
       ShipDate, DueDate
FROM adventureworks.salesorderheader;


INSERT INTO adventureworks_stg.DmnProduct(ProductID, Name, Color, Size, Weight)
SELECT ProductID, Name, Color, Size, Weight
FROM adventureworks.product;

