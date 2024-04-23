from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import WebCrawlerItem


class WebCrawlerGazzetta(Spider):
    name = "web_crawler_gazzetta"

    allowed_domains = ["dal15al25.gazzetta.it"]
    start_urls = [
        "https://dal15al25.gazzetta.it/",
    ]

    def parse(self, response):
        # Logic of how to extract the HTML
        article_list = Selector(response).xpath('//*[@class="articles-list"]/article/div/div/p/a')
        print(article_list)

        next_page = Selector(response).xpath('//*[@class="next-posts"]/a/@href').extract()

        next_page_link = next_page[0] if next_page else None

        for article in article_list:
            # Trigger recursively the parsing of articles
            article_link = article.xpath('@href').extract()[0]
            yield Request(article_link, callback=self.parse_articles)

        # Recursively go to the next page
        if next_page_link:
            #yield Request(next_page_link, callback=self.parse)
            pass



    def parse_articles(self, response):
        item = WebCrawlerItem()
        item['title'] = response.xpath('//*[@class="article-title"]/h1/text()').extract()[0]
        item['content'] = ' '.join(response.xpath('//*[@class="article-content"]/p/text()').extract())
        item['link'] = response.url
        item['comments'] = []

        comments = response.xpath('//*[@class="commentlist"]/li')
        for comment in comments:
            comment_obj = {
                'user': comment.xpath('.//*[@class="comment_author"]/text()').extract()[0],
                'created_at_utc': comment.xpath('.//*[@class="comment_time"]/text()').extract()[0],
                'text': " ".join(comment.xpath('.//*[@class="comment_text"]/p/text()').extract()),
            }
            item['comments'].append(comment_obj)


        yield item
