import scrapy
import re

from movies_data.items import Movie


class ImdbSpider(scrapy.Spider):
    name = "Imdb_spider"

    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):
        for href in response.xpath('//td[@class="titleColumn"]//a/@href').extract():
            yield scrapy.Request(f"https://www.imdb.com{href}", callback=self.parse_movie)

    def parse_movie(self, response):
        title = self._get_title(response)
        director = response.xpath('//span[contains(text(), "Director")]/following-sibling::div//a/text()').get()
        rating = float(response.xpath('//div[contains(text(), "IMDb RATING")]/following-sibling::a//span/text()').get())
        year = int(response.xpath('//a[contains(text(), "Release date")]/following-sibling::div//text()').re_first("\d{4}"))
        stars = response.xpath('//a[contains(text(), "Stars")]/following-sibling::div//li//a/text()').getall()

        yield Movie(title=title, director=director, imdb_rating=rating, year=year, stars=stars)

    @staticmethod
    def _get_title(response):
        original_title_text = response.xpath('//div[contains(text(), "Original title")]/text()').get()
        if original_title_text:
            return re.search("Original title: (.*)", original_title_text).group(1)
        return response.xpath('//h1[contains(@class, "TitleHeader")]/text()').get()