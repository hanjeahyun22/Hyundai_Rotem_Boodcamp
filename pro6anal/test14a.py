# ANOVA (Analysis of Variance)

# 세 개 이상의 집단 간 평균의 차이가 통계적으로 유의미한지 검정하는 방법이다.
# t-test는 두 집단 간의 평균을 비교하지만, ANOVA는 세 집단 이상의 평균을 동시에 비교할 때 사용한다.
# (여러 번의 t-test를 수행할 경우 발생하는 1종 오류의 증가를 방지하기 위함)

# [가설 설정]
# 귀무가설(H0): 모든 집단의 평균이 같다.
# 대립가설(H1): 적어도 한 집단의 평균은 다르다.

# [주요 가정]
# 1. 독립성: 각 집단의 관측치는 서로 독립적이어야 함.
# 2. 정규성: 각 집단의 데이터는 정규분포를 따라야 함.
# 3. 등분산성: 모든 집단의 분산은 동일해야 함.


# 서로 독립인 세 집단의 평균 차이 검정
# 일원분산분석(One way ANOVA)
# 실습) 세가지 교육방법을 적용하여 1개월 동안 교육받은 교육생 80명을 대상으로 실기시험을 실시.
# 독립변수(범주형) : 교육방법(한개의 요인), 방법의 종류가 3가지(그룹이 3개)
# 종속변수(연속형) : 실기 시험 평균 점수

# 귀무 : 세 가지 교육방법에 따른 실기시험 평균 점수에 차이가 없다.
# 대립 : 세 가지 교육방법 중 적어도 한 방법의 실기시험 평균 점수에 차이가 있다.

import pandas as pd
import scipy.stats as stats
from statsmodels.formula.api import ols
# [ols(Ordinary Least Squares) - 최소 제곱법 회귀]
pd.set_option('display.float_format', '{:.4f}'.format)
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/three_sample.csv")
print(data.head(3))
#    no  method  survey  score
# 0   1       1       1     72
# 1   2       3       1     87
# 2   3       2       1     78
print(data.shape)  # (80,4)
print(data.describe())

# 이상치 제거
import matplotlib.pyplot as plt
# plt.boxplot(data['score'])
# plt.show()

data = data.query('score <= 100')
print(data.shape)  # (78, 4)
print(data.describe())

# 교차표 (교육 방법 별 건수)
data2 = pd.crosstab(index=data['method'], columns='count')
data2.index = ['방법1', '방법2', '방법3']
print(data2)

data3 = pd.crosstab(data['method'], data['survey'])
data3.index = ['방법1', '방법2', '방법3']
data3.columns = ['매우만족', '불만족']
print(data3)

print('ANOVA 검정 ---')
# F 통계 값을 얻기 위해 회귀분석결과(linear model)를 사용함.
import statsmodels.api as sm
linreg = ols("data['score'] ~ data['method']", data=data).fit()  # 회귀 분석 모델 생성
result = sm.stats.anova_lm(linreg, typ=1)
print(result)

# ANOVA 검정 ---
#                 df(자유도)   sum_sq(제곱합)   mean_sq(제곱평균)  F(F값)    PR(>F)(P값)
# data['method']  1.0000          27.9809        27.9809          0.1222       0.7276
# Residual       76.0000         17398.1345     228.9228            NaN          NaN

# [최종 판정] 유의수준 0.05 기준
# p-value(0.7276) > 0.05 이므로 귀무가설을 채택한다.
# 결론: 세 가지 교육방법에 따른 실기시험 평균 점수에 유의미한 차이가 없다.
# (즉, 교육방법이 점수에 영향을 주었다고 볼 수 없다.)

f_value = result.loc["data['method']", 'F']
p_value = result.loc["data['method']", 'PR(>F)']
print('f_value : ', f_value)
print('p_value : ', p_value)


# 사후 분석(Post Hoc Analysis) 하기
# 세 기지 교육 방법에 따른 시험 점수에 차이 여부는 알려주지만
# 정확히 어느 그룹의 평균값이 의미가 있는지는 알려주지 않는다.
# 그룹 간 평균 차이를 구체적으로 알려 주지 않음
# 그러므로 그룹 간의 관계를 보기 위해 추가적인 사후분석이 필요
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(data['score'], data['method'])
print(tukResult)
# Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject  : 유의미한 차이가 없으면 False, 차이가 있다면 True
# ----------------------------------------------------
#      1      2   0.9725 0.9702 -8.9458 10.8909  False
#      1      3   1.4904 0.9363 -8.8183  11.799  False
#      2      3   0.5179 0.9918 -9.6125 10.6483  False
# ----------------------------------------------------

# Tukey HSD 결과 시각화
import matplotlib.pyplot as plt
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()
# Tukey HSD : 원래 반복 수가 동일하다는 가정하에 고아노디 ㄴ방법
# 집단 간 평균 차이를 정밀하게 확인가능
# 각 집단의 표본 수의 차이가 크면 결과의 신뢰가 떨어짐
