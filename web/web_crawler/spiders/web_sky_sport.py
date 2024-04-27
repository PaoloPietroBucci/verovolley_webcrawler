from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import WebCrawlerItem

import time

class WebCrawlerSkySport(Spider):
    name = "web_crawler_sky_sport"

    allowed_domains = ["sport.sky.it"]
    start_urls = [
        "https://sport.sky.it/argomenti/italvolley",
    ]

    def parse(self, response):
        # Logic of how to extract the HTML
        news_list = Selector(response).xpath('//*[@class="c-card  c-card--CA25-m c-card--CA25-t c-card--CA25-d c-card--no-abstract-m c-card--media  c-card--base"]')

        next_page = Selector(response).xpath('//*[@class="c-pagination__arrow-next"]/@href').extract()

        next_page_link = next_page[0] if next_page else None

        for news_item in news_list:
            # Trigger recursively the parsing of posts
            news_link = news_item.xpath('@href').extract()[0]
            yield Request(news_link, callback=self.parse_posts)

        # Recursively go to the next page
        if next_page_link:
            yield Request(next_page_link, callback=self.parse)

    def parse_posts(self, response):
        item = WebCrawlerItem()
        item['title'] = response.xpath('//*[@class="c-hero__title c-hero__title-content j-hero__title"]/text()').extract()[0]
        item['date'] = response.xpath('//*[@class="c-hero__date"]/text()').extract()
        item['content'] = ' '.join(response.xpath('//*[@class="c-article-section j-article-section l-spacing-m"]/p/text()').extract())
        item['link'] = response.url
        yield item
