import psycopg2
import os


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

# загружаем данные из файлов в новую базу
with psycopg2.connect(conn_string_to) as conn, conn.cursor() as cursor:

    # сделаем таблицы в новой базе как в старой
    for table, data in tables.items():
        # сначала удалим таблицы с подобными именами, которые уже могут там быть
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        conn.commit() # комитим транзакцию

        # cоздадим таблицы с идентичными полями
        fields = []
        for name, typ in data['coulumns']: # тут можно изменить типы колонок
            # if 'character varying' in typ:
                # typ = 'character varying(2000)'

            fields.append(f'{name} {typ}')

        fileds = ', '.join(fields)
        query = f"CREATE TABLE {table} ({fileds})"
        cursor.execute(query) # выполнение запроса
        conn.commit() # комитим транзакцию

    # выполним копирование данных
    for table, _ in tables.items():
        with open(f'/tmp/{table}.csv', 'r') as f:
            q = f"COPY {table} from STDIN WITH DELIMITER ',' CSV HEADER;"
            cursor.copy_expert(q, f)
            print(f'В новую базу загружен файл {table}')
        conn.commit() # комитим транзакцию

# проверяем как данные сохранились из одной базы в другую, подсчитывая количество строк до и после переноса
with psycopg2.connect(conn_string_to) as conn, conn.cursor() as cursor:
    cursor.execute(f'SELECT relname, n_tup_ins - n_tup_del FROM pg_stat_user_tables;')
    tables_new = {name: rows_cnt for name, rows_cnt in cursor.fetchall()}
    tables_old = {name: data['records_count'] for name, data in tables.items()}
    # сравниваем со старыми значениями
    bad_items = [k for k in tables_old if k not in tables_new or tables_old[k] != tables_new[k]]
    if len(bad_items):
        for tbl in bad_items:
            print(f'В таблице {tbl} должно быть {tables_old[tbl]} записей, а перенеслось {tables_new[tbl]}')
            print(f'Исходная таблица содержит следующие колонки:')
            for name, typ in tables[tbl]["coulumns"]:
                print(f'{name} {typ}')
    else:
        print(f'Все данные успешно перенесены!')
        for name, cnt in tables_new.items():
            print(f'В таблице {name} находится {cnt} записей')

# Удаляем csv файлы дампов базы
for table, _ in tables.items():
    os.remove(f'/tmp/{table}.csv')
