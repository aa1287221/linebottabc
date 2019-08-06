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
import tempfile, os

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('kiCs2B8D8LSZZ32aJ+5nXT/V1r9gRXKMbBS7l9RsTfuhMbWVmbiRvhlwzOj8uYzciNw/OTGz5+mz9xKEHAIyhWSn9ylEXAM/6ow/Osep8NT+NgoovpBxk/0T/bgLfc/VgqxiM/aNbTqczQXA7VRfuQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('62df28a9d6ba49c16352e84f51e97120')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

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

def news(Title,title,label1,text1,data1,label2,text2,data2):
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
                        action=PostbackAction(label=label1,text=text1,data=data1)
                    ),
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label2,text=text2,data=data2)
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text=Title, contents=bubble)
    return message

def upload(Title,title,text,label1,data1,text1,label2,data2,text2,label3,data3,text3,label4,data4,text4,label5,data5,text5):
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
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label2,text=text2,data=data2),
                    ),
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label3,text=text3,data=data3),
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label4,text=text4,data=data4),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label5,text=text5,data=data5),
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
    if postback == '最新消息':
        line_bot_api.reply_message(event.reply_token, news('最新消息選單','最新消息選單','平台新聞','平台新聞','新聞','活動消息','活動消息','活動'))
    elif postback == '新聞':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('很抱歉，功能尚未開通'))
    elif postback == '活動':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('很抱歉，功能尚未開通'))    
    elif postback == '平台上架':
        line_bot_api.reply_message(event.reply_token, upload('平台上架選單','平台上架選單','page1','送件須知','送件','送件須知','下載專區','下載','下載專區','電子合約','合約','電子合約','檔案上傳','上傳','檔案上傳','審核進度','審核','審核進度'))
    elif postback == '會員服務':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('很抱歉，功能尚未開通'))
    elif postback == '線上諮詢':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('您可以直接透過輸入關鍵字詢問來讓我幫助您！'))

@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage)) #圖片上傳
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])
'''
@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳成功'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0
'''
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