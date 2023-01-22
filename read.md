---
title: 網路爬蟲_Selenium
tags: 工作整理
description: 網路爬蟲_Selenium
---

# 使用Selenium模擬瀏覽器進行網路爬蟲

### 簡介：
利用 Python 內的 Selenium 套件模擬人為操作瀏覽器的行為，如：滾動視窗、滑鼠點擊及登入帳密等操作，進行網頁資料的獲取。


### 工具使用介紹：

:point_right:網路爬蟲 : Python (Selenium)



### 範例網站：
1. Facebook
2. Dcard


<br>

## Demo1 : 登入Facebook搜集社團資訊

:star:**簡介：** 透過獲取社團連結，後續可透過社群連結爬取社團每月文章數量等資訊

:star:**檔名：** fb_scrapy.py

:star:**重點操作介紹：**



- *登入帳號密碼*

    ![](https://i.imgur.com/YbHfVs4.png)

    ```python!
    #登入帳號密碼
    user_name = driver.find_element(By.XPATH,"//input[@type='text']")
    user_name.send_keys("帳號")
    password = driver.find_element(By.XPATH,"//*[@id='pass']")
    password.send_keys("密碼")
    log_in_button = driver.find_element(By.XPATH,"//button[@type='submit']")
    log_in_button.click()
    time.sleep(15)
    ```

<br>

- *輸入欲搜尋之關鍵字*

    ![](https://i.imgur.com/JpA95zU.png)

    ```python!
    #搜尋寵物相關資訊
    search = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/label/input")
    search.send_keys("欲搜尋之關鍵字")
    search.send_keys(Keys.ENTER)
    time.sleep(15)
    ```

<br>

- *點擊社團*

    ![](https://i.imgur.com/K6yUjk2.png)

    ```python!
    #點擊社團
    group=driver.find_element(By.LINK_TEXT,'社團')
    group.click()
    time.sleep(10)
    ```

<br>

- *持續滾動視窗，直至視窗底部*

    ```python!
    #滾到最底才會出現的class
    footer=soup.find_all('span',class_="x193iq5w xeuugli 
                             x13faqbe x1vvkbs xlh3980 xvmahel 
                             x1n0sxbx x1lliihq x1s928wv 
                             xhkezso x1gmr53x x1cpjm7i 
                             x1fgarty x1943h6x x4zkp8e 
                             x3x7a5m x6prxxf xvq8zen xo1l8bm 
                             xi81zsa x2b8uid")  
    #如果滾到最底則跳出迴圈
    if len(footer) !=0 :
        with open('url_0116.txt','w') as f:
            for i in url:
                f.write(i+'\n')
        url_total.append(url)
        break
    ```

<br>

- *結果*

    :point_down:獲取所有社團連結資訊
    
    ![](https://i.imgur.com/ldfyCpk.png)



<br>

## Demo2 : 爬取Dcard看板文章內容

:star:**簡介：** 爬取Dcard文章資料

:star:**檔名：** dcard_scrapy.py


:star:**重點操作說明：**

- *滾動特殊處理*

    發現文章第三篇與第四篇之間及第四篇與第五篇之間隔著非文章內容資    料，滾動頁面時進行滾動特殊處理，方可避免定位不到文章問題

    ![](https://i.imgur.com/Obc0rfl.png)


    ```python!
    #滾動特殊處理
    if specount==3:
        height=posts.size['height']+192
    elif specount==4:
        height=posts.size['height']+215
    else:
        height=posts.size['height']
    ```

    <br>


- *移動鼠標點選文章連結後關閉文章視窗*
    ![](https://i.imgur.com/eEuZGKx.png)

    ```python!
    #文章連結
    ahref=posts.find_element(By.TAG_NAME,'a')

    #點擊文章連結
    webdriver.ActionChains(driver).move_to_element(ahref ).click(ahref ).perform()

    time.sleep(3)

    #文章內容
    content=driver.find_element(By.CSS_SELECTOR,".sc-ba53eaa8-0.iSPQdL").text

    #關閉文章視窗
    driver.find_element(By.CSS_SELECTOR,".sc-ab9e99c9-2.cEeHvv").click()
    ```