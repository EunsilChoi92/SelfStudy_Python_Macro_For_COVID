from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tkinter import *
import time
import os, sys



# pyinstaller
# Terminal에 pyinstaller --add-binary "chromedriver.exe;." --onefile --noconsole start_gui.py
# onefile은 에러 자주 나서 생략하는 게 좋을듯


# chromedriver 실행
def run_cd():
    global driver
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


# 로그인 함수
def login():
    id = id_ent.get()
    pw = pw_ent.get()

    run_cd()

    driver.get("https://hcms.mohw.go.kr/clinic/state")

    xpath_send_keys("//input[@id='id']", id)
    xpath_send_keys("//input[@id='password']", pw)
    xpath_click("//button[@id='submitBtn']")


win = Tk()
win.geometry("400x800")
win.option_add("*Font", "궁서 20")

# 아이디 라벨
id_label = Label(win)
id_label.config(text="ID")
id_label.pack()

# 아이디 입력칸
id_ent = Entry(win)
id_ent.pack()

# 비밀번호 라벨
pw_label = Label(win)
pw_label.config(text="PW")
pw_label.pack()

# 비밀번호 입력칸
pw_ent = Entry(win)
pw_ent.pack()

# 차팅 시간 라벨 "2022-02-06 19:00"
chart_time_label = Label(win)
chart_time_label.config(text="차팅시간")
chart_time_label.pack()


year_list = ["2022"]
month_list = []
day_list = [0]
hour_list = []
minute_list = ["00", "30"]

def add_list(list, start, end):
    for i in range(start, end+1):
        list.append(i)

# 차팅 시간 드롭다운(연도)
year_var = StringVar(win)
year_var.set("연도")

chart_time_year = OptionMenu(win, year_var, *year_list)
chart_time_year.config(width=90, font=("궁서", 12))
chart_time_year.config(bg="white")
chart_time_year.pack()

# 차팅 시간 입력칸(월)
add_list(month_list, 1, 12)

month_var = StringVar(win)
month_var.set("월")

chart_time_month = OptionMenu(win, month_var, *month_list)
chart_time_month.config(width=90, font=("궁서", 12))
chart_time_month.config(bg="white")


def my_show(*args):
    if month_var.get() == "2":
        print("2월!")
        day_list.clear()
        add_list(day_list, 1, 28)
        day_var.set(day_list)

month_var.trace('w', my_show)

chart_time_month.pack()


# 차팅 시간 입력칸(일)


day_var = StringVar(win)
day_var.set("일")

chart_time_day = OptionMenu(win, day_var, *day_list)
chart_time_day.config(width=90, font=("궁서", 12))
chart_time_day.config(bg="white")
chart_time_day.pack()

# 차팅 시간 입력칸(시)
add_list(hour_list, 0, 23)

hour_var = StringVar(win)
hour_var.set("시")

chart_time_hour = OptionMenu(win, hour_var, *hour_list)
chart_time_hour.config(width=90, font=("궁서", 12))
chart_time_hour.config(bg="white")
chart_time_hour.pack()

# 차팅 시간 입력칸(분)
minute_var = StringVar(win)
minute_var.set("분")

chart_time_minute = OptionMenu(win, minute_var, *minute_list)
chart_time_minute.config(width=90, font=("궁서", 12))
chart_time_minute.config(bg="white")
chart_time_minute.pack()

# 차팅 내용 라벨
chart_content_label = Label(win)
chart_content_label.config(text="차팅내용")
chart_content_label.pack()

# 차팅 내용 입력칸
chart_content_ent = Entry(win)
chart_content_ent.pack()

# 입력 버튼
login_btn = Button(win)
login_btn.config(text="입력")
login_btn.config(command=login)
login_btn.pack()



# url = 'https://hcms.mohw.go.kr/'
# driver.get(url)
# time.sleep(0.5)
#
#
# # ID 입력
# id = "ces1"
# xpath_send_keys("//input[@id='id']", id)
#
#
# # Password 입력
# pw = "1q2w3e4r!"
# xpath_send_keys("//input[@id='password']", pw)
# time.sleep(0.5)
#
#
# # 로그인
# xpath_click("//button[@id='submitBtn']")
# time.sleep(1)
#
#
#
# # 환자 리스트로 이동
# url = 'https://hcms.mohw.go.kr/clinic/state'
# driver.get(url)
# time.sleep(1)
#
#
# # 환자 리스트 개수 전체로 바꾸기
# show_list_xpath = "//select[@id='viewEntry']"
# show_list = Select(driver.find_element(By.ID, "viewEntry"))
# show_list.select_by_visible_text("전체")
# time.sleep(1)
#
#
# # 환자 리스트 모두 가져오기
# patient_list_xpath = "//div[@class='patients-stats ']"
# patient_list = driver.find_elements(By.XPATH, patient_list_xpath)
#
#
# # 환자 리스트에서 환자번호 추출해서 각 환자의 개인차트 url을 리스트에 저장
# patient_url_list = []
# for element_patient in patient_list:
#     patient_url = element_patient.get_attribute("data-url")[1:]
#     final_url = "https://hcms.mohw.go.kr/clinic" + patient_url +"&refererPage=1#medicalMemoSection"
#     patient_url_list.append(final_url)
#
#
# # 리스트에 저장된 url로 이동 후 차팅
# cnt = 0     # 카운트(나중에 재원 환자 수와 맞는지 확인할 것)
# patient_list_charted = []  # 차팅한 환자 이름 리스트
#
# for url in patient_url_list:
#     driver.get(url)
#
#     # 차팅 여부 확인
#     charting_time = "2022-02-06 19:00"  # ex) 2022-02-02 19:00
#     check = True
#
#     chart_table = driver.find_element(By.ID, "memoDataTable")   # 차트 테이블
#     child_td = chart_table.find_elements(By.TAG_NAME, "td")     # 차트 테이블의 자식 요소들 중에서 td 태그를 가진 요소들
#
#     # 같은 차팅 시간이 이미 존재하면 False로 바뀜
#     for td in child_td:
#         text = td.get_attribute('innerText')
#         if text == charting_time:
#             check = False
#             break
#
#     if check:
#         # 차팅 내용 입력
#         charting = "체온 측정 후 앱에 등록함.\n특이 호소 없음."
#         xpath_send_keys("//textarea[@id='memoContent']", charting)
#
#         # 차팅 시간
#         xpath_send_keys("//input[@id='eventDateTime3']", charting_time)
#
#         # 차팅 저장 -------주의!!!!!!!_----------
#         xpath_click("//button[@id='medicalMemo']")
#
#         # 카운트
#         cnt += 1
#
#         # 차팅한 환자 주소 추가
#         patient_list_charted.append(url)
#
#     time.sleep(2)
#
# print("-----------차팅한 환자 url-----------")
# for patient_charted in patient_list_charted:
#     print(patient_charted)
# print("---------차팅한 환자 url 끝---------")
# print("차팅 횟수 : %d" % cnt)


win.mainloop()
