# 네이버 항공권
# 크롤링 및 웹 자동화
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_util(xpath_str):
    WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_str)))

browser = webdriver.Chrome()
browser.maximize_window()

url = 'https://flight.naver.com/' # 네이버 항공권 페이지
browser.get(url)

begin_date = browser.find_element(By.XPATH, '//button[text()="가는 날"]')
begin_date.click()

#time.sleep(1) # 1초 대기
wait_util('//b[text()="27"]') # 30초 대기
day27 = browser.find_elements(By.XPATH, '//b[text()="27"]') # 27일
day27[0].click()

wait_util('//b[text()="31"]')
day31 = browser.find_elements(By.XPATH, '//b[text()="31"]')
day31[0].click()

arrival = browser.find_element(By.XPATH, '//b[text()="도착"]')
arrival.click()

domestic = browser.find_element(By.XPATH, '//button[text()="국내"]')
domestic.click()

jeju = browser.find_element(By.XPATH, '//i[contains(text(), "제주국제공항")]')
jeju.click()

search = browser.find_element(By.XPATH, '//span[contains(text(), "항공권 검색")]')
search.click()

elem = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="domestic_Flight__sK0eA result"]')))
print(elem.text)

input('종료하려면 enter키를 입력해주세요!')
browser.quit()