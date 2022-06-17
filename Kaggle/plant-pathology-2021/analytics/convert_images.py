import os
from tools_tensor import Model
from matplotlib.image import imread
from matplotlib.image import imsave

from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count
# import gc

def calculation_single_process(*args):
    """Проводит расчёты. Запускается асинхронно много раз через функцию
    calculation.paralell_execution. Должно быть вынесено за пределы функции
    calculation, из которой вызывается (требование python).

    :param gc_start:
    :param gc_period:
    """
    paths = list(*args)
    for idx, file_path in enumerate(paths):
        save_to = file_path.replace('source/train_images/',
                                    # f'source/train_images_{model.STRATEGY}/')
                                    f'/mnt/img/train_images_{model.IMG_WIDTH}_{model.IMG_HEIGHT}_{model.STRATEGY}/')

        if not os.path.isfile(save_to):
            # print(f'Обрабатываем: {save_to}')
            img = model.get_image(file_path,
                                  width=model.IMG_WIDTH,
                                  height=model.IMG_HEIGHT,
                                  convert_to_tensor=False)

            if 'SELECT_OBJECT' in model.STRATEGY:
                img[img>1] = 1

            try:
                imsave(save_to, arr=img)
                print(f'Сохранили: {save_to}')
            except Exception as e:
                print(f'Ошибка сохранения файла: {save_to}: {e}')

            # if idx % 100 == 0:
                # gc.collect()
                # print(f'ОЗУ освобождена')
        else:
            # print(f'Файл уже существует: {save_to}')
            pass
    # gc.collect()

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
    'SELECT_OBJECT',
    'REMOVE_CORNERS',
    'INCREASE_CONTRAST',
    'INCREASE_CONTRAST_REMOVE_CORNERS',
]


for width, height in [[500, 350], [800, 600], [600, 400]]:
    img_size = f'{width}_{height}'
    for strategy in strategies:
        # directory = f'source/train_images_{strategy}/'
        directory = f'/mnt/img/train_images_{img_size}_{strategy}/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        model = Model(
            VERBOSE=True,  # подробный вовод процесса работы скрипта
            CSV_PATH='source/train.csv',  # CSV файл с данными
            FOLDER_PATH='source/train_images/',  # Путь к папке с изображениями
            # IMG_WIDTH=1000,  # ширина изображения
            # IMG_HEIGHT=600,  # высота изображения
            IMG_WIDTH=600,  # ширина изображения
            IMG_HEIGHT=400,  # высота изображения
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
                                     folder_path=model.FOLDER_PATH,
                                     limit=model.LIMIT,
                                     verbose=model.VERBOSE)

        calculation(DF['path'].to_list())
        # process_multithread(DF['path'].to_list())


print('Готово')
