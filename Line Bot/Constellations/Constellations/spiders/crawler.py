import scrapy
import js2xml
from bs4 import BeautifulSoup
from lxml import etree
from Constellations.Constellations.items import ConstellationsItem
#from Constellations.items import ConstellationsItem

class ConstellationsCrawler(scrapy.Spider):
    name = 'constellations'
    allowed_domains = ['astro.click108.com.tw', 'refer.click108.com.tw']
    start_urls = ['http://astro.click108.com.tw/']
    
    def parse(self, response):
        res = BeautifulSoup(response.body, 'lxml')
        for news in res.select('div .STAR12_BOX li'):            
            yield scrapy.Request(news.select('a')[0]['href'], callback = self.parse_detail, dont_filter = True)
    
    def parse_detail(self, response):
        res = BeautifulSoup(response.body, 'lxml')
        scripts = res.find_all('script')
        for script in scripts:
            src_text = js2xml.parse(script.string, encoding='utf-8',debug=False)
            src_tree = js2xml.pretty_print(src_text)
            selector = etree.HTML(src_tree)
            
        yield scrapy.Request(selector.xpath("//right/string/text()")[0] + '/', callback = self.parse_detail2, dont_filter = True)
        
    
    def parse_detail2(self, response):
        res = BeautifulSoup(response.body_as_unicode(), 'lxml')
        constellationsItem = ConstellationsItem()
        
        for horoscope in res.select('div .HOROSCOPE_BTN'):
            constellationsItem['name'] = horoscope.select('h3')[0].text
        
        constellationsItem['date'] = response.selector.xpath('//select[@id="iAcDay"]/option[@selected="selected"]/text()').extract()[0]
            
        for content in res.select('div .TODAY_CONTENT'):
            constellationsItem['whole_star'] = content.select('p')[0].text
            constellationsItem['whole_desc'] = content.select('p')[1].text
            constellationsItem['love_star'] = content.select('p')[2].text
            constellationsItem['love_desc'] = content.select('p')[3].text
            constellationsItem['work_star'] = content.select('p')[4].text
            constellationsItem['work_desc'] = content.select('p')[5].text
            constellationsItem['money_star'] = content.select('p')[6].text
            constellationsItem['money_desc'] = content.select('p')[7].text
            
            return constellationsItem
        
        