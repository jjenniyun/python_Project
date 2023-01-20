# 공공데이터포털
# 우리 동네 아파트 실거래가 분석
# 참고 : https://github.com/WooilJeong/PublicDataReader/blob/main/assets/docs/portal/TransactionPrice.md#%EC%95%84%ED%8C%8C%ED%8A%B8%EB%A7%A4%EB%A7%A4-%EC%8B%A4%EA%B1%B0%EB%9E%98-%EC%83%81%EC%84%B8-%EC%9E%90%EB%A3%8C-%EC%A1%B0%ED%9A%8C-%EC%84%9C%EB%B9%84%EC%8A%A4
# !pip install PublicDataReader
# 주피터 노트북으로 진행
import PublicDataReader as pdr
# 서비스키 할당하기
service_key = "" # 공공데이터 포털에서 제공하는 키

# 국토교통부 실거래가 정보 조회 openapi세션 정의하기
ts = pdr.Transaction(service_key, debug=True)

# 데이터 조회 인스턴스 만들기
from PublicDataReader import TransactionPrice
api = TransactionPrice(service_key)

# 시군구코드 조회하기
sigungu_name = "분당구"
code = pdr.code_bdong()
code.loc[(code['시군구명'].str.contains(sigungu_name, na=False)) &
         (code['읍면동명'].isna())]

# 지역, 월 별 데이터 프레임 만들기
# 특정 년월 자료만 조회하기
# 부동산 상품 종류
# 부동산 거래 유형
df = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="41135",
    year_month="202212",
    )
df

df.to_excel('result_202212.xlsx') # 파일로 저장하기

# 특정 기간 자료 조회하기
df = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="41135",
    start_year_month="202212",
    end_year_month="202301",
    )

# Folium 지도 시각화 라이브러리