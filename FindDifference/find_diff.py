# 가상환경 사용
# 틀린그림찾기 앱을 통해서 게임 진행
# 틀린그림 찾기 자동화
# 1. 이미지 추출하기
import os, time
import pyautogui 
from PIL import ImageChops
import cv2

# 왼쪽 (원본) 이미지
# 시작좌표 (0, 22)
# 오른쪽 비교대상 시작 이미지
# 시작 좌표(964, 22)

# 이미지 크기 
# width 956
# height 764
while True:
    result = pyautogui.confirm('틀린 그림 찾기', buttons=['시작', '종료'])
    if result == '종료':
        break # 프로그램 종료
    
    width, height = 956, 764
    y_pos = 22
    
    src = pyautogui.screenshot(region=(0, y_pos, width, height))
    #src.save('src.jpg')
    
    test = pyautogui.screenshot(region=(964, y_pos, width, height))
    #test.save('test.jpg')
    
    diff = ImageChops.difference(src, test)
    diff.save('diff.jpg')
    
    # 파일 생성 대기
    while not os.path.exists('diff.jpg'):
        time.sleep(1)
    
    #src_img = cv2.imread('src.jpg')
    #test_img = cv2.imread('test.jpg')
    diff_img = cv2.imread('diff.jpg')
    
    gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY) # 흑백으로 바꾸기
    gray = (gray > 25) * gray # threshold 25(많이 어두운값) 제외 하고 그보다 큰 값 유효하게 판단
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # 외곽선 검출 / 윤곽선 검출
    
    COLOR = (0,200, 0) # 초록색(bgr기준)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100: # 외곽선 면적 크기 >100 사각형 그리기
            x,y,width, height = cv2.boundingRect(cnt) # 외곽선 둘러싸는 사각형 정보
            #cv2.rectangle(src_img, (x,y), (x+width, y+height), COLOR, 2)
            #cv2.rectangle(test_img, (x,y), (x+width, y+height), COLOR, 2)
            #cv2.rectangle(diff_img, (x,y), (x+width, y+height), COLOR, 2)
            to_x = x+ (width // 2)
            to_y = y+ (height // 2) + y_pos
            pyautogui.moveTo(to_x, to_y, duration=0.2)
            pyautogui.click(to_x,to_y)
            
    
    
    
    # cv2.imshow('src', src_img)
    # cv2.imshow('test', test_img)
    # cv2.imshow('diff', diff_img)
    
    #cv2.waitKey(0) # 무한대기
    #cv2.destroyAllWindows() # 프로그램 종료