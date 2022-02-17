import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import tkinter
from tkinter import *
from tkinter.ttk import *
import time
import os
import os, sys
from bs4 import BeautifulSoup
import threading



# pyinstaller -w -F --icon=koreaLogo.ico --add-binary "chromedriver.exe;." --add-data="koreaLogo.ico;." start_gui_with_combobox.py


# chromedriver 실행
def run_cd():
    global driver
    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path)
    else:
        driver = webdriver.Chrome()


# 어떤 요소가 존재하는지 확인하기 위한 함수(사용 안 함)
# def check_exists_by_xpath(xpath):
#     try:
#         driver.find_element(By.XPATH, xpath)
#     except NoSuchElementException:
#         return False
#     return True


# xpath로 요소 찾아서 텍스트 입력하는 함수
def xpath_send_keys(xpath, keys):
    element = driver.find_element(By.XPATH, xpath)
    element.send_keys(keys)


# xpath로 요소 찾아서 클릭하는 함수
def xpath_click(xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()


bagic_geometry = "400x400"
middle_geometry = "400x430"
long_geometry = "400x670"


win = Tk()
win.geometry(bagic_geometry)
win.resizable(width=False, height=False)
win.title("생치 일괄 차팅 넣기")
win.option_add("*Font", "돋움 15")
win.wm_attributes("-topmost", 1)

# 작업표시줄 아이콘 변경
path = os.path.join(os.path.dirname(__file__), 'koreaLogo.ico')
if os.path.isfile(path):
    win.iconbitmap(path)

# top_frame - 아이디, 비밀번호
top_frame = Frame(win)
top_frame.pack(pady=20, side="top")

# 아이디 라벨
id_label = Label(top_frame)
id_label.config(text="ID")
id_label.config(width=5)
id_label.grid(row=1, column=1)

# 아이디 입력칸
id_ent = Entry(top_frame)
id_ent.grid(row=1, column=2)

# 비밀번호 라벨
pw_label = Label(top_frame)
pw_label.config(text="PW")
pw_label.config(width=5)
pw_label.grid(pady=5, row=2, column=1)

# 비밀번호 입력칸
pw_ent = Entry(top_frame)
pw_ent.config(show="*")
pw_ent.grid(row=2, column=2)

# 로그인 에러 메시지 라벨
login_error_label = Label(top_frame)
login_error_label.config(text="아이디나 비밀번호를 확인해주세요")
login_error_label.config(font="돋움 10")
login_error_label.config(foreground="red")


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
    chart_time_day.set("일")
    chart_time_day.config(values=day_list)


# middle_frame_time - 차팅 시간(시간 라벨 + 시간 콤보박스)
middle_frame_time = Frame(win)
middle_frame_time.pack(pady=5, side="top")

# 차팅 시간 라벨 프레임
middle_frame_1 = Frame(middle_frame_time)
middle_frame_1.pack(side="top")

# 차팅 시간 콤보박스 프레임
middle_frame_2 = Frame(middle_frame_time)
middle_frame_2.pack(side="top")


# 차팅 시간 라벨 ex) "2022-02-06 19:00"
chart_time_label = Label(middle_frame_1)
chart_time_label.config(text="차팅시간")
chart_time_label.pack(pady=5)

# 차팅 시간 콤보박스(연도)
year_var = StringVar(middle_frame_time)

chart_time_year = Combobox(middle_frame_2)
chart_time_year.config(values=year_list)
chart_time_year.config(width=6)
chart_time_year.config(state="readonly")
chart_time_year.set('연도')
chart_time_year.grid(row=2, columnspan=2)

# 차팅 시간 콤보박스(월)
add_list(month_list, 1, 12)
month_var = StringVar(middle_frame_2)

chart_time_month = Combobox(middle_frame_2)
chart_time_month.config(values=month_list)
chart_time_month.config(width=3)
chart_time_month.bind("<<ComboboxSelected>>", change_day_combobox)
chart_time_month.config(state="readonly")
chart_time_month.set("월")
chart_time_month.grid(padx=3, row=2, column=3)

# 차팅 시간 콤보박스(일)
day_var = StringVar(middle_frame_2)

chart_time_day = Combobox(middle_frame_2)
chart_time_day.config(width=3)
chart_time_day.config(state="readonly")
chart_time_day.set("일")
chart_time_day.grid(row=2, column=4)

# 차팅 시간 콤보박스(시)
add_list(hour_list, 0, 23)
hour_var = StringVar(middle_frame_2)

chart_time_hour = Combobox(middle_frame_2)
chart_time_hour.config(values=hour_list)
chart_time_hour.config(width=3)
chart_time_hour.config(state="readonly")
chart_time_hour.set("시")
chart_time_hour.grid(padx=3, row=2, column=5)

# 차팅 시간 콤보박스(분)
minute_var = StringVar(middle_frame_2)

chart_time_minute = Combobox(middle_frame_2)
chart_time_minute.config(values=minute_list)
chart_time_minute.config(width=3)
chart_time_minute.config(state="readonly")
chart_time_minute.set("분")
chart_time_minute.grid(row=2, column=6)


# middle_frame_content - 차팅내용
middle_frame_content = Frame(win)
middle_frame_content.pack(pady=15, side="top")

# 차팅 내용 라벨
chart_content_label = Label(middle_frame_content)
chart_content_label.config(text="차팅내용")
chart_content_label.pack(pady=3)

# 차팅 내용 입력칸
chart_content_ent = Text(middle_frame_content, wrap=WORD)
chart_content_ent.config(width=26, height=5)
chart_content_ent.pack()

# bottom_frame - 결과창 프레임(재원환자수, 차팅한 환자수, 차팅 안 한 환자수, 차팅 한 환자목록, 차팅 안 한 환자목록)
bottom_frame = Frame(win)
bottom_frame.pack(side="top")


# 모든 위젯 값이 제대로 들어갔는지 확인
def check_all_inserted():
    if (id_ent.get() == "") or (pw_ent.get() == "") or (chart_time_year.get() == "연도") or (chart_time_month.get() == "월") or (chart_time_day.get() == "일") or (chart_time_hour.get() == "시") or (chart_time_minute.get() == "분") or (chart_content_ent.get(1.0, "end") == "\n") or (chart_content_ent.get(1.0, "end") == ""):
        win.geometry(middle_geometry)
        label = Label(middle_frame_content)
        label.config(text="모든 항목을 다 입력해주세요")
        label.config(foreground="red")
        label.config(font="돋움 13")
        label.pack(pady=1)

        time.sleep(2)
        label.pack_forget()

        if len(login_error_label.grid_info()) == 0:
            win.geometry(bagic_geometry)
        else:
            win.geometry(middle_geometry)
        result = False
    else:
        result = True
    return result


# 아이디와 비밀번호가 정확한지 확인(로그인에 실패하면 url이 바뀌지 않음)
def check_id_pw():
    result_url = driver.current_url
    if result_url == "https://hcms.mohw.go.kr/login/staff":
        return True
    return False


# 로그인 함수
def login():
    id = id_ent.get()
    pw = pw_ent.get()

    run_cd()

    driver.get("https://hcms.mohw.go.kr")
    driver.implicitly_wait(5)
    time.sleep(0.5)

    xpath_send_keys("//input[@id='id']", id)
    xpath_send_keys("//input[@id='password']", pw)
    xpath_click("//button[@id='submitBtn']")
    time.sleep(0.5)

    # 에러 메세지가 있으면 로그인 에러 라벨 출력
    if check_id_pw():
        win.geometry(middle_geometry)
        login_error_label.grid(row=3, columnspan=3)
        time.sleep(1)
        driver.quit()
        return False
    else:
        login_error_label.grid_forget()
        login_btn.pack_forget()
        loading_label.pack()
        return True


# 환자 정보 가져오기
def get_patient_list(session):
    # 환자 리스트로 이동
    driver.get('https://hcms.mohw.go.kr/clinic/state')
    driver.implicitly_wait(3)
    time.sleep(1)

    # 환자 리스트 개수 전체로 바꾸기
    show_list = Select(driver.find_element(By.ID, "viewEntry"))
    show_list.select_by_visible_text("전체")
    driver.implicitly_wait(3)
    time.sleep(1)

    response = session.get("https://hcms.mohw.go.kr/clinic/api/state?size=1000")

    return response.json()['items']


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


# 차팅 시간 조합
def make_charting_time():
    return "{}-{}-{} {}:{}".format(chart_time_year.get()
                                   , chart_time_month.get()
                                   , chart_time_day.get()
                                   , chart_time_hour.get()
                                   , chart_time_minute.get())


# 입력한 차팅 시간과 대조해서 이미 있으면 False, 없으면 True return
def check_chart(soup):
    chart_table = soup.find("table", {'id': 'memoDataTable'})
    chart_tr = chart_table.find_all("tr")
    for tr in chart_tr:
        # 각 tr의 첫번째 td = 처리일시(차팅시간)
        chart_td = tr.find_all()
        first_td = chart_td[0]
        text = first_td.get_text()
        if text == final_charting_time:
            return False
    return True


# 정해진 서식에 따라 라벨 만들기
def show_cnt(text1, text2):
    label = Label(bottom_frame)
    label.config(text="{} : {}".format(text1, text2))
    label.config(font="돋움 13")
    label.pack(pady=2)


# 차팅한 환자와 차팅 안 한 환자 목록 보여주기
def show_patient_list_frame(bottom_frame_list, charted_or_not, direction, list):
    # 차팅한 환자 또는 차팅 안 한 환자 목록 프레임
    frame = Frame(bottom_frame_list)
    frame.pack(side=direction, padx=2, pady=3)

    label = Label(frame)
    label.config(text=charted_or_not)
    label.config(font="돋움 15 bold")
    label.pack()

    # 스크롤바 생성
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # 환자 목록 listbox 생성
    listbox = Listbox(frame)
    listbox.config(selectmode="extended")
    listbox.config(font="고딕, 12")
    listbox.config(width=13, height=8)
    listbox.config(yscrollcommand=scrollbar.set)

    for p in list:
        listbox.insert(END, "{}호 {} ".format(p['roomId'], p['pName']))

    listbox.pack(side="left", pady=3)
    scrollbar.config(command=listbox.yview)


# 결과 보여주기
def show_result(cnt, charted_cnt, not_charted_cnt, charted_list, not_charted_list):
    win.geometry(long_geometry)

    show_cnt("재원환자수", cnt)
    show_cnt("차팅한 환자수", charted_cnt)
    show_cnt("차팅 안 한 환자수", not_charted_cnt)

    # bottom_frame 안에 frame 하나 더 만들기 = bottom_frame_list
    # bottom_frame_list 안에 차팅한 환자 목록과 차팅 안 한 환자 목록을 보여주는 frame 두 개가 들어있음
    bottom_frame_list = Frame(bottom_frame)
    bottom_frame_list.pack(side="bottom", pady=5)

    show_patient_list_frame(bottom_frame_list, "차팅함", "left", charted_list)
    show_patient_list_frame(bottom_frame_list, "차팅 안 함", "right", not_charted_list)


def chart():
    # 모든 항목이 입력되었으면 True return, 빠진 항목이 있으면 False return
    if check_all_inserted():
        # login() 로그인이 성공하면 True return, 실패하면 False return
        if login():
            session = update_session()

            global final_charting_time
            final_charting_time = make_charting_time()
            patient_info_list = get_patient_list(session)

            driver.quit()

            loading_label.config(text="차팅중...")

            charted_cnt = 0  # 차팅한 환자수
            not_charted_cnt = 0  # 차팅 안 한 환자수
            charted_list = [] # 차팅한 환자 리스트
            not_charted_list = []  # 차팅 안 한 환자 리스트

            recordedByName = ""
            # 각 url별로 data를 받아 post로 data 전송
            for info in patient_info_list:
                mPatientIdx = str(info['patientIdx'])

                url = "https://hcms.mohw.go.kr/clinic/info?patientIdx=" + mPatientIdx + "&refererPage=1#medicalMemoSection"
                response = session.get(url)
                soup = BeautifulSoup(response.text, "html.parser")

                if recordedByName == "":
                    recordedByName = soup.find("input", {"class": "form-control"}).get('value')
                    print(recordedByName)
                recordedById = id_ent.get()

                datas = {
                    'patientIdx': mPatientIdx,
                    'contents': chart_content_ent.get(1.0, "end"),
                    'recordedDate': final_charting_time,
                    'recordedByName': recordedByName,
                    'recordedById': recordedById
                }

                roomId = info['roomNumber']
                pName = info['patientName']

                request_url = "https://hcms.mohw.go.kr/clinic/api/memoData"
                p = {'roomId': roomId, 'pName': pName}

                if check_chart(soup):
                    session.post(request_url, params=datas)
                    charted_cnt += 1
                    charted_list.append(p)
                else:
                    not_charted_cnt += 1
                    not_charted_list.append(p)

            loading_label.pack_forget()
            show_result((charted_cnt+not_charted_cnt), charted_cnt, not_charted_cnt, charted_list, not_charted_list)

            restart_btn.pack()


# 프로그램을 실행하는 동안 응답없음을 막기 위해 스레드 사용
def th():
    th = threading.Thread(target=chart)
    th.daemon = True
    th.start()


# 재시작
def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# 차팅중 라벨
loading_label = Label(bottom_frame)
loading_label.config(text="로딩중... \n인터넷 창이 닫힙니다")
loading_label.config(justify="center")

# 버튼 프레임
button_frame = Frame(win)
button_frame.pack(pady=5, side="top")

# 입력 버튼
login_btn = tkinter.Button(button_frame)
login_btn.config(text="입력")
login_btn.config(width=10, height=1)
login_btn.config(command=th)
login_btn.pack()

# restart 버튼
restart_btn = tkinter.Button(button_frame)
restart_btn.config(text="다시")
restart_btn.config(width=10, height=1)
restart_btn.config(command=restart)


win.mainloop()
