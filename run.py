# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import codecs
import re
from archivenow import archivenow
import time
import datetime, pytz
import os
tz = pytz.timezone('Asia/Bangkok')
now1 = datetime.datetime.now(tz)
f = os.path.join("data/",str(now1.strftime('%Y')))
if not os.path.exists(f):
    os.makedirs(f)
f = os.path.join(f,str(now1.strftime('%m')))
if not os.path.exists(f):
    os.makedirs(f)
f = os.path.join(f,str(now1.strftime('%d')))
if not os.path.exists(f):
    os.makedirs(f)

with open("last_num.txt","r", encoding="utf-8-sig") as file:
    i = int(file.read().strip())
# Code from https://github.com/delrayo/Pytest-Selenium-GitHubActions/blob/main/conftest.py
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
chrome_options = Options()
options = [
	"--headless",
	"--disable-gpu",
	"--window-size=1920,1200",
	"--ignore-certificate-errors",
	"--disable-extensions",
	"--no-sandbox",
	"--disable-dev-shm-usage"
]
for option in options:
	chrome_options.add_argument(option)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


i2=1
i_backup = i
e = 0
data={}
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
while e < 20:
	url="https://www.thaigov.go.th/news/contents/details/"+str(i)
	try:
		driver.get(url)
		if driver.title != "รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-":
			print(url)
			title = driver.title#re.search('<title>(.*?)</title>',r.text).group(1) #soup.title.text
			if title!="รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-":
				soup = BeautifulSoup(driver.page_source, "lxml")
				article = soup.find('div',{'class':'border-normal clearfix'}).text #soup.article.text
				collection = soup.find('span',{'class':'Circular headtitle-2 font_level6 color2 col-xs-9 remove-xs'}).text
				collection = re.sub('\?|\.|\!|\/|\;|\:', '', collection)

				_text = ''
				for line in article.split('\n'):
					line = line.strip()
					if line:
						_text = _text + '\n' + line
				article = _text
				
				all_data = title + "\n\n" + article + "\n\nที่มา : " + url
				
				if collection not in data:
					data[collection] = 1
				with codecs.open(os.path.join(f,collection+"_"+str(data[collection])+".txt"), "w", "utf-8") as temp:
					temp.write(all_data)
				temp.close()
				data[collection] += 1
				i2+=1
				e = 0
				try:
					archivenow.push(url,"ia")
					time.sleep(8)
				except:
					pass
				i+=1
				i_backup= i
			else:
				e += 1
				i+=1
		else:
			e+=1
	except Exception as ex:
		e+=1
		print(ex)#
#	#print(e)
#	#print(i)

with open("last_num.txt","w",encoding="utf-8") as f:
    f.write(str(i_backup))
