# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BusinessItem(scrapy.Item):
    name = scrapy.Field()
    yelp_url = scrapy.Field()
    website_url = scrapy.Field()
    rating = scrapy.Field()
    reviews_number = scrapy.Field()
    reviews = scrapy.Field()
