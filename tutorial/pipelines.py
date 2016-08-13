# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from datetime import datetime
class TutorialPipeline(object):
    connection = pymysql.connect(host='pyhelldb.cuiejbtb7cxp.ap-northeast-1.rds.amazonaws.com',
                                 user='arnold',
                                 password='nuttertools0824',
                                 charset='utf8',
                                 db='pymovie',
                                 cursorclass=pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        #item['html']=item['type']+item['title']

        tags={'动作':'1','喜剧':'2','爱情':'3','战争':'4','科幻':'5','恐怖':'6','剧情':'7','历史':'8','武侠':'9','惊悚':'10','悬疑':'11','犯罪':'12','灾难':'13','歌舞':'14','微电影':'15'}
        #item={'tags': '剧情片,战争,惊悚,动作'}
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `core_film` (`film_name`, `download_link`,`film_intro`,`dim_date`,`cover_img_link`,`film_director`,`film_actors`,`film_pub_year`,`film_country`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (str(item['title']),str(item['downloadlink']),str(item['intro']),str(item['datetime']),str(item['coverlink']),str(item['director']),str(item['actors']),str(item['year']),str(item['country'])))
                self.connection.commit()
                for tag in item['tags'].split(','):
                    cursor.execute("insert into `core_film_tags` (`film_id`,`tag_film_id`) VALUES ((select id from core_film where film_name=%s limit 1),%s)",(str(item['title']),str(tags[tag[:2]])))
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
