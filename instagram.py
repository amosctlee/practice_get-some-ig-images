import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome('./chromedriver.exe')
driver.get("https://www.instagram.com/")

# 等待頁面載入
try:
    account_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.-MzZI:nth-child(1) .zyHYP'))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.-MzZI+ .-MzZI .zyHYP'))
    )
except:
    print('something wrong')

# 輸入帳號密碼
account_field.send_keys(input('輸入手機、用戶名或email: '))
password_field.send_keys(input("輸入密碼: "))

# 按下登入
driver.find_element_by_css_selector('.y3zKF ._4EzTm').click()

# 是否要儲存登入資料:下次再說
try:
    dont_save_secret = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.yWX7d'))
    )
    dont_save_secret.click()
except:
    print('沒有按到按鈕')

# 是否開啟通知 稍後再說
try:
    dont_notice = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.HoLwm'))
    )
    dont_notice.click()
except:
    print('沒有按到按鈕')

# 跳過推薦用戶頁面，直接到explore 頁面
driver.get("https://www.instagram.com/explore")

# 等待圖片載入
time.sleep(3)

# 找到圖片所在位置
photos = driver.find_elements_by_css_selector('.FFVAD')
photo_urls = []
for p in photos:
    photo_urls.append(p.get_attribute('srcset').split(' ')[0])

print(photo_urls)

# 建立資料夾
if not os.path.exists('IGPhotos'):
    os.mkdir('IGPhotos')

# 將抓到的圖片存起來
for i, url in enumerate(photo_urls):
    response = requests.get(url)
    with open(f"IGPhotos/{i}.jpg", "wb") as f:
        f.write(response.content)
