# 터미널창 초기화
import os
os.system('cls')

import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
from scipy.stats import wilcoxon
import pandas as pd


'''
[one-sample t 검정 : 문제1]  
영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다. 
한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다. 
연구소의 발표결과가 맞는지 새로 개발된 백열전구를 임의로 수집하여 수명 시간 관련 자료를 얻었다. 
한국 연구소의 발표가 맞는지 새로운 백열전구의 수명을 분석하라.
수집된 자료 :  305 280 296 313 287 240 259 266 318 280 325 295 315 278
'''
# 새 백열전구 수명 데이터
lamp = [305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]

print(f"표본 수: {len(lamp)}")
print(f"표본 평균: {np.mean(lamp):.2f}")
print(f"표본 표준편차: {np.std(lamp, ddof=1):.2f}")

# 연구소 주장: 기존 250시간보다 50시간 더 길다 → 평균 300시간
# 귀무가설(H0): 새로운 백열전구 평균 수명은 300시간이다.
# 대립가설(H1): 새로운 백열전구 평균 수명은 300시간이 아니다.

# 정규성 검정
shapiro_result = stats.shapiro(lamp)
print(f"Shapiro-Wilk p-value: {shapiro_result.pvalue:.4f}")

# 단일표본 t-검정
result = stats.ttest_1samp(lamp, popmean=300)
print(f"t-통계량: {result.statistic:.4f}")
print(f"p-value: {result.pvalue:.4f}")

# 판정
alpha = 0.05
if result.pvalue < alpha:
    print("귀무가설 기각")
    print("→ 새로운 백열전구 평균 수명은 300시간과 차이가 있다.")
else:
    print("귀무가설 채택")
    print("→ 새로운 백열전구 평균 수명은 300시간이라고 볼 수 있다.")

# 비모수 검정
wilcox_result = wilcoxon(np.array(lamp) - 300)
print(wilcox_result)

# 시각화
sns.displot(lamp, kde=True)
plt.xlabel('수명')
plt.ylabel('빈도')
plt.show()

stats.probplot(lamp, plot=plt)
plt.show()
plt.close()


'''
[one-sample t 검정 : 문제2] 
국내에서 생산된 대다수의 노트북 평균 사용 시간이 5.2 시간으로 파악되었다. A회사에서 생산된 노트북 평균시간과 차이가 있는지를 검정하기 위해서 A회사 노트북 150대를 랜덤하게 선정하여 검정을 실시한다.  
실습 파일 : one_sample.csv
참고 : time에 공백을 제거할 땐 ***.time.replace("     ", ""),

        null인 관찰값은 제거.
'''
# CSV 파일 읽기
# 파일명은 실제 보유한 파일명으로 수정
one_sample = pd.read_csv('one_sample.csv')

print(one_sample.head())
print(one_sample.info())

# time 컬럼 공백 제거
one_sample['time'] = one_sample['time'].astype(str)
one_sample['time'] = one_sample['time'].str.replace('     ', '', regex=False)
one_sample['time'] = one_sample['time'].str.strip()

# 숫자형 변환
one_sample['time'] = pd.to_numeric(one_sample['time'], errors='coerce')

# 결측치 제거
one_sample = one_sample.dropna(subset=['time'])

print(one_sample.head())
print(f"데이터 개수: {len(one_sample)}")
print(f"A회사 노트북 평균 사용 시간: {one_sample['time'].mean():.4f}")

# 귀무가설(H0): A회사 노트북 평균 사용 시간은 5.2시간이다.
# 대립가설(H1): A회사 노트북 평균 사용 시간은 5.2시간이 아니다.

# 표본 수가 150개로 충분히 크므로 정규성 여부와 상관없이 t-검정 가능
# 그래도 정규성 검정 수행
shapiro_result = stats.shapiro(one_sample['time'])
print(f"Shapiro-Wilk p-value: {shapiro_result.pvalue:.4f}")

# 단일표본 t-검정
result = stats.ttest_1samp(one_sample['time'], popmean=5.2)
print(f"t-통계량: {result.statistic:.4f}")
print(f"p-value: {result.pvalue:.4f}")

# 판정
alpha = 0.05
if result.pvalue < alpha:
    print("귀무가설 기각")
    print("→ A회사 노트북 평균 사용 시간은 5.2시간과 차이가 있다.")
else:
    print("귀무가설 채택")
    print("→ A회사 노트북 평균 사용 시간은 5.2시간이라고 볼 수 있다.")

# 필요 시 비모수 검정
wilcox_result = wilcoxon(one_sample['time'] - 5.2)
print(wilcox_result)

# 시각화
sns.displot(one_sample['time'], kde=True)
plt.xlabel('사용 시간')
plt.ylabel('빈도')
plt.show()

stats.probplot(one_sample['time'], plot=plt)
plt.show()
plt.close()




'''
[one-sample t 검정 : 문제3] 
https://www.price.go.kr/tprice/portal/main/main.do 에서 
메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)
'''


file_name = '개인서비스지역별_동향[2026-02월]331-0시15분.xls'

raw = pd.read_excel(file_name, engine='xlrd')

print(raw.head())
print(raw.columns)

# 미용 행만 추출
beauty = raw[raw['품목'] == '미용']

# 지역별 가격 컬럼 선택
price_cols = ['서울', '부산', '대구', '인천', '광주', '대전', '울산',
            '경기', '강원', '충북', '충남', '전북', '전남',
            '경북', '경남', '제주']

# 세종은 NaN이라 제외
prices = beauty[price_cols].values.flatten()

# NaN 제거
prices = pd.Series(prices).dropna()

print(f"표본 수: {len(prices)}")
print(f"평균 미용 요금: {prices.mean():.2f}")
print(f"표준편차: {prices.std():.2f}")

# 정규성 검정
shapiro_result = stats.shapiro(prices)
print(f"Shapiro-Wilk p-value: {shapiro_result.pvalue:.4f}")

# 단일표본 t-검정
result = stats.ttest_1samp(prices, popmean=15000)
print(f"t-통계량: {result.statistic:.4f}")
print(f"p-value: {result.pvalue:.4f}")

# 판정
if result.pvalue < 0.05:
    print("귀무가설 기각")
    print("→ 전국 평균 미용 요금은 15000원과 차이가 있다.")
else:
    print("귀무가설 채택")
    print("→ 전국 평균 미용 요금은 15000원이라고 볼 수 있다.")

# 비모수 검정
wilcox_result = wilcoxon(prices - 15000)
print(wilcox_result)

# 시각화
sns.displot(prices, kde=True)
plt.xlabel('미용 요금')
plt.ylabel('빈도')
plt.show()

stats.probplot(prices, plot=plt)
plt.show()
plt.close()