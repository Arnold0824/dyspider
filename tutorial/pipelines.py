# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from datetime import datetime
class TutorialPipeline(object):
    connection = pymysql.connect(host='101.200.156.230',
                                 user='root',
                                 password='DSxrjk230s',
                                 charset='utf8',
                                 db='pymovie',
                                 cursorclass=pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        #item['html']=item['type']+item['title']



        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `core_film` (`film_name`, `download_link`,`film_html`,`dim_date`,`cover_img_link`) VALUES (%s, %s,%s,%s,%s)"
                cursor.execute(sql, (str(item['title']),str(item['downloadlink']),str(item['intro']),str(item['datetime']),str(item['coverlink'])))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

            # with self.connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT * FROM `core_film`"
            #     cursor.execute(sql)
            #     result = cursor.fetchall()
            #     print(result)
        finally:
            pass
            # self.connection.close()
        return item
