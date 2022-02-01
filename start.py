from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('D:/temp/chromedriver.exe')

url = 'https://hcms.mohw.go.kr/'
driver.get(url)
time.sleep(0.5)

# ID 입력
id_path = "//input[@id='id']"
id_input = driver.find_element(By.XPATH, id_path)
id_input.send_keys("ID")

# Password 입력
pw_path = "//input[@id='password']"
pw_input = driver.find_element(By.XPATH, pw_path)
pw_input.send_keys("password")
time.sleep(0.5)

# 로그인
login_path = "//button[@id='submitBtn']"
login_btn = driver.find_element(By.XPATH, login_path)
login_btn.click()
time.sleep(1)

# 팝업창이 있다면
#check_notice_path = "//label[@id='check-notice']"   # 다시 보지 않기 체크가 존재하는지 확인하기 위해
a = driver.find_element(By.ID, 'check-notice1')



'''
if check_notice_path == "//label[@id='check-notice']" :
    
    check_notice_box_path = "//input[@class='never-see-again']"
    check_notice_box = driver.find_element(By.XPATH, check_notice_box_path)
    check_notice_box.click()
'''