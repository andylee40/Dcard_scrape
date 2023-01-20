#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 14:44:24 2022

@author: admin
"""
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC   
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude
from matplotlib.pyplot import imread
import json
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import re
import numpy as np



# proxy="--proxy-server=http://"+valid_ips[0]
chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument(proxy)
chromeOptions.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')


#過濾中文英文數字以外字符
def filter_str(desstr, restr=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)


#爬蟲程式
def scrape(counts):
    
    global df
    #儲存標題以利判斷
    data=[]
    #儲存所有資料
    data2=[]
    specount=0
    #指定瀏覽器開啟
    #/Users/lihongcheng/Desktop/fb_scrape/chromedriver
    #service=Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chromeOptions)#,chrome_options=chromeOptions
    #進入寵物版
    driver.get("https://www.dcard.tw/f/pet")

    #將視窗開至最大
    driver.maximize_window()
    #開始爬蟲
    while True:
        #等待加載特定元素出現
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'article')))
        #找出文章位置
        post=driver.find_elements(By.TAG_NAME,'article')
        try:
            for posts in post:
                #print(posts)
                push_list=[]
                #標題
                title=posts.find_element(By.TAG_NAME,'h2').text
                
                #喜歡數
                try:
                    like=int(posts.find_element(By.CSS_SELECTOR,'.sc-1b0f4fad-0.jizqFI').text)
                except:
                    like=0
                #回應數
                try:
                    respon=int(posts.find_element(By.CSS_SELECTOR,'.sc-9130b5d8-2.cYLwhJ').text)
                except:
                    respon=0
               
                #滾動特殊處理
                if specount==3:
                    height=posts.size['height']+192
                elif specount==4:
                    height=posts.size['height']+215
                else:
                    height=posts.size['height']
                
                #文章內容
                if title in data:
                    continue
                else:
                    print(title)
                    #文章連結
                    ahref=posts.find_element(By.TAG_NAME,'a')
                    #點擊文章連結
                    webdriver.ActionChains(driver).move_to_element(ahref ).click(ahref ).perform()
                    time.sleep(3)
                    #文章內文字
                    content=driver.find_element(By.CSS_SELECTOR,".sc-ba53eaa8-0.iSPQdL").text
                    
                    #關閉文章視窗
                    driver.find_element(By.CSS_SELECTOR,".sc-ab9e99c9-2.cEeHvv").click()
                    time.sleep(1)
                    #疊加
                    data.append(title)
                    push_list.append(filter_str(title))
                    push_list.append(like)
                    push_list.append(respon)
                    push_list.append(filter_str(content))
                    #push_list.append(filter_str(title)+':'+filter_str(content))
                    #with open('explore.txt', 'a', encoding='utf-8') as file:
                        #file.write(filter_str(title)+':'+filter_str(content)+'\n')
                    #push_list.append(filter_str(content))
                #抓取熱門前100篇文章
                if len(data) > counts:
                     print('工作完成')
                     break   
                #向下滾動到下一個元素出現
                driver.execute_script("window.scrollBy(0,"+str(height)+");")
                time.sleep(1)
                #data2.append(push_list[0])
                data2.append(push_list)
                specount=specount+1
            df=pd.DataFrame(data=data2,columns=['title','like','response','content'])
        except:
            continue
        #抓取熱門前100篇文章
        if len(data) > counts:
             break
        
    #關閉瀏覽器
    driver.quit()

if __name__=='__main__':
    page=10
    scrape(page)
    print(df.corr())
