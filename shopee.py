from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys


# Selenium登入
options = Options()
options.add_argument('--headless')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'./chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
driver.get('https://shopee.tw/buyer/login?next=https%3A%2F%2Fshopee.tw%2Fshop%2F13854632%2Fsearch')
# print(driver.page_source)
final_page = int(input('請輸入欲擷取頁數: '))
account = str(input('請輸入蝦皮帳號: '))
passwd = str(input('請輸入密碼: '))

driver.find_element_by_name('loginKey').send_keys(account) # 帳號
driver.find_element_by_name('password').send_keys(passwd) # 密碼
button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div/form/div/div[2]/button')
sleep(2)
button.click()
print('請於瀏覽器輸入手機驗證碼並靜待30秒')
sleep(30) # 利用等待時間手動輸入驗證碼
print('============開始擷取============')

name_list = []
price_list = []
sold_list = []
page = 0
while final_page != page:
    try:
        real_page = page + 1
        print(f'正在擷取第{real_page}頁............', end='')
        driver.get(f'https://shopee.tw/shop/13854632/search?page={page}&sortBy=pop')
        sleep(3)
        
        # 取得完整html
        # print(driver.page_source)

        # note: 直接將driver.page_source加入變數會抓不到inner html(?)

        # 解析html
        soup = BeautifulSoup(driver.page_source, 'lxml')
        sleep(1) 
        
        names = soup.find_all('div',{'class':'_1NoI8_ A6gE1J _1co5xN'})
        sleep(0.5)
        for name in names:
            name = name.text
            name_list.append(name)
        prices = soup.find_all('div',{'class':'_1w9jLI _1DGuEV _7uLl65'})
        sleep(0.5)
        for price in prices:
            price = price.text
            price_list.append(price)

        solds = soup.find_all('div', {'class':'_245-SC'})
        sleep(0.5)
        for sold in solds:
            sold = sold.text
            sold_list.append(sold)
        page += 1
        sleep(1)
        print('完成')
    except NoSuchElementException:
        break
    

# 轉成DataFrame並輸出成CSV
print('輸出至CSV............', end='')
out_put = {'品項':name_list, '價格':price_list, '賣出數量':sold_list}
df = pd.DataFrame(out_put)
df.to_csv('shopee.csv', encoding='utf-8-sig', index=False)
print('完成')

# 結束selenium
driver.close()
os.system("pause")