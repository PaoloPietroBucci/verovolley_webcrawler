from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import BlogPostItem

import unidecode

class WebCrawlerSkySport(Spider):
    name = "web_crawler_sky_sport"

    allowed_domains = ["sport.sky.it"]
    start_urls = [
        "https://sport.sky.it/argomenti/italvolley",
    ]

    def parse(self, response):
        # Logic of how to extract the HTML
        news_list = Selector(response).xpath('//*[@class="c-card  c-card--CA25-m c-card--CA25-t c-card--CA25-d c-card--no-abstract-m c-card--media  c-card--base"]')

        # Link of next page
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
        item = BlogPostItem()

        # Format title
        item['title'] = unidecode.unidecode(response.xpath('//*[@class="c-hero__title c-hero__title-content j-hero__title"]/text()').extract()[0])

        # Format date
        raw_date = response.xpath('//*[@class="c-hero__date"]/text()').extract()[0]
        item['date'] = self.format_date(raw_date)

        # Format text
        raw_text = response.xpath('//*[@class="c-article-section j-article-section l-spacing-m"]/p')
        inner_text = self.format_innertext(raw_text)
        # Format accents and special characters
        formatted_text = unidecode.unidecode(inner_text[0] if inner_text else "")
        item['content'] = formatted_text

        # Add Link
        item['link'] = response.url

        yield item

    def map_months(self, month):
        # map the inputs to the function blocks
        months_mapping = {
        'gen': '1',
        'feb': '2',
        'mar': '3',
        'apr': '4',
        'mag': '5',
        'gun': '6',
        'lug': '7',
        'ago': '8',
        'set': '9',
        'ott': '10',
        'nov': '11',
        'dic': '12',
        }

        return months_mapping[month]

    def format_date(self, raw_date):
        month = self.map_months(raw_date.split(' ')[1])
        formatted_date = raw_date.split(' ')[0] + "/" + month + "/" + raw_date.split(' ')[2] + " " + raw_date.split(' ')[4].strip()
        return formatted_date

    def format_innertext(self, elements, delimiter=" "):
        return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)
