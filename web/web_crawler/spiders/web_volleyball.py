from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import BlogPostItem

import unidecode


class WebCrawlerVolleyball(Spider):
    name = "volleyball"

    allowed_domains = ["volleyball.it"]
    start_urls = [
        "https://volleyball.it/nc/istituzionale/archivio.html",
    ]

    def parse(self, response):
        # Fill the html form to get the posts from Sept 2021 up until now
        formdata = {'tx_ttnews[start_full]': '2021-09-01', 'tx_ttnews[end_full]': '2024-04-24' }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'search'},
                                        callback=self.parse_article_list)



    def parse_article_list(self, response):
        # Logic of how to extract the HTML
        news_list = Selector(response).xpath('//*[@class="news-searchlist-item"]/h2/a')

        next_pages = Selector(response).xpath('//*[@class="browseLinksWrap"]/a')

        next_page_link = None
        for next_page in next_pages:
            # Find the next page
            if(next_page.xpath('text()').extract()[0] == '>'):
                next_page_link = next_page.xpath('@href').extract()[0]

        for news_item in news_list:
            # Trigger recursively the parsing of posts
            news_link = news_item.xpath('@href').extract()[0]
            yield Request(news_link, callback=self.parse_article)

        # Recursively go to the next page
        if next_page_link:
            yield Request(next_page_link, callback=self.parse_article_list)

    def parse_article(self, response):
        post = BlogPostItem()

        # Format title
        post['title'] = unidecode.unidecode(response.xpath('//*[@class="title"]/text()').extract()[0])

        # Format date
        raw_date = response.xpath('//*[@class="news-list-date-header"]/text()').extract()[0]
        post['date'] = self.format_date(raw_date)

        # Format text
        raw_text = response.xpath('//*[@class="news-single-content"]/p')
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
        'gennaio': '1',
        'febbraio': '2',
        'marzo': '3',
        'aprile': '4',
        'maggio': '5',
        'gunio': '6',
        'luglio': '7',
        'agosto': '8',
        'settembre': '9',
        'ottobre': '10',
        'novembre': '11',
        'dicembre': '12',
        '': ''
        }

        return months_mapping[month]

    def format_date(self, raw_date):
        month = self.map_months(raw_date.split(' ')[1])
        formatted_date = raw_date.split(' ')[0] + "/" + month + "/" + raw_date.split(' ')[2] + ' ' + raw_date.split(' ')[3]
        return formatted_date

    def format_innertext(self, elements, delimiter=" "):
        return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)
