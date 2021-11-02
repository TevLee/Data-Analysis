
import pandas as pd
import time
import requests

from selenium import webdriver
# explicitly wait 사용할 때 아래 3개 그냥 암기
from selenium.webdriver.common.by import By # By는 패키지
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("#1. selenium get url")
options = webdriver.ChromeOptions()
options.add_argument("headless")
url = "https://store.musinsa.com/app/"
driver = webdriver.Chrome("../driver/chromedriver", options=options)
# 웹 페이지 전체가 로딩될 때까지 10초간 대기하고, 
# 10초안에 로딩이 완료되면 다음 코드 실행
driver.implicitly_wait(10) 
driver.get(url)

print("#2. maximize window...")
#화면 최대화
driver.maximize_window()


print("#3. log-in...")
# 로그인 클릭 - 1 (wait)
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#default_top > div.header-member > button"))).click()
# 아이디 (wait)
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.musinsa-wrapper.wrapper-member.devicePC > div > form > input:nth-child(2)"))).send_keys("ltwy0311")
# 비밀번호 (wait)
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.musinsa-wrapper.wrapper-member.devicePC > div > form > input:nth-child(3)"))).send_keys("sotong13")
# 로그인 클릭 -2 (wait)
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.musinsa-wrapper.wrapper-member.devicePC > div > form > button"))).click()

print("#4. Best Hoody items ...")
# 인기 => 휴드 집업 링크 => 새탭으로 열기
bestHood_link = driver.find_element_by_css_selector("#ui-id-2 > ul:nth-child(1) > li:nth-child(1) > a").get_attribute("href")
driver.execute_script("window.open('{}')".format(bestHood_link))
# 후드 집업 탭으로 이동
driver.switch_to_window(driver.window_handles[1])
print("#5. tab open ok! I'm waititng...")
time.sleep(3)


# 단독 상품 체크
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn_exclusive"))).click()
# 세일 상품 체크 (wait 사용)
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn_sale"))).click()
print("#6. item option check...")
time.sleep(1)

# 금액 단위( 최소 - 최대 금액 ) 입력
# 최소
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#minPrice"))).send_keys("10000")
# 최대
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#maxPrice"))).send_keys("50000")
# 검색버튼 클릭
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn_price_search"))).click()
print("#7. item option check done! I'm waiting...")

print("#8. Hoody item crawling start...")
# 부모 태그
outers = driver.find_elements_by_css_selector("#searchList > li")

# 전체 데이터 크롤링

datas = []

for idx, outer in enumerate(outers[:10]):
    title = outer.find_element_by_css_selector("p.list_info > a").get_attribute("title"),
    price = outer.find_element_by_css_selector("p.price").text.split(" ")[1][:-1],
    sale = outer.find_element_by_css_selector(".icon_new").text.split()[1],
    link = outer.find_element_by_css_selector("p.list_info > a").get_attribute("href"),
    img = outer.find_element_by_css_selector("img").get_attribute("data-original")
    print("image tag link ...{}".format(img))

    datas.append({
        "title" : title,
        "price": price,
        "sale" : sale,
        "link" : link,
        "img" : img
    })
    print("#9. idx: {}, title : {}".format(idx,title))
driver.quit()
df = pd.DataFrame(datas)
df.to_excel("./musinsa/musinsa.xlsx",encoding="utf-8")
print("#10. crawling Done! diver quit & excel save")

print("11. img download")
# 이미지 다운로드
for idx, rows in df.iterrows():
    thumb_link = rows["img"]
    response = requests.get(thumb_link)
    name = str(idx) +"_"+ str(rows["title"])
    with open("./musinsa/{}.png".format(name), "wb") as f:
        f.write(response.content)
print("#12. image download Done")
print("# Finish ...")
