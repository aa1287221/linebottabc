# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium import webdriver
import serial    #import serial module
import time
import datetime
import schedule
import numpy as np
import multiprocessing as mp
import re

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('kiCs2B8D8LSZZ32aJ+5nXT/V1r9gRXKMbBS7l9RsTfuhMbWVmbiRvhlwzOj8uYzciNw/OTGz5+mz9xKEHAIyhWSn9ylEXAM/6ow/Osep8NT+NgoovpBxk/0T/bgLfc/VgqxiM/aNbTqczQXA7VRfuQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('62df28a9d6ba49c16352e84f51e97120')

def classs():
    url="http://training.tabc.org.tw/files/901-1000-6,c0-1.php"
    browser = webdriver.Chrome()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    tabc = soup.find_all('a',class_='otabc_link')
    tabcc = soup.find_all('font')
    content = ''
    title = []
    link = []
    status = []
    for t in tabc:
        title.append(t.get_text())
        link.append(t.get('href'))
    for tt in tabcc:
        status.append(tt.get_text())
    for i in range(0,9):
        content+='標題：{}\n\n網址：{}\n\n報名狀態：{}\n\n'.format(title[i],link[i],status[i])
    browser.quit()
    return content

def news():
    url="http://www.tabc.org.tw/tw/modules/news/index.php?storytopic=0&storynum=10" 
    browser = webdriver.Chrome()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source , 'lxml')
    new = soup.find_all(class_='news-list')
    neww = soup.find_all(class_='news-note')
    content = ''
    title = []
    #link = []
    for ne in new:
        title.append(re.sub(r'\n','', ne.text))
    '''
    for nee in neww:
        link.append(nee.get('href'))
    '''
    for i in range(0,9):
        content+='標題：{}\n\n'.format(title[i])
    browser.quit()
    return content

def flex(Title,title,label1,text1,data1,label2):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/aKCu3NS.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=title, weight='bold', size='xl',align='center')
                        
                        ]
            ),
            footer=BoxComponent(
                layout='horizontal',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#0B74A5',
                        action=PostbackAction(label=label1, text=text1,data=data1),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#C23232',
                        action=URIAction(label=label2,uri='http://training.tabc.org.tw/bin/acctinfo.php'),
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text= Title , contents=bubble)
    return message

def flexbutton(Title,title,label1,text1,data1,label2):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/aKCu3NS.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=title, weight='bold', size='xl',align='center')
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label1,text=text1,data=data1),
                    ),
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=URIAction(label=label2,uri='http://www.tabc.org.tw/tw/modules/pages/map')
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text=Title, contents=bubble)
    return message    

@handler.add(PostbackEvent)
def handle_postback(event):
    postback = event.postback.data
    profile = line_bot_api.get_profile(event.source.user_id)
    if postback == '會員專區':
        line_bot_api.reply_message(event.reply_token, flex("會員專區",'會員專區','綁定會員','綁定','綁定','註冊會員'))
    elif postback == '綁定':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('很抱歉，功能尚未開通'))
    elif postback == '最新消息':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(news()))
    elif postback == '其他功能':
        line_bot_api.reply_message(event.reply_token, flexbutton("其他功能",'其他功能','優惠折扣','優惠折扣','優惠','聯絡我們'))
    elif postback == '優惠':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('很抱歉，功能尚未開通'))
    elif postback == '課程資訊':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(classs()))

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

import os
if __name__ == "__main__":
    app.run()