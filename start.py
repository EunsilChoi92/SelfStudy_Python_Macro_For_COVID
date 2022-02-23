from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import os, sys


# pyinstaller
# chromedriver가 컴퓨터에 있는지 확인
# Terminal에 pyinstaller --add-binary "chromedriver.exe;." --onefile --noconsole start_gui_with_optionmenu.py
if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome()


# 어떤 요소가 존재하는지 확인하기 위한 함수
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# xpath로 요소 찾아서 텍스트 입력하는 함수
def xpath_send_keys(xpath, keys):
    element = driver.find_element(By.XPATH, xpath)
    element.send_keys(keys)


# xpath로 요소 찾아서 클릭하는 함수
def xpath_click(xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()



# driver = webdriver.Chrome('D:/temp/chromedriver.exe')

url = 'https://hcms.mohw.go.kr/'
driver.get(url)
time.sleep(0.5)


# ID 입력
id = "ces1"
xpath_send_keys("//input[@id='id']", id)


# Password 입력
pw = "1q2w3e4r!"
xpath_send_keys("//input[@id='password']", pw)
time.sleep(0.5)


# 로그인
xpath_click("//button[@id='submitBtn']")
time.sleep(1)





'''
# 팝업창이 존재한다면 다시보지않기 체크 후 닫기 버튼 클릭 -> 클릭이 안됨.. 아직 해결 못함 ㅜㅜ
while check_exists_by_xpath("//label[@id='check-notice']"):
    if check_exists_by_xpath("//label[@id='check-notice']"):
        # check_notice_box_path = "//input[@class='never-see-again']"
        # check_notice_box = driver.find_element(By.XPATH, check_notice_box_path)
        # check_notice_box.click()

        close_btn_xpath = "//button[@class='close']"
        close_btn = driver.find_element(By.XPATH, close_btn_xpath)


        time.sleep(0.5)
'''


# 환자 리스트로 이동
url = 'https://hcms.mohw.go.kr/clinic/state'
driver.get(url)
time.sleep(1)


# 환자 리스트 개수 전체로 바꾸기
show_list_xpath = "//select[@id='viewEntry']"
show_list = Select(driver.find_element(By.ID, "viewEntry"))
show_list.select_by_visible_text("전체")
time.sleep(1)


# 환자 리스트 모두 가져오기
patient_list_xpath = "//div[@class='patients-stats ']"
patient_list = driver.find_elements(By.XPATH, patient_list_xpath)


# 환자 리스트에서 환자번호 추출해서 각 환자의 개인차트 url을 리스트에 저장
patient_url_list = []
for element_patient in patient_list:
    patient_url = element_patient.get_attribute("data-url")[1:]
    final_url = "https://hcms.mohw.go.kr/clinic" + patient_url +"&refererPage=1#medicalMemoSection"
    patient_url_list.append(final_url)


# 리스트에 저장된 url로 이동 후 차팅
cnt = 0     # 카운트(나중에 재원 환자 수와 맞는지 확인할 것)
patient_list_charted = []  # 차팅한 환자 이름 리스트

for url in patient_url_list:
    driver.get(url)

    # 차팅 여부 확인
    charting_time = "2022-02-09 19:00"  # ex) 2022-02-02 19:00
    check = True

    chart_table = driver.find_element(By.ID, "memoDataTable")   # 차트 테이블
    child_td = chart_table.find_elements(By.TAG_NAME, "td")     # 차트 테이블의 자식 요소들 중에서 td 태그를 가진 요소들

    # 같은 차팅 시간이 이미 존재하면 False로 바뀜
    for td in child_td:
        text = td.get_attribute('innerText')
        if text == charting_time:
            check = False
            break

    if check:
        # 차팅 내용 입력
        charting = "체온 측정 후 앱에 등록함.\n특이 호소 없음."
        xpath_send_keys("//textarea[@id='memoContent']", charting)

        # 차팅 시간
        xpath_send_keys("//input[@id='eventDateTime3']", charting_time)

        # 차팅 저장 -------주의!!!!!!!_----------
        xpath_click("//button[@id='medicalMemo']")

        # 카운트
        cnt += 1

        # 차팅한 환자 주소 추가
        patient_list_charted.append(url)

    time.sleep(2)

print("-----------차팅한 환자 url-----------")
for patient_charted in patient_list_charted:
    print(patient_charted)
print("---------차팅한 환자 url 끝---------")
print("차팅 횟수 : %d" % cnt)

