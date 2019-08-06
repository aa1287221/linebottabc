#import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium import webdriver
url="http://www.tabc.org.tw/tw/modules/news/"
browser = webdriver.Chrome()
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'lxml')
news = soup.find_all('a')
content=''
for n in news:
        if "a href=" in str(n):
                title = n.get_text()
                link = n.get('href')
                content+='標題：{}\n\n網址：{}\n\n'.format(title,link)
print(content)