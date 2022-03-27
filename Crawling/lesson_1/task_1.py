# 1. Посмотреть документацию к API GitHub, разобраться как вывести список
# наименований репозиториев для конкретного пользователя, сохранить
# JSON-вывод в файле *.json.

import requests
import json

login = 'AlekseyGur'
url = f'https://api.github.com/users/{login}/repos'
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)

    print(f'Cписок репозиториев пользователя {login}:')
    for repo in data:
        if login == repo['name']:
            continue  # пропускаем репозиторий конфигов
        print(f"{repo['name']} - {repo['url']}")

    # сохранение данных в файл
    with open(login + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
