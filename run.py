# -*- coding: utf-8 -*-
# import requests
from bs4 import BeautifulSoup
import codecs
import uuid
import re
from archivenow import archivenow
import time
import datetime, pytz
import os
tz = pytz.timezone('Asia/Bangkok')
now1 = datetime.datetime.now(tz)

# firefox
# Add driver to PATH
import sys
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from pyvirtualdisplay import Display

REMOTE=True
if REMOTE:
    display = Display(visible=0, size=(800, 600))
    display.start()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.chrome.options.Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)


browser = webdriver.Chrome(options=options, service=Service(
    '/usr/bin/chromedriver'))

if REMOTE:
    #https://stackoverflow.com/a/17536547/2268280
    browser.set_page_load_timeout(30)
#

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

i2=1
i_backup = i
e = 0
data={}
# Google bot
headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"} 
while e < 200:
	url="https://www.thaigov.go.th/news/contents/details/"+str(i)
	try:
		browser.get(url)
		time.sleep(1)
		#r = requests.get(url, headers=headers, timeout=60, verify=False)
		# print(r.status_code)
		text=str(browser.page_source)
		print(text)
		# browser.close()
		if "<title>รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-</title>" not in text: #r.status_code == 200:
			print(url)
			title = re.search('<title>(.*?)</title>',text).group(1) #soup.title.text
			if title!="รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-":
				soup = BeautifulSoup(text, "lxml")
				article = soup.find('div',{'class':'border-normal clearfix'}).text #soup.article.text
				print("article")
				collection = soup.find('span',{'class':'Circular headtitle-2 font_level6 color2 col-xs-9 remove-xs'}).text
				print("collection")
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
				with codecs.open(os.path.join(f,collection+"_"+str(data[collection])+"_"+str(uuid.uuid4())+".txt"), "w", "utf-8") as temp:
					temp.write(all_data)
				temp.close()
				data[collection] += 1
				print(str(title)+"\t"+str(url))
				try:
					archivenow.push(url,"ia")
					time.sleep(8)
				except:
					pass
				i2+=1
				e = 0
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
