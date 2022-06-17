from tools_tensor import Model
import pandas as pd
import sys

width = 1000
height = 668

width = 600
height = 400
strategy = 'JUST_RESIZE'
model_name = 'ResNet50'

img_size = f'{width}_{height}'


models_paths = [
    # 'models_selectel/2022.06.13 14:12:56_600_400_MobileNetV2_JUST_RESIZE_86.98413',
    'models_selectel/2022.06.13 13:04:16_600_400_MobileNetV2_JUST_RESIZE_89.32735',
    # 'models_selectel/2022.06.13 13:31:30_600_400_MobileNetV2_JUST_RESIZE_89.19049',
]

compare = pd.DataFrame()

for models_path in models_paths:
    model = Model(
        VERBOSE=True,  # подробный вовод процесса работы скрипта
        CSV_PATH='source/train.csv',  # CSV файл с данными
        # IMG_FOLDER='source/train_images/',  # Путь к папке с изображениями
        IMG_FOLDER=f'source/train_images_{img_size}_{strategy}/',  # Путь к папке с изображениями
        IMG_WIDTH=width,  # ширина изображения
        IMG_HEIGHT=height,  # высота изображения
        BATCH_SIZE=16,  # параметр для машинного обучения
        BUFFER_SIZE=100,  # количество предзагруженных изображений, которые стоят в очереди на обработку
        # LEARNING_RATE=0.0001,  # агрессивность обучения
        EPOCHS=17,  # Количество эпох машинного обучения
        LIMIT_CLASSES=['rust'],  # пытаемся предсказать только один класс
        LIMIT=500,  # Максимальное количество изображений для обработки
        MEMORY_LIMIT=None,  # Ограничение на использование ОЗУ вычислительного устройства (в МБ).
        MEMORY_GROWTH=False,  # В положении "True" заставляет tensorflow занимать ОЗУ в GPU по мере необходимости.
        ONLY_CPU=True,  # Использовать только CPU.

        STRATEGY=strategy,
                    # 'JUST_RESIZE'  # тлько изменить размер (делается у всех других стратегий)
                    # 'INCREASE_CONTRAST'  # увеличивает контраст фото
                    # 'SELECT_OBJECT':  # выделение центра на изображении, градация серого,
                    #         изменение размера, применение разных цветовых каналов,
                    # 'REMOVE_CORNERS': # выделение центра на изображении (края
                    #                     удаляются), изменение размера

        MODEL=model_name,  # модель машинного обучения
        LABEL=f'{img_size}_{model_name}_{strategy}',
    )

    # Загружаем модель, чтобы сделать предсказание для одного фото
    model_tensor, info, predict_sample = model.model_load(
        file_path=models_path,
        verbose=True
    )

    predict_ds, model.DF = model.get_ds_df(csv_path=model.CSV_PATH,
                                 img_folder=model.IMG_FOLDER,
                                 # img_folder_augmented=model.IMG_FOLDER_AUGMENTED,
                                 limit_classes=model.LIMIT_CLASSES,
                                 limit=model.LIMIT,
                                 classes_same_size=model.CLASSES_SAME_SIZE,
                                 verbose=model.VERBOSE)

    # Получим список классов и функцию преобразования класса в тензор
    model.LABEL_LOOKUP, classes = model.get_lookup_func(model.DF,
                                            saved_labels=info['classes'],
                                            labels_column_name='labels',
                                            verbose=model.VERBOSE)

    # Подготавливает датасет для проверки точности модели после создания
    predict_ds = model.prepare_ds_rate_check(predict_ds,
                                  model.DF,
                                  model.LABEL_LOOKUP,
                                  num_parallel_calls='AUTOTUNE',
                                  batch_size=model.BATCH_SIZE,
                                  prefetch_buffer='AUTOTUNE',
                                  shuffle_size=0)

    # Сделаем предсказание
    prediction = model.predict(model_tensor,
                               predict_ds,
                               df=model.DF,
                               classes=classes,
                               classes_thresholds=info['threshold']['val'],
                               verbose=model.VERBOSE)

    if not len(compare.index):
        compare = prediction[['file_name']]

    # выбираем только те, что не определились
    # for col in prediction.columns:
    for col in info["classes"]:
        if '[UNK]' in col:
            continue
        if 'file_name' in col:
            continue
        if 'path' in col:
            continue

        prediction = prediction[prediction[col] == False]

    compare = pd.merge(compare,
                       prediction,
                       on = 'file_name',
                       how = 'left',
                       # suffixes=('', '')
                       )

    # print('Список файлов, которые не были определены')
    # print(prediction)
    # unpredicted_prc = 100 * len(prediction.index) / model.LIMIT
    # print(f'{unpredicted_prc} %')
    #
    # prediction['path'].to_csv(f'{info["classes"]} - rust.csv')

print(compare.dropna())

# ==================================================
# models_selectel/2022.06.10 12:33:43_600_400_MobileNetV2_JUST_RESIZE_99.7037
# ['healthy', 'scab']
# ==================================================
# models_selectel/2022.06.10 11:53:20_600_400_MobileNetV2_JUST_RESIZE_99.7912
# ['healthy', 'complex']
# ==================================================
# models_selectel/2022.06.09 17:17:58_0.66364_600_400_MobileNetV2_JUST_RESIZE_99.7
# ['healthy', 'frog_eye_leaf_spot']



#          Real  Predicted  amount %  correct %
# scab     4826       3652      76.0       75.0
# healthy  4624       5794     125.0       99.0
# models_selectel/2022.06.13 14:12:56_600_400_MobileNetV2_JUST_RESIZE_86.98413
# ==========================================================================================
#          Real  Predicted  amount %  correct %
# healthy  4624       3969      86.0       86.0
# complex  1602       2249     140.0       99.0
# models_selectel/2022.06.13 13:31:30_600_400_MobileNetV2_JUST_RESIZE_89.19049
# ==========================================================================================
#                     Real  Predicted  amount %  correct %
# healthy             4624       3899      84.0       83.0
# frog_eye_leaf_spot  3181       3902     123.0       98.0
# models_selectel/2022.06.13 13:04:16_600_400_MobileNetV2_JUST_RESIZE_89.32735
# ==========================================================================================
#                     Real  Predicted  amount %  correct %
# scab                4826       4857     101.0       92.0
# healthy             4624       4738     102.0       96.0
# frog_eye_leaf_spot  3181       3216     101.0       92.0
# complex             1602       1351      84.0       68.0
# models_selectel/2022.06.13 11:39:06_600_400_MobileNetV2_JUST_RESIZE_90.45879
