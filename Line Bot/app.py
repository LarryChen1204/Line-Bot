from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests 
from bs4 import BeautifulSoup
import psycopg2
import datetime
from PIL import Image

app = Flask(__name__)

line_bot_api = LineBotApi('7VXREbXnJmngav6NMsnXiMEjBVA08f6HgH96JxCe+z4OVc51qK5mOAye3IB45Kx8yKyOpKUEAq3QPJTSkpzysm2tIZS77gKaYp7kNuPT2wMjfcg4RFhepsb2wZN94iXADWivITXH1kDILIoIjyUzwQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fecd2c905ee7f9491e00d11b702a995b')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #爬文最新電影
    def movie():
        target_url = 'https://movies.yahoo.com.tw/'
        rs = requests.session()
        res = rs.get(target_url, verify = False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')   
        h_text, h_href, h_pic= [], [], []
        
        for pic, data in zip(soup.select('div.movie_foto img'), soup.select('div.movielist_info h2 a')):
            h_text.append(data.text)
            h_href.append(data['href'])
            h_pic.append(pic['src'])
            
        return h_text, h_href, h_pic
    
    #爬文星座
    def horoscope1(h_name):
        content = ""
        
        hostname = 'ec2-54-157-78-113.compute-1.amazonaws.com'
        username = 'asoewrnhfxmhxb'
        password = 'e2dd638c5540c9f413d73cf8d1eef8240841c845c5ae1b955b07fc2bd0c55049'
        database = 'dbp958hjtdc6t9'
        
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = conn.cursor()
        
        sql = 'select name, date, whole_star, whole_desc, love_star, love_desc, work_star, work_desc, money_star, money_desc from constellations where name = %s and date = %s'
        cur.execute(sql, (h_name,datetime.date.today().strftime('%Y-%m-%d'),))
        c = cur.fetchall()
        
        for row in c:
            content = row
        conn.close()

        return content
    
    if event.message.text == '電影':
        m_title, m_uri, m_pic = movie()

        data = []
        data2 = []
        
        data_len = max(len(m_title), len(m_uri), len(m_pic))
        
        for i in range(data_len):
            if i <= 9:
                data.append(CarouselColumn(thumbnail_image_url = m_pic[i], title = m_title[i], text = '電影介紹', actions = [URITemplateAction(label = '前往', uri = m_uri[i])]))
            elif i >= 10 and i < 20:
                data2.append(CarouselColumn(thumbnail_image_url = m_pic[i], title = m_title[i], text = '電影介紹', actions = [URITemplateAction(label = '前往', uri = m_uri[i])]))
        
        message = [TemplateSendMessage(
            alt_text = '最新電影',
            template = CarouselTemplate(
                columns = data
            )
        ),
        TemplateSendMessage(
            alt_text = '最新電影',
            template = CarouselTemplate(
                columns = data2
            )
        )
        ]
    elif event.message.text.lower().find("susan") > -1:
        message = [StickerSendMessage(package_id='1', sticker_id='410'), StickerSendMessage(package_id='1', sticker_id='117')]
        
    elif event.message.text.find("座") > -1:
        c = horoscope1(event.message.text)
        if c :
            message = [TextSendMessage(text = '{}, {}'.format(c[0], c[1])), TextSendMessage(text = '{}\n{}\n'.format(c[2], c[3])), TextSendMessage(text = '{}\n{}\n'.format(c[4], c[5])), TextSendMessage(text = '{}\n{}\n'.format(c[6], c[7])), TextSendMessage(text = '{}\n{}\n'.format(c[8], c[9]))]
        elif event.message.text == '博愛座':
            message = ImageSendMessage(
            original_content_url='https://image.cache.storm.mg/styles/smg-800x533-fp/s3/media/image/2016/04/21/20160421-051022_U5966_M149662_4cfc.jpg',
            preview_image_url='https://image.cache.storm.mg/styles/smg-800x533-fp/s3/media/image/2016/04/21/20160421-051022_U5966_M149662_4cfc.jpg'
            )
    
    elif event.message.text.upper().find("弱G") > -1:
        message = [StickerSendMessage(package_id='1', sticker_id='3'), StickerSendMessage(package_id='1', sticker_id='17')]
    
    elif event.message.text.lower().find("help") > -1:
        str = '### 功能介紹 ###\n' + '1. 輸入"電影": 查看目前最新電影\n' + '2. 輸入星座: 查看當日運勢(Ex: 射手座)\n' + '###功能持續新增中###'
        message = [TextSendMessage(text = str)]
        
    else:
        message = ''
    
    if message != '':
        line_bot_api.reply_message(event.reply_token, message)

import os

if __name__ == "__main__":
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
