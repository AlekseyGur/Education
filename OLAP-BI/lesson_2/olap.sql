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
   UnitPrice FLOAT,
   PRIMARY KEY (ProductID, SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_olap.DmnOrder (
   SalesOrderID INT,
   SalesOrderNumber VARCHAR(25),
   AccountNumber VARCHAR(15),
   CreditCardID INT,
   CONSTRAINT adventureworks_olap_DmnOrder_fk FOREIGN KEY (SalesOrderID) REFERENCES adventureworks.salesorderheader(SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_olap.DmnDate (
   SalesOrderID INT,
   OrderDate TIMESTAMP,
   ModifiedDate DATETIME,
   ShipDate DATETIME,
   DueDate DATETIME,
   CONSTRAINT adventureworks_olap_DmnDate_fk FOREIGN KEY (SalesOrderID) REFERENCES adventureworks.salesorderheader(SalesOrderID)
) ENGINE=InnoDB;

CREATE TABLE adventureworks_olap.DmnProduct (
   ProductID INT,
   Name VARCHAR(50),
   Color VARCHAR(15),
   Size VARCHAR(5),
   Weight DECIMAL(8,2),
   CONSTRAINT adventureworks_olap_DmnProduct_fk FOREIGN KEY (ProductID) REFERENCES adventureworks.product(ProductID)
) ENGINE=InnoDB;


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

