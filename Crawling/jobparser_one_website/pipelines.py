# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy1204

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            pass
            # item['min_salary'], item['max_salary'], item['currency'] = self.process_salary(item['salary'])
            # del item['salary']
        else:
            pass


        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        return 1, 2, 3
