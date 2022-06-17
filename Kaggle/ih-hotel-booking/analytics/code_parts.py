# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import seaborn as sns
from sklearn.feature_selection import mutual_info_regression
from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier
# from xgboost import XGBRegressor
# from sklearn.metrics import mean_absolute_error
# from sklearn.preprocessing import OneHotEncoder, LabelEncoder
# import os
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
# import datetime
# import re
from fast_ml.feature_engineering import FeatureEngineering_DateTime
from lazypredict.Supervised import LazyClassifier
# import time
from joblib import dump, load
from string import ascii_uppercase

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# https://www.kaggle.com/code/alexgur/ih-hotel-booking
# https://www.kaggle.com/code/gauravduttakiit/hotel-cancellation-prediction-lazypredict/notebook

def make_mi_scores_multithread(X, y, discrete_features='auto'):
    # multithread
    def make_mi_scores(*args):
        # singlethread (uses only one CPU core)
        X, y, discrete_features = list(*args)
        if isinstance(X, pd.Series):
            X = pd.DataFrame(X)
        mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
        mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
        mi_scores = mi_scores.sort_values(ascending=False)
        return mi_scores

    # разделим датасет по колонкам, чтобы сделать несколько потоков обработки
    cpu_cnt = cpu_count()

    # сделаем так, чтобы каждому ядру процессора досталось примерно
    # равное поличество колонок на обработку
    chunk_size = 1
    column_to_process = len(X.columns)
    if cpu_cnt < column_to_process:
        chunk_size = (column_to_process // cpu_cnt) + 1

    X_chunk = [X.iloc[:,i:i + chunk_size] for i in range(0, len(X.columns), chunk_size)]
    args_list = []
    for chunk in X_chunk:
        args_list.append([chunk, y, discrete_features])

    pool = ThreadPool(cpu_cnt)  # параметр - количество потоков
    results = pool.map(make_mi_scores, args_list)  # вернёт список результатов
    pool.close()
    results = pd.concat(results)  # объединяем результаты
    results = pd.DataFrame(results)

    assert len(X) == len(results), 'При определении коррелляции параметров с' \
                                   'результатом была утеряна часть данных!'
    return results
#
def make_mi_scores(X, y, discrete_features='auto'):
    if isinstance(X, pd.Series):
        X = pd.DataFrame(X)
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores
#
# def plot_mi_scores(scores):
#     scores = scores.sort_values(ascending=True)
#     width = np.arange(len(scores))
#     ticks = list(scores.index)
#     plt.barh(width, scores)
#     plt.yticks(width, ticks)
#     plt.title("Mutual Information Scores")

# def date_split(df, column: str):
#     """Разбивает колонку с датами на несколько колонок с разными частями даты и в разных форматах.
#     :prarm date_col: колонка фрейма pd с датой
#     :return: несколько колонок с датами в разном формате
#     """
#     # import datetime
#
#     # получить статистику по длинам строк (распределение), чтобы оценить какие там данные
#     date_lengths = df[column].str.len()
#     date_lengths.value_counts()
#
#     # если у нас есть странные строки с датой, то проверяем их
#     indices = np.where([date_lengths != 10])[1]  # формат вида "2017-06-24"
#     if indices.size > 0:
#         print('Неверный формат даты в индексах:', indices)
#         # сбрасываем значения или сами руками прописываем верное
#         # df.loc[indices, 'Date'] = ''
#
#     date_parsed = pd.to_datetime(df[column],
#                                  format="%Y-%m-%d",
#                                  infer_datetime_format=True)
#
#     # https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.quarter.html
#     df[f'{column}_day'] = date_parsed.dt.day
#     df[f'{column}_month'] = date_parsed.dt.month
#     df[f'{column}_month_name'] = date_parsed.dt.month_name()
#     df[f'{column}_isoweekday'] = date_parsed.dt.weekday
#     df[f'{column}_year'] = date_parsed.dt.year
#     df[f'{column}_year_quarter'] = date_parsed.dt.quarter
#     df[f'{column}_week'] = date_parsed.dt.isocalendar().week
#     df[f'{column}_week_day_name'] = date_parsed.dt.day_name()
#     df[f'{column}_leap_year'] = date_parsed.dt.is_leap_year
#
#     df = df.drop(column, axis=1)  # удаляем исходную колонку
#
#     return df

def predict_rate_bool(valid, pred, threshold: float = 0.5) -> int:
    """Вычисляет процент правильных предсказаний
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

def reduce_mem_usage(props):
    start_mem_usg = props.memory_usage().sum() / 1024**2
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in.
    print("******************************")
    for col in props.columns:
        if props[col].dtype != object:  # Exclude strings

            # Print current column type
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
            print("dtype after: ", props[col].dtype)

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

def undummify(df, prefix_sep="__"):
    cols2collapse = {
        item.split(prefix_sep)[0]: (prefix_sep in item) for item in df.columns
    }
    series_list = []
    for col, needs_to_collapse in cols2collapse.items():
        if needs_to_collapse:
            undummified = (
                df.filter(like=col)
                .idxmax(axis=1)
                .apply(lambda x: x.split(prefix_sep, maxsplit=1)[1])
                .rename(col)
            )
            series_list.append(undummified)
        else:
            series_list.append(df[col])
    undummified_df = pd.concat(series_list, axis=1)
    return undummified_df


# def one_hot(df, columns: list = []):
#     """Делает кодировку "OneHot" для всех столбцов "columns"
#     :prarm df: pandas data frame
#     :prarm columns: предсказанные значения
#     :return df:
#     """
#     # https://towardsdatascience.com/categorical-encoding-using-label-encoding-and-one-hot-encoder-911ef77fb5bd
#
#     dum_df = pd.get_dummies(df, columns=[columns])
#
#     # object_cols = [col for col in X_train.columns if X_train[col].dtype == "object"]
#     #
#     # # Apply one-hot encoder to each column with categorical data
#     # OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
#     # OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
#     # OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))
#     #
#     # # One-hot encoding removed index; put it back
#     # OH_cols_train.index = X_train.index
#     # OH_cols_valid.index = X_valid.index
#     #
#     # # Remove categorical columns (will replace with one-hot encoding)
#     # num_X_train = X_train.drop(object_cols, axis=1)
#     # num_X_valid = X_valid.drop(object_cols, axis=1)
#     #
#     # # Add one-hot encoded columns to numerical features
#     # X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
#     # X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)
#
#     return df


def process(df):
    # проверям типы колонок:
    for column in df.columns:
        print(f'{df[column].dtype}: {column}')

    # уникальные значения:
    # for column in df.columns:
    #     print(f'"{column}": {list(pd.unique(df[column]))}')

    # кол-во пустых ячеек таблицы
    missing_values_count = df.isnull().sum()

    # В каких именно колонках отсутствуют строки
    print(missing_values_count)

    total_cells = np.product(df.shape)  # всего количество ячеек
    total_missing = missing_values_count.sum()
    total_missing_prc = round(100 * total_missing / total_cells)

    print(f'Всего ячеек: {total_cells}')
    print(f'Пустых ячеек: {total_missing_prc} %')

    # df.info()

    # в каких столбцах есть пропущенные значения
    #     round(df.isnull().sum() * 100 / len(df), 2).sort_values(ascending=False)
    #
    #
    # int64: is_cancelled
    # int64: lead_time - 0.03
    # int64: stays_in_weekend_nights - 0
    # int64: stays_in_week_nights - 0
    # int64: adults - 0
    # float64: children - 0
    # int64: babies - 0
    # object: meal
    # object: country
    # object: market_segment
    # object: distribution_channel
    # int64: is_repeated_guest - 0
    # int64: previous_cancellations - 0.04
    # int64: previous_bookings_not_canceled - 0
    # object: reserved_room_type
    # object: assigned_room_type
    # int64: booking_changes - 0.02
    # object: deposit_type
    # float64: agent - 0
    # float64: company - 0.01
    # int64: days_in_waiting_list - 0
    # object: customer_type
    # float64: adr - 0
    # int64: required_car_parking_spaces - 0.03
    # int64: total_of_special_requests - 0.04
    # object: reservation_status_date
    # object: arrival_date
    #
    #
    #
    #     df_mi = df[['stays_in_weekend_nights', 'stays_in_week_nights', 'adr']]
    #     df_mi = df_mi.fillna(value=0).astype('int64')
    #     mi_scores = mutual_info_regression(df_mi, df['is_cancelled'])
    #     mi_scores = pd.Series(mi_scores, name="MI Scores", index=df_mi.columns)
    #     mi_scores.sort_values(ascending=False)
    #
    #
    #
    #     mutual_info_regression
    #
    # df['agent'] = df['agent'].astype('int64')
    # df['company'] = df['company'].astype('int64')
    # mi_scores = make_mi_scores_multithread(mi_scores_df, df['is_cancelled'])
    #
    # df_scores = []
    # for col in df.columns:
    #     if 'is_cancelled' in col:
    #         continue
    #     df_scores.append(make_mi_scores(df[col], df['is_cancelled']))
    # df_scores = pd.concat(df_scores)
    # df_scores.sort_values(ascending=False)
    #
    # pdf = []
    # for col in df.columns:
    #     if 'is_cancelled' in col:
    #         continue
    #     # for col in ['lead_time', 'previous_cancellations']:
    #     mi = make_mi_scores(pd.DataFrame(df[col][:10000]), df['is_cancelled'][:10000])
    #     print(mi)
    #     pdf.append(mi)
    # pdf = pd.concat(pdf)
    # pdf.sort_values(ascending=False)
    #
    # labels = []
    # for col, val in pdf.items():
    #     if any(sub in col for sub in ['agent__', 'company__', 'country__']) and value < 0.005:
    #         labels.append(col)
    # labels
    # pdf = pdf.drop(labels=labels)
    #
    # pdf = pdf.drop(labels=pdf[pdf < 0.005].index)
    #
    #
    #
    # pdfm = make_mi_scores_multithread(df, df['is_cancelled'])
    # pdfm
    #
    # for col in pdf.columns:
    #     if any(sub in col for sub in ['agent__', 'company__']) and pdf[col] == 0:
    #         print(col)

    #
    #     # df['is_repeated_guest'].corr(df['is_cancelled'])
    #
    #     mi_scores_df = df[['is_repeated_guest', 'company']].fillna(value=0)
    #
    #     mi_scores_df = pd.get_dummies(mi_scores_df, prefix_sep='__')
    #     mi_scores = make_mi_scores(mi_scores_df, df['is_cancelled'])
    #     mi_scores.sort_values(ascending=False)

    # Заполнить пустые значения
    df['country'] = df['country'].fillna(value='No')
    # df[['company']] = df[['company']].fillna(value='No')  # 94 % отсутствует
    df['agent'] = df['agent'].fillna(value=0) # id агенства
    df['company'] = df['company'].fillna(value=0) # id company
    df['children'] = df['children'].fillna(value=0)

    # преобразуем изменённые колонки к новому типу
    df['children'] = df['children'].astype('int64')
    df['agent'] = df['agent'].astype('int64')

    # parce date
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'],
                                                   format="%Y-%m-%d",
                                                   infer_datetime_format=True)

    df['arrival_date'] = pd.to_datetime(df['arrival_date'],
                                        format="%Y-%m-%d",
                                        infer_datetime_format=True)

    # удалим бессмысленные поля
    # df = df.drop('id_booking', axis=1)  # id_booking - порядковый номер записи
    df = df.drop('company', axis=1)

    # разбираем поля даты на составляющие
    # df = date_split(df, 'reservation_status_date')
    # df = date_split(df, 'arrival_date')

    # посмотрим на колонки с типом "объект"
    object_cols = [col for col in df.columns if df[col].dtype == "object"]
    df[object_cols].nunique()
    for i in object_cols:
        print(i)
        print(round(df[i].value_counts(), 2), '\n')  # Вернёт возможные варианты значений

    # заменим 'Undefined' на 'SC', потому что по описанию отсутствие данных - это и есть 'SC'
    df.meal = df.meal.replace('Undefined', 'SC')
    df.meal.value_counts()

    # заменяем все значения 'Undefined' на Nan
    df = df.replace('Undefined', np.nan)
    round(df.isnull().sum() * 100 / len(df), 2).sort_values(ascending=False)

    # -------------

    # значения стран стоит преобразовать в регионы, котому что их слишком много разных (174)
    # https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
    country = pd.read_csv('res/ISO-3166-Countries-with-Regional-Codes.csv')
    country = country[['alpha-3', 'region']]
    country.columns = ['country', 'region']
    country.head()

    df = df.merge(country, on='country', how='left', left_index=True, right_index=True)
    df = df.drop(['country'], axis=1)
    df.head()  # добавится 1 колонка 'region'

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
    df.head()
    # с помощью разницы reserved_room_type и assigned_room_type создаём новый параметр
    df['room_type_diff'] = df.reserved_room_type - df.assigned_room_type
    df['room_type_diff'].value_counts()
    df = df.drop(['reserved_room_type','assigned_room_type'], axis=1)  # больше не нужно
    df.head()

    # в новом параметре важно только общее впечатление: номер хуже или лучше
    def positive_zero_negative(x):
        if x == 0:
            return 0
        return 1 if x > 0 else -1

    df['room_type_diff'] = df['room_type_diff'].apply(positive_zero_negative)
    df['room_type_diff'].value_counts()

    # питание заменяем на цифры (чем больше цифра, тем больше еды):
    # Undefined/SC – no meal package;
    # BB – Bed & Breakfast;
    # HB – Half board (breakfast and one other meal – usually dinner);
    # FB – Full board (breakfast, lunch and dinner)
    df.meal = df.meal.replace({'Undefined':0, 'SC':0, 'BB':1, 'HB':2, 'FB':3})
    df.meal.value_counts()

    # разбираем даты на составляющие, добавляем новые колонки
    dtf = FeatureEngineering_DateTime()
    dtf.fit(df, datetime_variables=['reservation_status_date', 'arrival_date'])
    df = dtf.transform(df)
    df.head()
    # удаляем столбцы со слишком уникальными/редкими значениями в датах (стоит поискать не только в датах)
    nunique_date = df.nunique().reset_index()
    nunique_date[nunique_date['index'].str.contains('_date:') == True]
    remove_col = nunique_date[(nunique_date[0]==len(df)) | (nunique_date[0]==0) | (nunique_date[0]==1) ]['index'].tolist()
    remove_col
    df = df.drop(remove_col, axis=1)
    df.head()

    # исправляем значения полей "is_" на тип bool (а то они int, а это неверно по смыслу)
    if 'arrival_date:is_weekend' in df.columns:
        df['arrival_date:is_weekend'] = df['arrival_date:is_weekend'].replace({0:False, 1:True})

    if 'reservation_status_date:is_weekend' in df.columns:
        df['reservation_status_date:is_weekend'] = df['reservation_status_date:is_weekend'].replace({0:False, 1:True})

    df.head()
    # удаляем исходные поля дат
    df = df.drop(['reservation_status_date','arrival_date'], axis=1)
    df.info()

    # надо переименовать все колонки, иначе могут быть проблемы с функциями в дальнейшем
    # df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))
    # df.head()

    # разбиваем на one hot все поля типа object
    df['agent'] = df['agent'].astype('object')  # надо воспринимать агентов как разные источники, а не цифры
    df['company'] = df['company'].astype('company')  # надо воспринимать агентов как разные источники, а не цифры
    df = pd.get_dummies(df, prefix_sep='__')
    df.head()




    mi_scores = make_mi_scores_multithread(mi_scores_df, df['is_cancelled'])

    # we have to find features that don't affect a target
    df_scores = []
    for col in df.columns:
        if 'is_cancelled' in col:
            continue
        df_scores.append(make_mi_scores(df[col], df['is_cancelled']))
    df_scores = pd.concat(df_scores)
    df_scores.sort_values(ascending=False)
    # results:
    # adr                                        0.14
    # arrival_date:year                          0.10
    # country__PRT                               0.10
    # ...............................................
    # In the end of that list there would be only columns that can't make any
    # significant impact on target value "is_cancelled". Most of them are "agent"
    # and "company" features. Lets delete all with values less s 0.005:
    df_valueble = df.drop(labels=df_scores[df_scores < 0.005].index.to_list(), axis=1)



    # заполнение следующими значениями из колонки
    # subset_nfl_data.fillna(method='bfill', axis=0).fillna(0)

    # уникальные значения:
    # for column in df.columns:
    #     print(f'{df[column].dtype} - {column}: {list(pd.unique(df[column]))[:20]}')

    # Кодировка oneHot для полей типа object
    # object_cols = [col for col in df.columns if df[col].dtype == "object"]
    # object_cols.append('agent')
    # df = pd.get_dummies(df, columns=object_cols)
    #
    # for column in df.columns:
    #     if df[column].dtype == "UInt32":
    #         df[column] = df[column].astype('int64')
    #
    # object_cols = [col for col in df_valid.columns if df_valid[col].dtype == "object"]
    # object_cols.append('agent')
    # df_valid = pd.get_dummies(df_valid, columns=object_cols)
    #
    # for column in df_valid.columns:
    #     if df_valid[column].dtype == "UInt32":
    #         df_valid[column] = df_valid[column].astype('int64')

    # начинаем разделение и обработку параметров "X" и цели предсказания "y"
    # X_train = df.copy()  # все параметры, кроме предсказываемого
    # y_train = X_train.pop('is_cancelled')  # бронь была отменена. Будем предсказывать это
    #
    # X_valid = df_valid.copy()  # все параметры, кроме предсказываемого
    # y_valid = X_valid.pop('is_cancelled')  # бронь была отменена. Будем предсказывать это

    # # оцениваем зависимость предсказания от каждого параметра
    # mi_scores = make_mi_scores(X, y)
    #
    # # оставляем только те параметры, которые довольно значимы (значение > 0.005)
    # to_work = mi_scores.loc[mi_scores > 0.05].index
    # X = X[to_work]

    # X['reservation_status_date_week'] = X['reservation_status_date_week'].astype('int64')
    # X['arrival_date_week'] = X['arrival_date_week'].astype('int64')

    return df


# на чём тренируем модель
df = pd.read_csv("source/tb_hotel_traintest.csv", index_col='id_booking')
df = process(df)  # обрабатываем данные, готовим колонки
df, NAlist = reduce_mem_usage(df)  # оптимизируем типы переменных

# сохраняем колонки. Они понадобятся на стадии предсказаний, потому что модель не может работать без всех колонок
columns_native = df.columns.to_list()

# что предсказываем
df = pd.read_csv("source/tb_hotel_feat_valid.csv", index_col='id_booking')
df = process(df)  # обрабатываем данные, готовим колонки
df, NAlist = reduce_mem_usage(df)  # оптимизируем типы переменных

columns_predict = df.columns.to_list()

# находим лишние колонки, которые появились в новом дата сете, удаляем их
columns_to_delete = list(set(columns_predict) - set(columns_native))
df = df.drop(columns_to_delete, axis=1)

# находим колонки, которых не достаёт в новом дата сете, и заполняем их нулями
columns_to_add = list(set(columns_native) - set(columns_predict))
if 'is_cancelled' in columns_to_add:  # is_cancelled - предсказываемое значение
    columns_to_add.remove('is_cancelled')
for col in columns_to_add:
    df[col] = 0

len(columns_native) == len(df.columns.to_list()) + 1  # тут сделать assert. Добавляем "+ 1" на колонку с предсказываемым значением

# делаем предсказание
model = load('models/99.92505_XGBClassifier_n_estimators=860_learning_rate=0.4625')
cols_when_model_builds = model.get_booster().feature_names  # порядок полей при создании модели и её использовании должен совпадать

len(columns_native)
len(cols_when_model_builds)
set(cols_when_model_builds) - set(df.columns.to_list())
set(df.columns.to_list()) - set(cols_when_model_builds)

dfr = df[cols_when_model_builds]  # используем только нужне поля в правильном порядке



y_pred = model.predict(dfr)
dfr = dfr.assign(is_cancelled = y_pred)
dfr['is_cancelled'].to_csv('result.csv', sep=',', encoding='utf-8')


# In [78]: len(columns_native)
# Out[78]: 398
#
# In [79]: len(columns_predict)
# Out[79]: 285
#
# In [80]: len(set(columns_native) - set(columns_predict))
# Out[80]: 119



# разделяем датасет, готовим модель
# df_sample = df.sample(n=50000)  # берём небольшую часть для теста
X = df.copy()  # все параметры, кроме предсказываемого
y = X.pop('is_cancelled')  # бронь была отменена. Будем предсказывать это

# round(y.value_counts()*100 / len(y), 2)  # почти 40 % отказываются от брони!

X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                      train_size=0.8,
                                                      test_size=0.2,
                                                      shuffle=True,
                                                      # stratify=y,
                                                      random_state=0)

# проверка работы всех возможных моделей, чтобы выбрать наиболее эффективную
# clf = LazyClassifier(verbose=0, predictions=True)
# models, predictions = clf.fit(X_train, X_valid, y_train, y_valid)
# models
# лучшим по точности оказался XGBClassifier. Вторым и в 10 раз быстрее LGBMClassifier


start = time.time()

# применяем лучший способ
# model = XGBClassifier(n_estimators=680, learning_rate=0.3, tree_method='gpu_hist', predictor='gpu_predictor') # 99.7487%
model = XGBClassifier(n_estimators=860, learning_rate=0.4625) # 99.92505%
model.fit(X_train, y_train)
y_pred = model.predict(X_valid)
print(f'Вероятность правильного предсказания gpu_hist: {predict_rate_bool(y_pred, y_valid)}%')

end = time.time()
print(end - start)

# Best: 0.997875 using {'n_estimators': 860, 'learning_rate': 0.4625}



start = time.time()

# применяем лучший способ
model = XGBClassifier(n_estimators=680, learning_rate=0.3) # Вероятность правильного предсказания: 99.7487%
model.fit(X_train, y_train)
y_pred = model.predict(X_valid)
print(f'Вероятность правильного предсказания cpu: {predict_rate_bool(y_pred, y_valid)}%')

end = time.time()
print(end - start)





# сохранение модели в файл
dump(model, f'models/{predict_rate_bool(y_pred, y_valid)}_XGBClassifier_n_estimators=860_learning_rate=0.4625')
# model = load('models/99.7487_n_estimators=680_learning_rate=0.3')



# from sklearn.metrics import classification_report
# for i in predictions.columns.tolist():
#     print('\t\t',i,'\n')
#     print(classification_report(y_valid, predictions[i]),'\n')



# загрузка модели из файла
# model = load('models/99.7487_n_estimators=680_learning_rate=0.3')




# from lazypredict.Supervised import LazyRegressor
# reg = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None)
# models, predictions = reg.fit(X_train, X_valid, y_train, y_valid)
# models

for thr in np.arange(0.005, 0.02, 0.002):
    df_valueble = df.drop(labels=df_scores[df_scores < thr].index.to_list(), axis=1)
    X = df_valueble.copy()
    y = X.pop('is_cancelled')

    X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                          train_size=0.8,
                                                          test_size=0.2,
                                                          shuffle=True,
                                                          random_state=0)

    model = XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_valid)

    pred_compare = [i[0] == i[1] for i in list(zip(y_pred, y_valid))]
    pred_prcnt = round(100 * sum(pred_compare) / len(pred_compare), 5)
    print(f'Probability of successful prediction = {pred_prcnt} % - {thr}')






# пробуем найти наиболее оптимальные параметры
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold
# from sklearn.metrics import accuracy


df_search = df.sample(n=50000)  # берём небольшую часть для теста
X_search = df_search.copy()  # все параметры, кроме предсказываемого
y_search = X_search.pop('is_cancelled')  # бронь была отменена. Будем предсказывать это

X_train_search, X_valid_search, y_train_search, y_valid_search = train_test_split(X_search, y_search,
                                                                                  train_size=0.8,
                                                                                  test_size=0.2,
                                                                                  shuffle=True,
                                                                                  # stratify=y,
                                                                                  random_state=0)

model = XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor')

param_grid = {
    'n_estimators': np.arange(10, 1000, 10),
    'learning_rate': np.arange(0.0005, 0.5, 0.0005),
    # 'max_depth': np.arange(3, 13, 1),
    # 'min_child_weight': np.arange(0.0001, 0.5, 0.001),
    # 'gamma': np.arange(0.0, 40.0, 0.005),
    # 'subsample': np.arange(0.01, 1.0, 0.01),
    # 'colsample_bylevel': np.arange(0.1, 1.0, 0.01),
    # 'colsample_bytree': np.arange(0.1, 1.0, 0.01),
    #
    # 'min_samples_leaf': np.arange(1, 8),
    # 'min_samples_split': np.arange(2, 10, 2),

    # 'objective': ['binary:logistic'],
    # 'scale_pos_weight': st.randint(0, 2),
}

# kfold = KFold(n_splits=10, shuffle=True, random_state=10)
# grid_search = RandomizedSearchCV(model, param_grid, scoring="accuracy", n_iter = 500, cv=kfold)
# GridSearchCV
grid_search = RandomizedSearchCV(model, param_grid, scoring="accuracy", n_iter = 50)
grid_result = grid_search.fit(X_train_search, y_train_search)

# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']

# применяем лучшую модель
model = grid_result.best_estimator_
model.fit(X_train_search, y_train_search)
y_pred = model.predict(X_valid_search)
print(f'Вероятность правильного предсказания gpu_hist: {predict_rate_bool(y_pred, y_valid_search)}%')


print(f'Вероятность правильного предсказания cpu: {predict_rate_bool(y_pred, y_valid)}%')

# Best: 0.997875 using {'n_estimators': 860, 'learning_rate': 0.4625}


from sklearn.model_selection import GridSearchCV



apt-get install linux-headers-$(uname -r)


# learning_rate = 0
# for learning_rate in range(20, 50, 1):
#     learning_rate = learning_rate/100
#     model = XGBRegressor(n_estimators=100, learning_rate=learning_rate)
#     model.fit(X_train, y_train,
#               eval_set=[(X_valid, y_valid)],
#               verbose=False)
#     y_pred = model.predict(X_valid)
#     rate = predict_rate_bool(y_pred, y_valid)
#     with open(f'learning_rate_{len(X)}', 'a+') as f:
#         st = f'Вероятность {learning_rate}: {rate}%\n'
#         print(st)
#         f.write(st)
#     if learning_rate < rate:
#         learning_rate = rate
#
# with open(f'learning_rate_{len(X)}', 'a+') as f:
#     st = f'Максимум на learning_rate = {learning_rate}%\n'
#     print(st)
#     f.write(st)
#


# params = {
#         'max_depth': [3,4,5,6,7,8,10],
#         'learning_rate':[0.001, 0.003, 0.01,0.03, 0.1,0.3],
#         'n_estimators':[50,100,200,300,500,1000],
#         .... whatever ....
# }
# xgb = xgboost.XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor')
# tuner = GridSearchCV(xgb, params=params)
# tuner.fit(X_train, y_train)
#
# # OR you can pass them in params also.




# n_estimators_max = 0
# for n_estimators in range(10, 2001, 10):
#     model = XGBRegressor(n_estimators=n_estimators)
#     model.fit(X_train, y_train,
#               eval_set=[(X_valid, y_valid)],
#               verbose=False)
#     y_pred = model.predict(X_valid)
#     rate = predict_rate_bool(y_pred, y_valid)
#     with open(f'result_{len(X)}', 'a+') as f:
#         st = f'Вероятность {n_estimators}: {rate}%\n'
#         print(st)
#         f.write(st)
#     if n_estimators_max < rate:
#         n_estimators_max = rate
#
# with open(f'result_{len(X)}', 'a+') as f:
#     st = f'Максимум на n_estimators = {n_estimators_max}%'
#     print(st)
#     f.write(st)


# Вероятность 10: 91.40287%
# Вероятность 20: 95.31787%
# Вероятность 30: 97.38118%
# Вероятность 40: 98.00282%
# Вероятность 50: 98.21885%
# Вероятность 60: 98.50101%
# Вероятность 70: 98.6465%
# Вероятность 80: 98.85813%
# Вероятность 90: 98.96834%
# Вероятность 100: 98.98157%
# Вероятность 110: 99.00362%
# Вероятность 120: 99.05211%
# Вероятность 130: 99.05211%
# Вероятность 140: 99.1447%
# Вероятность 150: 99.24169%
# Вероятность 160: 99.24169%
# Вероятность 170: 99.32105%
# Вероятность 180: 99.36073%
# Вероятность 190: 99.35632%
# Вероятность 200: 99.38277%
# Вероятность 210: 99.39159%
# Вероятность 220: 99.44449%
# Вероятность 230: 99.46213%
# Вероятность 240: 99.47095%
# Вероятность 250: 99.48417%
# Вероятность 260: 99.47095%
# Вероятность 270: 99.49299%
# Вероятность 280: 99.48417%
# Вероятность 290: 99.48417%
# Вероятность 300: 99.4974%
# Вероятность 310: 99.51063%
# Вероятность 320: 99.52385%
# Вероятность 330: 99.54149%
# Вероятность 340: 99.5503%
# Вероятность 500: 99.7002%


# model = XGBRegressor()
# model = XGBRegressor(n_estimators=680, learning_rate=0.05, n_jobs=4)
# model.fit(X_train, y_train)
# y_pred = model.predict(X_valid)
# print(f'Вероятность правильного предсказания: {predict_rate_bool(y_pred, y_valid)}%')


# model = XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=4)
# model = XGBRegressor(tree_method='gpu_hist', gpu_id=0)



# return n_estimators_max

# from multiprocessing import Process



def prc(*args, **kwargs):
# print(*args)
print(y_valid)
# print(**kwargs)

# def prc(*args, **kwargs):

import time

start = time.time()

for n_estimators in range(10, 1000, 10):
    model = XGBRegressor(n_estimators=n_estimators)
    model.fit(X_train, y_train,
              eval_set=[(X_valid, y_valid)],
              verbose=False)
    y_pred = model.predict(X_valid)
    rate = predict_rate_bool(y_pred, y_valid)
    print(f'Вероятность {n_estimators}: {rate}%')
    if n_estimators_max < rate:
        n_estimators_max = rate

end = time.time()
print(end - start)

start = time.time()
def prc(n_est):
    model = XGBRegressor(n_estimators=n_est)
    model.fit(X_train, y_train,
              eval_set=[(X_valid, y_valid)],
              verbose=False)
    y_pred = model.predict(X_valid)
    rate = predict_rate_bool(y_pred, y_valid)
    print(f'Вероятность при n_estimators={n_estimators}: {rate}%')
    return [n_est, rate]

pool = ThreadPool(1)
results = pool.map(prc, list(range(10, 1000, 10)))

print(results)

maximum = sorted(results, key=lambda x: x[1])[-1]

print(f'Макс. вероятность при n_estimators={maximum[0]}: {maximum[1]}%')

end = time.time()
print(end - start)


# results = []
# for item in my_array:
#     results.append(my_function(item))

print("Mean Absolute Error: " + str(mean_absolute_error(y_pred, y_valid)))


#
# X = pd.DataFrame(df['hotel'].copy())
# k = LabelEncoder().fit(X['hotel']).transform(X['hotel'])
# print(k)
#
# # filtered_df = df.apply(pd.to_numeric, errors='ignore')
# # le_dict = {}
# # for col in filtered_df.columns:
# #     print(col)
# #     le_dict[col] = LabelEncoder().fit(filtered_df[col])
# #     filtered_df[col] = le_dict[col].transform(filtered_df[col])
# #
#
# X = pd.DataFrame(df['hotel'].copy())
#
# # enc = OneHotEncoder()
# # enc.fit(X)
# # pd.DataFrame(X)
#
# # creating initial dataframe
# # bridge_types = ('Arch','Beam','Truss','Cantilever','Tied Arch','Suspension','Cable')
# # bridge_df = pd.DataFrame(bridge_types, columns=['Bridge_Types'])# generate binary values using get_dummies
# X = pd.DataFrame(df[['hotel','children']].copy())
# dum_df = pd.get_dummies(X, columns=['hotel'], prefix=["Type_is"])

#
#
# # Apply one-hot encoder to each column with categorical data
# # OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
# enc = OneHotEncoder()
# OH_cols = pd.DataFrame(enc.fit_transform(X['hotel']))
#
# # One-hot encoding removed index; put it back
# OH_cols.index = X.index
#
# # Remove categorical columns (will replace with one-hot encoding)
# # num_X_train = X.drop('agent', axis=1)
#
# # Add one-hot encoded columns to numerical features
# X = pd.concat([X, OH_cols], axis=1)




# X_train, X_valid, y_train, y_valid = train_test_split(X, y,
#                                                       train_size=0.8,
#                                                       test_size=0.2,
#                                                       random_state=0)
#
# X_train, X_valid = one_hot(X_train, X_valid)
#
#
# mi_scores = make_mi_scores(X, y)
# print(mi_scores)
#




#
# X = df['hotel']
# encoder = OneHotEncoder(handle_unknown="ignore")
# X = np.array(X).reshape(1,-1)
# encoder.fit(X)
# X = encoder.transform(X)
# X
# pd.DataFrame(X)

#
# for column in df.columns:
#     print(f'{df[column].dtype}: {column}')
#
# # df = df.select_dtypes(exclude=['object'])
# X = df[:10000].copy()  # все параметры, кроме предсказываемого
# y = X.pop('is_cancelled')  # бронь была отменена. Будем предсказывать это
#
# # === определяем зависимость результата от параметров ===
# if 0:
    # # факторизация всех объектных
    # for colname in X.select_dtypes("object"):
    #     X[colname], _ = X[colname].factorize()
    #
    # # все параметры должны стать теперь integer dtypes
    # # discrete_features = X.dtypes == int
    # # discrete_features = [pd.api.types.is_integer_dtype(t) for t in X.dtypes]
    #
    # # степень зависимости цели "y" от параметров "X"
    # # mi_scores = make_mi_scores(X, y, discrete_features)
    # mi_scores = make_mi_scores(X, y)
    # print(mi_scores)


#
#
# X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
#
#
#
#
#
#
#
#
#
# # Divide data into training and validation subsets
# # X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
#
# X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
#
# model = XGBRegressor()
# model.fit(X_train, y_train)
# y_pred = model.predict(X_valid)
# print("Mean Absolute Error: " + str(mean_absolute_error(y_pred, y_valid)))
# print(f'Вероятность правильного предсказания: {predict_rate_bool(y_valid, y_valid)}%')
#
# model = XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=4)
# model.fit(X_train, y_train,
#              early_stopping_rounds=5,
#              eval_set=[(X_valid, y_valid)],
#              verbose=False)
#
# y_pred = model.predict(X_valid)
# print("Mean Absolute Error: " + str(mean_absolute_error(y_pred, y_valid)))
# for i in range(5, 95, 5):
#     print(f'Вероятность {i/100}: {predict_rate_bool(y_valid, y_pred, i/100)}%')



# print(f'Количество деревьев n_estimators=: {n_estimators}')
# print(f'Ошибка mean_absolute_error=: {mean_absolute_error}')
# print(f'Вероятность правильного предсказания: {predict_rate_bool(y_valid, y_pred_bool)}%')


# for n_estimators in range(10, 200, 10):  # количество деревьев
#     X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
#     model = RandomForestRegressor(n_estimators=n_estimators, random_state=1)
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_valid)
#     mean_absolute_error = mean_absolute_error(y_valid, y_pred)
#
#     # предсказываемое значение имеет тип bool, поэтому вероятность возвращается как
#     # число от 0 до 1. Считаем, что если больше 0.5, то = True
#     y_pred_bool = y_pred > 0.5
#
#     # вычисляем процент правильных предсказаний
#     pred_compare = [i[0] and i[1] for i in list(zip(y_valid, y_pred_bool))]
#     pred_prcnt = 100 * sum(pred_compare) / len(pred_compare)
#     print(f'Количество деревьев n_estimators=: {n_estimators}')
#     print(f'Ошибка mean_absolute_error=: {mean_absolute_error}')
#     print(f'Вероятность правильного предсказания: {pred_prcnt}%')


# model = RandomForestRegressor(n_estimators=100, random_state=0)
# model.fit(X_train, y_train)
# preds = model.predict(X_valid)
# mae = mean_absolute_error(y_valid, preds)
#
# print("Validation MAE for Random Forest Model: {:,.0f}".format(mae))
# print(preds)




# day_of_month_earthquakes = df['arrival_date_parsed'].dt.day
# sns.displot(day_of_month_earthquakes, kde=False, bins=31)


# int64: is_cancelled
# int64: lead_time
# int64: stays_in_weekend_nights
# int64: stays_in_week_nights
# int64: adults
# Int64: children
# int64: babies
# object: meal
# object: country
# object: market_segment
# object: distribution_channel
# int64: is_repeated_guest
# int64: previous_cancellations
# int64: previous_bookings_not_canceled
# object: reserved_room_type
# object: assigned_room_type
# int64: booking_changes
# object: deposit_type
# float64: agent
# float64: company
# int64: days_in_waiting_list
# object: customer_type
# float64: adr
# int64: required_car_parking_spaces
# int64: total_of_special_requests
# object: reservation_status_date
# object: arrival_date
# int64: id_booking
#
#
# # 'children','company','agent','country',
#
# X1 = X.iloc[:,:5]
# discrete_features = X1.dtypes == int
# mi_scores = make_mi_scores(X1[:15000], y[:15000], discrete_features)
# print(mi_scores)



#                                Accuracy  Balanced Accuracy  ROC AUC  F1 Score  Time Taken
# Model
# XGBClassifier                      0.99               0.99     0.99      0.99       13.29
# LGBMClassifier                     0.98               0.97     0.97      0.98        1.60
# LinearSVC                          0.96               0.95     0.95      0.96       16.47
# PassiveAggressiveClassifier        0.95               0.94     0.94      0.95        2.15
# BaggingClassifier                  0.95               0.93     0.93      0.95        3.51
# RandomForestClassifier             0.95               0.93     0.93      0.95        5.29
# ExtraTreesClassifier               0.94               0.92     0.92      0.94        6.66
# LogisticRegression                 0.94               0.92     0.92      0.94        2.37
# DecisionTreeClassifier             0.92               0.91     0.91      0.92        0.80
# SGDClassifier                      0.93               0.91     0.91      0.93        1.67
# Perceptron                         0.91               0.90     0.90      0.91        0.69
# CalibratedClassifierCV             0.91               0.88     0.88      0.91       61.53
# ExtraTreeClassifier                0.86               0.85     0.85      0.86        0.34
# SVC                                0.88               0.83     0.83      0.87      180.09
# KNeighborsClassifier               0.86               0.83     0.83      0.86       74.30
# LinearDiscriminantAnalysis         0.87               0.83     0.83      0.87        2.38
# RidgeClassifier                    0.87               0.83     0.83      0.87        2.20
# RidgeClassifierCV                  0.87               0.83     0.83      0.87        1.69
# AdaBoostClassifier                 0.85               0.81     0.81      0.84        2.83
# LabelSpreading                     0.84               0.78     0.78      0.83      354.67
# LabelPropagation                   0.84               0.78     0.78      0.83      277.62
# NuSVC                              0.83               0.78     0.78      0.82      325.78
# BernoulliNB                        0.78               0.74     0.74      0.77        0.39
# NearestCentroid                    0.77               0.73     0.73      0.76        0.32
# QuadraticDiscriminantAnalysis      0.60               0.65     0.65      0.61       12.68
# GaussianNB                         0.45               0.57     0.57      0.37        0.35
# DummyClassifier                    0.53               0.50     0.50      0.54        0.27
