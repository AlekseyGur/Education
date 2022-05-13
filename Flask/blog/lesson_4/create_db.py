#!virt/bin/python

# создаёт базу данных, копирует в неё необходимые настройки

try:  
    from migrate.versioning import api
    from config import Config as cf
    from app import db
    import os.path

    db.create_all()
    if not os.path.exists(cf.SQLALCHEMY_MIGRATE_REPO):
       api.create(cf.SQLALCHEMY_MIGRATE_REPO, 'database repository')
       api.version_control(cf.SQLALCHEMY_DATABASE_URI, cf.SQLALCHEMY_MIGRATE_REPO)
    else:
       api.version_control(cf.SQLALCHEMY_DATABASE_URI, cf.SQLALCHEMY_MIGRATE_REPO, api.version(cf.SQLALCHEMY_MIGRATE_REPO))
       
    print('Создание папки migrations завершено. Файлы записаны.')
    print('Выполните команду для создания таблиц и столбцов: flask db migrate')
    print('Затем надо выполнить команду: flask db upgrade')
       
except ModuleNotFoundError as e:
    print('Перед выполнением скрипта запустить команду "flask db init" для создания папки migrations. Запускать из-под virt!')
    
