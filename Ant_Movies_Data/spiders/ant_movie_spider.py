import scrapy
import time
import random
import requests

class AntMoviesSpider(scrapy.Spider):
    name = 'ant_movies_data_spider'
    start_urls = [
        'http://theater.mtime.com/China_Beijing/'
    ]

    def parse(self,response):
        #获取正在热映电影的url
        movie_show_url_list = []
        movie_show_dev_xpaths = response.xpath('//div[@id="hotplayContent"]/div')
        movie_show_first_url = movie_show_dev_xpaths.xpath('./div[@class="moviebox clearfix"]/div[@class="firstmovie fl"]/dl/dt/a/@href').extract()[0]

        #yield scrapy.Request(movie_show_first_url, callback=self.parse_movie_detail_info)
        #print(movie_show_first_url)
        movie_show_url_list.append(movie_show_first_url)
        movie_show_others_list_xpath = movie_show_dev_xpaths.xpath('./div[@class="moviebox clearfix"]/div[@class="othermovie fr"]/ul[@class="clearfix"]')

        for movie_show_other_ul_xpath in movie_show_others_list_xpath:
            #print(len(movie_show_other_ul_xpath.xpath('./li[@class="clearfix"]').extract()))
            for movie_show_other_li_xpath in movie_show_other_ul_xpath.xpath('./li[@class="clearfix"]'):
                movie_show_other_url =  movie_show_other_li_xpath.xpath('./a/@href').extract()[0]
                #print(movie_show_other_url)
                movie_show_url_list.append(movie_show_other_url)

        #print(movie_show_other_url)
        movie_show_more_list_xpath =  movie_show_dev_xpaths.xpath('./div[@id="hotplayMoreDiv"]/div[@class="othermovie"]/ul[@class="clearfix"]')
        #i = 0    #debug
        for movie_show_other_ul_xpath in movie_show_more_list_xpath:
            #print(len(movie_show_other_ul_xpath.xpath('./li[@class="clearfix"]').extract()))
            for movie_show_other_li_xpath in movie_show_other_ul_xpath.xpath('./li[@class="clearfix"]'):
                movie_show_other_url =  movie_show_other_li_xpath.xpath('./a/@href').extract()[0]
                #print(movie_show_other_url)
                movie_show_url_list.append(movie_show_other_url)

        for movie_show_url in movie_show_url_list:
            #print(movie_show_url)
            #此处可以直接yield 到电影详情页面去获取其他信息
            yield scrapy.Request(movie_show_url, callback=self.parse_movie_detail_info)

        #获取即将上映电影的url

        movie_will_show_id_dicts = response.xpath('//div[@id="upcomingRegion"]/@mids').extract()[0]

        for movie_will_show_id in movie_will_show_id_dicts.split(","):
            movie_will_show_url = "http://movie.mtime.com/" + movie_will_show_id
            #print(movie_will_show_url)
            #此处可以直接yield 到电影详情页面去获取其他信息
            #yield scrapy.Request(movie_will_show_url, callback=self.parse_movie_detail_info)

    def parse_movie_detail_info(self,response):
        movie_detail_info_dev_xpath = response.xpath('//div[@class="db_topcont"]')
        movie_detail_info_head_xpath = movie_detail_info_dev_xpath.xpath('./div[@id="db_head"]')
        
        #电影海报url
        movie_info_image_url = movie_detail_info_head_xpath.xpath('./div[@class="db_coverout"]/div[@class="db_coverinner"]/div[@class="db_coverpicbox"]/div[@class="db_cover __r_c_"]/a/img/@src').extract()[0]
        
        #电影标题
        movie_info_title_text = movie_detail_info_head_xpath.xpath('./div[@class="db_ihead"]/div[@class="db_head"]/div[@class="clearfix"]/h1/text()').extract()[0]

        movie_detail_info_head_other_xpath = movie_detail_info_head_xpath.xpath('./div[@class="db_ihead"]/div[@class="db_head"]/div[@class="otherbox __r_c_"]')

        #电影时长
        movie_info_time_length_text = '0分钟'
        movie_info_time_length_text_xpath = movie_detail_info_head_other_xpath.xpath('./span/text()')
        if(len(movie_info_time_length_text_xpath.extract())>0):
            movie_info_time_length_text = movie_info_time_length_text_xpath.extract()[0]
        
        #电影类型
        movie_info_type_texts = ''

        for movie_detail_info_head_type_xpath in movie_detail_info_head_other_xpath.xpath('./a[@property="v:genre"]'):
            if(len(movie_detail_info_head_type_xpath.xpath('./text()').extract())>0):
                movie_info_type_text = movie_detail_info_head_type_xpath.xpath('./text()').extract()[0]
                if(movie_info_type_texts == ''):
                    movie_info_type_texts = movie_info_type_text
                else:
                    movie_info_type_texts = movie_info_type_texts + '/' + movie_info_type_text

        #电影上映时间
        movie_info_release_date_text = '0000-00-00'
        movie_info_release_date_text_xpath = movie_detail_info_head_other_xpath.xpath('./a[@property="v:initialReleaseDate"]/@content')
        if(len(movie_info_release_date_text_xpath.extract())>0):
            movie_info_release_date_text = movie_info_release_date_text_xpath.extract()[0]

        #电影视觉类型(2D/3D/IMAX)
        movie_info_version_text = '2D'
        #movie_version_types = ['2D','3D','IMAX']
        if(len(movie_detail_info_head_other_xpath.xpath('./text()'))>0):
            movie_info_version_text_xpath = movie_detail_info_head_other_xpath.xpath('./text()[' + str(len(movie_detail_info_head_other_xpath.xpath('./text()'))) + ']')
            if(len(movie_info_version_text_xpath.extract())>0):
                #for movie_version_type in movie_version_types:
                movie_info_version_text_tmp = movie_info_version_text_xpath.extract()[0]
                if('D' in movie_info_version_text_tmp ):
                    if('-' in movie_info_version_text_tmp):
                        movie_info_version_text = movie_info_version_text_tmp.split('-')[1].strip()
                    else:
                        movie_info_version_text = movie_info_version_text_tmp

        #print(movie_info_version_text)
                
        #debug print
        #print(movie_info_image_url,movie_info_title_text)
        print(movie_info_image_url,movie_info_title_text,movie_info_time_length_text,movie_info_type_texts,movie_info_release_date_text,movie_info_version_text)