# 네이버 증권
# 주식정보 크롤링
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = "https://finance.naver.com/sise/sise_market_sum.naver?&page="
browser.get(url)

# 2. 조회 항목 초기화(체크되어 있는 항목 체크 해재)
checkboxes = browser.find_elements(By.NAME, 'fieldIds') # 여러개 항목
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면
        checkbox.click() # 클릭(체크 해제)

# 3. 조회 항목 설정( 원하는 항목 )
items_to_select = ['영업이익','자산총계','매출액'] #label 에는 '(억)'이 따로 있음
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element 찾음 → td
    label = parent.find_element(By.TAG_NAME, 'label') # label tag를 가지는 값 반환
    #print(label.text) # 이름 확인
    if label.text in items_to_select: # 선택항목과 일치한다면
        checkbox.click() # 체크
        
# 4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]') # a태그의 href속성의 )
btn_apply.click()

for idx in range(1,41): # 1~41 미만 페이지 반복
    # 사전 작업 : 페이지 이동
    browser.get(url+str(idx))
    
    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    # 결측치 처리
    # 1)row 기준
    df.dropna(axis='index', how='all',inplace=True) # 모든 내용이 결측치로 채워져있을 때 제외
    # 2)column 기준
    df.dropna(axis='columns', how='all',inplace=True)
    if len(df) == 0: # 더이상 가져올 데이터가 없다면?
        break

    # 6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')
    
browser.quit() # 브라우저 종료