-- создание OLAP базы
DROP DATABASE IF EXISTS adventureworks_olap;
CREATE DATABASE IF NOT EXISTS adventureworks_olap;
USE adventureworks_olap;

-- создание таблиц
CREATE TABLE adventureworks_olap.FctSales (
   ProductID INT,
   SalesOrderID INT,
   OrderQty INT,
   ModifiedDate DATETIME,
   UnitPrice FLOAT
);

CREATE TABLE adventureworks_olap.DmnOrder (
   SalesOrderID INT,
   SalesOrderNumber VARCHAR(25),
   AccountNumber VARCHAR(15),
   CreditCardID INT
);

CREATE TABLE adventureworks_olap.DmnDate (
   SalesOrderID INT,
   OrderDate TIMESTAMP,
   ModifiedDate DATETIME,
   ShipDate DATETIME,
   DueDate DATETIME
);

CREATE TABLE adventureworks_olap.DmnProduct (
   ProductID INT,
   Name VARCHAR(50),
   Color VARCHAR(15),
   Size VARCHAR(5),
   Weight DECIMAL(8,2)
);


-- заполнение таблиц
INSERT INTO adventureworks_olap.FctSales(ProductID, SalesOrderID,
                     OrderQty, ModifiedDate, 
                     UnitPrice)
SELECT ProductID, SalesOrderID, 
       OrderQty, ModifiedDate,
       UnitPrice
FROM adventureworks.salesorderdetail;


INSERT INTO adventureworks_olap.DmnOrder(SalesOrderID, SalesOrderNumber,
                     AccountNumber, CreditCardID)
SELECT SalesOrderID, SalesOrderNumber,
       AccountNumber, CreditCardID
FROM adventureworks.salesorderheader;


INSERT INTO adventureworks_olap.DmnDate(SalesOrderID, OrderDate, ModifiedDate,
                    ShipDate, DueDate)
SELECT SalesOrderID, OrderDate, ModifiedDate,
       ShipDate, DueDate
FROM adventureworks.salesorderheader;


INSERT INTO adventureworks_olap.DmnProduct(ProductID, Name, Color, Size, Weight)
SELECT ProductID, Name, Color, Size, Weight
FROM adventureworks.product;

