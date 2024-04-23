from scrapy import Spider, Request
import re
from ..items  import BlogPostItem


class OASportSpider(Spider):
    name = 'ivolleymagazine'
    allowed_domains = ['ivolleymagazine.it']
    start_urls = ['https://www.ivolleymagazine.it/category/news/']

    def parse(self, response):
        pages_article = response.xpath('//h2[contains(@class, "entry-title")]/a/@href').getall()
        for article in pages_article:
            link = response.urljoin(article)
            yield Request(url=link, callback=self.parse_article)
        next_page = response.xpath('//li[contains(@class, "next")]/a/@href').get()
        yield Request(url=next_page, callback=self.parse)
    def parse_article(self, response):
        post = BlogPostItem()
        article_paragrafs = response.xpath('//div[contains(@class, "entry-content")]/p/text()').getall()
        unique_text = ' '.join(article_paragrafs)
        article_title = response.xpath('//h1/text()').get()
        post['title'] = article_title.strip()
        post['content'] = unique_text.strip()
        yield post
#  scrapy crawl ivolleymagazine -o output.json
