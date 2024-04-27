from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from web_crawler.items import BlogPostItem


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
        item = BlogPostItem()
        ss = response.xpath('//*[@class="elementor-element elementor-element-34954c7b elementor-widget elementor-widget-theme-post-title elementor-page-title elementor-widget-heading"]')
        item['title'] = response.xpath('//*[@class="elementor-element elementor-element-34954c7b elementor-widget elementor-widget-theme-post-title elementor-page-title elementor-widget-heading"]/div/h1/text()').extract()[0]
        item['content'] = ' '.join(response.xpath('//*[@class="elementor-element elementor-element-3104ed9c elementor-drop-cap-view-stacked elementor-drop-cap-yes elementor-widget-text-editor elementor-widget elementor-widget-my-custom-post-content"]/div/p/text()').extract())
        item['link'] = response.url
        yield item
