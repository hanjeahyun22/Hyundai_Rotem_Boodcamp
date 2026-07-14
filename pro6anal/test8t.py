# [단일 모집단의 평균에 대한 가설검정 (One-sample t-test)]

# 실습 예제: A중학교 1학년 1반 학생들의 국어 점수 평균이 80점인지 검정

# 귀무가설(H0): 학생들의 국어 점수 평균은 80점이다.
# 대립가설(H1): 학생들의 국어 점수 평균은 80점이 아니다.

import numpy as np 
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv")
print(data.head())
print(data.describe())
print(f"데이터 크기: {data.shape}")  # (20, 4)
print(f"국어 점수 평균: {data['국어'].mean():.2f}")  # 72.9

# [정규성 검정]
# Shapiro-Wilk test: 데이터가 정규분포를 따르는지 확인 (표본 30개 미만 시 권장)
# 귀무가설: 해당 데이터는 정규분포를 따른다.
# 대립가설: 해당 데이터는 정규분포를 따르지 않는다.
shapiro_test = stats.shapiro(data['국어'])
print(f"Shapiro p-value: {shapiro_test.pvalue:.8f}")
# [판정] p-value(0.0129) < 0.05 이므로 정규성을 만족하지 않음

# 1. 비모수 검정 (Non-parametric test)
# 정규성을 만족하지 않거나 표본이 작을 때 사용: 윌콕슨 부호 순위 검정 (Wilcoxon signed-rank test)
wilcox_result = wilcoxon(data['국어'] - 80)
print(f"Wilcoxon: {wilcox_result}") 
# [판정] p-value(0.3978) >= 0.05 이므로 귀무가설 채택

# 2. 모수 검정 (Parametric test)
# 정규성을 만족한다고 가정할 경우: 단일표본 t-검정 (One-sample t-test)
result = stats.ttest_1samp(data['국어'], popmean=80)
print(f"t-test: {result}") 
# [판정] p-value(0.1986) >= 0.05 이므로 귀무가설 채택

# [최종 결론] 정규성은 부족하나 유의수준 0.05에서 국어 점수 평균은 80점이라고 할 수 있다.(귀무 채택)
# 표본 수가 크다면 ttest_1samp을 사용해도 된다.
# 보고서 작성 시 "shapiro-wilk" 검정 결과 정규성 가정이 다소 위배되었으나
# 비모수검정(wilcoxon) 결과도 동일하므로 ttest-1samp 결과를 신뢰할 수 있다.

print('-'*40)
# 실습 예제 2)
# 여아 신생아 몸무게의 평균 검정 수행 babyboom.csv
# 여아 신생아의 몸무게는 평균이 2800(g)으로 알려져 왔으나 이보다 더 크다는 주장이 나왔다.
# 표본으로 여아 18명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검정해 보자

# 귀무가설(H0): 여아 신생아의 몸무게 평균은 2800g이다.
# 대립가설(H1): 여아 신생아의 몸무게 평균은 2800g이 아니다. (양측 검정)
# *참고: '크다' 혹은 '작다'로 방향성을 정하면 단측 검정이 되지만, 
# 일반적으로 차이가 있는지 확인하기 위해 '아니다'로 설정하는 양측 검정을 주로 사용합니다.

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv")
print(data2.head(3))
print(data2.describe())
print()
fdata = data2[data2.gender == 1]  # 여아 데이터 추출
print(fdata, ' ',len(fdata))  # 18
print(f"여아 표본 평균: {fdata['weight'].mean():.2f}")  # 3132.44
print(f"여아 표본 평균: {fdata['weight'].std():.2f}")   # 631.58


print('-'*40)
# 단일표본 t-검정 (양측 검정)
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print(f"t-통계량: {result2.statistic:.4f}, p-value: {result2.pvalue:.4f}")
# t-통계량: 2.2332
# p-value: 0.0394
# df = 17

# [판정] 유의수준 0.05 기준
# 해석 1(p값) : p-value(0.0393) < 0.05 이므로 대립가설 채택(여아 신생아의 몸무게 평균은 2800g이 아니다.)
# 해석 2(t분포표) : t값 2.2332, df 17, alpha 0.05, cv(임계값) 1.740
#                   t 값이 cv 값 귀무 기각영역에 있으므로 귀무가설 기각

print('-'*40)
# 정규성 확인
print(f"정규성 p-value: {stats.shapiro(fdata['weight']).pvalue:.4f}")  
# [판정] p-value(0.0180) < 0.05 이므로 정규성을 만족하지 않음

# 정규성 만족여부 시각화 1
sns.displot(fdata['weight'], kde=True)
plt.xlabel('data')
plt.ylabel('value')
plt.show()

# 정규성 만족여부 시각화 2  Quantile-Quantile plot
stats.probplot(fdata['weight'], plot=plt)
plt.show()
# Q-Q plot상에서 잔차가 정규성을 만족하지 못함

print('-'*40)
# wilcoxon 비모수 검정
result3 = wilcoxon(fdata['weight'] - 2800)
print(f"Wilcoxon: {result3}")
# Wilcoxon statistic = 37.0 
# Wilcoxon p-value = 0.034233

# [판정] 유의수준 0.05 기준
# p-value(0.0342) < 0.05 이므로 귀무가설을 기각하고 대립가설을 채택한다.
# 결론: 여아 신생아의 몸무게 평균은 2800g이라고 할 수 없다. (차이가 있다)
# 비모수 검정 결과도 t-검정과 동일하게 유의미한 차이를 보임.
