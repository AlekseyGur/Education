def schema_cassandra_table(df, primary_key:str=''):
    """Преобразует схему датасета pyspark в список полей и типов для создания таблицы в cassandra"""
    sr = []
    for i in df_cassandra.schema:
        t = 'int'
        if 'String' in str(i.dataType):
            t = 'text'
        sr.append(f" {i.name} {t}")
    
    s = ','.join(sr)
    
    s += f", primary key ({primary_key})"
        
    return s