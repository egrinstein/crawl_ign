import scrapy
class IGNItem(scrapy.Item):
    title = scrapy.Field()
    genre = scrapy.Field()
    platform = scrapy.Field()
    publication_date = scrapy.Field()
    rating = scrapy.Field()
    rating_phrase = scrapy.Field()
    editors_choice = scrapy.Field()
    url = scrapy.Field()
