import os
import tensorflow as tf
import numpy as np
from tools_tensor import Model
from matplotlib.image import imread
from matplotlib.image import imsave
# from keras.preprocessing.image import img_to_array

from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count

# Необходимые функции для pipeline, которые используются при работе с моделями
# tensorflow. Пригодны для работы над задачами MultiLabel классификации.
from tools_image import resize

def calculation_single_process(*args):
    """Проводит расчёты. Запускается асинхронно много раз через функцию
    calculation.paralell_execution. Должно быть вынесено за пределы функции
    calculation, из которой вызывается (требование python).

    :param gc_start:
    :param gc_period:
    """
    paths = list(*args)
    for idx, file_path in enumerate(paths):
        save_to = file_path.replace(f'/mnt/img/train_images_{model.IMG_WIDTH}_{model.IMG_HEIGHT}_{model.STRATEGY}/',
                                    # f'source/train_images_{model.STRATEGY}/')
                                    f'/mnt/img/train_images_augmented_{model.IMG_WIDTH}_{model.IMG_HEIGHT}_{model.STRATEGY}/')
        save_to = '.'.join(save_to.split('.')[:-1])

        if not os.path.isfile(f'{save_to}_1.jpg'):
            # print(f'Прочитали: {file_path}')
            img = imread(file_path)

            # convert to numpy array
            data = tf.keras.preprocessing.image.img_to_array(img)

            # expand dimension to one sample
            samples = np.expand_dims(data, 0)

            # create image data augmentation generator
            datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                                         featurewise_center=True,
                                         rotation_range=(0-30),
                                         width_shift_range=0.2,
                                         height_shift_range=0.2,
                                         brightness_range=[0.7,1.3],
                                         shear_range=0.2,
                                         zoom_range=0.2,
                                         channel_shift_range=0.2,
                                         horizontal_flip=True,
                                         vertical_flip=True,
                                         fill_mode='nearest')

            it = datagen.flow(samples, batch_size=1)

            for i in range(1, 11):  # создаём оп 10 слегка изменённых копий изображений
                batch = it.next()
                image = batch[0].astype('uint8')
                save_name = f'{save_to}_{i}.jpg'

                try:
                    imsave(save_name, arr=image)
                    print(f'Сохранили: {save_name}')
                except Exception as e:
                    print(f'Ошибка сохранения файла: {save_name}: {e}')

        else:
            print(f'Файл уже существует: {save_to}_1.jpg')
            pass

def calculation(paths):
    def paralell_execution(func, args, cpu_count, method='multiprocessing'):
        """Делает параллельные вычисления разными способами.
        :params int cpu_count: Количество CPU для расчётов
        :params str method: Выбор способа разделения задач по процессорам:
            multithreading - годится для задач, где нужно ждать. К примеру,
            параллельная загрузка файлов.

            multiprocessing - годится для задач, где нужна вычислительная
            мощность всех ядер.

            Экспериментально установлено: multiprocessing будет выигрывать
            multithreading только на больших объёмах расчётов и большом
            количестве CPU (6+). В противном случае multithreading будет
            слегка быстрее.
        """
        res = None
        if method == 'multiprocessing':
            with ProcessPoolExecutor(cpu_count) as ex:
                res = ex.map(func, args)

        if method == 'multithreading':
            with ThreadPoolExecutor(cpu_count) as ex:
                res = ex.map(func, args)

        # Преобразование list(res) и запускает весь процесс подсчёта. Если
        # нужно запустить принудительно ранее, то можно заменить map на submit и
        # выполнить метод res.result()
        return list(res)

    # Разделим данные, чтобы сделать несколько потоков обработки
    # Если используется метод разделения по процессорам (не по потокам), то
    # стоит станавливать значение точно равным количеству CPU.
    # Если же по количеству потоков, то можно попробовать кол-во CPU * 2. Но
    # есть большая вероятность словить ошибку OOM
    cpu_cnt = cpu_count()

    # сделаем так, чтобы каждому ядру процессора досталось примерно
    # равное поличество данных на обработку
    chunk_size = 1
    paths_to_process = len(paths)
    if cpu_cnt < paths_to_process:
        chunk_size = (paths_to_process // cpu_cnt) + 1

    X_chunk = [paths[i:i + chunk_size] for i in range(0, paths_to_process, chunk_size)]
    args_list = []
    for chunk in X_chunk:
        args_list.append(chunk)

    paralell_execution(func=calculation_single_process,
                       args=args_list,
                       cpu_count=cpu_cnt,
                       method='multiprocessing')

# Попробуем несколько способов подготовки изображений
strategies = [
    'JUST_RESIZE',
    # 'SELECT_OBJECT',
    # 'REMOVE_CORNERS',
    # 'INCREASE_CONTRAST',
    # 'INCREASE_CONTRAST_REMOVE_CORNERS',
]

# [500, 350], [800, 600], [600, 400], [1000, 600]

for width, height in [[600, 400]]:
    for strategy in strategies:
        # directory = f'source/train_images_{strategy}/'
        directory = f'/mnt/img/train_images_{width}_{height}_{strategy}/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory_augmented = f'/mnt/img/train_images_augmented_{width}_{height}_{strategy}/'
        if not os.path.exists(directory_augmented):
            os.makedirs(directory_augmented)

        model = Model(
            VERBOSE=True,  # подробный вовод процесса работы скрипта
            CSV_PATH='source/train.csv',  # CSV файл с данными
            IMG_FOLDER=f'/mnt/img/train_images_{width}_{height}_{strategy}/',  # Путь к папке с изображениями
            IMG_FOLDER_AUGMENTED=f'/mnt/img/train_images_augmented_{self.IMG_WIDTH}_{self.IMG_HEIGHT}_{self.STRATEGY}/',
            IMG_WIDTH=width,  # ширина изображения
            IMG_HEIGHT=height,  # высота изображения
            BATCH_SIZE=16,  # параметр для машинного обучения
            BUFFER_SIZE=100,  # количество предзагруженных изображений, которые стоят в очереди на обработку
            LEARNING_RATE=0.0001,  # агрессивность обучения
            EPOCHS=17,  # Количество эпох машинного обучения
            LIMIT=None,  # Максимальное количество изображений для обработки
            MEMORY_LIMIT=None,  # Ограничение на использование ОЗУ вычислительного устройства (в МБ).
            MEMORY_GROWTH=False,  # В положении "True" заставляет tensorflow занимать ОЗУ в GPU по мере необходимости.
            ONLY_CPU=False,  # Использовать только CPU.

            STRATEGY=strategy,
                        # 'JUST_RESIZE'  # тлько изменить размер (делается у всех других стратегий)
                        # 'INCREASE_CONTRAST'  # увеличивает контраст фото
                        # 'SELECT_OBJECT':  # выделение центра на изображении, градация серого,
                        #         изменение размера, применение разных цветовых каналов,
                        # 'REMOVE_CORNERS': # выделение центра на изображении (края
                        #                     удаляются), изменение размера

            # MODEL=model_name,  # модель машинного обучения
            # LABEL=f'{model_name}_{strategy}',
        )

        ds, DF = model.get_ds_df(csv_path=model.CSV_PATH,
                                 img_folder=model.IMG_FOLDER,
                                 img_folder_augmented=model.IMG_FOLDER_AUGMENTED,
                                 limit=model.LIMIT,
                                 verbose=model.VERBOSE)

        calculation(DF['path'].to_list())

print('Готово')
