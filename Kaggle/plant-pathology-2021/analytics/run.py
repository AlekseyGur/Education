# минимальные требования: 190 ГБ ОЗУ

from tools_tensor import Model

# Попробуем несколько моделей
models = [
    # 'ResNet50',
    # 'ResNet152V2',
    'MobileNetV2',
    # 'EfficientNetV2L',
    # 'MobileNetV3Large',
]
# Попробуем несколько способов подготовки изображений
strategies = [
    'JUST_RESIZE',
    # 'SELECT_OBJECT',
    # 'REMOVE_CORNERS',
    # 'INCREASE_CONTRAST',
    # 'INCREASE_CONTRAST_REMOVE_CORNERS',
]

# [500, 350], [800, 600], [600, 400], [1000, 600]
width, height = 600, 400
img_size = f'{width}_{height}'


for model_name in models:
    for strategy in strategies:
        try:
            model = Model(
                VERBOSE=True,  # подробный вовод процесса работы скрипта
                CSV_PATH='/mnt/img/source/train.csv',  # CSV файл с данными
                # IMG_FOLDER='/mnt/img/train_images/',  # Путь к папке с изображениями
                # IMG_FOLDER=f'/mnt/img/train_images_{img_size}_{strategy}/',  # Путь к папке с изображениями
                # IMG_FOLDER_AUGMENTED=f'/mnt/img/train_images_augmented_{width}_{height}_{strategy}/',
                IMG_WIDTH=width,  # ширина изображения
                IMG_HEIGHT=height,  # высота изображения
                # LIMIT_CLASSES=['frog_eye_leaf_spot', 'healthy'],  # Тренировать предсказание тольк заданных классов
                CLASSES_SAME_SIZE=False,  # Использовать одинаковое количество изображений для всех классов (количество у каждого класса будет равняться минимальному по классам)
                BATCH_SIZE=16,  # параметр для машинного обучения
                BUFFER_SIZE=100,  # количество предзагруженных изображений, которые стоят в очереди на обработку
                # LEARNING_RATE=0.0001,  # агрессивность обучения
                EPOCHS=30,  # Количество эпох машинного обучения
                LIMIT=None,  # Максимальное количество изображений для обработки
                EARLY_STOPPING=None,  # Максимальное количество эпох, в которых не было прогресса перед остановкой обучения
                # REDUCE_LR_ON_PLATEAU=None,  # Максимальное количество эпох, в которых обучение вышло на плато, после которых будет уменьшен LEARNING_RATE
                MEMORY_LIMIT=None,  # Ограничение на использование ОЗУ вычислительного устройства (в МБ).
                MEMORY_GROWTH=False,  # В положении "True" заставляет tensorflow занимать ОЗУ в GPU по мере необходимости.
                ONLY_CPU=False,  # Использовать только CPU.
                # STRATEGY=strategy,
                #             # 'JUST_RESIZE'  # тлько изменить размер (делается у всех других стратегий)
                #             # 'INCREASE_CONTRAST'  # увеличивает контраст фото
                #             # 'SELECT_OBJECT':  # выделение центра на изображении, градация серого,
                #             #         изменение размера, применение разных цветовых каналов,
                #             # 'REMOVE_CORNERS': # выделение центра на изображении (края
                #             #                     удаляются), изменение размера
                #
                # MODEL=model_name,  # модель машинного обучения
                # LABEL=f'{img_size}_{model_name}_{strategy}',

                STRATEGY=strategy,
                MODEL=model_name,
                IMG_FOLDER=f'/mnt/img/train_images_{img_size}_{strategy}/',  # Путь к папке с изображениями
                LABEL=f'{img_size}_{model_name}_{strategy}',
            )

            for scls in [
                # 6 х
                ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                #
                # # 5 х
                # ['healthy',                       'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',         'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',         'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust',                   'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew'           ],
                #
                # # 4 х
                # ['healthy',                       'scab', 'rust', 'powdery_mildew'           ],
                # ['healthy', 'frog_eye_leaf_spot',         'rust', 'powdery_mildew'           ],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',         'powdery_mildew'           ],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust',                            ],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew'           ],
                #
                #
                # ['healthy',                       'scab', 'rust',                   'complex'],
                # ['healthy', 'frog_eye_leaf_spot',         'rust',                   'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',                           'complex'], # - есть
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust',                   'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust'                             ],
                #
                #
                # ['healthy',                       'scab',         'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',                 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',         'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',                           'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',         'powdery_mildew'           ],
                #
                #
                # ['healthy',                               'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',         'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',                 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',         'rust',                   'complex'],
                # ['healthy', 'frog_eye_leaf_spot',         'rust', 'powdery_mildew'           ],
                #
                #
                # ['healthy',                       'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy',                               'rust', 'powdery_mildew', 'complex'],
                # ['healthy',                       'scab',         'powdery_mildew', 'complex'],
                # ['healthy',                       'scab', 'rust',                   'complex'],
                # ['healthy',                       'scab', 'rust', 'powdery_mildew'           ],
                #
                # # 3 х
                # ['healthy',                               'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot',                 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab',                           'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust',                            ],
                #
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                # ['healthy', 'frog_eye_leaf_spot', 'scab', 'rust', 'powdery_mildew', 'complex'],
                #
                # # 2 х
                # ['healthy', 'frog_eye_leaf_spot',                                   'complex'],
                # ['healthy',                       'scab',                           'complex'],
                # ['healthy',                               'rust',                   'complex'],
                # ['healthy',                                       'powdery_mildew', 'complex'],
                #
                # ['healthy', 'frog_eye_leaf_spot',                 'powdery_mildew',          ],
                # ['healthy',                       'scab',         'powdery_mildew',          ],
                # # ['healthy',                               'rust', 'powdery_mildew',        ], # - есть
                # ['healthy',                                       'powdery_mildew', 'complex'],
                #
                # ['healthy', 'frog_eye_leaf_spot',         'rust',                            ],
                # ['healthy',                               'rust',                   'complex'],
                #
                # ['healthy', 'frog_eye_leaf_spot', 'scab',                                    ],
                # ['healthy',                       'scab', 'rust',                            ],
                # ['healthy',                       'scab',         'powdery_mildew',          ],
                # ['healthy',                       'scab',                           'complex'],
                #
            # ['healthy', 'frog_eye_leaf_spot', 'scab',                                  ], # - есть
                # ['healthy', 'frog_eye_leaf_spot',         'rust',                            ],
                # ['healthy', 'frog_eye_leaf_spot',                 'powdery_mildew',          ],
                # ['healthy', 'frog_eye_leaf_spot',                                   'complex'],

                # 1 х
                # ['healthy', 'frog_eye_leaf_spot'                                             ],  # - 100 %
                # ['healthy',                                                         'complex'],  # - 100 %
                # ['healthy',                         'scab'                                   ],  # - 100 %
                # ['healthy',                                       'powdery_mildew'           ],  # - 88 %
                # ['healthy',                               'rust'                             ],  # - 0 %

                # без healthy
                # ['frog_eye_leaf_spot', 'rust', 'scab'],
                # ['frog_eye_leaf_spot']

                # ['healthy', 'frog_eye_leaf_spot', 'complex', 'scab']
            ]:
                print(f'Используются только классы: {scls}')
                model.LIMIT_CLASSES = scls
                # model.LABEL = f'{img_size}_{model_name}_{strategy}_augmented',
                model.run() # тренируем, сохраняем файл модели

            del model

        except Exception as e:
            print('=' * 200)
            print(f'Не удалось получить данные по "{img_size}_{model_name}_{strategy}"')
            print('=' * 200)
            raise

# Загружаем модель, чтобы сделать предсказание для одного фото
# model, model_classes, history, rate = ts.model_load(verbose=VERBOSE)

# [scab]                                 4826
# [healthy]                              4624
# [frog_eye_leaf_spot]                   3181
# [rust]                                 1860
# [complex]                              1602
# [powdery_mildew]                       1184
# [scab, frog_eye_leaf_spot]              686
# [scab, frog_eye_leaf_spot, complex]     200
# [frog_eye_leaf_spot, complex]           165
# [rust, frog_eye_leaf_spot]              120
# [rust, complex]                          97
# [powdery_mildew, complex]                87

# healthy - контрольная
# frog_eye_leaf_spot - 100 % -
# scab - 100 %
# complex - 100 % -
# powdery_mildew - 88 % -
# rust - 0 % -
