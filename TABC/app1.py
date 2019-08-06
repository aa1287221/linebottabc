# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import serial    #import serial module
import plant
import time
import datetime
import schedule
import numpy as np
import multiprocessing as mp
p=np.load("plant.npz")
app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('kiCs2B8D8LSZZ32aJ+5nXT/V1r9gRXKMbBS7l9RsTfuhMbWVmbiRvhlwzOj8uYzciNw/OTGz5+mz9xKEHAIyhWSn9ylEXAM/6ow/Osep8NT+NgoovpBxk/0T/bgLfc/VgqxiM/aNbTqczQXA7VRfuQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('62df28a9d6ba49c16352e84f51e97120')

global save_val

humidity = [None]
temperature = [None]
light = [None]
dust = [None]
plant_kine=[None]
high_temp = [None]
low_temp = [None]
high_wet = [None]
low_wet = [None]
save_val = [None,None]
ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1);   #open named port at 9600,1s timeot
# 監聽所有來自 /callback 的 Post Request
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

def picture_line(url):                                                                           #send picture
    messages=ImageSendMessage(original_content_url=url, preview_image_url=url)
    return messages
def buttons_template(message_name,Title,small_title,url,label1,response1,data1,label2,response2,data2):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=url,
                size='full',
                aspect_ratio='1:1',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=Title, weight='bold', size='xl'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text=small_title,
                                        wrap=True,
                                        color='#0B74A5',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
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
                        action=PostbackAction(label=label1,text=response1,data=data1),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#C23232',
                        action=PostbackAction(label=label2,text=response2,data=data2),
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text=message_name, contents=bubble)
    return message

def multiple_button(Title,title,text,label1,data1,text1,label2,data2,text2,label3,data3,text3,label4,data4,text4,label5,data5,text5,label6,data6,text6):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/DakjALH.jpg',
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
                    ),
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=PostbackAction(label=label6,text=label6,data=label6)
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text=Title, contents=bubble)
    return message

def multiple_button2(Title,title,text,label1,data1,text1,label2,data2,text2,label3,data3,text3,label4,data4,text4,label5,data5,text5,label6,data6,text6):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/DakjALH.jpg',
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
                    ),
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color = '#624490',
                        action=URIAction(label=label6,uri='line://ti/p/@208wrpmy')
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text=Title, contents=bubble)
    return message    

def flex(Title,title,label1,text1,data1,label2,text2,data2):
    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/DakjALH.jpg',
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
                        action=PostbackAction(label=label2, text=text2,data=data2),
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text= Title , contents=bubble)
    return message


def autocontrol():
    global humidity
    global temperature
    global light
    global dust
    global plant_kind
    global high_temp
    global low_temp
    global high_wet
    global low_wet
    
    ser.write('h'.encode()) #writ a string to port
    humidity = ser.readall().decode()
    ser.write('t'.encode())#writ a string to port
    temperature = ser.readall().decode()
    ser.write('c'.encode())#writ a string to port
    light = ser.readall().decode()
    ser.write('v'.encode())#writ a string to port
    dust = ser.readall().decode()
    
    
    
    if temperature> high_temp:
        print('1')
        #ser.write('a'.encode());#writ a=關燈
    elif temperature< low_temp:
        #ser.write('b'.encode());#writ b=開燈
        print('2')
    elif dust> high_wet:
        #ser.write('b'.encode());#writ b=開登
        print('3')
    elif dust< low_wet:
        #ser.write('c'.encode());#writ c=澆水
        print('4')
    else :
        pass
    
    return temperature,dust,humidity
    



def autocontrol123():
    global humidity
    global temperature
    global light
    global dust
    global plant_kind
    global high_temp
    global low_temp
    global high_wet
    global low_wet
    
    ser.write('h'.encode()) #writ a string to port
    humidity = ser.readall().decode()
    ser.write('t'.encode())#writ a string to port
    temperature = ser.readall().decode()
    ser.write('c'.encode())#writ a string to port
    light = ser.readall().decode()
    ser.write('v'.encode())#writ a string to port
    dust = ser.readall().decode()
    
    
    
    if temperature> high_temp[0]:
        print('1')
        #ser.write('a'.encode());#writ a=關燈
    elif temperature< low_temp[0]:
        #ser.write('b'.encode());#writ b=開燈
        print('2')
    elif dust> high_wet[0]:
        #ser.write('b'.encode());#writ b=開登
        print('3')
    elif dust< low_wet[0]:
        #ser.write('c'.encode());#writ c=澆水
        print('4')
    else :
        pass
        
        
        
@handler.add(PostbackEvent)
def handle_postback(event):
    global plant_kind
    global high_temp
    global low_temp
    global high_wet
    global low_wet
    postBack = event.postback.data
    profile = line_bot_api.get_profile(event.source.user_id)
    if postBack == 'test':
        line_bot_api.reply_message(event.reply_token, TextSendMessage("hello ryan"))
    elif postBack == 'exit':
        line_bot_api.reply_message(event.reply_token, TextSendMessage("明阿災加個來"))
    elif postBack == "種":
        time.sleep(1)
        line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入你要種的植物"))
    elif postBack == "高溫":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入最高溫度(單位為°C)"))
    elif postBack == "低溫":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入最低溫度(單位為°C)"))
    elif postBack == "高濕":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入最高土壤濕度(單位為%)"))
    elif postBack == "低濕":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入最低土壤濕度(單位為%)")) 
    elif postBack == "黃":
        plant_kind="黃金葛";high_temp=str(p['gold'][0]);low_temp=str(p['gold'][1]);high_wet=str(p['gold'][2]);low_wet=str(p['gold'][3])
        line_bot_api.reply_message(event.reply_token,buttons_template("幫我確認一下資料好媽?"+profile.display_name,"設定資訊如下","品種： %s \n溫度範圍: %s °C ~ %s °C \n土壤濕度範圍: %s  ~ %s  \n"%(plant_kind,low_temp,high_temp,low_wet,high_wet),
                                "https://imgur.com/DakjALH.jpg" ,"可以哦","很讚",'無',"不太優","手動設定",'無'))
    elif postBack == "聖":
        plant_kind="聖誕紅";high_temp=str(p['santa'][0]);low_temp=str(p['santa'][1]);high_wet=str(p['santa'][2]);low_wet=str(p['santa'][3])    
        line_bot_api.reply_message(event.reply_token,buttons_template("幫我確認一下資料好媽?"+profile.display_name,"設定資訊如下","品種： %s \n溫度範圍: %s °C ~ %s °C \n土壤濕度範圍: %s  ~ %s  \n"%(plant_kind,low_temp,high_temp,low_wet,high_wet),
                                "https://imgur.com/DakjALH.jpg" ,"可以哦","很讚",'無',"不太優","手動設定",'無'))
    elif postBack == "常":
        plant_kind="常春藤";high_temp=str(p['spring'][0]);low_temp=str(p['spring'][1]);high_wet=str(p['spring'][2]);low_wet=str(p['spring'][3])
        line_bot_api.reply_message(event.reply_token,buttons_template("幫我確認一下資料好媽?"+profile.display_name,"設定資訊如下","品種： %s \n溫度範圍: %s °C ~ %s °C \n土壤濕度範圍: %s  ~ %s  \n"%(plant_kind,low_temp,high_temp,low_wet,high_wet),
                                "https://imgur.com/DakjALH.jpg" ,"可以哦","很讚",'無',"不太優","手動設定",'無'))
    elif postBack == "虎":
        plant_kind="虎尾蘭";high_temp=str(p['tiger'][0]);low_temp=str(p['tiger'][1]);high_wet=str(p['tiger'][2]);low_wet=str(p['tiger'][3])
        line_bot_api.reply_message(event.reply_token,buttons_template("幫我確認一下資料好媽?"+profile.display_name,"設定資訊如下","品種： %s \n溫度範圍: %s °C ~ %s °C \n土壤濕度範圍: %s  ~ %s  \n"%(plant_kind,low_temp,high_temp,low_wet,high_wet),
                                "https://imgur.com/DakjALH.jpg" ,"可以哦","很讚",'無',"不太優","手動設定",'無'))
    elif postBack == "手動設定":
        line_bot_api.reply_message(event.reply_token, multiple_button("做啥呢","手動設定清單",'page1',"要種什麼",'種',"我要種甚麼勒",'設定最高溫度','高溫','最高溫度','設定最低溫度','低溫','最低溫度',"設定最高土壤濕度",'高濕',"設定最高土壤濕度",'設定最低土壤濕度','低濕','設定最低土壤濕度','離開設定清單','exit','離開設定清單'))
          
           



@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    global plant_kind
    global high_temp
    global low_temp
    global high_wet
    global low_wet

 # get who send profile
    profile = line_bot_api.get_profile(event.source.user_id)
 
 # convert recive message to utf8 for chinese
    msg = event.message.text
#     line_bot_api.reply_message(event.reply_token,)

 
    save_val[0]=msg

  
    if msg == "初次見面":
        line_bot_api.reply_message(event.reply_token, flex("Hello~ "+profile.display_name,'歡迎使用Chat Plant','第一次來','第一次來','無','其實我是老司機','逼卡上車','無'))
    elif msg == "第一次來":
        line_bot_api.reply_message(event.reply_token, flex("想怎麼做呢",'想怎麼做','手動','手動設定','無','自動','自動設定','無'))
    elif msg == "手動設定":
        line_bot_api.reply_message(event.reply_token, multiple_button("做啥呢","手動設定清單",'page1',"要種什麼",'種',"我要種甚麼勒",'設定最高溫度','高溫','最高溫度','設定最低溫度','低溫','最低溫度',"設定最高土壤濕度",'高濕',"設定最高土壤濕度",'設定最低土壤濕度','低濕','設定最低土壤濕度','離開設定清單','exit','離開設定清單'))
    elif msg == "自動設定":
        line_bot_api.reply_message(event.reply_token, multiple_button2('做啥呢','請問要種什麼呢？','page2','黃金葛','黃','黃金葛','聖誕紅','聖','聖誕紅','常春藤','常','常春藤','虎尾蘭','虎','虎尾蘭','沒有我要的','手動設定','QQ','回報客服','客服','求建檔'))
    elif msg == "很讚":
        line_bot_api.reply_message(event.reply_token,TextSendMessage('已幫你自動設定完成'))
    elif msg ==  "來去逛逛":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(plant.flower()))
    elif msg == "沒錯哦":
        line_bot_api.reply_message(event.reply_token,[TextSendMessage("我真牛逼"),TextSendMessage("填寫完畢後請點左下方按鈕回到主選單")])  
    elif msg == "逼卡上車":
        line_bot_api.reply_message(event.reply_token,flex("有什麼我能為你服務呢",'有什麼我能為你服務呢','數值調整','手動設定','無','目前沒事','目前沒事','無'))
    elif msg == "目前沒事":
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(profile.display_name+"你真是個小調皮"),TextSendMessage("有空可以找我們客服聊天喔~")])  
    elif msg == '健康檢查':
        temperature1,dust1,humidity1=autocontrol()
        message = '溫度:%s土壤濕度:%s空氣濕度:%s'%(temperature1,dust1,humidity1)
        line_bot_api.reply_message(event.reply_token,buttons_template("爽",plant_kind+"生長環境",message,
                            "https://imgur.com/DakjALH.jpg","採取行動","採取行動",'1',"這樣就好","這樣就好",'2')) 
    elif msg == "這樣就好":
        line_bot_api.reply_message(event.reply_token,TextSendMessage('歡迎下次再來'))
    elif msg == "採取行動":
        line_bot_api.reply_message(event.reply_token,flex('你覺得呢 黑心老闆?','想對我做什麼','多喝點水','m開啟','無','曬曬太陽','l開啟','無'))
    elif msg == "m開啟":
        ser.write('a'.encode());#writ a string to port
        line_bot_api.reply_message(event.reply_token,TextSendMessage("喝得很飽"))
    elif msg == "l開啟":
        ser.write('b'.encode());#writ a string to port
        line_bot_api.reply_message(event.reply_token,TextSendMessage("這個燈我喜歡"))
    elif msg == "目前空氣濕度":
        ser.write('h'.encode())#writ a string to port
        humidity = ser.readall().decode()
        line_bot_api.reply_message(event.reply_token,TextSendMessage("目前空氣濕度:"+humidity))
    elif msg == "溫度":
        ser.write('t'.encode())#writ a string to port
        temperature = ser.readall().decode() 
        line_bot_api.reply_message(event.reply_token,TextSendMessage("溫度:"+temperature))
    elif msg == "光度":
        ser.write('c'.encode())#writ a string to port
        light = ser.readall().decode()
        line_bot_api.reply_message(event.reply_token,TextSendMessage("光度"+light))
    elif msg == "土壤濕度":
        ser.write('v'.encode());#writ a string to port
        dust= ser.readall().decode()
        line_bot_api.reply_message(event.reply_token,TextSendMessage("土壤濕度"+dust))
    elif msg == "還活著嗎":
        line_bot_api.reply_message(event.reply_token, flex('你覺得呢 黑心老闆?','老大 我快渴死了','出手相救','開啟','無','自生自滅','message text','無'))   
    if msg == "我要種什麼勒":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(""))
    elif msg == '最高溫度':
        plant_kind = save_val[1]
    elif msg == "最低溫度":
        high_temp = save_val[1]
    elif msg == "設定最高土壤濕度":
        low_temp=save_val[1]
    elif msg == "設定最低土壤濕度":
        high_wet=save_val[1]
    elif msg == '離開設定清單':
        low_wet=save_val[1]
        line_bot_api.reply_message(event.reply_token,buttons_template("幫我確認一下資料好嗎？"+profile.display_name,"設定資訊如下 有記錯嗎？","品種： %s \n溫度範圍: %s °C ~ %s °C \n土壤濕度範圍: %s  ~ %s  \n"%(plant_kind,low_temp,high_temp,low_wet,high_wet),
                            "https://imgur.com/DakjALH.jpg" ,"沒錯哦","沒錯哦",'無',"大錯特錯","手動設定",'無'))

    save_val[1]=save_val[0]
    save_val[0]=[None]

def line():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='localhost', port=port)
def run_time():
    while True:
        time.sleep(20)
        autocontrol123()


# print(profile.display_name)
# print(profile.user_id)
# print(profile.picture_url)

import os
if __name__ == "__main__":

