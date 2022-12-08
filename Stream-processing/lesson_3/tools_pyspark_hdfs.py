from typing import Union

class Spark_HDFS():
    SC = None # spark context
    FS = None # hdfs FileSystem in spark
    Path = None # функция получения java идентификаторов файлов в hdfs
    
    def __init__(self, spark):
        self.SC = spark.sparkContext
        self.Path = self.SC._jvm.org.apache.hadoop.fs.Path
        self.FS = (self.SC._jvm.org
                  .apache.hadoop
                  .fs.FileSystem
                  .get(self.SC._jsc.hadoopConfiguration()) )
    
    def ls(self, path:str, recursive:bool=False, return_paths:bool=False) -> Union[list, None]:
        """Показывает список файлов в директории HDFS по заданному пути
        :param path: путь к директории внутри HDFS
        :param recursive: рекурсивно
        :param return_list: возвратить список путей к файлам
        """
        status = self.FS.listFiles(self.Path(path), recursive)
            
        files = []
        while status.hasNext():
            p = status.next().getPath().toString()
            files.append(p)
            
        if files:
            print(f'Список файлов в директории {path}:')
            for f in files:
                print(f)
        else:
            print(f'Нет файлов в директории {path}')
        
        if return_paths:
            return files
    
    def read(self, path:str) -> list:
        """Читает содержимое файла в список по строкам
        :param path: путь к файлу внутри HDFS
        :return: список строк
        """
        out = self.FS.openFile(self.Path(path)) \
            .build() \
            .get() #  FSDataInputStreamBuilder
        
        lines = []
        while True:
            ln = out.readLine()
            if ln:
                lines.append(ln)
            else:
                break
                
        return lines
                
    def cat(self, path:str) -> None:
        """Читает содержимое файла в консоль
        :param path: путь к директории внутри HDFS
        """
        print(f'Содержимое файла {path}:')
        lines = self.read(path)
        for ln in lines:
            print(ln)

    def rm(self, path:str, recursive:bool=True) -> bool:
        """Удаляет файл в HDFS по заданному пути
        :param path: путь к файлу внутри HDFS
        :param recursive: удалить рекурсивно
        :return: Ture (если успешно) и False (если проблема)
        """
        res = self.FS.delete(self.Path(path), True)
        msg = f'Файл успешно удалён: {path}' if res else f'Ну удалось удалить файл: {path}'
        print(msg)
        return res

    def put(self, local_file:str, hdfs_file:str, delSrc:bool=False, overwrite:bool=True) -> bool:
        """Копирует локальный файл в HDFS
        :param local_file: путь к локальному файлу 
        :param hdfs_file: путь к файлу внутри HDFS
        :param delSrc: удалить файл-источник после успешной передачи
        :param overwrite: перезаписать файл, если он уже существует
        :return: Ture (если успешно) и False (если проблема)
        """ 
        res = True
        try:
            self.FS.copyFromLocalFile(delSrc, 
                                 overwrite, 
                                 self.Path(local_file), 
                                 self.Path(hdfs_file)
                                )
        except Exception as e:
            print(e)
            res = False

        msg = f'Файл успешно скопирован: {local_file}' if res else f'Ну удалось скопировать файл: {local_file}'
        print(msg)
        return res 
