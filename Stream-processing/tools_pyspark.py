import time
import signal
from typing import Union
from tools_kafka import Kafka

def stop_all_streams(spark):
    """Останаваливает все стримы"""
    for active_stream in spark.streams.active:
        print(f'Stopping stream: {active_stream}')
        active_stream.stop()


def console_output(df, freq:int=5):
    """Воводит содержимое потока spark в консоль. При этом учитывает, 
    что функция может запускаться из ноутбука jupyter. В таком случае
    сначала сохраняет поток в sink и читает из таблицы
    :param df: DataFrame
    :param freq: периодичность вывода. Кол-во секунд.
                 Если скрипт запущен в jupyter, то это кол-во секунд,
                 после которого происходит считывание записанных данных.
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell in ['ZMQInteractiveShell', 'TerminalInteractiveShell']:
            # ZMQInteractiveShell - Jupyter notebook or qtconsole
            # TerminalInteractiveShell - Terminal running IPython
            # stram = sink(df, path='jupyter_console', form='memory')
            # time.sleep(freq)
            # return stram
            # дописать эту функцию!
            return df.writeStream \
                .format("console") \
                .trigger(processingTime=f'{freq} seconds') \
                .options(truncate=False) \
                .start()
            
    except NameError: # вывод в обычную консоль
        return df.writeStream \
            .format("console") \
            .trigger(processingTime=f'{freq} seconds') \
            .options(truncate=False) \
            .start()
        
def sink(df, 
         path:str,
         form:str='memory', 
         checkpoint:str='', 
         freq:int=5, 
         timeout:int=0,
         json:bool=False):
    """Сохраняет данные в spark, используя механизмы "sink".
    Может сохранить как в память, так и в файл
    :param df: pyspark.sql.dataframe.DataFrame
    :param form: сохранить в файлах, в памяти или kafka: memory, kafka, parquet
    :param path: если form = memory: название таблицы в памяти
                 если form = kafka: топик
                 если form = parquet: путь к файлу
    :param checkpoint: путь к файлу чекпойнта
    :param freq: периодичность вывода. Кол-во секунд
    :param timeout: кол-во секунд, через сколько остановить поток.
                    Если ноль, то не остановит (доработать эту функцию)
    :param json: работает в режиме sink -> kafka
                    Если True, то передаёт в kafka строки в формате json 
    :return: DataFrame
    """
    if 'DataFrame' not in str(type(df)):
        print('Принимает только объекты <pyspark.sql.dataframe.DataFrame>')
        return
        
    if freq <= 1:
        freq = 1
    
    dfr = df
    if form == 'memory':
        dfr = df.writeStream \
            .format("memory") \
            .queryName(path) \
            .trigger(processingTime='%s seconds' % freq )
        
    elif form == 'kafka':
        kf = Kafka()
        if path not in kf.ls():
            print(f'Такого топика не существует: {path}')
            print(f'Создаём топик: {path}')
            t = kf.add(name=path, retention=86400*30)
            
        if not checkpoint:
            checkpoint = 'checkpoint_sink_default'
            print(f'Не было передано значение checkpoint.'\
                  f'Указываем принудительно: {checkpoint}')
        
        if json:
            dfr = dfr.selectExpr("CAST(null AS STRING) as key", 
                                 "CAST(to_json(struct(*)) AS STRING) as value")
        else:
            dfr = dfr.selectExpr("CAST(null AS STRING) as key", 
                                 "CAST(struct(*) AS STRING) as value")
        
        dfr = dfr.writeStream \
            .format("kafka") \
            .option("topic", path) \
            .option("kafka.bootstrap.servers", kf.SERVERS)
        
    else:
        dfr = df.writeStream \
            .format("parquet") \
            .trigger(processingTime='%s seconds' % freq ) \
            .option("path", path)
    
    if checkpoint and form == 'memory':
        checkpoint = ''
        print(f'Значение checkpoint передано, но не будет учтено для режима form=memory')
        
    if checkpoint:
        dfr = dfr.option("checkpointLocation", checkpoint)
    
    dfr.start()
        
    # try:
    #     signal.alarm(timeout)
    #     исполняемый код, который надо прервать
    #     signal.alarm(0)
    # except Exception as e:
    #     print(e)

    return dfr
