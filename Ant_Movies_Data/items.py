# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AntMoviesDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #电影标题
    movie_name = scrapy.Field()
    #电影评分
    movie_rate = scrapy.Field()
    #电影logo
    movie_img_url = scrapy.Field()
    #导演
    movie_director = scrapy.Field()
    #主演
    movie_actors = scrapy.Field()
    #类型
    movie_type = scrapy.Field()
    #制片国家/地区
    movie_country = scrapy.Field()
    #语言
    movie_language = scrapy.Field()
    #片长
    movie_length = scrapy.Field()
    #剧情介绍
    movie_description = scrapy.Field()
    #上映时间
    movie_show_time = scrapy.Field()
    #剧照
    movie_stage_photos = scrapy.Field()
    #版本3D 、 2D
    movie_version = scrapy.Field()
    #movie logo name
    movie_image_name = scrapy.Field()
