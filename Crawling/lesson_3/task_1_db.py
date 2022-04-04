from pymongo import MongoClient


class DB():
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)  # соединение
        mongodb = client['crawler']  # база
        self.vacancies = mongodb.vacancies  # коллекция

    def get_id(self, site: str, vacancyid: str) -> str:
        """Получение уникального id вакансии для сохранения/поиска в базе данных.
        :param site: обязательное, символьный код сайта
        :param vacancyid: обязательное, уникальный id вакансии
        :return: уникальный id вакансии
        """
        return f'{site}/{vacancyid}'

    def check_id_exist(self, id: str) -> bool:
        """Существует ли вакансия с таким id в базе. .
        :param id: обязательное, уникальный id вакансии, который записывается
                   в _id (в mongodb). Получается через метод "get_id"
        :return: True - есть в базе. False - нет в базе
        """
        return self.vacancies.find_one({'_id': id}) is not None

    def get_list(self, min_salary: float = 0.0) -> list:
        """Возвращает список вакансии.
        :param min_salary: минимальная сумма оплаты (учитываются поля min и max)
        :return: список вакансий или пустой список в случае неудачи
        :raises Errors: может вернуть ошибку, если нет соединения с базой
        """
        req = {'$and': [{'max': {'$gte': min_salary}},
                        {'min': {'$gte': min_salary}}]}

        try:
            return self.vacancies.find(req)
        except Exception as e:
            print('Ошибка при получении выборки из базы:')
            print(e)
            return []

    def add_vacancy(self, vacancy_info: dict, vacancyid: str) -> str:
        """Добавление вакансии в базу. Словарь vacancy_info должен содержать поля:
        ['name'] - Наименование вакансии
        ['min'] - Минимальная зарплата
        ['max'] - Максимальная зарплата
        ['currency'] - Валюта зарплаты
        ['url'] - Ссылка на саму вакансию (обязательное поле)
        ['site'] - Сайт, откуда собрана вакансия (обязательное поле)

        :param vacancyid: обязательное, уникальный id вакансии
        :return: id успешно добавленного элемента. False в случае неудачи.
        """
        id = self.get_id(vacancy_info['site'], vacancyid)

        if self.check_id_exist(id):
            print(f'Вакансия с кодом "{id}" уже есть в базе. Пропускаем')
            return False

        try:
            vacancy_info['_id'] = id
            res = self.vacancies.insert_one(vacancy_info)
            print(f'Вакансия с кодом "{res.inserted_id}" успешно сохранена')
            return res.inserted_id
        except Exception as e:
            print('Ошибка при сохранении вакансии в базу:')
            print(e)
            return False
