import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'W6Ge6bH4Sry1'  # нужен при активном CSRF_ENABLEDZ
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENID_PROVIDERS = [
      { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
      { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
      { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
      { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
      { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

    # соединение с базой SLQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # необходим для расширения Flask-SQLAlchemy. Это путь к файлу с нашей базой данных
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # папка, где мы будем хранить файлы SQLAlchemy-migrate
