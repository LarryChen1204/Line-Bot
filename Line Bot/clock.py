from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time
import sys
import os

from scrapy.crawler import CrawlerProcess
from Constellations.Constellations.spiders import crawler
from scrapy.settings import Settings
import my_settings as my_settings

from crochet import setup
setup()

sched = BlockingScheduler()

spider = crawler.ConstellationsCrawler
crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)

@sched.scheduled_job('interval', minutes=10)
def timed_job_awake_your_app():
    print('awake app every 10 minutes.')
    url = 'https://your_app.herokuapp.com/'
    r = requests.get(url)
    print("--> r.content")
    print(r.content)

def my_job():
    print('hello world')
    process.crawl(spider)
 
sched = BlockingScheduler()
#sched.add_job(my_job, 'interval', seconds=60)
#sched.add_job(my_job, 'interval', hours=24, start_date='2020-04-11 16:01:00', end_date='2021-04-11 16:01:01')
sched.add_job(my_job, 'interval', hours=24, start_date='2020-04-12 00:29:00', end_date='2021-04-11 16:01:01')
sched.start()