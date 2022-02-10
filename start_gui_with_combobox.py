import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tkinter import *
from tkinter.ttk import *
import time
import os, sys
from bs4 import BeautifulSoup
import json


# pyinstaller
# Terminal에 pyinstaller --add-binary "chromedriver.exe;." --onefile --noconsole start_gui_with_optionmenu.py
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


# combobox에 추가할 list들
year_list = ["2022"]
month_list = []
day_list = [0]
hour_list = []
minute_list = ["00", "30"]

# month, day, hour 리스트에  추가
def add_list(list, start, end):
    for i in range(start, end+1):
        str_num = ""
        if i < 10:
            str_num = "0" + str(i)
        else:
            str_num = str(i)
        list.append(str_num)

# day_list 요소 변경
def change_day_list(end):
    day_list.clear()
    add_list(day_list, 1, end)

# 선택한 month에 따라 day combobox 변경
def change_day_combobox(*args):
    month = int(chart_time_month.get())
    if month == 2:
        change_day_list(28)
    elif ((month < 8) and (month % 2 == 1)) or ((month > 7) and (month % 2 == 0)):
        change_day_list(31)
    else:
        change_day_list(30)
    chart_time_day.config(values=day_list)


# 차팅 시간 라벨 ex) "2022-02-06 19:00"
chart_time_label = Label(win)
chart_time_label.config(text="차팅시간")
chart_time_label.pack()

# 차팅 시간 콤보박스(연도)
year_var = StringVar(win)

chart_time_year = Combobox(win)
chart_time_year.config(values=year_list)
chart_time_year.insert(0, '연도')
chart_time_year.pack()

# 차팅 시간 콤보박스(월)
add_list(month_list, 1, 12)
month_var = StringVar(win)

chart_time_month = Combobox(win)
chart_time_month.config(values=month_list)
chart_time_month.bind("<<ComboboxSelected>>", change_day_combobox)
chart_time_month.insert(0, '월')
chart_time_month.pack()

# 차팅 시간 콤보박스(일)
day_var = StringVar(win)

chart_time_day = Combobox(win)
chart_time_day.insert(0, '일')
chart_time_day.pack()

# 차팅 시간 콤보박스(시)
add_list(hour_list, 0, 23)
hour_var = StringVar(win)

chart_time_hour = Combobox(win)
chart_time_hour.config(values=hour_list)
chart_time_hour.insert(0, '시')
chart_time_hour.pack()

# 차팅 시간 콤보박스(분)
minute_var = StringVar(win)

chart_time_minute = Combobox(win)
chart_time_minute.config(values=minute_list)
chart_time_minute.insert(0, '분')
chart_time_minute.pack()


# 차팅 내용 라벨
chart_content_label = Label(win)
chart_content_label.config(text="차팅내용")
chart_content_label.pack()


# 차팅 내용 입력칸
chart_content_ent = Entry(win)
chart_content_ent.pack()


# 로그인 함수
def login():
    id = id_ent.get()
    pw = pw_ent.get()

    run_cd()

    driver.get("https://hcms.mohw.go.kr")
    driver.implicitly_wait(10)

    xpath_send_keys("//input[@id='id']", id)
    xpath_send_keys("//input[@id='password']", pw)
    xpath_click("//button[@id='submitBtn']")
    time.sleep(2)


def make_charting_time():
    return "{}-{}-{} {}:{}".format(chart_time_year.get()
                                   , chart_time_month.get()
                                   , chart_time_day.get()
                                   , chart_time_hour.get()
                                   , chart_time_minute.get())

def get_patient_list():
    # 환자 리스트로 이동
    driver.get('https://hcms.mohw.go.kr/clinic/state')
    driver.implicitly_wait(10)
    time.sleep(1)

    # 환자 리스트 개수 전체로 바꾸기
    show_list = Select(driver.find_element(By.ID, "viewEntry"))
    show_list.select_by_visible_text("전체")
    driver.implicitly_wait(10)
    time.sleep(1)

    # 환자 리스트 모두 가져오기
    patient_list_xpath = "//div[@class='patients-stats ']"
    patient_list = driver.find_elements(By.XPATH, patient_list_xpath)

    # 환자 리스트에서 환자번호 추출해서 각 환자의 개인차트 url을 리스트에 저장
    patient_url_list = []
    for element_patient in patient_list:
        patient_url = element_patient.get_attribute("data-url")[1:]
        final_url = "https://hcms.mohw.go.kr/clinic" + patient_url + "&refererPage=1#medicalMemoSection"
        patient_url_list.append(final_url)

    return patient_url_list

# 세션 정보 변경
def update_session():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 Edg/96.0.1054.62'
    }
    session.headers.update()
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        session.cookies.update(c)
    return session

# 입력한 차팅 시간과 대조해서 이미 있으면 False, 없으면 True return
def check_chart(soup):
    chart_table = soup.find("table", {'id': 'memoDataTable'})
    chart_td = chart_table.find_all("td")
    for td in chart_td:
        text = td.get_text()
        if text == final_charting_time:
            return False
        else:
            return True

def chart():
    login()
    patient_url_list = get_patient_list()

    global final_charting_time
    final_charting_time = make_charting_time()

    session = update_session()
    # response = session.get("https://hcms.mohw.go.kr/clinic/api/state?size=1000")

    cnt = 0 # 전체 환자수
    charted_cnt = 0 # 차팅한 환자수
    not_charted_cnt = 0 # 차팅 안 한 환자수
    not_charted_list = [] # 차팅 안 한 환자 리스트
    
    # 각 url별로 data를 받아 post로 data 전송
    for url in patient_url_list:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        mPatientIdx = soup.find("input", {"id": "patientIdx"}).get('value')
        recordedByName = soup.find("input", {"class": "form-control"}).get('value')
        recordedById = id_ent.get()

        datas = {
            'patientIdx': mPatientIdx,
            #'contents': chart_content_ent.get(),
            'contents': "체온 측정 후 앱에 등록함.\n특이 호소 없음.",
            'recordedDate': final_charting_time,
            'recordedByName': recordedByName,
            'recordedById': recordedById
        }

        roomId = soup.find("input", {"id": "roomId"}).get('value')
        pName = soup.find("input", {"id": "pName"}).get('value')

        request_url = "https://hcms.mohw.go.kr/clinic/api/memoData"
        p = {'roomId':roomId, 'pName':pName}

        if check_chart(soup):
            #response = session.post(request_url, params=datas)
            charted_cnt += 1
        else:
            not_charted_cnt += 1
            not_charted_list.append(p)
        cnt += 1

    show_cnt("재원환자수", cnt)
    show_cnt("차팅한 환자수", charted_cnt)
    show_cnt("차팅 안 한 환자수", not_charted_cnt)

    str = ""
    for p in not_charted_list:
        str += "{}호 {}\n".format(p['roomId'], p['pName'])

    show_cnt("차팅 안 한 환자", ("\n" + str))

def show_cnt(text1, text2):
    label = Label(win)
    label.config(text="{} : {}".format(text1, text2))
    label.pack()


# 입력 버튼
login_btn = Button(win)
login_btn.config(text="입력")
login_btn.config(command=chart)
login_btn.pack()

win.mainloop()
