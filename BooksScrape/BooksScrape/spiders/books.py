# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="http://books.toscrape.com",
            headers={"User-Agent": self.user_agent},
        )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//article"),
            callback="parse_item",
            follow=True,
            process_request="set_user_agent",
        ),
        Rule(
            LinkExtractor(restrict_xpaths="//li[@class='next']/a"),
            process_request="set_user_agent",
        ),
    )

    def set_user_agent(self, request):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath("//h1/text()").get(),
            "price": response.xpath("//p[@class='price_color']/text()").get(),
        }
