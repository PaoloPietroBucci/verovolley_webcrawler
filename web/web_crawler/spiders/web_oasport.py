from scrapy import Spider, Request

from ..items  import BlogPostItem

import unidecode


class OASportSpider(Spider):
    name = 'oasport'
    allowed_domains = ['oasport.it']
    start_urls = ['https://www.oasport.it/category/squadre/pallavolo/']

    def parse(self, response):
        pages_article = response.xpath('//li[contains(@class, "mvp-blog-story-wrap")]/a/@href').getall()

        for article in pages_article:
            # Trigger recursively the parsing of posts
            link = response.urljoin(article)
            yield Request(url=link, callback=self.parse_article)

        # Recursively go to the next page
        next_page = response.xpath('//div[contains(@class, "pagination")]/a/@href').getall()
        yield Request(url=next_page[-2], callback=self.parse)

    def parse_article(self, response):
        post = BlogPostItem()

        # Format title
        article_title = response.xpath('//h1/text()').get()
        post['title'] = unidecode.unidecode(article_title)

        # Format date
        date = response.xpath('//*[@class="post-date updated"]/@datetime').extract()[0]
        post['date'] = date

        # Format text
        article_paragrafs = response.xpath('//div[@id="mvp-content-main"]/p//text()').getall()
        unique_text = ' '.join(article_paragrafs)
        post['content'] = unidecode.unidecode(unique_text)

        # Add Link
        post['link'] = response.url

        yield post

#  scrapy crawl oasport -o output.json
