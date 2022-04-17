import scrapy
from scrapy.http import HtmlResponse
from scr.items import JobparserItem

class HhRuSpider(scrapy.Spider):
    name = 'hh.ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://moscow.hh.ru/search/vacancy?area=1&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()

        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()
        # print(name, salary)
        yield JobparserItem(name=name,salary=salary)
