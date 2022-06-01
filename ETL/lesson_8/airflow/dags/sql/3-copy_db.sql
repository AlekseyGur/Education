-- dag который копирует данные из исходной\source бд в целевую в stage, сохраняя формат

\connect my_database;

INSERT INTO stage.OrderDetails  SELECT * FROM public.OrderDetails;
INSERT INTO stage.Products      SELECT * FROM public.Products;
INSERT INTO stage.Suppliers     SELECT * FROM public.Suppliers;
INSERT INTO stage.Orders        SELECT * FROM public.Orders;
