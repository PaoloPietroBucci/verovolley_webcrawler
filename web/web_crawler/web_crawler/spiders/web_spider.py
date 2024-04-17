from scrapy import Spider
from scrapy.selector import Selector

from web_crawler.items import WebCrawlerItem


class WebCrawlerSpider(Spider):
    name = "web_crawler"
    allowed_domains = ["https://www.volleynews.it/"]
    start_urls = [
        "https://www.volleynews.it/category/serie-a/a1femminile/",
    ]

    def parse(self, response):
            news_list = Selector(response).xpath('//*[@class="elementor-widget-container"]/h2/a')
            print(len(news_list))
            for news_item in news_list:
                item = WebCrawlerItem()
                item['title'] = news_item.xpath('text()').extract()[0]
                item['url'] = news_item.xpath('@href').extract()
                yield item
