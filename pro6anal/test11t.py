# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여 
# 강수 여부에 따른 매출액의 평균에 차이가 있는지 검정
# 두 집단 : 강수량이 있을때, 맑을때

# 귀무가설 : 어느 음식점의 매출 데이터는 강수 여부에 따라 매출액 평균에 차이가 없다.
# 대립가설 : 어느 음식점의 매출 데이터는 강수 여부에 따라 매출액 평균에 차이가 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 매출 데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv",
                        dtype={"YMD":object})  # int -> object 변환
print(sales_data.head(2)) # (328,3)
#         YMD    AMT  CNT
# 0  20190514      0    1
# 1  20190519  18000    1
print(sales_data.info())

print('-'*40)
# 날씨 데이터 읽기
wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(2))  # (702,9)
#    stnId          tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  2018-06-01   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  2018-06-02   23.4   17.6   30.1    0.0    4.5    2.0    0.0
print(wt_data.info())

print('-'*40)
# sales: YMD 20190514, wt: tm 2018-06-01 => 병합을 위해 데이터 변환 필요
wt_data.tm = wt_data.tm.map(lambda x:x.replace('-',''))
print(wt_data.head(2))
#    stnId        tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  20180601   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  20180602   23.4   17.6   30.1    0.0    4.5    2.0    0.0

print('-'*40)
# 두 데이터를 병합
frame = sales_data.merge(wt_data, how='left', left_on=['YMD'], right_on=['tm'])
print(frame.columns)
# ['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn',
#    'maxWs', 'avgWs', 'ddMes']
print(frame.head(),' ',len(frame))

data = frame.iloc[:, [0,1,7,8]] # 'YMD','AMT','maxTa','sumRn'
print(data.head())
print('결측치 확인 : ', data.isnull().sum())

# 독립표본 t검정 -----
print(data["sumRn"] > 0)  # 강수량이 조금이라도 있으면 True를 반환

# 칼럼추가 : 강수량이 있으면 1, 없으면 0
# data['rain_yn'] = (data["sumRn"] > 0).astype(int)
# print(data.head())
print(True * 1, ' ', False * 1)  # astype없이 정수화 시키기
data['rain_yn'] = (data.loc[:,("sumRn")] > 0) * 1
print(data.head(3))
#       YMD     AMT    maxTa   sumRn  rain_yn
# 0  20190514      0   26.9    0.0        0
# 1  20190519  18000   21.6   22.0        1
# 2  20190521  50000   23.8    0.0        0

# boxplot으로 시각화
sp = np.array(data.iloc[:,[1, 4]])  # AMT, rain_yn
# print(sp)
tg1 = sp[sp[:,1] == 0, 0]  # 집단1 : 맑은날 매출액
tg2 = sp[sp[:,1] == 1, 0]  # 집단2 : 비가오는날 매출액
print(tg1[:3])   # [     0  50000 125000]
print(tg2[:3])   # [ 18000 274000 318000]
print("맑은날의 매출액 : ", tg1.mean())      # 761040.2542372881
print("비가오는날의 매출액 : ", tg2.mean())  # 757331.5217391305
plt.boxplot([tg1, tg2], meanline=True, showmeans=True, notch=True)
plt.show()

# 정규성 검정
print(len(tg1), " ", len(tg2))  # 236   92
print(stats.shapiro(tg1).pvalue)  # 0.05605
print(stats.shapiro(tg2).pvalue)  # 0.88275
# [판정] 두 집단 모두 p-value > 0.05 이므로 정규성을 만족함.

# 등분산성 검정
print(stats.levene(tg1, tg2).pvalue)  # 0.7123
# [판정] p-value(0.7123) > 0.05 이므로 등분산성을 만족함.

# 독립표본 t-검정 수행
result = stats.ttest_ind(tg1, tg2, equal_var=True)
print(f"t-통계량: {result.statistic:.4f}")  # 0.1011
print(f"p-value: {result.pvalue:.4f}")      # 0.9195

# [최종 판정] 유의수준 0.05 기준
# p-value(0.9195) >= 0.05 이므로 귀무가설을 채택한다.
# 결론: 강수 여부에 따른 매출액 평균에 유의미한 차이가 없다.