from scrapy import Spider, Request
import re
from ..items  import BlogPostItem

import unidecode


class OASportSpider(Spider):
    name = 'ivolleymagazine'
    allowed_domains = ['ivolleymagazine.it']
    start_urls = ['https://www.ivolleymagazine.it/category/news/campionati/a2-maschile-e-femminile/']

    def parse(self, response):
        # Logic of how to extract the HTML
        pages_article = response.xpath('//h2[contains(@class, "entry-title")]/a/@href').getall()

        # Trigger recursively the parsing of articles
        for article in pages_article:
            link = response.urljoin(article)
            yield Request(url=link, callback=self.parse_article)

        # Recursively go to the next page
        next_page = response.xpath('//li[contains(@class, "next")]/a/@href').get()
        yield Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        post = BlogPostItem()
        # Format title
        post['title'] = unidecode.unidecode(response.xpath('//h1/text()').get()).strip()

        # Format date
        raw_date = response.xpath('//*[@class="entry-date published updated"]/@datetime').extract()[0]
        post['date'] = raw_date

        # Format text
        raw_text = response.xpath('//div[contains(@class, "entry-content")]/p/text()').getall()
        inner_text = ' '.join(raw_text)
        # Format accents and special characters
        formatted_text = unidecode.unidecode(inner_text).strip()
        post['content'] = formatted_text

        # Add Link
        post['link'] = response.url
        yield post

#  scrapy crawl ivolleymagazine -o output.json
