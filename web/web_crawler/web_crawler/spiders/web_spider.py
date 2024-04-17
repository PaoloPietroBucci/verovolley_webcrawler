from scrapy import Spider
from scrapy.selector import Selector

from web_crawler.items import WebCrawlerItem


class WebCrawlerSpider(Spider):
    name = "web_crawler"

    # TODO: Add domains of different websites
    allowed_domains = ["https://www.volleynews.it/"]
    start_urls = [
        "https://www.volleynews.it/category/serie-a/a1femminile/",
    ]

    def parse(self, response):
        # Logic of how to extract the HTML

            # TODO: Recursively crawl the extracted url's
            news_list = Selector(response).xpath('//*[@class="elementor-widget-container"]/h2/a')

            for news_item in news_list:
                item = WebCrawlerItem()
                # For now just store the tile of the post and its url
                item['title'] = news_item.xpath('text()').extract()[0]
                item['url'] = news_item.xpath('@href').extract()
                # TODO: Export it in JSON
                yield item
