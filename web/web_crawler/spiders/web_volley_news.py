from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import BlogPostItem

import unidecode

class WebCrawlerVolleyNews(Spider):
    name = "volley_news"

    allowed_domains = ["www.volleynews.it"]
    start_urls = [
        "https://www.volleynews.it/category/serie-a/a1femminile/",
    ]

    def parse(self, response):
        # Logic of how to extract the HTML
        news_list = Selector(response).xpath('//*[@class="elementor-widget-container"]/h2/a')

        next_pages = Selector(response).xpath('//*[@class="ngg-navigation"]/a/@href').extract()

        next_page_link = next_pages[0] if next_pages else None

        for news_item in news_list:
            # Trigger recursively the parsing of posts
            news_link = news_item.xpath('@href').extract()[0]
            yield Request(news_link, callback=self.parse_posts)

        # Recursively go to the next page
        if next_page_link:
            yield Request(next_page_link, callback=self.parse)



    def parse_posts(self, response):
        post = BlogPostItem()
        post['title'] = unidecode.unidecode(response.xpath('//*[@class="elementor-element elementor-element-34954c7b elementor-widget elementor-widget-theme-post-title elementor-page-title elementor-widget-heading"]/div/h1/text()').extract()[0])

        # Format date
        raw_date = response.xpath('//*[@class="elementor-widget-container"]/time/@datetime').extract()[0]
        post['date'] = self.format_date(raw_date)

        # Format text
        raw_text = response.xpath('//*[@class="elementor-element elementor-element-3104ed9c elementor-drop-cap-view-stacked elementor-drop-cap-yes elementor-widget-text-editor elementor-widget elementor-widget-my-custom-post-content"]/div/p')
        inner_text = self.format_innertext(raw_text)
        # Format accents and special characters
        formatted_text = unidecode.unidecode(inner_text[0] if inner_text else "")
        post['content'] = formatted_text

        # Add link
        post['link'] = response.url

        yield post

    def map_months(self, month):
        # map the inputs to the function blocks
        months_mapping = {
        'Gennaio': '1',
        'Febbraio': '2',
        'Marzo': '3',
        'Aprile': '4',
        'Maggio': '5',
        'Gunio': '6',
        'Luglio': '7',
        'Agosto': '8',
        'Settembre': '9',
        'Ottobre': '10',
        'Novembre': '11',
        'Dicembre': '12',
        '': ''
        }

        return months_mapping[month]

    def format_date(self, raw_date):
        month = self.map_months(raw_date.split(' ')[1])
        formatted_date = raw_date.split(' ')[0] + "/" + month + "/" + raw_date.split(' ')[2]
        return formatted_date

    def format_innertext(self, elements, delimiter=" "):
        return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)
