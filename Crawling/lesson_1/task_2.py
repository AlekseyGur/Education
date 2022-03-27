# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json


params = {'access_token': '****access_token****',
          'count': 10,  # количество групп на страницу
          'extended': '1',  # полная информация о паблице
          'offset': 0,  # смещение (элементы, а не страницы!)
          'v': '5.131'}

url = 'https://api.vk.com/method/groups.get'
response = requests.get(url, params=params)

if response.status_code == 200:
    data = json.loads(response.text)

    print(f'Cписок названий групп пользователя в ВКонтакте:')
    for group in data['response']['items']:
        print(group['name'])

    # сохранение данных в файл
    with open('vk.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
