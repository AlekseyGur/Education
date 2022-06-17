import pandas as pd
from glob import glob
from json import dump as json_dump, load as json_load
import time
import datetime

# df = pd.read_csv('source/train.csv')
# da = df[df['labels'].isin(['frog_eye_leaf_spot', 'scab', 'rust'])]
# df['labels'] = df['labels'].str.split(' ')
# df['labels'].value_counts()

infos = []
for path in glob('models_selectel/old/*/info'):
    with open(path) as f:
        info = json_load(f)
        if 'predicted_amount' in info:
            info['path'] = path
            info['predicted_amount'] = pd.DataFrame(info['predicted_amount'])
            info['timestamp'] = time.mktime(datetime.datetime.strptime(info['date'], '%Y.%m.%d %H:%M:%S').timetuple())

            infos.append(info)

def sortByTimestamp(x):
    return int(x['timestamp'])

infos = sorted(infos, key=sortByTimestamp, reverse=True)

for info in infos:
    classes = list(info['predicted_amount'].index)
    print(info['predicted_amount'])
    print(info['path'].rstrip('/info'))
    # if len(classes) == 2 and 'healthy' in classes:
    #     print(info['path'].rstrip('/info'))
    #     # print(info['date'])
    #     # print(info['path'])
    #     # print(info['timestamp'])
    #     print(classes)
    #     # print(info['predicted_amount'])
    #     # print(round(max(info['history']['val_f1_score']), 5))
    print('=' * 90)


# for path in glob('models_selectel/*/info'):
#     with open(path) as f:
#         info = json_load(f)
#         if 'predicted_amount' in info:
#             info['predicted_amount'] = pd.DataFrame(info['predicted_amount'])
#             print(info['predicted_amount'].index.to_list())


# 2022.06.09 19:22:54
#                     Real  Predicted      %
# complex             2151          1    0.0
# frog_eye_leaf_spot  4352          1    0.0
# healthy             4624      13069  283.0
# powdery_mildew      1271         25    2.0
# rust                2077          2    0.0
# scab                5712       5534   97.0
# ==================================================
# 2022.06.09 17:17:58
#                     Real  Predicted      %
# frog_eye_leaf_spot   817        817  100.0
# healthy             1183       1183  100.0
# ==================================================
# 2022.06.09 17:59:08
#                     Real  Predicted      %
# frog_eye_leaf_spot  3181       3183  100.0
# healthy             4624       4635  100.0
# scab                4826       4823  100.0
# ==================================================
# Общее количество предсказаний по значениям:
#                     Real  Predicted      %
# frog_eye_leaf_spot  3181          1    0.0
# healthy             4624      10245  222.0
# powdery_mildew      1184        519   44.0
# rust                1860         95    5.0
# scab                4826       4815  100.0
# ==================================================
