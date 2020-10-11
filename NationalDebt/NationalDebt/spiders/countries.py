# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = [
        'https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//tbody/tr")
        for country in countries:
            name = country.xpath(".//td/a/text()").get()
            debt = country.xpath(".//td[2]/text()").get()
            yield {
                "country_name": name,
                "gdb_debt": debt
            }
