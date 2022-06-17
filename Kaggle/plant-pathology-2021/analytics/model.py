import numpy as np
import pandas as pd
from glob import glob as list_files_in_dir
from os.path import getctime, abspath, exists
from datetime import datetime
from xgboost import XGBClassifier
from fast_ml.feature_engineering import FeatureEngineering_DateTime
from string import ascii_uppercase
from json import dump as json_dump, load as json_load
from sklearn.model_selection import train_test_split
import re


MODELS_DIR = 'models'  # Папка для сохранения моделей

# Доделать кеширование данных:
# MODELS_INFO = {}  # данные о моделях, чтобы не читать с диска каждый раз


class Model():

    def create(self, path_to_csv: str = 'source/tb_hotel_traintest.csv'):
        """Создаёт модель, получая данные из файла CSV.
        :param str path_to_csv: путь к CSV файлу с набором данных
        :return tulp: модель, точность предсказания, статус сохранения моедли
        """
        df = None
        try:
            df = pd.read_csv(path_to_csv, index_col='id_booking')
        except:
            return {'error': 'Не удалось загрузить файл'}

        df = self.prepare(df, 'create')  # обрабатываем данные, готовим колонки
        df, NAlist = self.reduce_mem_usage(df)  # оптимизируем типы переменных

        # assert if NAlist not []

        X = df.copy()  # все параметры, кроме предсказываемого
        y = X.pop('is_cancelled')  # будем предсказывать это

        # model = XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor')
        model = XGBClassifier(n_estimators=860,  # экспериментальное значение
                              learning_rate=0.4625, # экспериментальное значение
                              tree_method='gpu_hist',
                              predictor='gpu_predictor')

        X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                              train_size=0.8,
                                                              test_size=0.2,
                                                              shuffle=True,
                                                              # stratify=y,
                                                              random_state=0)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_valid)
        rate = self.predict_rate_bool(y_pred, y_valid)

        save_status = self.save(model, rate, X.columns.to_list())

        try:
            return {
                'model': model.predict(df).tolist()[0],
                'rate': rate,
                'columns': X.columns.to_list(),
                'save_status': save_status,
            }
        except:
            pass
        return {'error': f'Не удалось создать и сохранить модель'}

    def save(self, model, prcnt: float, columns: list):
        """Сохраняет модель в файл.
        :param model: модель для сохранения
        :param prcnt: точность предсказания модель на тестовой выборке
        :param columns: колонки в наборе данных при создании модели
        :return: ошибки при сохранении или ОК
        """
        if not exists(MODELS_DIR):
            os.makedirs(directory)

        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        path = f'{MODELS_DIR}/{prcnt}_{now}'
        status = 'OK'

        try:
            model.save_model(f'{path}.model')
        except:
            status = f'Невозможно сохранить модель в файл "{path}". '

        try:
            # model.save_config(f'{path}.config')
            with open(f'{path}.config', 'w', encoding='utf-8') as f:
                json_dump(model.get_params(), f)
        except:
            status += f'Невозможно сохранить конфиг в файл "{path}". '

        try:
            with open(f'{path}.columns', 'w', encoding='utf-8') as f:
                json_dump(columns, f)
        except:
            status += f'Невозможно сохранить название колонок, которые были '\
                      f'использованы при создании модели, в файл "{path}". '

        return status

    def load(self, path: str):
        """Загружает модель из файла.
        :param path: путь к файлу модели
        :return: модель с загруженными параметрами
        """
        if '.model' not in path:
            return False

        xgb = XGBClassifier()
        xgb.load_model(path)
        return xgb

    def get_list(self) -> list:
        """Возвращает список моделей, которые есть в системе, с описаниями
        :return: список словарей с описанием моделей (не без самих моделей).
        """
        paths = [f for f in list_files_in_dir(f'{MODELS_DIR}/*.model')]
        # Первая часть названия файла модели - точность предсказания на тестовой
        # выборке. Вторая часть - дата создания:
        # 99.92505_2022-04-26_13:13:57.model

        models_info = []
        for path_ext in paths:
            path = path_ext.split('.model')[0]  # путь без расширения файла
            file_name = path.lstrip(f'{MODELS_DIR}/')

            columns = []  # колонки, которые были при создании модели
            with open(f'{path}.columns') as f:
                columns = json_load(f)

            config = []  # настройки, которые были при создании модели
            with open(f'{path}.config') as f:
                config = json_load(f)

            m = {}
            m['name'] = file_name  # имя файла
            m['path'] = abspath(path_ext)  # абсолютный путь к файлу модели
            m['accuracy'] = file_name.split('_')[0]  # точность предсказаний
            m['date'] = file_name.split('_')[1]  # дата создания
            m['time'] = file_name.split('_')[-1]  # время создания
            m['date_time'] = f'{m["date"]} {m["time"]}'

            dt = datetime.strptime(m["date_time"], '%Y-%m-%d %H:%M:%S')
            m['timestamp'] = datetime.timestamp(dt)  # timestamp создания
            m['config'] = config  # конфиг модели
            m['columns'] = columns  # колонки, которые были при создании модели

            models_info.append(m)

        return models_info

    def get_best(self) -> dict:
        """Получаем данные сохранённой модели с наибольшей предсказательной силой
        :return dict: данные о модели
        """
        models = self.get_list()
        if not models:
            return {}

        return max(models, key=lambda x: x['accuracy'])

    def get_last(self) -> dict:
        """Получаем данные сохранённой модели , которая была создана последней по
        времени
        :return dict: данные о модели
        """
        models = self.get_list()
        if not models:
            return {}

        return max(models, key=lambda x: x['timestamp'])

    def get_by_name(self, name: str = '') -> dict:
        """Получаем данные сохранённой модели с определённым именем.
        :param str name: название файла модели
        :return dict: данные о модели
        """
        name = re.sub('[^.,0-9a-zа-яё-_]', '', str(input_str), flags=re.IGNORECASE)

        models = self.get_list()
        if not models:
            return {}

        res = [i['name'] == name for i in models]
        if not res:
            return {}

        return res[0]

    def predict(self, params):
        """Предсказываем значение, используя модель.
        :param str params: название файла модели
        :return int: предсказанное значение
        """
        df = {}
        default_params = self.params_reqired()
        reqired = default_params.copy()

        params_cleared = {}  # очищенные параметры, подготовленные к передаче в модель

        for key, val in params.items():
            if key in reqired:
                val_type = reqired[key]['type']  # нужный тип переменной
                clear_funct = str
                if 'float' in val_type:
                    clear_funct = float
                if 'int' in val_type:
                    clear_funct = int
                if 'bool' in val_type:
                    clear_funct = bool
                if 'str' in val_type:
                    clear_funct = str

                if clear_funct:
                    try:
                        params_cleared.update({key: clear_funct(val)})
                        reqired.pop(key, None)
                    except Exception as e:
                        print(e)
                        pass

        if not (len(params_cleared) == len(default_params) and len(reqired) == 0):
            return {'error': f'Передайте ещё параметры: {reqired.keys()}'}

        df = pd.DataFrame(params_cleared, index=[0])
        df = self.prepare(df)
        df, NAlist = self.reduce_mem_usage(df)

        # делаем предсказание на модели, которая была создана последней
        model_last_info = self.get_last()

        model = None
        try:
            model = self.load(model_last_info['path'])
        except:
            return {'error': f'Невозможно загрузить данные модели по адресу {path}'}

        # набор полей, который передаётся в модель при предсказании, должен
        # совпадать с набором, который был при создании модели
        columns_predict = df.columns.to_list()
        columns_native = model_last_info['columns']
        # находим лишние колонки, которые появились в новом дата сете, удаляем их
        columns_to_delete = list(set(columns_predict) - set(columns_native))
        df = df.drop(columns_to_delete, axis=1)

        # находим колонки, которых не достаёт в новом дата сете, и заполняем их нулями
        columns_to_add = list(set(columns_native) - set(columns_predict))
        df_zero = pd.DataFrame(0, index=np.arange(1), columns=columns_to_add)
        df = df.join(df_zero)

        len(columns_native) == len(df.columns.to_list())  # тут сделать assert.

        df = df[columns_native]  # используем только нужне поля в правильном порядке

        try:
            return {'value': model.predict(df).tolist()[0]}
        except:
            pass
        return {'error': f'Не удалось сделать предсказание'}

    def predict_rate_bool(self, valid, pred, threshold: float = 0.5) -> int:
        """Вычисляет процент правильных предсказаний. Используется в методе create
        :prarm valid: точно известные значения
        :prarm pred: предсказанные значения
        :prarm threshold: порог (от 0 до 1) выше - значение True, ниже - False
        :return: процент правильных предсказаний
        """
        pred_bool = pred > threshold
        valid_bool = valid > threshold

        pred_compare = [i[0] == i[1] for i in list(zip(valid_bool, pred_bool))]
        pred_prcnt = 100 * sum(pred_compare) / len(pred_compare)
        return round(pred_prcnt, 5)

    def reduce_mem_usage(self, props, debug=False):
        """Именьшаем размер данных, которые занимает pandas DataFrame путём
        изменения типов колонок.
        :prarm DataFrame props: DataFrame набор данных для уменьшения
        :return DataFrame: изменённый набор данных
        """
        NAlist = [] # Keeps track of columns that have missing values filled in.
        start_mem_usg = props.memory_usage().sum() / 1024**2

        if debug:
            print(f"Memory usage of properties dataframe is :{start_mem_usg} MB")
            print("******************************")

        for col in props.columns:
            if props[col].dtype != object:  # Exclude strings

                # Print current column type
                if debug:
                    print("Column: ", col, end="\t")
                    print("dtype before: ", props[col].dtype, end="\t")

                # make variables for Int, max and min
                IsInt = False
                mx = props[col].max()
                mn = props[col].min()

                # Integer does not support NA, therefore, NA needs to be filled
                if not np.isfinite(props[col]).all():
                    NAlist.append(col)
                    props[col].fillna(mn-1, inplace=True)

                # test if column can be converted to an integer
                asint = props[col].fillna(0).astype(np.int64)
                result = (props[col] - asint)
                result = result.sum()
                if result > -0.01 and result < 0.01:
                    IsInt = True


                # Make Integer/unsigned Integer datatypes
                if IsInt:
                    if mn >= 0:
                        if mx < 255:
                            props[col] = props[col].astype(np.uint8)
                        elif mx < 65535:
                            props[col] = props[col].astype(np.uint16)
                        elif mx < 4294967295:
                            props[col] = props[col].astype(np.uint32)
                        else:
                            props[col] = props[col].astype(np.uint64)
                    else:
                        if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                            props[col] = props[col].astype(np.int8)
                        elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                            props[col] = props[col].astype(np.int16)
                        elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                            props[col] = props[col].astype(np.int32)
                        elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                            props[col] = props[col].astype(np.int64)

                # Make float datatypes 32 bit
                else:
                    props[col] = props[col].astype(np.float32)

                # Print new column type
                if debug:
                    print("dtype after: ", props[col].dtype)

        if debug:
            print("******************************")

            # Print final result
            print("___MEMORY USAGE AFTER COMPLETION:___")
            mem_usg = props.memory_usage().sum() / 1024**2
            print("Memory usage is: ",mem_usg," MB")
            print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")

            if NAlist:
                print("_____!!!!!!!!!!!!!!!!!!_____")
                print("")
                print("Warning: the following columns have missing values filled with 'df['column_name'].min() -1': ")
                print("")
                print(NAlist)
                print("")
                print("_____!!!!!!!!!!!!!!!!!!_____")

        return props, NAlist

    def prepare(self, df, action='predict'):
        """Подготавливаем модель к предсказанию, очищаем данные, добавляем поля
        :param DataFrame df: набор данных для обработки
        :param str action: "predict" для предсказаний, "create" для создания модели
        :return DataFrame df: изменённый набор данных для обработки
        """
        # Заполнить пустые значения
        df.fillna({'children': 0,
                   'agent': 'No',
                   'country': 'No',
                   'company': 'No'}, inplace=True)

        # преобразуем изменённые колонки к новому типу
        df['children'] = df['children'].astype('int64')

        # parce date
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'],
                                                       format="%Y-%m-%d",
                                                       infer_datetime_format=True)

        df['arrival_date'] = pd.to_datetime(df['arrival_date'],
                                            format="%Y-%m-%d",
                                            infer_datetime_format=True)

        # удалим бессмысленные поля
        df = df.drop('company', axis=1)

        # заменим 'Undefined' на 'SC', потому что по описанию отсутствие данных - это и есть 'SC'
        df.meal = df.meal.replace('Undefined', 'SC')

        # заменяем все значения 'Undefined' на None
        df = df.replace('Undefined', None)

        # значения стран стоит преобразовать в регионы, котому что их слишком много разных (174)
        country = pd.read_csv('res/ISO-3166-Countries-with-Regional-Codes.csv')
        country = country[['alpha-3', 'region']]
        country.columns = ['country', 'region']

        # df = df.merge(country, on='country', how='left', left_index=True, right_index=True)
        df = df.merge(country, on='country', how='left')
        df = df.drop(['country'], axis=1)

        del country  # больше не нужно

        # делаем замену буквенных обазначений в reserved_room_type и assigned_room_type на цифры. Потому что по количеству и смыслу буквы убывают:
        # df.reserved_room_type.value_counts()
        # A    70324
        # D    24074
        # E     7383
        # F     3569
        # G     2416
        # C     2264
        # B     2078
        # H      684
        # I      347
        # K      258
        # P       11
        # L        1
        replece_dict = dict(zip(ascii_uppercase, range(1,27)))
        df.reserved_room_type = df.reserved_room_type.replace(replece_dict)
        df.assigned_room_type = df.assigned_room_type.replace(replece_dict)
        # с помощью разницы reserved_room_type и assigned_room_type создаём новый параметр
        df['room_type_diff'] = df.reserved_room_type - df.assigned_room_type
        df = df.drop(['reserved_room_type','assigned_room_type'], axis=1)  # больше не нужно

        # в новом параметре важно только общее впечатление: номер хуже или лучше
        def positive_zero_negative(x):
            if x == 0:
                return 0
            return 1 if x > 0 else -1

        df['room_type_diff'] = df['room_type_diff'].apply(positive_zero_negative)

        # питание заменяем на цифры (чем больше цифра, тем больше еды):
        # Undefined/SC – no meal package;
        # BB – Bed & Breakfast;
        # HB – Half board (breakfast and one other meal – usually dinner);
        # FB – Full board (breakfast, lunch and dinner)
        df.meal = df.meal.replace({'Undefined':0, 'SC':0, 'BB':1, 'HB':2, 'FB':3})

        # разбираем даты на составляющие, добавляем новые колонки
        dtf = FeatureEngineering_DateTime()
        dtf.fit(df, datetime_variables=['reservation_status_date', 'arrival_date'])
        df = dtf.transform(df)

        if action == 'create':
            # удаляем столбцы со слишком уникальными/редкими значениями в датах (стоит поискать не только в датах)
            nunique_date = df.nunique().reset_index()
            nunique_date[nunique_date['index'].str.contains('_date:') == True]
            remove_col = nunique_date[(nunique_date[0]==len(df)) |
                                      (nunique_date[0]==0) |
                                      (nunique_date[0]==1) ]['index'].tolist()
            df = df.drop(remove_col, axis=1)

            # # можно пойти другим путём: удалить столбцы, которые оказывают наименьшее влияние на результат.
            # # Для этого сделаем функцию оценки влияния:
            # def make_mi_scores(X, y, discrete_features='auto'):
            #     if isinstance(X, pd.Series):
            #         X = pd.DataFrame(X)
            #     mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
            #     mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
            #     mi_scores = mi_scores.sort_values(ascending=False)
            #     return mi_scores
            # # Передадим в эту функцию все столбцы, чтобы определить наиболее
            # df_scores = []
            # for col in df.columns:
            #     if 'is_cancelled' in col:
            #         continue
            #     df_scores.append(make_mi_scores(df[col], df['is_cancelled']))
            # df_scores = pd.concat(df_scores)
            # df_scores.sort_values(ascending=False)
            # # В результате получим таблицу, в которой будет оценка влияния
            # # столбцов набора данных на результат. Обрежем самые мало влияющие,
            # # к примеру, которые со значением меньше 0.005
            # df = df.drop(labels=df_scores[df_scores < 0.005].index.to_list(), axis=1)

        # исправляем значения полей "is_" на тип bool (а то они int, а это неверно по смыслу)
        if 'arrival_date:is_weekend' in df.columns:
            df['arrival_date:is_weekend'] = df['arrival_date:is_weekend'].replace({0:False, 1:True})

        if 'reservation_status_date:is_weekend' in df.columns:
            df['reservation_status_date:is_weekend'] = df['reservation_status_date:is_weekend'].replace({0:False, 1:True})

        # удаляем исходные поля дат
        df = df.drop(['reservation_status_date','arrival_date'], axis=1)

        # разбиваем на one hot все поля типа object
        df['agent'] = df['agent'].astype('object')  # надо воспринимать агентов как разные источники, а не цифры
        df = pd.get_dummies(df, prefix_sep='__')

        return df

    def params_reqired(self):
        """Словарь из параметров, которые надо передать модели для предскзания"""
        return { # обязательные параметры
            'hotel': {'type': 'str', 'descr': 'Тип гостиницы'},
            'lead_time': {'type': 'int', 'descr': 'Количество дней между датой бронирования и датой заселения в отель (на момент бронирования).'},
            'arrival_date': {'type': 'date (YYYY-MM-DD)', 'descr': 'Дата прибытия в отель (на момент бронирования).'},
            'stays_in_weekend_nights': {'type': 'int', 'descr': 'Количество выходных дней в бронировании.'},
            'stays_in_week_nights': {'type': 'int', 'descr': 'Количество рабочих дней в бронировании.'},
            'adults': {'type': 'int', 'descr': 'Количество взрослых.'},
            'children': {'type': 'int', 'descr': 'Количество детей.'},
            'babies': {'type': 'int', 'descr': 'Количество младенцев.'},
            'meal': {'type': 'str', 'descr': 'Тип питания, включенный в бронирование.'},
            'country': {'type': 'str', 'descr': 'Страна заказчика.'},
            'market_segment': {'type': 'str', 'descr': 'Маркетинговая сегментация клиентов.'},
            'distribution_channel': {'type': 'str', 'descr': 'Канал продаж, через который было совершено резервирование.'},
            'is_repeated_guest': {'type': 'int', 'descr': 'Клиент уже останавливался в отеле? (0 = нет, 1 = да).'},
            'previous_cancellations': {'type': 'int', 'descr': 'Сколько бронирований клиент отменил в прошлом.'},
            'previous_bookings_not_canceled': {'type': 'int', 'descr': 'Сколько бронирований клиент сделал и не отменил в прошлом.'},
            'reserved_room_type': {'type': 'str', 'descr': 'Желаемый тип номера.'},
            'assigned_room_type': {'type': 'str', 'descr': 'Тип зарезервированного номера.'},
            'booking_changes': {'type': 'str', 'descr': 'Количество изменений бронирования между датой бронирования и записью/отменой.'},
            'deposit_type': {'type': 'str', 'descr': 'Тип первоначального взноса, вносимого при бронировании.'},
            'days_in_waiting_list': {'type': 'int', 'descr': 'Сколько дней прошло для подтверждения бронирования.'},
            'customer_type': {'type': 'str', 'descr': 'Тип бронирования.'},
            'adr': {'type': 'float', 'descr': 'Average Daily Rate, средняя цена каждой ночи в бронировании.'},
            'required_car_parking_spaces': {'type': 'int', 'descr': 'Количество парковочных мест, необходимых для бронирования.'},
            'total_of_special_requests': {'type': 'int', 'descr': 'Количество особых пожеланий в бронировании (двуспальная кровать, этаж, номер с видом...)'},
            'reservation_status_date': {'type': 'date (YYYY-MM-DD)', 'descr': 'Дата последнего обновления бронирования.'},
            'agent': {'type': 'str', 'descr': 'ID Агента, сделавшего бронирование (пропустить, если бронирование было сделано не агентом).'},
            'company': {'type': 'str', 'descr': 'ID компании, осуществившей бронирование (пропустить, если бронирование не корпоративное)'},
        }
