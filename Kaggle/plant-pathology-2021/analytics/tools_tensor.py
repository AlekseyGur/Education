import tensorflow as tf
import numpy as np
import seaborn as sns
import tensorflow_addons as tfa
import pandas as pd

from matplotlib.image import imread
from sklearn.preprocessing import MultiLabelBinarizer
from skimage import exposure
from glob import glob
from json import dump as json_dump, load as json_load
from os.path import exists, isfile, getctime
from os import makedirs, environ
from datetime import datetime
from time import time

import sys

# Необходимые функции для pipeline, которые используются при работе с моделями
# tensorflow. Пригодны для работы над задачами MultiLabel классификации.
from tools_image import show_img, spectrum, compare, opencv2tensorflow, \
                        skimage2opencv, opencv2skimage, datatype_restore, \
                        crop_box, split_channels, remove_edge_oval, resize, \
                        image_extract_object, increase_contrast


class Model:

    def __init__(self, **kwargs):
        # стандартные параметры
        self.CSV_PATH = ''  # CSV файл с данными
        self.IMG_FOLDER = ''  # Путь к папке с изображениями
        self.IMG_FOLDER_AUGMENTED = ''  # Путь к папке с аугментированными изображениями
        self.VERBOSE = True  # подробный вовод процесса работы скрипта
        self.IMG_WIDTH = 1000  # ширина изображения
        self.IMG_HEIGHT = 668  # высота изображения
        self.BATCH_SIZE = 16  # параметр для машинного обучения
        self.BUFFER_SIZE = 10  # количество предзагруженных изображений, которые стоят в очереди на обработку
        self.LEARNING_RATE = None  # агрессивность обучения
        self.EPOCHS = 1  # Количество эпох машинного обучения
        self.EARLY_STOPPING = 7  # Максимальное количество эпох, в которых не было прогресса перед остановкой обучения
        self.REDUCE_LR_ON_PLATEAU = 3  # Максимальное количество эпох, в которых обучение вышло на плато, после которых будет уменьшен LEARNING_RATE
        self.LIMIT = None  # Максимальное количество изображений для обработки
        self.LIMIT_CLASSES = []  # Тренировать предсказание тольк заданных классов
        self.MEMORY_LIMIT = None  # Ограничение на использование ОЗУ вычислительного устройства (в МБ).
        self.MEMORY_GROWTH = True  # В положении "True" заставляет tensorflow занимать ОЗУ в GPU по мере необходимости.
        self.ONLY_CPU = False  # Использовать только CPU
        self.LABEL = None  # Дополнительная пометка для названия папки с файлами модели
        self.STRATEGY = 'RESIZE'  # стратегия обработки изображения
        self.MODEL = 'ResNet50'  # модель машинного обучения
        self.CLASSES_SAME_SIZE = False,  # Использовать одинаковое количество изображений для всех классов (количество у каждого класса будет уменьшено до минимального по классам)

        # пользовательские параметры презаписывают стандартные
        for key, value in kwargs.items():
            if isinstance(value, str):
                exec("self.%s = '%s'" % (key, value))
            else:
                exec("self.%s = %s" % (key, value))
            print("self.%s = %s" % (key, value))



        # переменные для всего класса
        self.LABEL_LOOKUP = None
        self.DF = None
        self.DEVICES = []

        # список устройств, на которых будут проводиться вычисления
        if not self.DEVICES:
            self.DEVICES = self.init_devices(memory_limit=self.MEMORY_LIMIT,
                                             memory_growth=self.MEMORY_GROWTH,
                                             only_cpu=self.ONLY_CPU,
                                             verbose=self.VERBOSE)

    def run(self):
        # Загрузим данные из файла, получим датасет тензора и датафрейм
        ds, self.DF = self.get_ds_df(csv_path=self.CSV_PATH,
                                     img_folder=self.IMG_FOLDER,
                                     img_folder_augmented=self.IMG_FOLDER_AUGMENTED,
                                     limit=self.LIMIT,
                                     limit_classes=self.LIMIT_CLASSES,
                                     classes_same_size=self.CLASSES_SAME_SIZE,
                                     verbose=self.VERBOSE)
        images_count_fit = len(self.DF.index)

        # Получим список классов и функцию преобразования класса в тензор
        self.LABEL_LOOKUP, classes = self.get_lookup_func(self.DF,
                                                labels_column_name='labels',
                                                verbose=self.VERBOSE)

        # Разделяем выборку на обучающую и проверочную
        train_ds, val_ds = self.split_ds(ds,
                                         self.DF,
                                         self.LABEL_LOOKUP,
                                         batch_size=self.BATCH_SIZE,
                                         shuffle_size=self.BUFFER_SIZE,
                                         prefetch_buffer='AUTOTUNE',
                                         proportion=0.2,
                                         num_parallel_calls='AUTOTUNE',
                                         verbose=self.VERBOSE)

        # Создаём и тренируем модель
        time_fit_start = time()
        model, history = self.model_create_fit(train_ds,
                                          val_ds,
                                          classes=classes,
                                          width=self.IMG_WIDTH,
                                          height=self.IMG_HEIGHT,
                                          learning_rate=self.LEARNING_RATE,
                                          epochs=self.EPOCHS,
                                          verbose=self.VERBOSE)
        time_fit_end = time()

        # Определяем пороги срабатываний модели и точность предсказаний модели,
        # используя тренировочную выборку. Процент верныйх предсказаний должен быть
        # очень высоким. Иначе тренировки было. Недостаточно - "underfitting".
        # Но если точность близка к 100%, то это жуе "overfitting".
        predict_ds, self.DF = self.get_ds_df(csv_path=self.CSV_PATH,
                                     img_folder=self.IMG_FOLDER,
                                     img_folder_augmented=self.IMG_FOLDER_AUGMENTED,
                                     limit=self.LIMIT,
                                     limit_classes=self.LIMIT_CLASSES,
                                     classes_same_size=self.CLASSES_SAME_SIZE,
                                     verbose=self.VERBOSE)  # Этот лимит должден
                                         # совпадать с тем,
                                         # что был при обучении. Иначе неверно
                                         # будут найдены пороги!

        # Получим список классов и функцию преобразования класса в тензор
        self.LABEL_LOOKUP, classes = self.get_lookup_func(self.DF,
                                                saved_labels=classes,
                                                labels_column_name='labels',
                                                verbose=self.VERBOSE)

        # Подготавливает датасет для проверки точности модели после создания.
        predict_ds = self.prepare_ds_rate_check(predict_ds,
                                      self.DF,
                                      self.LABEL_LOOKUP,
                                      num_parallel_calls='AUTOTUNE',
                                      batch_size=self.BATCH_SIZE,
                                      prefetch_buffer='AUTOTUNE',
                                      shuffle_size=0)

        # Сделаем предсказание
        time_predict_start = time()
        prediction = self.predict(model,
                                   predict_ds,
                                   df=self.DF,
                                   classes=classes,
                                   verbose=self.VERBOSE)
        time_predict_end = time()

        # Проверим точность предсказания, получим пороговые значения для классов
        rate, info, predict_sample = self.get_rate_threshold(model,
                                                           self.DF,
                                                           classes=classes,
                                                           predicted=prediction,
                                                           verbose=self.VERBOSE)

        # сохраняем модель с историей и вероятностью предсказания
        self.model_save(model=model,
                        predict_sample=predict_sample,
                        model_name=self.MODEL,
                        preprocess_strategy=self.STRATEGY,
                        info=info,
                        history=history,
                        rate=rate,
                        duration_fit=int(time_fit_end-time_fit_start),
                        duration_predict=int(time_predict_end-time_predict_start),
                        width=self.IMG_WIDTH,
                        height=self.IMG_HEIGHT,
                        images_count_fit=images_count_fit,
                        label=self.LABEL)

        # model, info, predict_sample = self.model_load(verbose=self.VERBOSE)
        # print(predict_sample)

    def predict(self,
                model,
                predict_ds,
                df=[],
                classes:list=[],
                classes_thresholds:dict = {},
                verbose:bool = False):
        """Предсказание .
        :param predict_ds: Датасет, подготовленный для предсказаний
        :param model: модель для предсказаний
        :param classes: список классов, которые содержатся в LABEL_LOOKUP
        :param classes_thresholds: список классов, которые содержатся в
                                   LABEL_LOOKUP, вместе с пороговыми значениями.
                                   Если указывать, то будут возвращены
                                   логические True/False хначения. Иначе цифры
                                   вероятностей.
        :param df: DataFrame, Series или список с путями к файлам изображений.
        :param verbose: Вывод данных об используемых устройствах.
        :return: DataFrame.
        """
        prediction = model.predict(predict_ds)

        if classes:
            prediction = pd.DataFrame(prediction, columns=list(classes))

            if classes_thresholds:
                for cls, val in classes_thresholds.items():
                    prediction[cls] = prediction[cls] > val

        if len(df):
            assert len(df) == len(prediction.index), 'Количество' \
                        ' результатов не совпадает с количеством изображений.' \
                        ' при предсказании были утеряны результаты!'

            prediction = pd.concat([df[['path', 'file_name']], prediction],
                                   axis=1)

        if verbose:
            print('Предсказанные значения:')
            print(prediction)

        return prediction

    def init_devices(self,
                     memory_limit = None,
                     memory_growth:bool = True,
                     only_cpu:bool = False,
                     verbose:bool = False):
        """Готовим вычислительные мощности до совершения любых операций.
        Эта функция должна запускаться в самом начале кода.

        Приоритет использования устройств по убыванию: TPU, GPU, CPU

        :param memory_limit: Ограничение на использование ОЗУ вычислительного
                             устройства (в МБ).
        :param memory_growth: В положении "True" заставляет tensorflow занимать ОЗУ
                              в GPU по мере необходимости.
                              В положении "False" занимает всё ОЗУ устройства без
                              остатка при запуске скрипта. А если GPU кто-то хоть
                              немного использует, то tensorflow покажет ошибку OOM.
                              При этом надо учитывать, что если GPU есть в системе,
                              то tensorflow до него все равно доберётся и использует
                              на свои нужды примерно 1.1 Гб. Поэтому меньше этого
                              значения лучше не указывать - появится ошибка OOM.
        :param only_cpu: Использовать только CPU.
        :param verbose: Вывод данных об используемых устройствах.
        :return: Список устройств, которые надо вызывать через "with()" вокруг
                 блока с вычислениями, которые надо сделать на этих устройствах.
        """
        if self.MEMORY_LIMIT:
            memory_limit=self.MEMORY_LIMIT,
        if self.MEMORY_GROWTH:
            memory_growth=self.MEMORY_GROWTH,
        if self.ONLY_CPU:
            only_cpu=self.ONLY_CPU,
        if self.VERBOSE:
            verbose=self.VERBOSE

        if only_cpu:
            environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
            environ["CUDA_VISIBLE_DEVICES"] = ""

        units = []
        devices = tf.config.list_physical_devices()
        TPUs = [x for x in devices if x.device_type == 'TPU']
        GPUs = [x for x in devices if x.device_type == 'GPU']
        CPUs = [x for x in devices if x.device_type == 'CPU']

        if only_cpu:
            units = tf.config.list_logical_devices('CPU')
            if verbose:
                print(f'Принудительно используется только CPU')
        elif TPUs:
            units = tf.config.list_logical_devices('TPU')
        elif GPUs:
            if not self.DEVICES:  # Physical devices cannot be modified after being initialized
                if memory_growth:
                    for gpu_instance in GPUs:
                        tf.config.experimental.set_memory_growth(gpu_instance, True)
                        if verbose:
                            print(f'Использование ОЗУ по мере необходимости на'\
                                  f' устройстве {gpu_instance}')

                if memory_limit:
                    for gpu_instance in GPUs:
                        tf.config.set_logical_device_configuration(
                            gpu_instance,
                            [tf.config.LogicalDeviceConfiguration(
                                                            memory_limit=memory_limit)])
                        if verbose:
                            print(f'Установлено ограничение на используемую память GPU'\
                                  f' в {memory_limit} МБ на устройстве {gpu_instance}')

            units = tf.config.list_logical_devices('GPU')
        elif CPUs:
            units = tf.config.list_logical_devices('CPU')

        devices_to_use = None
        if len(units) > 1:
            devices_to_use = tf.distribute.MirroredStrategy(units)
            devices_to_use = devices_to_use.scope()
        else:
            devices_to_use = tf.device(units[0])

        if verbose:
            print(f'Используются устройства для вычислений {len(units)} шт.: {units}')

        return devices_to_use

    def get_label(self, df, file_path, label_lookup_function):
        """Возвращает данные labels по определённому пути файла. Данные возвращаютс
        в форме OneHot тензора.
        :param DataFrame df: Столец 'path' - пути к файлам, 'labels' - список классов.
        :param file_path: Путь к файлу, для которого нужно получить 'labels'.
        :param label_lookup_function: функция OneHot преобразования списка 'labels'.
        :return: Возвращает OneHot тензор выбранного файла.
        """
        labels = df[df['path'] == file_path]['labels']
        assert len(labels.index) == 1, 'Файлы в датасете не являются уникальными. ' \
                                       'Невозможно определить вектор классов.'

        return label_lookup_function(labels.iloc[0])

    def get_image(self,
                  file_path:str,
                  width:int,
                  height:int,
                  convert_to_tensor:bool=True):
        """Подготавливает изображение к использованию в модели. Изменяет размер
        изображения (размеры при предсказании должны совпадать с теми, что были
        при ообучении).
        :param file_path: Путь к файлу, который нужно обработать.
        :param int width: Ширина выходного изображения.
        :param int height: Высота выходного изображения.
        :param bool convert_to_tensor: Результат в виде тензора.
        :return: Тензор или изображение.
        """
        img = imread(file_path)

        if 'SELECT_OBJECT' in self.STRATEGY: # выделение центра на изображении, градация серого, изменение размера,
              # применение разных цветовых каналов,
            img, image_mask_size = image_extract_object(img,
                                                        bottom=40,
                                                        top=90,
                                                        bin_size=45)
            if image_mask_size < 15:  # размер объекта на изображении, кол-во % процентов
                img, image_mask_size = image_extract_object(img)

            # делаем контрастность с помощью equalize_adapthist
            img = exposure.equalize_adapthist(img)

        if 'REMOVE_CORNERS' in self.STRATEGY: # выделение центра на изображении (края удаляются), изменение размера
            img, _ = remove_edge_oval(img)

        if 'INCREASE_CONTRAST' in self.STRATEGY: # увеличивает контраст изображения
            img = increase_contrast(img)

        # изменим размер
        # if 'RESIZE' in self.STRATEGY:  # это делать надо всегда
        img = resize(img, width, height)

        # преобразуем обратно в тензор
        if convert_to_tensor:
            img = tf.convert_to_tensor(img, dtype=tf.float32)

        return img

    def process_path(self, file_path):
        """Подготавливает изображения и "labels" к использованию в pipeline для модели.
        :param file_path: Путь к файлу изображения.
        :param DataFrame df: Столец 'path' - пути к файлам, 'labels' - список классов.
        :param label_lookup: функция OneHot преобразования списка 'labels'.
        :return: Тензор изображения и 'labels'
        """
        if not isinstance(self.DF, pd.DataFrame):
            raise NameError('Не найдена глобальная переменная self.DF')
        if not self.LABEL_LOOKUP:
            raise NameError('Не найдена глобальная переменная self.LABEL_LOOKUP')
        if not self.IMG_WIDTH:
            raise NameError('Не найдена глобальная переменная self.IMG_WIDTH')
        if not self.IMG_HEIGHT:
            raise NameError('Не найдена глобальная переменная self.IMG_HEIGHT')

        file_path = bytes.decode(file_path.numpy())

        labels = self.get_label(df=self.DF,
                                file_path=file_path,
                                label_lookup_function=self.LABEL_LOOKUP)

        img = self.get_image(file_path=file_path,
                             width=self.IMG_WIDTH,
                             height=self.IMG_HEIGHT,
                             convert_to_tensor=True)

        return img, labels

    def prepare_ds_rate_check(self,
                              ds,
                              df,
                              label_lookup,
                              num_parallel_calls,
                              batch_size:int,
                              prefetch_buffer,
                              shuffle_size:int = 0):
        """Подготавливает датасет для проверки точности предсказания после
        создания модели.
        :param label_lookup: функция для получения класса изображения
        :param num_parallel_calls: Кол-во параллально обрабатывающихся изображений.
                                   Целое число. Либо строка 'AUTOTUNE', для
                                   автоматического определения.
        :param ds: Тензор с изображениями.
        """
        # Автоматический выбор количества подготваливаемых изображений
        if 'AUTOTUNE' in str(num_parallel_calls):
            num_parallel_calls = tf.data.experimental.AUTOTUNE
        if 'AUTOTUNE' in str(prefetch_buffer):
            prefetch_buffer = tf.data.experimental.AUTOTUNE

        ds = ds.map(lambda x: tf.py_function(self.process_path,
                                             inp=[x],
                                             Tout=[tf.float32, tf.float32]),
                    num_parallel_calls=num_parallel_calls)

        ds = ds.batch(batch_size)
        ds = ds.prefetch(buffer_size=prefetch_buffer)

        # В момент проверки нельзя перемешивать
        # if shuffle_size:
            # ds = self.configure_for_performance(ds,
            #                                batch_size=16,
            #                                prefetch_buffer=prefetch_buffer,
            #                                shuffle_size=16)

        return ds

    def configure_for_performance(self,
                                  ds,
                                  batch_size:int,
                                  prefetch_buffer,
                                  shuffle_size:int = 0):
        """Задаёт параметры pipeline для улучшения производительности модели.
        Чтобы не все изображения читались с диска одновременно, а небольшими
        порциями по мере необходимости.
        :param ds: Тензор изображений.
        :param shuffle_size: - ?
        :param prefetch_buffer: - ? Кол-во параллально обрабатывающихся изображений.
                                   Целое число. Либо строка 'AUTOTUNE', для
                                   автоматического определения.
        :param batch_size: - ?
        :return: Тензор изображений.
        """
        # Автоматический выбор количества подготваливаемых изображений
        if 'AUTOTUNE' in str(prefetch_buffer):
            prefetch_buffer = tf.data.experimental.AUTOTUNE

        ds = ds.cache()
        if shuffle_size:
            ds = ds.shuffle(buffer_size=shuffle_size)
        ds = ds.batch(batch_size)
        ds = ds.prefetch(buffer_size=prefetch_buffer)
        return ds

    def get_ds_df(self,
                  csv_path:str,
                  img_folder:str = '',
                  img_folder_augmented:str = '',
                  limit:int = None,
                  limit_classes:list = [],
                  classes_same_size:bool = False,
                  verbose:bool = False):
        """Загружает данные из CSV файла и изображения. Возвращает тензор для
        машинного обучения.
        :param str csv_path: csv файл, в котором есть колонки
            'image' - название файлов изображений
            'labels' - строка с классами изображении (через пробел: 'one two three')
        :param str img_folder: Путь к папке со всеми изображениями.
                                Например: 'source/train_images/'
        :param str img_folder_augmented: Путь к папке с изменёнными изображениями, у
                                которых перед расширением стоит порядковый
                                номер версии. Например:
                                'source/train_images_aug/12387_1.jpg'
                                'source/train_images_aug/12387_2.jpg'
                                'source/train_images_aug/12387_3.jpg'
                                При этом первая часть названия файла должна
                                совпадать с оригиналом, из которого был
                                образовано аугментированное изображение.
        :param int limit: Максимальное количество изображений, которое нужно
                          использовать. Если 0, то используются все фото.
        :param list limit_classes: Использовать только определённые классы.
                                   Если None, то все возможные
        :param verbose: Вывод данных об используемых устройствах.
        :param classes_same_size: Использовать одинаковое количество изображений для
                            всех классов (количество у каждого класса будет
                            уменьшено до минимального по классам)
        :return: Возвращает несколько значений:
            Тензор,
            Список файлов в тензоре,
            DataFrame, в котором есть два столбца:
                'path' - название файлов изображений
                'labels' - списки с классами изображении (['one', 'two', 'three'])
        """
        # загрузим данные из файла (список изображений и болезней)
        source = pd.read_csv(csv_path)
        if limit_classes:
            source = source[source['labels'].isin(limit_classes)]

            assert len(source.index) != 0, f'Нет данных с классами {limit_classes}'

            if classes_same_size:
                # Все классы должны быть представлены равномерно. Поэтому
                # выбираем определённое количество изображений из каждого класса
                add = []
                min_amount = source['labels'].value_counts()[-1]
                for cls in limit_classes:
                    add.append(source[source['labels']==cls][:min_amount])

                source = pd.concat(add)

                if verbose:
                    print('Количество элементов в классах сделано равным')

                # Общий лимит должен срабатывать так, количество классом
                # оставалось равномерным
                if limit and limit < len(source.index):
                    source = source.sample(frac=1).reset_index(drop=True)[0:limit]

            if verbose:
                print('Количество элементов в классах:')
                print(source['labels'].value_counts())

        if verbose:
            print(f'Загружаем данные датасета из файла: {csv_path}')
            print(f'Количество записей в файле: {len(source.index)}')

        # разделим строку из названий классов на список
        df = pd.DataFrame()
        df['labels'] = source['labels'].str.split(' ')
        df['file_name'] = source['image']
        df['path'] = img_folder + source['image']
        if verbose:
            print(f'Сделали подготовку классов в датасете')

        # добавляем аугментированные фото. Этот процесс очень долгий, потому
        # что выполняется на одном ядре.
        if img_folder_augmented:
            add = []
            if verbose:
                print(f'Добавляем файлы аугментации из: {img_folder_augmented}')

            if 1:  # собираем все что можно по типу '.../12387_3.jpg', потом все
                   # равно удалим несуществующие
                max_num = 0
                aug_amount = 0
                for aug_path in glob(img_folder_augmented + '*'):
                    aug_amount += 1
                    # Файлы аугментации имеют вид:
                    # '.../12387_1.jpg'
                    # '.../12387_2.jpg'
                    # '.../12387_3.jpg'
                    # Получим максимальный номер копии, который после _ (в примере выше - это 3)
                    file_num_ext = int(aug_path.split('/')[-1].split('_')[-1].split('.')[0])
                    if max_num < file_num_ext:
                        max_num = file_num_ext

                if max_num:
                    if verbose:
                        print(f'Нашли файлов аугментации: {aug_amount}')

                    for i in range(1, max_num):
                        m = df.copy()
                        m['path'] = m['path'].str.split('.').str[0]  # отрезали .jpg
                        m['path'] = m['path'].str.split('/').str[-1]  # отрезали путь ../ осталось только имя файла
                        m['path'] = img_folder_augmented + m['path'] + '_' + str(i) + '.jpg'
                        add.append(m[['labels', 'path']])

                    add_df = pd.concat(add)
                    df = pd.concat([df, add_df])

                    if verbose:
                        print(f'Закончили сбор файлов аугментации')
                        print(df)


            if 0:  # способ точного сбора файлов (медленный из-за функции поиска по датасету)
                df_aug = pd.DataFrame()
                df_aug['labels'] = source['labels'].str.split(' ')
                df_aug['file_name'] = source['image'].str.split('.').str[0]  # '12387'
                df_aug['path'] = img_folder + source['image']  # '.../12387.jpg'

                for aug_path in glob(img_folder_augmented + '*'):
                    # У аугментированных файлов перед расширением стоит
                    # порядковый номер версии. Например:
                    # '.../12387_1.jpg'
                    # '.../12387_2.jpg'
                    # '.../12387_3.jpg'
                    file_name = aug_path.split('/')[-1].split('_')[-2]  # '12387'
                    m = df_aug[df_aug['file_name'] == file_name].copy()

                    if len(m.index):
                        m['path'] = img_folder_augmented + m['file_name']
                        add.append(m[['labels', 'path']])
                        if verbose:
                            print(f'Добавляем аугментированный файл {aug_path}')
                            print(m)

                if verbose:
                    print(f'Нашли файлов аугментации: {len(add)}')

                add_df = pd.concat(add)
                df = pd.concat([df, add_df])

                if verbose:
                    print(f'Закончили сбор файлов аугментации')

        # оставим только те данные, по которым есть файлы изображений
        images = []
        for pth in df['path'].to_list():
            if isfile(pth):
                images.append(pth)
            else:
                print(f'Не найден файл изображения: {pth}')

        if limit:  # ограничение на количество файлов
            images = images[0:limit]


        df = df[df['path'].isin(images)].reset_index(drop=True)

        if verbose and limit:
            print(f'Установлен лимит в {limit} элементов для всей выборки:')
            print(df['labels'].value_counts())

        assert len(df.index) != 0, f'Не найдено ни одного файла из' \
                                   f' датасета в папке {img_folder}'

        if limit and (len(df.index) < limit):
            print(f'Найдено меньше изображений, чем запрашивается' \
                  f' лимитом: {len(df.index)}')


        # сделаем тензор
        ds = tf.data.Dataset.list_files(df['path'], shuffle=False)
        image_count = len(ds)
        if verbose:
            print(f'Всего изображений: {image_count}')

        # Сохраним пути к файлам (понадобится на стадии определения точности модели)
        # ds_paths = [b.decode("utf-8") for b in ds.as_numpy_iterator()]

        return ds, df

    def get_lookup_func(self,
                        df,
                        labels_column_name:str = 'labels',
                        saved_labels:dict = {},
                        verbose:bool = False):
        """Создаёт функцию для кодирования labels в oneHot.
        :param df: DataFrame с колонкой, в которой классы
                   записаны списком. К примеру, ['one', 'two', 'three']
        :param labels_column_name: Название колонки с классами
        :param saved_labels: Список классов, которые должны быть. Если задано, то
                             классы из датафрейма df игнорируются. Используется во
                             время предсказаний, когда обрабатывать весь df
                             заново нет возможности. Пример значения:
                             ['one', 'two', 'three']
        :param verbose: Вывод данных одного случайного значения.
        :return: Возвращает два объекта:
                 1. Функцию, которой надо передать список классов
                    ['one', 'two'], а в ответ получаешь [0, 1, 1, 0]
                 2. Словарь возможных классов.
                    Например ['[UNK]', 'one', 'two', 'three']
        """
        labels = None
        if saved_labels:
            labels = tf.ragged.constant(list(saved_labels))
        else:
            labels = tf.ragged.constant(df[labels_column_name].values)

        label_lookup = tf.keras.layers.StringLookup(output_mode="multi_hot")
        label_lookup.adapt(labels)
        # vocab = {i: 0 for i in label_lookup.get_vocabulary()}
        vocab = label_lookup.get_vocabulary()

        if verbose:
            print("Словарь:")
            print(vocab)

            if len(df['labels'].index):
                sample_label = df['labels'].iloc[0]
                print(f"Пример классов у элемента: {sample_label}")

                label_binarized = label_lookup(sample_label)
                print(f"Пример классов у элемента в OneHot представлении: {label_binarized}")

        return label_lookup, vocab

    def split_ds(self,
                 ds,
                 df,
                 label_lookup,
                 num_parallel_calls,
                 batch_size:int,
                 shuffle_size:int,
                 prefetch_buffer:int,
                 proportion:float = 0.2,
                 verbose:bool = False):
        """Разбивает датасет на тестовую и проверочную выборку.

        :param label_lookup: функция для получения класса изображения
        :param int batch_size: - ?
        :param int shuffle_size: - ?
        :param int prefetch_buffer: - ?
        :param num_parallel_calls: Кол-во параллально обрабатывающихся изображений.
                                   Целое число. Либо строка 'AUTOTUNE', для
                                   автоматического определения.
        :param float proportion: Доля проверочной выборки.
        :param verbose: Вывод информации о выборках.
        :return: тестовый, проверочный датасет
        """
        ds_paths = [b.decode("utf-8") for b in ds.as_numpy_iterator()]
        image_count = len(ds_paths)

        # Автоматический выбор количества подготваливаемых изображений
        if 'AUTOTUNE' in str(num_parallel_calls):
            num_parallel_calls = tf.data.experimental.AUTOTUNE

        # перемешиваем (если запускать много раз, то можно выбрать модель с
        # лучшей предсказательной силой. Таким способом можно добавить ~15% к
        # предсказательной силе модели).
        ds = ds.shuffle(image_count, reshuffle_each_iteration=False)

        # разбиваем на две группы для тренировки модели
        val_size = int(image_count * proportion)
        train_ds = ds.skip(val_size)  # тренировочная выборка
        val_ds = ds.take(val_size)  # проверочная выборка

        if verbose:
            # пути к файлам
            train_ds_path = [b.decode("utf-8") for b in train_ds.as_numpy_iterator()]
            val_ds_path = [b.decode("utf-8") for b in val_ds.as_numpy_iterator()]

            print(f'Файлов в тестовой выборке: {len(train_ds_path)}')
            print(f'Файлов в проверочной выборке: {len(val_ds_path)}')

        # Используем py_function. Иначе внутрь функции будет передаваться не
        # значение элемента, а тензор
        train_ds = train_ds.map(lambda x: tf.py_function(self.process_path,
                                                         inp=[x],
                                                         Tout=[tf.float32, tf.float32]),
                                num_parallel_calls=num_parallel_calls)

        val_ds = val_ds.map(lambda x: tf.py_function(self.process_path,
                                                     inp=[x],
                                                     Tout=[tf.float32, tf.float32]),
                                num_parallel_calls=num_parallel_calls)

        # Задаём флаг кеширования и т.п.
        train_ds = self.configure_for_performance(train_ds,
                                             batch_size=batch_size,
                                             prefetch_buffer=prefetch_buffer,
                                             shuffle_size=shuffle_size)

        val_ds = self.configure_for_performance(val_ds,
                                           batch_size=batch_size,
                                           prefetch_buffer=prefetch_buffer,
                                           shuffle_size=shuffle_size)
        return train_ds, val_ds

    def get_rate_threshold(self,
                           model,
                           df,
                           predicted,
                           classes:list,
                           verbose:bool = False):
        """Вычисляет предсказательную силу модели и пороговые значения для классов
        модели (объяснение далее). Прмиеняется на той же выборке, на которой
        проходило обучение, чтобы проверить всё ли правильно работает.

        Проблема в том, что модель может возвращать вероятность того, что объект
        относится к классу (число от 0 до 1). А сделать последний вывод
        "Да, относится к классу" или "Нет, не относится к классу" мы должны сами.
        Для этого зададим порог, при котором можно считать, что "Да". К примеру,
        предположим, что если выше 0.87, то это "Да". Но такой порог есть у каждого
        параметра и он может быть разным.

        Поэтому после создания модели надо сразу определить пороги для каждого
        класса. Для этого cделаем предсказания по тренировочным данным (на которых
        обучали модель) и сравним с теоретическим значением, при этом меняя порог для
        каждого параметра, чтобы получить наибольшую вероятность предсказания.

        К примеру, предсказали и получили список значений. Задали порог
        равный "0.87". Проверили сколько значений совпадает с теоретическими.
        Повторили процедуру до тех пор, пока не нашли лучшее значение порога.

        :param model: Проверяемая модель машинного обучения.
        :param classes: Список классов MultyLabel, который был создан во
                        время тренировки модели
        :param predicted: Предсказанные значения классов для файлов, указанных в df.
        :param df: DataFrame, в котором есть два столбца:
            'path' - название файлов изображений, по которым будет идти проверка
            'labels' - списки с классами изображении (['one', 'two', 'three'])
        :param verbose: Подробный вывод результата.
        :return: Вероятность верного предсказания всех классов одновременно;
                 значения уровней для каждого класса, при которых можно
                    считать предсказание верным;
                 значения (в %) уровней для каждого класса, при которых можно
                    считать предсказание верным.
        """
        assert len(predicted.index) == len(df.index), \
            f'Предсказанных результатов {len(predicted.index)} != {len(df.index)} входных изображений'

        # Классы без неопознанных '[UNK]' (нужно, если использовался tensorflow)
        classes_clean = [i for i in classes if i != '[UNK]']

        # В этом словаре будет названия классов и соответствующие им пороги (значения)
        threshold = {k: 0 for k in classes_clean}
        # В этой копии вероятность будет сохраняться в %
        threshold_prc = threshold.copy()
        # В этой копии максимальные значения классов
        threshold_max = threshold.copy()

        # сделаем преобразование OneHot со всеми столбцами из предсказываемых параметров
        mlb = MultiLabelBinarizer(classes=classes)

        real = pd.DataFrame(mlb.fit_transform(list(df['labels'])),
                                 columns=mlb.classes_,
                                 index=df.index)

        # Количество полей в новой выборке и в сохранённой должны одинаковым
        # если какие-то поля пропущены, то добавляем их со значением False
        for col_real in classes_clean:
            if col_real not in real.columns:
                real[col_real] = False

        real = real > 0  # переведём числа 0 и 1 в False и True

        # добавим колонку путей, чтобы по ней объединять результат
        real['path'] = df['path']

        # нужно, если использовался tensorflow
        real.drop('[UNK]', axis=1, errors='ignore', inplace=True)

        # список классов со значениями для валидации
        classes_valid = [i + '_valid' for i in classes_clean]

        # восстанавливаем названия столбцов после предсказания
        # pred = pd.DataFrame(predicted, columns=classes)
        pred = predicted[list(classes)]
        pred.drop('[UNK]', axis=1, errors='ignore', inplace=True)  # нужно, если использовался tensorflow

        # добавляем адреса файлов (почему без ".to_list()" не работает? разобраться)
        # pred['path'] = df['path'].to_list()

        pred = pd.concat([df['path'], pred], axis=1)
        print('pred')
        print(pred)


        # выберем только записи по тем файлам, которые есть в выборке
        real = real[real['path'].isin(pred['path'].to_list())]

        # делаем один тип колонкам, по которым собираемся объединять таблицы
        pred['path'] = pred['path'].astype("string")
        real['path'] = real['path'].astype("string")

        # объединяем таблицы предсказаний с таблицей для валидации
        res = pd.merge(pred,
                       real,
                       on = 'path',
                       how = 'left',
                       suffixes=('', '_valid'))

        # Проходимся по всем колонкам, подбирая наилучший порог для каждого
        # параметра, при котором максимальное количество совпадений с теорией.
        for col in list(classes_clean):
            if col == 'path':  # не относится к классам
                continue
            # if col == 'healthy':  # разберёмся с ним потом
            #     continue
            if col == '[UNK]':  # нужно, если использовался tensorflow
                continue

            for prc in range(0, 101):  # порог от 0% до 100% для подбора лучшего значения
                column_train = res[col]  # колонка с предсказанными данными
                column_valid = res[col + '_valid']  # колонка с реальными

                column_max = max(column_train)  # максимум по предсказаниям в колонке
                if threshold_max[col] < column_max:
                    threshold_max[col] = column_max

                # значение, выше которого считать предсказание верным
                threshold_value = column_max * prc / 100

                column_train = column_train > threshold_value

                # вероятность успешного предсказания
                rate = 100 * sum(column_train == column_valid) / len(column_valid)

                # если вероятность улучшилась, то перезаписываем значение порога
                if threshold_prc[col] < rate:
                    threshold[col] = threshold_value
                    threshold_prc[col] = rate

        if verbose:
            for col in list(classes_clean):
                print(f'Для параметра "{col}" лучший порог = {threshold[col]} ' \
                      f', что составляет {round(threshold_prc[col], 2)}%' \
                      f' от максимума')

        # применяем полученные оптимальные значения порогов, чтобы преобразовать
        # данные из чисел в бинарные
        for col, v in threshold.items():
            # if col == 'healthy':  # разберёмся с ним потом
            #     continue
            if col == '[UNK]':  # нужно, если использовался tensorflow
                continue

            res[col] = res[col] >= v

        # в столбце 'healthy' должно быть положительное значение только тогда,
        # когда болезней вообще нет (в других полях пусто)
        # res['healthy'] = res[classes_clean].iloc[:, pred[classes_clean].columns != 'healthy'].apply(lambda row: not any(row.values), axis=1)

        # Вычислим насколько точно модель предсказывает все классы одновременно.
        # Для этого соединяем все столбцы вместе, чтобы получить списоки, как это
        # сделано в исходных данных. Для этого переводим OneHot в обратно список
        real = res[classes_valid].apply(lambda row: [col_name.rstrip('_valid') for col_name, v in zip(classes_valid, row.values) if v], axis=1)
        pred = res[classes_clean].apply(lambda row: [col_name for col_name, v in zip(classes_clean, row.values) if v], axis=1)

        # Получились колонки со списками из классов (['one', 'two', 'three']).
        # Перед сравнением надо отсортировать эти списки, т.к. они могут
        # быть в неправильном порядке.
        real = real.apply(lambda x: sorted(x))
        pred = pred.apply(lambda x: sorted(x))

        # вероятность правильного предсказания (в %)
        rate = round(100.0 * sum(real == pred) / len(real), 5)

        print(f'Вероятность правильного предсказания по тестовой выборке: {rate} %')
        predict_sample = pd.concat([predicted['file_name'],
                                    real.rename('Real'),
                                    pred.rename('Predicted')],
                                   axis=1)
        if verbose:
            print(predict_sample)

        # Тут стоило бы сделать вывод графика "Normalized confusion matrix". Но пока
        # не знаю как его лучше сделать для MultyLabel классификации. Такой график
        # нужен, чтобы понимать, какой именно класс хуже предсказывается.
        # Код ниже работает верно только если в выборке
        # присутствуют все классы. Иначе неверно делается OneHot.
        # Чтобы избежать ошибки, надо проверять колич-во уникальных значений:
        cls_pred = None
        if len(set(real.sum())) == len(set(pred.sum())):
            realt = MultiLabelBinarizer(classes=classes_clean).fit_transform(real)
            predt = MultiLabelBinarizer(classes=classes_clean).fit_transform(pred)
            right_prc = MultiLabelBinarizer(classes=classes_clean).fit_transform(real[real==pred])

            reals = pd.DataFrame(realt, columns=classes_clean).sum().rename('Real')
            preds = pd.DataFrame(predt, columns=classes_clean).sum().rename('Predicted')
            right_prcs = pd.DataFrame(right_prc, columns=classes_clean).sum()

            prc = 100 * preds / reals
            prc = prc.round().rename('amount %')

            right_prcs = 100 * right_prcs / reals
            right_prcs = right_prcs.round().rename('correct %')

            print(f'Общее количество предсказаний по значениям:')
            cls_pred = pd.concat(
                [reals,
                 preds,
                 prc,  # сумма пресказанных * 100 / сумма теоретических
                 right_prcs]  # % верно пресказанных
            ,axis=1)
            print(cls_pred)

        info = {
            'accuracy': rate,
            'predicted_amount': cls_pred.to_dict() if isinstance(cls_pred, pd.DataFrame) else {},
            'classes': list(threshold),
            'threshold': {
                'val': threshold,
                'prc': threshold_prc,
                'max': threshold_max,
            },
        }

        return rate, info, predict_sample

    def model_create_fit(self,
                         train_ds,
                         val_ds,
                         classes:list,
                         width:int,
                         height:int,
                         learning_rate:float,
                         epochs:int = 18,
                         verbose:bool = False):
        """Создаёт модель, тренирует её и возвращает вместе с историей тренировки.
        :param train_ds: тестовый датасет
        :param val_ds: проверочный датасет
        :param list classes: Список возможных классов ['[UNK]', 'one', 'two']
        :param int width: Ширина входящего изображения.
        :param int height: Высота входящего изображения.
        :param int epochs: Количество эпох машинного обучения.
        :param float learning_rate: Параметр агрессивности обучения машины.
                                    Если None, то брать стандартный.
        :param verbose: Подробный вывод
        :return: Модель, история тренировки
        """

        if verbose:
            print(f'Будет тренироваться модель {self.MODEL}')

        def create_model(model_classes, width, height):
            # https://keras.io/api/applications/#usage-examples-for-image-classification-models

            # https://medium.com/deep-learning-with-keras/how-to-solve-multi-label-classification-problems-in-deep-learning-with-tensorflow-keras-7fb933243595

            # https://datascience.stackexchange.com/questions/102913/problem-with-using-f1-score-with-a-multi-class-and-imbalanced-dataset-lstm

            # Если задача состоит в multi-label classification, то надо:
            # - кодировать все labels в multi-hot vector
            # - activation = sigmoid  # это точно должна быть не softmax,
            #                         # потому что softmax может предсказать
            #                         # только одни лейбл, а у нас
            #                         # мультилейбл классификация!
            # - loss = BinaryCrossentropy()
            # - accuracy metric = BinaryAccuracy()

            if self.MODEL == 'ResNet152V2':
                inputs = tf.keras.Input(shape=(height, width, 3))
                x = tf.keras.applications.ResNet152V2(include_top=False,
                                                      weights=None)(inputs)

                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                outputs = tf.keras.layers.Dense(len(model_classes),
                                                        activation="sigmoid",
                                                        dtype='float32')(x)

                model = tf.keras.Model(inputs, outputs)
                return model

            if self.MODEL == 'ResNet50':
                inputs = tf.keras.Input(shape=(height, width, 3))
                x = tf.keras.applications.resnet50.ResNet50(include_top=False,
                                                            weights=None)(inputs)

                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                outputs = tf.keras.layers.Dense(len(model_classes),
                                                activation="sigmoid",
                                                dtype='float32')(x)

                model = tf.keras.Model(inputs, outputs)
                return model

            if self.MODEL == 'MobileNetV2':
                inputs = tf.keras.Input(shape=(height, width, 3))
                x = tf.keras.applications.MobileNetV2(include_top=False,
                                                      weights=None)(inputs)

                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                outputs = tf.keras.layers.Dense(len(model_classes),
                                                activation='sigmoid')(x)

                model = tf.keras.models.Model(inputs, outputs)
                return model

            if self.MODEL == 'MobileNetV3Large':
                inputs = tf.keras.Input(shape=(height, width, 3))
                x = tf.keras.applications.MobileNetV3Large(
                    alpha=1.0,
                    minimalistic=False,
                    include_top=False,
                    weights=None,
                    input_tensor=None,
                    classes=len(model_classes),
                    pooling=None,
                    dropout_rate=0.2,
                    classifier_activation='sigmoid',
                    include_preprocessing=True
                )(inputs)

                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                outputs = tf.keras.layers.Dense(len(model_classes),
                                                activation="sigmoid",
                                                dtype='float32')(x)

                model = tf.keras.Model(inputs, outputs)
                return model

            if self.MODEL == 'EfficientNetV2L':
                inputs = tf.keras.Input(shape=(height, width, 3))
                x = tf.keras.applications.EfficientNetV2L(
                    include_top=False,
                    weights=None,
                    input_tensor=None,
                    pooling=None,
                    classes=len(model_classes),
                    classifier_activation="sigmoid",
                    include_preprocessing=True
                )(inputs)

                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                outputs = tf.keras.layers.Dense(len(model_classes),
                                                activation="sigmoid",
                                                dtype='float32')(x)

                model = tf.keras.Model(inputs, outputs)
                return model

        def compile_model(model, model_classes, lr):
            # https://keras.io/examples/nlp/multi_label_classification/

            optimizer = None
            if learning_rate:
                optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
            else:
                optimizer = tf.keras.optimizers.Adam()
            loss = tf.keras.losses.BinaryCrossentropy()
            # loss = tf.keras.losses.CategoricalCrossentropy()  # только 1 класс за раз
            # loss = tf.keras.metrics.CategoricalAccuracy(name='categorical_accuracy')
            # metrics = ["categorical_accuracy"]

            metrics = [
                tfa.metrics.F1Score(num_classes=len(model_classes),
                                    average="macro",
                                    name="f1_score",
                                    threshold=0.5)
            ]

            model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
            # model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["categorical_accuracy"])
            # model.compile(loss='binary_crossentropy',
            #               optimizer=tf.keras.optimizers.Adam(lr=1e-4),
            #               metrics=metrics)
            return model

        def create_callbacks(metric, verbose):

            cpk_path = 'models/best_model.h5'

            checkpoint = tf.keras.callbacks.ModelCheckpoint(
                filepath=cpk_path,
                monitor=metric,
                mode='max',
                save_best_only=True,
                verbose=verbose
            )

            reducelr = tf.keras.callbacks.ReduceLROnPlateau(
                monitor=metric,
                mode='max',
                factor=0.01,
                patience=self.REDUCE_LR_ON_PLATEAU,
                verbose=0
            )

            earlystop = tf.keras.callbacks.EarlyStopping(
                monitor=metric,
                mode='max',
                patience=self.EARLY_STOPPING,
                verbose=verbose
            )

            callbacks = []

            if self.REDUCE_LR_ON_PLATEAU:
                callbacks.append(earlystop)

            if self.EARLY_STOPPING:
                callbacks.append(earlystop)

            # callbacks = [checkpoint, reducelr, earlystop]
            return callbacks

        # tf.keras.backend.clear_session()

        history = None

        self.DEVICES = self.init_devices()
        with self.DEVICES:

            model = create_model(classes, width, height)
            model = compile_model(model, classes, learning_rate)

            METRIC = "val_f1_score"
            callbacks = create_callbacks(METRIC, verbose)

            history = model.fit(train_ds,
                                epochs=epochs,
                                callbacks=callbacks,
                                validation_data=val_ds,
                                # validation_steps=len(val_ds.as_numpy_iterator()) // self.BATCH_SIZE,
                                verbose=verbose)

        return model, history

    def model_save(self,
                   model,
                   predict_sample,
                   model_name:str,
                   preprocess_strategy:str,
                   info:dict,
                   history:dict,
                   rate:str,
                   duration_fit:int,
                   duration_predict:int,
                   width:int,
                   height:int,
                   images_count_fit:int,
                   label:str):
        """Сохранение данных модели машинного обучения.
        :param model: Модель
        :param predict_sample: pandas DataFrame с данными предсказания на обучающей
                             выборке: два столбца "Real" и "Predicted".
        :param dict info: {  # названия классов и пороговые значения,
                             # при которых можно считать, что класс опознан:
                              'accuracy': ,  # вероятность правильного предсказания
                              'predicted_amount': {},  # количество предсказаний
                                        # по классам во время проверки точности
                                        # после создания модели.
                              'classes': [],  # названия классов
                              'date': '',  # дата создания модели
                              'fit_duration': 0,  # количество секунд, затраченное на обучение
                              'threshold': {
                                  'val': {},  # название + лучшее пороговое значение
                                  'prc': {},  # название + лучшее порог.значение (в % от максимума)
                                  'max': {},  # название + макс значение
                              },
                          }
        :param history: История фитирования моделью
        :param duration_fit: Количество секунд, затраченное на обучение модели
        :param duration_predict: Количество секунд, затраченное на предсказания
                                  по данным, на которых была тренирована модель
        :param width: Ширина изображений, на которых проводилась тренировка
        :param height: Высота изображений, на которых проводилась тренировка
        :param images_count_fit: Количество изображений, которое использовалось
                                 для обучения модели
        :param str rate: Вероятность успешного предсказания на обучающей выборке
                     одновремено по всем столбцам. Это значение вычисляется сразу
                     после создания модели.
        :param str model_name: Название модели: ResNet50, MobileNet и т.п.
        :param str preprocess_strategy: Способ предпоготовки изображений:
                                        JUST_RESIZE, SELECT_OBJECTt и т.п.
        :param label: Дополнительная пометка модели (используется префиксом
                      для названия папки с файлами)
        :return: Путь к папке с моделью
        """
        # папка для сохранения моделей
        now = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        timestamp = time()
        folder = f'models/{now}'
        # folder += f'_{round(max(history.history["f1_score"]), 5)}'

        if label:
            folder += f'_{label}'
        if rate:
            folder += f'_{rate}'

        if not exists(folder):
            makedirs(folder)

        # сохранение модели
        # tf.keras.models.save_model(model, f'models/{mark}_model')
        model.save(f'{folder}/model.h5')

        # сохранение весов модели
        model.save_weights(f'{folder}/weights.h5')

        # Сохранение данных о вероятности правильно предсказания,
        # сделанного на обучающей выборке.
        predict_sample.to_csv(f'{folder}/predict_sample', index=False)

        # соханение названий классов и пороговых значений
        with open(f'{folder}/info', 'w', encoding='utf-8') as f:
            # info = {
            #     'accuracy': 0,  # вероятность правильного предсказания
            #     'predicted_amount': {},  # количество предсказаний
            #                            # по классам во время проверки точности
            #                            # после создания модели.
            #     'history': {},  # история фитирования модели
            #     'classes': list(threshold),  # названия классов
            #     'width': 0,  # Ширина изображений, на которых проводилась тренировка
            #     'height': 0,  # Высота изображений, на которых проводилась тренировка
            #     'images_count_fit': 0,  # Количество изображений, которое использовалось
            #                             # для обучения модели
            #     'label': '',  # Дополнительная пометка модели
            #     'rate': '',  # Вероятность успешного предсказания на обучающей выборке
            #                  # одновремено по всем столбцам. Это значение вычисляется сразу
            #                  # после создания модели.
            #     'preprocess_strategy': '',  # Способ предпоготовки изображений:
            #                                 # JUST_RESIZE, SELECT_OBJECTt и т.п.
            #     'date': '',  # дата создания модели
            #     'duration_fit': 0,  # количество секунд, затраченное на обучение
            #     'duration_predict': 0,  # Количество секунд, затраченное на
            #                                предсказания по данным, на которых
            #                                была тренирована модель
            #     'threshold': {
            #         'val': {},  # название + лучшее пороговое значение
            #         'prc': {},  # название + лучшее порог.значение (в % от максимума)
            #         'max': {},  # название + макс значение
            #     },
            # }
            info['date'] = str(now)
            info['timestamp'] = timestamp
            info['duration_fit'] = duration_fit
            info['duration_predict'] = duration_predict
            info['label'] = label
            info['rate'] = str(rate)
            info['preprocess_strategy'] = preprocess_strategy
            info['width'] = width
            info['height'] = height
            info['model_name'] = model_name

            hist = history.history
            info['history'] = {k: np.array(v).tolist() for k, v in hist.items()}

            json_dump(info, f)

        # Создание графиков очень медленно работает на больших выборках
        # # Сохранение графика точности предсказаний.
        # self.plot_accuracy(predict_sample,
        #               info=info,
        #               output_file=f'{folder}/accuracy.png')
        #
        # # Сохранение графика истории обучения.
        # self.plot_history(history.history,
        #              output_file=f'{folder}/history.png')

        print(f'Модель сохранена: {folder}')
        return folder

    def model_load(self, file_path:str = '', verbose:bool = False):
        """Загрузка модели машинного обучения из файла.
        :param file_path: путь к файлу модели с расширением h5.
                          Если нет, то берётся последний файл по дате создания.
        :param verbose: Подробный вывод.
        :return: модель, словарь классов модели с порогами срабатываний,
                 история фитирования модели, вероятность верного предсказания на
                 выборке для обучения
        """
        if not file_path:
            list_of_files = glob('models/*/model.h5')
            file_path = max(list_of_files, key=getctime)

        if 'model.h5' not in file_path:
            file_path = f'{file_path}/model.h5'

        if not isfile(file_path):
            raise FileNotFoundError(f'Не удаётся загрузить файл: {file_path}')

        if verbose:
            print(f'Загружается файл: {file_path}')

        model = tf.keras.models.load_model(file_path)
        info = {  # названия классов и пороговые значения
            'accuracy': 0,  # вероятность правильного предсказания
            'predicted_amount': {},  # количество предсказаний
                      # по классам во время проверки точности
                      # после создания модели.
            'history': {},  # история фитирования модели
            'classes': [],  # названия классов
            'width': 0,  # Ширина изображений, на которых проводилась тренировка
            'height': 0,  # Высота изображений, на которых проводилась тренировка
            'label': '',  # Дополнительная пометка модели
            'rate': '',  # Вероятность успешного предсказания на обучающей выборке
                         # одновремено по всем столбцам. Это значение вычисляется сразу
                         # после создания модели.
            'preprocess_strategy': '',   # Способ предпоготовки изображений:
                                         # JUST_RESIZE, SELECT_OBJECTt и т.п.
            'date': '',  # дата создания модели
            'timestamp': '',  # дата создания модели
            'images_count_fit': 0, # Количество изображений, которое использовалось
                                   # для обучения модели
            'duration_fit': 0,  # количество секунд, затраченное на обучение
            'duration_predict': 0,  # Количество секунд, затраченное на
                                     # предсказания по данным, на которых
                                     # была тренирована модель
            'thresholds': {
                'val': {},  # название + лучшее пороговое значение
                'prc': {},  # название + лучшее порог.значение (в % от максимума)
                'max': {},  # название + макс значение
            },
        }
        predict_sample = []  # данные по истории обучения
        file_path_no_ext = file_path.rstrip('model.h5')

        if isfile(file_path_no_ext + 'info'):
            with open(file_path_no_ext + 'info') as f:
                info = json_load(f)
                if 'predicted_amount' in info:
                    info['predicted_amount'] = pd.DataFrame(info['predicted_amount'])

        if isfile(file_path_no_ext + 'predict_sample'):
            # данные о вероятности правильно предсказания,
            # сделанного на обучающей выборке
            predict_sample = pd.read_csv(file_path_no_ext + 'predict_sample')

        if verbose:
            print(f'Модель успешно загружена из файла: {file_path}')

        return model, info, predict_sample

    def create_model_plot(self, file_path:str = '', verbose:bool = False):
        """Создаёт графики обучения и вероятностей предсказаний для модели.
        Эту функцию не стоит запускать на на сервере, где происходят вычисления.
        Потому что она делается очень долго и выполняется только одним ядром CPU
        :param file_path: путь к файлу модели с расширением h5.
                          Если нет, то берётся последний файл по дате создания.
        :param verbose: Подробный вывод.
        """
        model, info, predict_sample = self.model_load(file_path = file_path,
                                                      verbose=verbose)

        # Сохранение графика истории обучения.
        self.plot_history(info['history'],
                     output_file=f'{folder}/history.png')

        # Сохранение графика точности предсказаний.
        self.plot_accuracy(predict_sample,
                      info=info,
                      output_file=f'{folder}/accuracy.png')


    def plot_history(self, history:dict, output_file:str):
        """Сохранение графика предсказаний.
        :param history: Словарь истории обучения модели.
        :param output_file: Путь к файлу, куда будет выгружено изображение графика
        :return: График в формате изображения seaborn
        """
        plot = pd.DataFrame(history).plot()
        plot = plot.get_figure()
        plot.savefig(output_file, bbox_inches="tight")

        return plot

    def plot_accuracy(self, df, info:dict, output_file:str):
        """Сохранение графика предсказаний.
        :param df: pandas DataFrame с данными предсказания на обучающей
                   выборке: два столбца "Real" и "Predicted".
        :param output_file: Путь к файлу, куда будет выгружено изображение графика
        :param dict info: {  # названия классов и пороговые значения,
                  # при которых можно считать, что класс опознан:
                   'accuracy': ,  # вероятность правильного предсказания
                   'predicted_amount': {},  # количество предсказаний
                             # по классам во время проверки точности
                             # после создания модели.
                   'history': {},  # история фитирования модели
                   'classes': [],  # названия классов
                   'width': 0,  # Ширина изображений, на которых проводилась тренировка
                   'height': 0,  # Высота изображений, на которых проводилась тренировка
                   'images_count_fit': 0, # Количество изображений, которое использовалось
                                          # для обучения модели
                   'date': '',  # дата создания модели
                   'timestamp': '',  # дата создания модели
                   'duration_fit': 0,  # количество секунд, затраченное на обучение
                   'duration_predict': 0,  # Количество секунд, затраченное на
                                            # предсказания по данным, на которых
                                            # была тренирована модель
                   'threshold': {
                       'val': {},  # название + лучшее пороговое значение
                       'prc': {},  # название + лучшее порог.значение (в % от максимума)
                       'max': {},  # название + макс значение
                   },
               }
        :return: График в формате изображения seaborn
        """
        realt = MultiLabelBinarizer(classes=info['classes']).fit_transform(df['Real'])
        predt = MultiLabelBinarizer(classes=info['classes']).fit_transform(df['Predicted'])

        reals = pd.DataFrame(realt, columns=info['classes']).sum().rename('Real')
        preds = pd.DataFrame(predt, columns=info['classes']).sum().rename('Predicted')
        prc = 100 * preds / reals

        print(f'Общее количество предсказаний по значениям:')
        print(pd.concat([reals, preds, prc.round().rename('%')], axis=1))

        # Раздеялем списки внутри значений клеток на несколько строк. Чтобы было
        # по одному значению в строчке.
        x = df['Real'].apply(pd.Series).reset_index().melt(id_vars='index')
        x = x.dropna()[['index', 'value']].set_index('index')

        y = df['Predicted'].apply(pd.Series).reset_index().melt(id_vars='index')
        y = y.dropna()[['index', 'value']].set_index('index')

        dfm = pd.merge(x, y,
                       left_index=True,
                       right_index=True)
        dfm.columns = ['Real', 'Predicted']

        # Строим график
        plot = sns.swarmplot(x=dfm['Real'],
                             y=dfm['Predicted'])

        plot.tick_params(axis='x', rotation=45)
        plot = plot.get_figure()
        plot.savefig(output_file, bbox_inches="tight")

        return plot
