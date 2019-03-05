# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class AntMoviesDataPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost",user='root',password='root',database='python_test')
        self.cursor = self.conn.cursor()

        #清理数据库
        sql = 'DELETE FROM ant_movie_info;'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print('sql except')
            self.conn.rollback()

    def process_item(self, item, spider):
        #电影标题
        movie_name = item.get('movie_name')
        #电影评分
        movie_rate = item.get('movie_rate')
        #电影logo
        movie_image_name = item.get('movie_image_name')
        #导演
        movie_director = item.get('movie_director')
        #主演
        movie_actors = item.get('movie_actors')
        #类型
        movie_type = item.get('movie_type')
        #制片国家/地区
        movie_country = item.get('movie_country')
        #语言
        movie_language = item.get('movie_language')
        #片长
        movie_length = item.get('movie_length')
        #剧情介绍
        movie_description = item.get('movie_description')
        #上映时间
        movie_show_time = item.get('movie_show_time')
        #version
        movie_version = item.get('movie_version')
        #price
        movie_price = 50.0
        #movie_stage_photos
        movie_stage_photos = item.get('movie_stage_photos')
        insert_sql = '''
                insert into ant_movie_info 
                (m_name, m_type, m_director, m_actor, m_country, m_version, 
                m_time_length, m_description, m_release_time, m_price, m_rate, 
                m_picture,m_stage_photos) 
                values 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            '''
        #重新插入数据
        try:
            self.cursor.execute(insert_sql,(movie_name,movie_type,movie_director,movie_actors,movie_country,movie_version,movie_length,movie_description,movie_show_time,movie_price,movie_rate,movie_image_name,movie_stage_photos))
            self.conn.commit()
        except Exception as e:
            print('except:',e)
            self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

    def clear_database(self):
        sql = 'DELETE FROM ant_movie_info;'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

