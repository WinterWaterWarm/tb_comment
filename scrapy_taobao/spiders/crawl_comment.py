import re
import json
import time
import logging
import scrapy
import requests
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy_taobao.items import taobao_comment_item
from selenium.webdriver.chrome.options import Options


class commment_spider(scrapy.Spider):

    name = 'comment'

    # 初始化中配置chromedriver
    def __init__(self,parms=None):

        self.search_key = parms     #控制台传入淘宝搜索关键字

        print('Chromedriver is starting')
        chrome_options = Options()
        chrome_options.add_argument('--headless')       #无头
        chrome_options.add_argument('disable-infobars') #关闭检测
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 1  0.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"',
        )
        chrome_options.add_argument('charset="utf-8"')  #编码格式
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    # 搜索商品页面为第一个页面
    def start_requests(self):
        urls = [
            'https://s.taobao.com/search?q=%s&sort=sale-desc'%self.search_key,
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #def closed(self,reason):
        #self.driver.quit()

    # 抓取各商品页面链接的parser
    def parse(self,response):
        self.driver.get(response.url)       #使用chromedriver抓取动态页面
        count = 0
        time.sleep(5)
        bsObj = BeautifulSoup(self.driver.page_source,'lxml')
        item_div = bsObj.find('div',{'class':'grid g-clearfix'})
        items = item_div.find_all('div',{'class':'ctx-box J_MouseEneterLeave J_IconMoreNew'})
        for item in items:
            count+=1
            url = item.find('div', {'class': 'row row-2 title'}).find('a').attrs['href'] #商品链接
            if 'https:' not in url:
                url = 'https:'+url
            name = item.find('div', {'class': 'row row-2 title'}).find('a').get_text().strip()      #商品名称
            sales = item.find('div', {'class': 'row row-1 g-clearfix'}).find('div', {'class': 'deal-cnt'}).get_text()   #商品销量
            #print('调用第%d个商品页面链接：%s'%(count,url))
            yield scrapy.Request(url=url,callback=self.parse_item,dont_filter=True,meta={'name':name,'sales':sales,'count':count})     #把商品页面链接回调

    #从商品页面中抓取有用信息的parser
    def parse_item(self,response):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        item = taobao_comment_item()
        item['name'] = response.meta['name']
        item['sales'] = response.meta['sales']
        item['count'] = response.meta['count']
        #print('开始处理第%d个商品'%item['count'])
        try:
            itemId = re.findall("itemId=(\d*)",response.text)[0]
            sellerId = re.findall("sellerId=(\d*)",response.text)[0]
        except:
            print('error in',response.url)
            return -1
        item['itemId'] = itemId
        item['url'] = response.url

        for current_page in range(1,10):
            url = 'https://rate.tmall.com/list_detail_rate.htm?current_page=%d&itemId=%s&sellerId=%s'%(current_page,itemId,sellerId)
            yield scrapy.Request(url=url,callback=self.parse_json,dont_filter=True,
                                 meta={'item':item})



    def parse_json(self,response):
        item = response.meta['item']
        comment = {}
        try:
            json_text = re.findall('\"rateList\":(\[.*?\]),\"searchinfo\":', response.text)[0]
            comment_list = json.loads(json_text)  # 解析json
        except:
            print('json error in ',response.url)
            return -1

        if comment_list != []:
        # 数据传入item中
            for comment_dict in comment_list:
                comment['auctionSku'] = comment_dict['auctionSku']
                comment['rateContent'] = comment_dict['rateContent']
                comment['rateDate'] = comment_dict['rateDate']
                comment['appendComment'] = comment_dict['appendComment']
                item['comment'] = comment
                yield item

        else:
            print('该商品评论太少:%s'%item['url'])



