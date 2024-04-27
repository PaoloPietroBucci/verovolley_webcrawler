from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import BlogPostItem


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
        item = BlogPostItem()
        item['title'] = response.xpath('//*[@class="title"]/text()').extract()[0]
        item['date'] = response.xpath('//*[@class="news-list-date-header"]/text()').extract()[0]
        item['content'] = ' '.join(response.xpath('//*[@class="news-single-content"]/p/text()').extract())
        item['link'] = response.url
        item['comments'] = []

        yield item
