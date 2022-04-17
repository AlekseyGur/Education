from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scr import settings

# === hh.ru ===
# from scr import settings
from scr.spiders.hh_ru import HhRuSpider
# from jobparser.spiders.hhru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhRuSpider)
    # process.crawl(SjruSpider)
    process.start()

# === Avito.ru ===
from scr.spiders.avito_ru import AvitoSpider
# from scr import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider, mark='asus')  # mark - это что искать
    process.start()
