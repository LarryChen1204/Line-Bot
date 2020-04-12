# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import sqlite3
import os
import psycopg2

class ConstellationsPipeline(object):
    
    def open_spider(self, spider):
        
        hostname = 'ec2-54-157-78-113.compute-1.amazonaws.com'
        username = 'asoewrnhfxmhxb'
        password = 'e2dd638c5540c9f413d73cf8d1eef8240841c845c5ae1b955b07fc2bd0c55049' # your password
        database = 'dbp958hjtdc6t9'
        
        
        #self.conn = sqlite3.connect('constellations.sqlite', check_same_thread = False)
        #Database_URL = os.popen('heroku config:get DATABASE_URL -a larrychen1204').read()[:-1]
        self.conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        #self.cur = self.connection.cursor()
        #self.conn = psycopg2.connect(Database_URL, sslmode = 'require')
        self.cur = self.conn.cursor()
        self.cur.execute('''create table if not exists
                            constellations(name        varchar(20),
                                           date        varchar(20),
                                           whole_star  text,
                                           whole_desc  text,
                                           love_star   text,
                                           love_desc   text,
                                           work_star   text,
                                           work_desc   text,
                                           money_star  text,
                                           money_desc  text,
                                           unique(name, date))
                         ''')
    
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
    
    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * '?')
        sql = 'insert into constellations({}) values({}) on conflict(name, date) do nothing'
        #sql1 = 'insert into constellations(%s) values(%s)'
        #self.cur.execute(sql.format(col, placeholders), tuple(item.values()))
        #self.cur.execute(sql.format(col, tuple(item.values())))
        
        self.cur.execute('insert into constellations values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on conflict(name, date) do nothing', tuple(item.values()))
        
        return item

