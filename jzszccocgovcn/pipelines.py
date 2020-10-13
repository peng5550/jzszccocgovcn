# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class JzszccocgovcnPipeline(object):


    def __init__(self, settings):
        self.host = settings.get("HOST")
        self.port = settings.get("PORT")
        self.usr = settings.get("USER")
        self.passwd = settings.get("PASSWD")
        self.database = settings.get("DB")
        self.table = settings.get("TABLE")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.usr, passwd=self.passwd, db=self.database,
                                    charset="utf8")
        self.db = self.conn.cursor()

    def close_spider(self, spider):
        self.db.close()
        self.conn.close()

    def insert_data(self, table_name, item_info):
        keys = ', '.join(list(item_info.keys()))
        values = ', '.join(['%s'] * len(item_info))
        insert_sql = "insert into `{}`({})values({});".format(table_name, keys, values)
        try:
            self.db.execute(insert_sql, tuple(item_info.values()))
            self.conn.commit()
        except Exception as e:
            print(e.args)
            self.conn.rollback()

    def select_data(self, table_name, item_info):
        string_list = []
        for i in item_info.keys():
            string = '%s="%s"' % (i, item_info.get(i))
            string_list.append(string)
        sql_string = ' and '.join(string_list)

        select_sql = "select * from {} where {};".format(table_name, sql_string)

        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return True
        else:
            return False

    def process_item(self, item, spider):
        item_info = {"idNo": item["data"]["idNo"]}
        if not self.select_data(table_name=self.table, item_info=item_info):
            self.insert_data(table_name=self.table, item_info=item["data"])
        return item


class DownloadImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        imageList = [(link, f"{item['data']['name'] + item['data']['idNo'][-8:]}-{index}.jpg") for index, link in
                     enumerate([item['data']["headImage"], item['data']["signImage"]] + item['data']["idCardImage"].split(", "))]
        # 下载图片
        for link, path in imageList:
            if not os.path.exists(path):
                yield scrapy.Request(link, meta={"path": path})
            else:
                print("已存在.")

    def file_path(self, request, response=None, info=None):

        return request.meta["path"]
