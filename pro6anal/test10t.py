# 독립 표본 t-test (independent two sample t-test)
# 실습 : 두가지 교육 방법에 따른 평균 시험 점수에 대한 검정 수행

# 귀무 : 두가지 교육 방법에 따른 시험점수 평균에 차이가 없다.
# 대립 : 두가지 교육 방법에 따른 시험점수 평균에 차이가 있다.

import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/two_sample.csv")
print(data.head())
# print(data.isnull().sum())  # null 값 확인
# print(data['score'].isnull().sum())
# print(data.shape) # (50,5)

# 교육 방법별 분리
ms = data[['method', 'score']]
m1 = ms[ms['method'] == 1]  # 방법 1
m2 = ms[ms['method'] == 2]  # 방법 2
print(m1.head(3))
print(m2.head(3))

# 교육방법에서 score 만 별도 기억
score1 = m1['score']
score2 = m2['score']
print(score1.isnull().sum())  # 0
print(score2.isnull().sum())  # 2

# score2 = score2.fillna(0)   # Nan을 0으로 대체
score2 = score2.fillna(score2.mean())  # Nan을 평균으로 대체

# 정규성 검정
print(stats.shapiro(score1)) #  pvalue=0.36799
print(stats.shapiro(score2)) #  pvalue=0.67142
# [판정] 두 집단 모두 p-value > 0.05 이므로 정규성을 만족함.

# 정규성 시각화
sns.histplot(score1, kde=True)
sns.histplot(score2, kde=True, color='blue')
plt.show()

# 등분산성 검정
from scipy.stats import levene, bartlett
print('등분산성 : ',levene( score1, score2).pvalue) # pvalue=0.4568
# [판정] p-value(0.4568) > 0.05 이므로 등분산성을 만족함.

# 독립표본 t-검정 수행
result = stats.ttest_ind(score1, score2, equal_var=True)
print(f"t-통계량: {result.statistic:.4f}")
print(f"p-value: {result.pvalue:.4f}")

# [최종 판정] 유의수준 0.05 기준
# 판정: p >= 0.05 이므로 귀무가설 채택. 두가지 교육 방법에 따른 시험점수 평균에 차이가 없다.