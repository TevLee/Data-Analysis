import pandas as pd
import time
from selenium import webdriver

option = webdriver.ChromeOptions() #화면없이 ram에서만 돌리기
option.add_argument("headless") #option

print("selenium headless... (1)")
url = "https://finance.naver.com/marketindex/"
driver = webdriver.Chrome("driver/chromedriver",options=option) #option 추가
driver.get(url)

driver.maximize_window()
# driver.set_window_size(1920, 1080) # 화면최대화
time.sleep(3)


print("selenium headless... (2)")
# 화면 스크롤 하단 이동
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

iframe = driver.find_element_by_css_selector("#frame_ex1") 
driver.switch_to_frame(iframe)
time.sleep(2)


print("selenium headless... (3)")
contents = driver.find_elements_by_css_selector("body > div > table > tbody > tr") 

datas = []
for content in contents[:3]:
    title = content.find_element_by_css_selector(".tit > a").text 
    sale = content.find_element_by_css_selector(".sale").text
    link = content.find_element_by_css_selector(".tit > a").get_attribute("href") 
    datas.append({
        "title" : title,
        "sale":sale,
        "link":link
    })
    time.sleep(2)
    print("selenium headless... (4).{}".format(title))

driver.quit()
df = pd.DataFrame(datas)
df.to_excel("source_code/sel_naver_finance_vscode.xlsx", encoding="utf-8")
print("Selenium quit!!")