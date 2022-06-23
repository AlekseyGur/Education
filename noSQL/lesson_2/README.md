---
title: Redis Practice
description:
---
# Redis

## Эксперимент

Сделать очень простую страницу с некоторой рекламной информацией для
посетителя.

Вычислять количество просмотров.

### webserver

- Для вебсервера возьмём фреймворк flask
- Создадим страницу в вебсервере
- Создадим один обработчик одного адреса (route) для предоставления страницы

### redis

- Для подключения к redis установим python3 коннектор
- В redis будем хранить счетчик посещений

## Реализация

### Окружение

- Установить redis сервер
- Установить python3
- Установить менеджер python3 пакетов pip3
- Установить pip3 пакет flask
- Установить pip3 пакет python3 redis коннектор
 
#### Docker

- Terminal
    ```
    docker pull redis
    ```

#### Или centos 8

- Terminal
    ```
    sudo dnf install -y python3 python3-pip
    sudo dnf install -y redis
    sudo pip3 install flask
    sudo pip3 install redis==3.5.3
    ```

## Код

- В терминале создадим директорию для проекта
    ``` bash
    mkdir thead
    cd thead
    ```

### Простое приложение `flask`

- Слева в панели с директориями и файлами
  - Выбрать директорию `thead`
  - Правой клавишей мыши контекстное меню New File
- Файл `ad.py`
  - Содержимое
    ``` python
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def theanswer():
        return '42'
    ```
- Запустим в терминале, посмотрим, что получилось
    ``` bash
    export FLASK_APP=ad.py
    export FLASK_ENV=development
    flask run --host=0.0.0.0
    ```
    - Первая строка указывает на файл нашего веб приложения
    - Вторая включает дополнительные функции для разработки, например,
    горячую перезагрузку кода
    - Третья строка запуск приложения по умолчанию на `127.0.0.1:5000`
- Откроем браузер на полученном урле
    ``` bash
    http://<ип адрес виртуалки>:5000
    ```
- Результат 42

### Запустим redis сервер

- `Terminal`
    - Docker
        ```
        docker run --rm --name redis -v $(pwd):/data --network host redis
        ```
    - Или локально
        ``` bash
        redis-server
        ```

- Добавим логику работы с `redis` в файл `ad.py`
  - Новое содержимое файла
    ``` python
    import redis
    from flask import Flask

    app = Flask(__name__)
    r = redis.Redis(host='localhost', port=6379, db=0)

    @app.route('/')
    def theanswer():
        r.incr('page:index:counter')
        return '42 - ' + str(r.get('page:index:counter'))
    ```
    - Перезапуск приложения не требуется, flask автоматически
      обнаружит изменение файла
- Откроем страницу 
    ``` bash
    http://<ип адрес виртуалки>:5000
    ```
- Результат 42 и количество посещений

### Зайдём пару раз на страницу

- `Terminal`
    ``` bash
    curl http://127.0.0.1:5000
    curl http://127.0.0.1:5000
    curl http://127.0.0.1:5000
    ```
- Закроем терминал

### Проверим счётчик в redis


- `Terminal`
    - Docker
        ```bash
        docker run --network host -it --rm redis redis-cli
        ```
    - Или локально
        ``` bash
        redis-cli
        ```
- `127.0.0.1:6379>`
    ```
    get page:index:counter
    ```
- Закроем терминал

## Результат

Веб-приложение, которое сохраняет количество просмотров страницы. На
текущий момент этот счетчик бесконечно увеличивается, и, чтобы понимать
просмотры за день, надо каждые сутки смотреть за скоростью изменения
счетчика.

## Посуточные счетчики

Давайте для каждых суток создавать новый счетчик.

- `ad.py`
    ``` python
    import redis
    from flask import Flask
    from time import strftime

    app = Flask(__name__)
    r = redis.Redis(host='localhost', port=6379, db=0)

    @app.route('/')
    def theanswer():
        day = strftime("%Y-%m-%d")
        r.incr('page:index:counter:'+day)
        return '42 - ' + str(r.get('page:index:counter:'+day))
    ```

### Зайдём пару раз на страницу

- Меню `Terminal`/`New Terminal`
    ``` bash
    curl http://127.0.0.1:5000
    curl http://127.0.0.1:5000
    curl http://127.0.0.1:5000
    ```

### Проверим счётчики в redis

- Меню `Terminal`/`New Terminal`
    ``` bash
    redis-cli
    ```
- Запросим все ключи по шаблону `page:index:counter:*`
    - `127.0.0.1:6379>`
        ```
        KEYS page:index:counter:*
        ```
- Запросим значение ключа за сегодня
    ```
    GET page:index:counter:<подставить дату>
    ```
- Закроем терминал

## Самостоятельное

Сделанное решение всеми сторонами хорошее, кроме ситуации, когда один и тот же
посетитель приходит больше одного раза. Это накручивает просмотры
в нашей небольшой домашней странице.

**Предложение:** в случае, если посетитель заходит повторно, не
учитывать это в статистике.

Второй вопрос который может возникнуть: интересно посмотреть статистику — «а кто именно заходил?».

**Предложение2:** записывать информацию о том, кто именно заходил на страницу.

**Рекомендации**
- Использовать куки для идентификации пользователя
- Рассмотреть наиболее подходящую структуру для счетчика посещений в Redis
- Подумать, как будет вычисляться статистика

## Troubleshooting

- Если на странице `Traceback (most recent call last)`
  - Значит допущена ошибка в python коде, перепроверьте, пожалуйста
- Если на странице `redis.sentinel.MasterNotFoundError`
  - Значит не запущен `redis sentinel`

 

---
title: Redis Cluster Practice
description:
---
## Код

- В терминале создадим директорию для проекта
    ``` bash
    mkdir thead
    cd thead
    ```

## Кластеризация (со звездочкой)

### Подготовка 

```
thead
├── ad.py
├── redis1
│   └── redis.conf
├── redis2
│   └── redis.conf
└── sentinel
    └── sentinel.conf
```

- Создадим директорию для первого узла redis
    ```
    mkdir redis1
    ```
- Файл `redis1/redis.conf`
    ```
    bind 127.0.0.1
    port 6379
    ```
- Создадим директорию для второго узла redis
    ```
    mkdir redis2
    ```
- Файл `redis2/redis.conf`
    ```
    bind 127.0.0.1
    port 6380
    slaveof 127.0.0.1 6379
    ```
- Создадим директорию для процесса sentinel, который будет следить за живостью узлов
    ```
    mkdir sentinel
    ```
- Файл конфига `sentinel/sentinel.conf`
    ```
    bind 127.0.0.1
    port 16379

    sentinel monitor THEAD_CLUSTER 127.0.0.1 6379 1
    ```
- Теперь укажем python приложению подключаться к sentinel и выполнять действия с счетчиком посетителей на мастер узле
  - `ad.py`
    ``` python
    from flask import Flask
    app = Flask(__name__)

    import redis

    from redis.sentinel import Sentinel

    sentinel = Sentinel([('localhost', 16379)], socket_timeout=0.1)
    master = sentinel.master_for('THEAD_CLUSTER', socket_timeout=0.1)

    from time import strftime
    @app.route('/')
    def theanswer():
        day = strftime("%Y-%m-%d")
        master.incr('page:index:counter:'+day)
        return '42 - ' + str(master.get('page:index:counter:'+day))
    ```

### Запуск

Запустим систему в 4х терминалах

- Первый терминал `Redis`
    ``` bash
    cd redis1
    redis-server redis.conf
    ```

- Второй терминал `Redis`
    ``` bash
    cd redis2
    redis-server redis.conf
    ```

- Третий терминал `Redis Sentinel`
    ``` bash
    cd sentinel
    redis-sentinel sentinel.conf
    ```

- Веб приложение
    ``` bash
    export FLASK_APP=ad.py
    export FLASK_ENV=development
    flask run --host 0.0.0.0
    ```

- Перейдем на страницу `127.0.0.1:5000`
- Выключим `Redis1` в терминале нажав `Ctrl-C`
- Перейдем на страницу ещё раз `127.0.0.1:5000`
  - Может возникнуть ошибка это значит Sentinel еще не переключил на запасной `Redis`
  - Обновим
- Включим `Redis1`
- Проверим, что счётчик везде одинаковый
    ``` bash
    redis-cli
    KEYS page:index:counter:*
    ```

    ```
    GET page:index:counter:<Подставить дату>
    ```

    ``` bash
    redis-cli -p 6380
    KEYS page:index:counter:*
    ```

    ```
    GET page:index:counter:<Подставить дату>
    ```

- Командой `GET имя ключа` получим и сравним значения счётчиков
