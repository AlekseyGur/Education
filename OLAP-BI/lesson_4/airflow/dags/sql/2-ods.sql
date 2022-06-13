-- Данные из базы STG переносятся в ODS, после чего по ним строятся графики BI. После копирования данных из STG всё удаляется
CREATE DATABASE IF NOT EXISTS adventureworks_ods;
USE adventureworks_ods;

-- создание таблиц
CREATE TABLE IF NOT EXISTS adventureworks_ods.Pivot (
   ProductID INT,
   SalesOrderID INT,
   OrderQty INT,
   UnitPrice FLOAT,
   Name VARCHAR(50),
   Color VARCHAR(15),
   Size VARCHAR(5),
   Weight DECIMAL(8,2),
   SalesOrderNumber VARCHAR(25),
   AccountNumber VARCHAR(15),
   CreditCardID INT,
   OrderDate TIMESTAMP,
   ModifiedDate DATETIME,
   ShipDate DATETIME,
   DueDate DATETIME
) ENGINE=InnoDB;


-- Добавляем в таблицу свежие данные
INSERT INTO adventureworks_ods.Pivot
SELECT FS.ProductID,
       FS.SalesOrderID,
       FS.OrderQty,
       FS.UnitPrice,
       DP.Name,
       DP.Color,
       DP.Size,
       DP.Weight,
       DO.SalesOrderNumber,
       DO.AccountNumber,
       DO.CreditCardID,
       DD.OrderDate,
       DD.ModifiedDate,
       DD.ShipDate,
       DD.DueDate
FROM adventureworks_stg.FctSales AS FS
INNER JOIN adventureworks_stg.DmnProduct AS DP ON FS.ProductID = DP.ProductID
INNER JOIN adventureworks_stg.DmnOrder AS DO ON FS.SalesOrderID = DO.SalesOrderID
INNER JOIN adventureworks_stg.DmnDate AS DD ON FS.SalesOrderID = DD.SalesOrderID;
