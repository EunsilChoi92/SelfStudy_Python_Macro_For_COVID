from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome('D:/temp/chromedriver.exe')

url = 'https://hcms.mohw.go.kr/'
driver.get(url)
time.sleep(0.5)

# ID 입력
id_path = "//input[@id='id']"
id_input = driver.find_element(By.XPATH, id_path)
id_input.send_keys("아이디")

# Password 입력
pw_path = "//input[@id='password']"
pw_input = driver.find_element(By.XPATH, pw_path)
pw_input.send_keys("비번")
time.sleep(0.5)

# 로그인
login_path = "//button[@id='submitBtn']"
login_btn = driver.find_element(By.XPATH, login_path)
login_btn.click()
time.sleep(1)

# 어떤 요소가 존재하는지 확인하기 위한 함수
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


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

show_list_xpath = "//select[@id='viewEntry']"
show_list = Select(driver.find_element(By.ID, "viewEntry"))
show_list.select_by_visible_text("전체")

time.sleep(1)
patient_list_xpath = "//div[@class='patients-stats ']"
patient_list = driver.find_elements(By.XPATH, patient_list_xpath)


# dfiver.get(url)이 한 번만 돌고 자꾸 에러가 남...ㅠㅠ
for element in patient_list:
    patient_url = element.get_attribute("data-url")[1:]
    print(patient_url)
    url = "https://hcms.mohw.go.kr/clinic" + patient_url +"&refererPage=1#medicalMemoSection"
    driver.get(url)

    # charting_area_xpath = "//textarea[@id='memoContent']"
    # charting_area = driver.find_element(By.XPATH, charting_area_xpath)
    # charting_area.send_keys("헤헤헤")
    #
    # time_input_xpath = "//input[@id='eventDateTime3']"
    # time_input = driver.find_element(By.XPATH, time_input_xpath)
    # time_input.send_keys("2022-02-02 19:00")
    #
    # time_btn_xpath = "//button[@id='medicalMemo']"
    # time_btn = driver.find_element(By.XPATH, time_btn_xpath)
    # time_btn.click()







#./info?patientIdx=512047&refererPage=1#medicalMemoSection
