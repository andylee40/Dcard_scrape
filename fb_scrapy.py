#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 13:11:48 2023

@author: lihongcheng
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
import pandas as pd
import numpy as np
import time
import os
import glob
from datetime import datetime
import datetime as yester
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from sqlalchemy import create_engine
from sqlalchemy.types import String, Integer,Date
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from selenium.webdriver.common.keys import Keys

#防止彈跳視窗
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=options)
driver.get("https://www.facebook.com/")
driver.maximize_window()

#登入帳號密碼
user_name = driver.find_element(By.XPATH,"//input[@type='text']")
user_name.send_keys("帳號")
password = driver.find_element(By.XPATH,"//*[@id='pass']")
password.send_keys("密碼")
log_in_button = driver.find_element(By.XPATH,"//button[@type='submit']")
log_in_button.click()
time.sleep(15)


#搜尋寵物相關資訊
search = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/label/input")
search.send_keys("寵物")
search.send_keys(Keys.ENTER)
time.sleep(15)


#點擊社團
group=driver.find_element(By.LINK_TEXT,'社團')
group.click()
time.sleep(10)

#儲存社團連結
url=[]
url_total=[]

count=0
while True:
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    
    count+=1
    
    #解析網頁原始碼
    source = driver.page_source
    soup=BeautifulSoup(source,'lxml')
        
    #尋找所有社團連結
    div = soup.find_all("a", class_= "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")
    for i in div:
        try:
            url.append(i.get('href'))
        except:
            continue
    
    #計算不重複社團連結數
    url = list(dict.fromkeys(url))
    
    print("往下滑動{}次，共尋找出{}個社團".format(count,len(url)))

    
    footer=soup.find_all('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid")    
    if len(footer) !=0 :
        with open('url_0116.txt','w') as f:
            for i in url:
                f.write(i+'\n')
        url_total.append(url)
        break
    
time.sleep(5)
driver.close()       






