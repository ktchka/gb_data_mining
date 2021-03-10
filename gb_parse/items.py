# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GbAutoYoulaItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    characteristics = scrapy.Field()
    descriptions = scrapy.Field()
    author = scrapy.Field()


class HHItem(scrapy.Item):
    utl = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()
