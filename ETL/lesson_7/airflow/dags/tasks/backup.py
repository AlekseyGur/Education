from airflow.hooks.postgres_hook import PostgresHook


def make(table_name:str = '', key_field:str = '', chunk_size:int = 10):
    """Делает построчный бэкап указанной базы данных. При этом сравнивая
    значения последнего сохранённого ключа с тем, что сохранён в бэкапе.
    :param str table_name: название таблицы, откуда сохраняется информация
    :param str key_field: название поля-первичного ключа в таблице
    :param str chunk_size: кол-во строк для переноса при одном запуске функции
    """
    # подключения
    src = PostgresHook(postgres_conn_id='postgres_from')
    dest = PostgresHook(postgres_conn_id='postgres_to')

    # курсоры
    src_conn = src.get_conn()
    src_cursor = src_conn.cursor()
    dest_conn = dest.get_conn()
    dest_cursor = dest_conn.cursor()

    # id последнего скопированного элемента
    dest_cursor.execute(f"SELECT MAX({key_field}) FROM {table_name};")
    id = dest_cursor.fetchone()[0]
    if id is None:
        id = 0

    # получаем следующую группу строк после указанного id
    src_cursor.execute(f"SELECT COUNT(*) FROM {table_name} \
                         WHERE {key_field} > {id} LIMIT {chunk_size};")
    count = src_cursor.fetchone()[0]
    if count is None:
        print(f'В таблице {table_name} новых записей не появилось')
        return
    else:
        src_cursor.execute(f"SELECT * FROM {table_name} \
                             WHERE {key_field} > {id} LIMIT {chunk_size};")

        # сохраняем порцию строк в базу бэкапа
        dest.insert_rows(table=table_name, rows=src_cursor)

        print(f'Скопировано {count} новых строк в бэкап таблицы {table_name}')
