import json

import scrapy

from movies_data.items import Movie


class RTSpider(scrapy.Spider):
    name = "rotten_tomatoes_spider"

    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/']

    def parse(self, response):
        for href in response.xpath('//td/a[contains(@class,"articleLink")]/@href').extract():
            yield scrapy.Request(f"https://www.rottentomatoes.com{href}", callback=self.parse_movie)

    def parse_movie(self, response):
        content = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
        title = content['name']
        director = response.xpath('//div[contains(text(), "Director")]/following-sibling::div//a/text()').get()
        rating = int(content['aggregateRating']['ratingValue'])
        year = int(response.xpath('//div[contains(text(), "Release Date")]/following-sibling::div//text()').re_first("\d{4}"))
        stars = [a.strip() for a in response.xpath('//div[contains(@class, "castSection")]//a/span/text()').getall()]

        yield Movie(title=title, director=director, rotten_tomatoes_rating=rating, year=year, stars=stars)