from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time


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



driver = webdriver.Chrome('D:/temp/chromedriver.exe')

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

for element in patient_list:
    patient_url = element.get_attribute("data-url")[1:]
    final_url = "https://hcms.mohw.go.kr/clinic" + patient_url +"&refererPage=1#medicalMemoSection"
    patient_url_list.append(final_url)


# 리스트에 저장된 url로 이동 후 차팅
cnt = 0     # 카운트(나중에 재원 환자 수와 맞는지 확인할 것)
for url in patient_url_list:
    driver.get(url)

    # 차팅 내용 입력
    charting = "차팅내용"
    xpath_send_keys("//textarea[@id='memoContent']", charting)

    # 차팅 시간
    charting_time = "2022-02-02 19:00"  # ex) 2022-02-02 19:00
    xpath_send_keys("//input[@id='eventDateTime3']", charting_time)

    # 차팅 저장 -------주의!!!!!!!_----------
    # xpath_click("//button[@id='medicalMemo']")

    # 카운트
    cnt += 1

    time.sleep(2)

print("차팅 횟수 : %d" % cnt)

