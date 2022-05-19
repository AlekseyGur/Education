import psycopg2


SERVER_IP = '192.168.122.153'
tables = {}  # {название_таблицы: {'coulumns': [(название_колонок, тип_данных)], 'records_count': кол-во строк}.

conn_string_from = f"host='{SERVER_IP}' port=54320 dbname='my_database' user='root' password='postgres'"
conn_string_to = f"host='{SERVER_IP}' port=5433 dbname='my_database' user='root' password='postgres'"

# получим все названия таблиц, чтобы скопировать из них информаицю
with psycopg2.connect(conn_string_from) as conn, conn.cursor() as cursor:
    # получаем список названий таблиц
    query = 'SELECT relname FROM pg_stat_user_tables;'
    cursor.execute(query)
    tbl_names = cursor.fetchall()

    # получаем количество записей в таблицах
    for table_name, *_ in tbl_names:
        query = f'SELECT COUNT(*) FROM {table_name};'
        cursor.execute(query)
        rows_count, *_ = cursor.fetchone()
        tables[table_name] = {}
        tables[table_name].update({'records_count': rows_count})

    # Запомним названия и типы колонок из каждой таблицы, чтобы создать в новой базе.
    # Не будем сохранять дополнительные атрибуты типа ключей и NOT NULL
    for table_name in tables:
        query = f"SELECT \
                        a.attname as Column, \
                        pg_catalog.format_type(a.atttypid, a.atttypmod) as Datatype \
                    FROM \
                        pg_catalog.pg_attribute a \
                   WHERE \
                        a.attnum > 0 \
                        AND NOT a.attisdropped \
                        AND a.attrelid = ( \
                            SELECT c.oid \
                            FROM pg_catalog.pg_class c \
                                LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace \
                            WHERE c.relname ~ '^({table_name})$' \
                                AND pg_catalog.pg_table_is_visible(c.oid) \
                        );"

        cursor.execute(query)
        clmns = cursor.fetchall()

        tables[table_name].update({'coulumns': clmns})

# выгружаем данные из старой базы в файлы
conn_string= f"host='{SERVER_IP}' port=54320 dbname='my_database' user='root' password='postgres'"
with psycopg2.connect(conn_string_from) as conn, conn.cursor() as cursor:
    for table in tables:
        q = f"COPY {table} TO STDOUT WITH DELIMITER ',' CSV HEADER;"
        with open(f'/tmp/{table}.csv', 'w') as f:
            cursor.copy_expert(q, f)
            print(f'Таблица {table} сохранена на диск')
