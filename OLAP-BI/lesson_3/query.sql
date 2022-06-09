SELECT `Color` AS `Color`,
       `YEAR(DD.OrderDate)` AS `YEAR(DD.OrderDate)`,
       `MONTH(DD.OrderDate)` AS `MONTH(DD.OrderDate)`,
       sum(`Weight`) AS `SUM(Weight)`
FROM
  (SELECT FS.ProductID,
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
          DAY(DD.OrderDate),
          MONTH(DD.OrderDate),
          YEAR(DD.OrderDate),
          DD.ModifiedDate,
          DD.ShipDate,
          DD.DueDate
   FROM adventureworks_olap.FctSales AS FS
   INNER JOIN adventureworks_olap.DmnProduct AS DP ON FS.ProductID = DP.ProductID
   INNER JOIN adventureworks_olap.DmnOrder AS DO ON FS.SalesOrderID = DO.SalesOrderID
   INNER JOIN adventureworks_olap.DmnDate AS DD ON FS.SalesOrderID = DD.SalesOrderID) AS virtual_table
GROUP BY `Color`,
         `YEAR(DD.OrderDate)`,
         `MONTH(DD.OrderDate)`
ORDER BY `SUM(Weight)` DESC
LIMIT 10000; 
