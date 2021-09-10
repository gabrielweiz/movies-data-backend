import scrapy


class Movie(scrapy.Item):
    title = scrapy.Field()
    director = scrapy.Field()
    imdb_rating = scrapy.Field()
    rotten_tomatoes_critics_rating = scrapy.Field()
    rotten_tomatoes_audience_rating = scrapy.Field()
    year = scrapy.Field()
    stars = scrapy.Field()
