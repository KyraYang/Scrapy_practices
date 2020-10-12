# -*- coding: utf-8 -*-
import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        glasses_rows = response.xpath('//div[@id="product-lists"]/div')
        for glasses in glasses_rows:
            name = glasses.xpath(
                './/descendant::div[@class="p-title"]/a/text()').get()
            if not name:
                continue
            yield{
                "product url": glasses.xpath('.//div[@class="product-img-outer"]/a/@href').get(),
                "product image": glasses.xpath('.//div[@class="product-img-outer"]/a/img[1]/@src').get(),
                "product name": name.strip(),
                "product price": glasses.xpath('.//descendant::div[@class="p-price"]/div/span[1]/text()').get(),
            }
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
