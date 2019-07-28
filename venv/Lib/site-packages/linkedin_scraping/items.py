# -*- coding: utf-8 -*-
import scrapy


class User(scrapy.Item):
    first_name = scrapy.Field(serializer=str)
    last_name = scrapy.Field(serializer=str)
    position = scrapy.Field(serializer=str)
    company = scrapy.Field(serializer=str)
    city = scrapy.Field(serializer=str)
    country = scrapy.Field(serializer=str)
