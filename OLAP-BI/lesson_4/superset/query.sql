SELECT `Color` AS `Color`,
       `YEAR(OrderDate)` AS `YEAR(OrderDate)`,
       `MONTH(OrderDate)` AS `MONTH(OrderDate)`,
       sum(`Weight`) AS `SUM(Weight)`
FROM
  (SELECT ProductID,
          SalesOrderID,
          OrderQty,
          UnitPrice,
          Name,
          Color,
          Size,
          Weight,
          SalesOrderNumber,
          AccountNumber,
          CreditCardID,
          OrderDate,
          DAY(OrderDate),
          MONTH(OrderDate),
          YEAR(OrderDate),
          ModifiedDate,
          ShipDate,
          DueDate
   FROM adventureworks_ods.Pivot) AS virtual_table
GROUP BY `Color`,
         `YEAR(OrderDate)`,
         `MONTH(OrderDate)`
ORDER BY `SUM(Weight)` DESC
LIMIT 10000; 
