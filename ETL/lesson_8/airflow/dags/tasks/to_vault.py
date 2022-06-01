import psycopg2
import os

# Структура vault хранилища: https://raw.githubusercontent.com/AlekseyGur/Education/master/ETL/lesson_4/DataVault-model/DataVault.svg


# В vault базе есть только 3 хаба: h_order, h_product, h_supplier. Они совпадают
# с табилцами Orders, Products, Suppliers. Переносить данные из стенджингового
# слоя в хабы будем порциями. То есть берём первую порцию, смотрим есть ли в
# ней изменения относительно сохранённых данных и записываем, если изменения
# случились. При этом не забываем отменить последнюю как истекшую (устанавливаем
# в vault таблице поле valid_to_dttm на текущую дату и время. если такое поле
# есть)
LIMIT = 10 # порция для сверки

SERVER_IP = '192.168.122.153'
CONN_TO = f"host='{SERVER_IP}' port=5433 dbname='my_database' user='root' password='postgres'"


def refresh_s_supplier(cursor, SupplierID:int):
    """Пересохраняет в таблицу саттелит s_supplier данные определённого поставщика.
    При этом старшая запись в s_supplier помечается как устаревшая (прописывается
    valid_to_dttm равной текущей дате)
    :params int SupplierID: id поставщика
    """
    # помечаем старую запись как устаревшую
    query =  '''UPDATE core.s_supplier
                SET valid_to_dttm = NOW(),
                    processed_dttm = NOW()
                WHERE valid_to_dttm IS NULL
                AND h_supplier_rk = %(SupplierID)s
                LIMIT 1;'''
    cursor.execute(query, {
        'SupplierID': SupplierID,
    })

    # добавляем новые данные
    query = '''SELECT
                    SupplierID,
                    CompanyName,
                    ContactName,
                    Address,
                    City,
                    Region,
                    PostalCode,
                    Country,
                    Phone,
                FROM stage.Suppliers;'''
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        SupplierID, CompanyName, ContactName, Address, City, Region, \
        PostalCode, Country, Phone = row
        query = f'''INSERT INTO core.s_supplier (
                        h_supplier_rk,
                        CompanyName,
                        ContactName,
                        Address,
                        City,
                        Region,
                        PostalCode,
                        Country,
                        Phone)
                    VALUES (
                            %(SupplierID)s,
                            %(CompanyName)s,
                            %(ContactName)s,
                            %(Address)s,
                            %(City)s,
                            %(Region)s,
                            %(PostalCode)s,
                            %(Country)s,
                            %(Phone)s
                        );'''
        cursor.execute(query, { 'SupplierID': SupplierID,
                                'CompanyName': CompanyName,
                                'ContactName': ContactName,
                                'Address': Address,
                                'City': City,
                                'Region': Region,
                                'PostalCode': PostalCode,
                                'Country': Country,
                                'Phons': Phon
                              })


def refresh_s_product(cursor, ProductID:int):
    """Пересохраняет в таблицу саттелит s_product данные определённого товара.
    При этом старшая запись в s_product помечается как устаревшая (прописывается
    valid_to_dttm равной текущей дате)
    :params int ProductID: id товара
    """
    # помечаем старую запись как устаревшую
    query =  '''UPDATE core.s_product
                SET valid_to_dttm = NOW(),
                    processed_dttm = NOW()
                WHERE valid_to_dttm IS NULL
                AND h_product_rk = %(ProductID)s
                LIMIT 1;'''
    cursor.execute(query, {
        'ProductID': ProductID,
    })

    # добавляем новые данные
    query = '''SELECT
                    ProductID,
                    ProductName,
                    QuantityPerUnit,
                    UnitPrice,
                    Discontinued
                FROM stage.Products
                WHERE ProductID = $(ProductID)s
                LIMIT 1;'''
    cursor.execute(query, {
        'ProductID': ProductID,
    })
    rows = cursor.fetchall()

    for row in rows:
        ProductID, ProductName, QuantityPerUnit, UnitPrice, Discontinued = row
        query = f'''INSERT INTO core.s_product (
                        h_product_rk,
                        ProductName,
                        QuantityPerUnit,
                        UnitPrice,
                        Discontinued)
                    VALUES (
                            %(ProductID)s,
                            %(ProductName)s,
                            %(QuantityPerUnit)s,
                            %(UnitPrice)s,
                            %(Discontinued)s
                        );'''
        cursor.execute(query, {
                                'ProductID': ProductID,
                                'ProductName': ProductName,
                                'QuantityPerUnit': QuantityPerUnit,
                                'UnitPrice': UnitPrice,
                                'Discontinue': Discontinue
                              })


# копируем данные из core в Vault
with psycopg2.connect(CONN_TO) as conn, conn.cursor() as cursor:
    # данные по новым добавлениям в хабы понадобится для создания линков
    added_products_ids = []  # список добавленных продуктов
    added_orders_ids = []  # список добавленных заказов
    added_l_order_product_ids = []  # список добавленных линков l_order_product

    # ========================================================
    # Добавление новых данных в хранилище
    # ========================================================

    # === Хабы ===

    # id последнего скопированного элемента из таблицы core.h_product
    cursor.execute("SELECT MAX(product_id) FROM core.h_product;")
    product_last_id = cursor.fetchone()[0]
    # id последнего скопированного элемента из таблицы stage.Products
    cursor.execute("SELECT MAX(ProductID) FROM stage.Products;")
    stage_product_last_id = cursor.fetchone()[0]

    if product_last_id < stage_product_last_id:  # есть новые данные - обработаем
        # переносим данные в Хаб h_product
        query = 'SELECT ProductID FROM stage.Products WHERE \
                 ProductID > %(product_last_id)s LIMIT %(LIMIT)s;'
        cursor.execute(query, {'product_last_id': product_last_id,
                               'LIMIT': LIMIT})
        rows = cursor.fetchall()
        for row in rows:
            ProductID, *_ = row
            query = 'INSERT INTO core.h_product (product_id) VALUES (%(ProductID)s);'
            cursor.execute(query, {'ProductID': ProductID})
            added_products_ids.append(ProductID)

        conn.commit()

        for row in rows:  # создадим записи саттелита
            ProductID, *_ = row
            refresh_s_product(cursor, ProductID)

        conn.commit()

    # id последнего скопированного элемента из таблицы core.h_order
    cursor.execute("SELECT MAX(order_id) FROM core.h_order;")
    h_order_last_id = cursor.fetchone()[0]
    # id последнего скопированного элемента из таблицы stage.Orders
    cursor.execute("SELECT MAX(OrderID) FROM stage.Orders;")
    stage_orders_last_id = cursor.fetchone()[0]

    if h_order_last_id < stage_orders_last_id:  # есть новые данные - обработаем
        # переносим данные в Хаб h_order
        query = 'SELECT OrderID FROM stage.Orders WHERE \
                 OrderID > %(h_order_last_id)s LIMIT %(LIMIT)s;'
        cursor.execute(query, {'h_order_last_id': h_order_last_id,
                               'LIMIT': LIMIT})

        for row in cursor.fetchall():
            OrderID, *_ = row
            query = 'INSERT INTO core.h_order (order_id) VALUES (%(OrderID)s);'
            cursor.execute(query, {'OrderID': OrderID})
            added_orders_ids.append(OrderID)

        conn.commit()


    # id последнего скопированного элемента из таблицы core.h_supplier
    cursor.execute("SELECT MAX(product_id) FROM core.h_supplier;")
    supplier_last_id = cursor.fetchone()[0]
    # id последнего скопированного элемента из таблицы stage.Suppliers
    cursor.execute("SELECT MAX(SupplierID) FROM stage.Suppliers;")
    stage_supplier_last_id = cursor.fetchone()[0]

    if supplier_last_id < stage_supplier_last_id:  # есть новые данные - обработаем
        # переносим данные в Хаб h_supplier
        query = 'SELECT SupplierID FROM stage.Suppliers WHERE \
                 SupplierID > %(supplier_last_id)s LIMIT %(LIMIT)s;'
        cursor.execute(query, {'supplier_last_id': supplier_last_id,
                               'LIMIT': LIMIT})
        rows = cursor.fetchall()
        for row in rows:
            SupplierID, *_ = row
            query = 'INSERT INTO core.h_supplier (product_id) VALUES (%(SupplierID)s);'
            cursor.execute(query, {'SupplierID': SupplierID})

        conn.commit()

        for row in rows:  # создадим записи саттелита
            SupplierID, *_ = row
            refresh_s_supplier(cursor, SupplierID)

        conn.commit()


    # === Линки ===

    # l_order_product
    for id in added_orders_ids:  # список добавленных заказов
        query = f'''SELECT
                        ProductID,
                        OrderID
                    FROM stage.OrderDetails
                    WHERE OrderID = %(id)s;'''
        cursor.execute(query, { 'id': id })

        for row in cursor.fetchall():
            ProductID, OrderID = row
            query = f'''INSERT INTO core.l_order_product (
                            h_order_rk,
                            h_product_rk)
                        VALUES (
                                %(ProductID)s,
                                %(OrderID)s
                            );'''
            cursor.execute(query, {
                                    'ProductID': ProductID,
                                    'OrderID': OrderID
                                  })

            l_order_product_rk = cursor.fetchone()[0]
            added_l_order_product_ids.append(l_order_product_rk)

    # l_product_supplier
    for id in added_orders_ids:  # список добавленных заказов
        query = f'''SELECT
                        ProductID,
                        SupplierID
                    FROM stage.Products
                    WHERE OrderID = %(id)s;'''
        cursor.execute(query, { 'id': id })

        for row in cursor.fetchall():
            ProductID, SupplierID = row
            query = f'''INSERT INTO core.l_product_supplier (
                            h_product_rk,
                            h_supplier_rk)
                        VALUES (
                                %(ProductID)s,
                                %(SupplierID)s
                            );'''
            cursor.execute(query, {
                                    'ProductID': ProductID,
                                    'SupplierID': SupplierID
                                  })

    conn.commit()


    # === Сателлиты линков ===

    for id in added_l_order_product_ids:
        query =  '''SELECT
                        l_order_product_rk,
                        h_order_rk,
                        h_product_rk
                    FROM core.l_order_product
                    WHERE l_order_product_rk = %(id)s;'''
        cursor.execute(query, { 'id': id })

        for row_link in cursor.fetchall():
            l_order_product_rk, h_order_rk, h_product_rk = row_link

            query = '''SELECT
                        od.UnitPrice,
                        od.Quantity,
                        od.Discount,
                        o.OrderDate,
                        o.RequiredDate,
                        o.Freight,
                        o.ShipAddress,
                        o.ShipCity,
                        o.ShipRegion,
                        o.ShipPostalCode,
                        o.ShipCountry
                    FROM stage.OrderDetails od
                    INNER JOIN stage.Orders o
                        ON od.OrderID = o.OrderID
                    WHERE o.OrderID = %(h_product_rk)s;'''
            cursor.execute(query, {
                                    'h_order_rk': h_order_rk,
                                    'h_product_rk': h_product_rk
                                  })

            for row in cursor.fetchall():
                UnitPrice, Quantity, Discount, OrderDate, RequiredDate, Freight, \
                ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry = row
                query = '''INSERT INTO core.l_s_order_product (
                                l_order_product_rk,
                                UnitPrice,
                                Quantity,
                                Discount,
                                OrderDate,
                                RequiredDate,
                                Freight,
                                ShipAddress,
                                ShipCity,
                                ShipRegion,
                                ShipPostalCode,
                                ShipCountry)
                            VALUES (
                                    %(l_order_product_rk)s,
                                    %(UnitPrice)s,
                                    %(Quantity)s,
                                    %(Discount)s,
                                    %(OrderDate)s,
                                    %(RequiredDate)s,
                                    %(Freight)s,
                                    %(ShipAddress)s,
                                    %(ShipCity)s,
                                    %(ShipRegion)s,
                                    %(ShipPostalCode)s,
                                    %(ShipCountry)s
                                );'''
                cursor.execute(query, {
                                        'l_order_product_rk': l_order_product_rk,
                                        'UnitPrice': UnitPrice,
                                        'Quantity': Quantity,
                                        'Discount': Discount,
                                        'OrderDate': OrderDate,
                                        'RequiredDate': RequiredDate,
                                        'Freight': Freight,
                                        'ShipAddress': ShipAddress,
                                        'ShipCity': ShipCity,
                                        'ShipRegion': ShipRegion,
                                        'ShipPostalCode': ShipPostalCode,
                                        'ShipCountry': ShipCountry
                                      })


    # ========================================================================
    # Обновляем данные в сателлитах, записываем новые, старые помечаем
    # ========================================================================

    # Актуализируем данные в саттелите s_product.
    # Для этого берём саттелиты с самыми старыми датами в processed_dttm,
    # Сверяем их данные с реальными, которые записаны в талице stage.Products
    query =  '''SELECT
                    h_product_rk,
                    ProductName,
                    QuantityPerUnit,
                    UnitPrice,
                    Discontinued,
                    processed_dttm
                FROM core.s_product
                ORDER BY processed_dttm ASC
                LIMIT %(LIMIT)s;'''
    cursor.execute(query, { 'LIMIT': LIMIT })

    for row in cursor.fetchall():
        h_product_rk, s_ProductName, s_QuantityPerUnit, s_UnitPrice, \
        s_Discontinued, processed_dttm = row

        # По h_product_rk получаем id продукта
        query =  '''SELECT product_id
                    FROM core.h_product
                    WHERE h_product_rk = $(h_product_rk)s
                    LIMIT 1;'''
        cursor.execute(query, { 'h_product_rk': h_product_rk,
                                'LIMIT': LIMIT })

        for product in cursor.fetchall():
            product_id, *_ = product

            # Проверяем изменились ли у каждого продукта данные,
            # сравниваем с сохранёнными
            query = '''SELECT
                        ProductName,
                        QuantityPerUnit,
                        UnitPrice,
                        Discontinued
                    FROM stage.Products
                    WHERE ProductID = $(ProductID)s
                    LIMIT 1;'''
            cursor.execute(query, { 'ProductID': product_id })
            for saved_product in cursor.fetchall():
                ProductName, QuantityPerUnit, UnitPrice, \
                Discontinued = saved_product

                if(s_ProductName, s_QuantityPerUnit, s_UnitPrice, s_Discontinued) \
                  != \
                  (ProductName, QuantityPerUnit, UnitPrice, Discontinued)
                    # обновляем данные, потому что устарели
                    refresh_s_product(cursor, product_id)


    # Актуализируем данные в саттелите s_supplier.
    # Для этого берём саттелиты с самыми старыми датами в processed_dttm,
    # Сверяем их данные с реальными, которые записаны в талице stage.Products
    query =  '''SELECT
                    h_supplier_rk,
                    CompanyName,
                    ContactName,
                    Address,
                    City,
                    Region,
                    PostalCode,
                    Country,
                    Phone,
                    processed_dttm
                FROM core.s_supplier
                ORDER BY processed_dttm ASC
                LIMIT %(LIMIT)s;'''
    cursor.execute(query, { 'LIMIT': LIMIT })

    for row in cursor.fetchall():
        h_supplier_rk, s_CompanyName, s_ContactName, s_Address, s_City, \
        s_Region, s_PostalCode, s_Country, s_Phone, processed_dttm = row

        # По h_supplier_rk получаем id продукта
        query =  '''SELECT supplier_id
                    FROM core.h_supplier
                    WHERE h_supplier_rk = $(h_supplier_rk)s
                    LIMIT 1;'''
        cursor.execute(query, { 'h_supplier_rk': h_supplier_rk,
                                'LIMIT': LIMIT })

        for row_product in cursor.fetchall():
            supplier_id, *_ = row_product

            # Проверяем изменились ли у каждого продукта данные,
            # сравниваем с сохранёнными
            query = '''SELECT
                            CompanyName,
                            ContactName,
                            Address,
                            City,
                            Region,
                            PostalCode,
                            Country,
                            Phone
                    FROM stage.Suppliers
                    WHERE SupplierID = $(SupplierID)s
                    LIMIT 1;'''
            cursor.execute(query, { 'SupplierID': supplier_id })
            for supplier in cursor.fetchall():
                CompanyName, ContactName, Address, City, Region, PostalCode, \
                Country, Phone = supplier

                if(s_CompanyName, s_ContactName, s_Address, s_City, \
                  s_Region, s_PostalCode, s_Country, s_Phone) \
                  != \
                  (CompanyName, ContactName, Address, City, \
                  Region, PostalCode, Country, Phone)
                    # обновляем данные, потому что устарели
                    refresh_s_supplier(cursor, supplier_id)
