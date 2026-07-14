# 독립 표본 t-검정(independent two sample t-test)
# 서로 다른 두 집단의 평균에 대한 통계 검정에 사용된다.
# 비교를 위해 평균과 표준편차 통계량을 사용한다.
# 독립변수: 범주형(두 집단), 종속변수: 연속형(수치)

# [가정]
# 1. 독립성: 두 집단은 서로 독립적이어야 함.
# 2. 정규성: 각 집단의 데이터는 정규분포를 따라야 함. (shapiro)
# 3. 등분산성: 두 집단의 분산이 동일해야 함. (levene, bartlett)

# 실습 1: 남녀 간의 성적 차이 검정
# 귀무(H0): 남녀 간의 성적 평균 차이가 없다.
# 대립(H1): 남녀 간의 성적 평균 차이가 있다.

# 실습2 : 남녀 두 집단 간 파이썬 시험의 평균 차이 검정
# 남녀의 시험 평균이 우연히 같을 확률은 얼마나 될까?
# 만약 우연히 발생했다면 평균은 같은 것이고, 우연이 아니면 평균은 다른 것이다,
# 95% 신뢰 구간에서 우연히 발생할 확률이 5% 이상이면 귀무가설 채택이다.

import pandas as pd
import scipy.stats as stats
import numpy as np

# 데이터 생성
male = [75, 85, 100, 72.5, 86.5]
female = [63.2, 76, 52, 100, 70]

print(f"남자 평균: {np.mean(male):.2f}")    # 83.80
print(f"여자 평균: {np.mean(female):.2f}")  # 72.24

# 1. 정규성 검정
print(f"남자 정규성 p-value: {stats.shapiro(male).pvalue:.4f}")    # p-value: 0.6004
print(f"여자 정규성 p-value: {stats.shapiro(female).pvalue:.4f}")  # p-value: 0.7780
# [판정] 두 집단 모두 p-value > 0.05 이므로 정규성을 만족함.
# 만약 집단의 표본 수가 30개 이상인 경우엔 정규분포를 따른다고 가정함으로 정규성 검정 안해도 된다.

# 2. 등분산성 검정 (Levene's test) : 데이터의 퍼짐 정도
# 귀무: 두 집단의 분산이 같다.
from scipy.stats import levene, bartlett
# levene : 정규분포에 덜 민감함 (데이터가 정규분포를 따르지 않아도 사용 가능)
# bartlett : 데이터가 정규분포를 따를 때 사용 (정규분포에 민감함)
levene_res = stats.levene(male, female)
print(f"등분산성 p-value: {levene_res.pvalue:.4f}")  # p-value: 0.4957
# [판정] p-value(0.4957) > 0.05 이므로 귀무가설을 채택하여 등분산성을 만족함.

# 3. 독립표본 t-검정 수행
# equal_var=True (등분산성 만족 시), equal_var=False (Welch's t-test, 만족하지 못할 시)
# t_stat, p_val = stats.ttest_ind(male, female)
t_stat, p_val = stats.ttest_ind(male, female, equal_var=True)  # equal_var=True (생략가능) : 두 집단의 분산이 같은 경우로 가정.
print(f"t-통계량: {t_stat:.4f}")  # t-통계량: 1.2332
print(f"p-value: {p_val:.4f}")    # p-value: 0.2525

# [판정] 유의수준 0.05 기준
# 결과: p >= 0.05 이므로 귀무가설 채택. 남녀 간 성적 차이가 없음.

print('-'*40)
# 참고: 만약 정규성을 만족하지 못할 경우 비모수 검정인 
# Mann-Whitney U test (stats.mannwhitneyu)를 사용한다.
m_u_stat, m_u_p = stats.mannwhitneyu(male, female)
print(f"Mann-Whitney p-value: {m_u_p:.4f}")   # Mann-Whitney p-value: 0.2492
# [판정] p-value(0.2492) >= 0.05 이므로 귀무가설을 채택한다. (남녀 간 성적 차이가 없음)