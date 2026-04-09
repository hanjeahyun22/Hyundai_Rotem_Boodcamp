"""
선형회귀 분석의 기본 충족 조건 5가지
1. 선형성(Linearity): 독립변수와 종속변수 간에 선형적 관계가 존재해야 함.
2. 독립성(Independence): 잔차(오차항)들 사이에 상관관계가 없어야 함 (자기상관성 부재).
3. 등분산성(Homoscedasticity): 독립변수의 모든 값에 대해 잔차의 분산이 일정해야 함.
4. 정규성(Normality): 잔차항이 평균이 0인 정규분포를 따라야 함.
5. 다중공선성 부재(No Multicollinearity): 다중회귀 시 독립변수들 간에 강한 상관관계가 없어야 함.
"""

# 선형회귀분석 모형의 적절성 선행 조건 실습
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

# 데이터 로드
advdf = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv", usecols=[1, 2, 3, 4])
print(advdf.info())
print(advdf.corr())

# 단순 선형 회귀 모델 - ols
# x : tv
# y : sales
lm = smf.ols('sales ~ tv', data=advdf).fit()
print(f"correlation coefficient : {lm.rsquared}, p-value : {lm.pvalues}, r_squared : {lm.rsquared_adj}")
print(lm.summary())
print()

# 예측
x_new = pd.DataFrame({'tv':advdf.tv[:3]})
print("실제값 : ", advdf.sales[:3].values)
print("예측값 : ", lm.predict(x_new).values)
print("직접계산 : ", lm.params.tv * 230.1 + lm.params.Intercept)

# 경험하지 않는 tv 광고비에 따른 상품 판매량
my_new = pd.DataFrame({'tv': [100, 350, 780]})
print("예측 상품 판매량 : ", lm.predict(my_new).values)
print()

# 시각화
plt.scatter(advdf.tv, advdf.sales)
plt.xlabel("tv 광고비")
plt.ylabel("상품 판매량")

y_pred = lm.predict(advdf.tv)
plt.plot(advdf.tv, y_pred, c='r')
plt.title("단순 선형 회귀 분석")
plt.show()
plt.close()

# 단순 선형 회귀 모델 적절성 선행조건(정규성, 선형성)
# 잔차(Residual) : 실제 관측값과 모델이 예측한 값이 차이
# 모델이 데이터를 얼마나 잘 설명하는지 보여주는 척도
fitted = lm.predict(advdf.tv)
residual = advdf.sales - fitted
print("실제값 : ", advdf["sales"][:5].values)
print("예측값 : ", fitted[:5].values)
print("Residual : ", residual[:5].values)
print("residual_mean : ", np.mean(residual))

print("residual의 정규성 : residual이 정규성(orthogonality)를 따르는지 확인")
from scipy import stats
stat, p = stats.normaltest(residual)
print(f"통계량 : {stat}, p-value : {p}")
print()
print("정규성 만족" if p > 0.05 else "정규성 불만족")
print()

import statsmodels.api as sm
# Q-Q plot으로 시각화
sm.qqplot(residual, line='s')
plt.title("Q-Q Plot으로 정규성 만족 확인")
plt.show()
plt.close()

print("Linearity 검정 : 독립변수의 변화에 종속변수도 변화 -> 특정 패턴 있으면 안됨")
from statsmodels.stats.diagnostic import linear_reset       # linearity 확인 모듈
reset_result = linear_reset(lm, power=2, use_f=True)
print("reset_result 결과 : ", reset_result, "p_value : ", reset_result.pvalue)
print("linearity 만족" if reset_result.pvalue > 0.05 else "linearity 위배")
print()
# linearity 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'})
plt.plot([fitted.min(), fitted.max()], [0, 0], '--', color='gray')

print("등분산성 검정 : 모든 x값에서 오차의 퍼짐이 유사해야 함.")
from statsmodels.stats.diagnostic import het_breuschpagan
# bp_test = het_breuschpagan(lm.resid, lm.model.exog)
bp_test = het_breuschpagan(residual, sm.add_constant(advdf.tv))
bp_stat, bp_p_value = bp_test[0], bp_test[1]
print(f"bp_stat : {bp_stat}, bp_p_value : {bp_p_value}")
print("등분산성 만족" if bp_p_value > 0.05 else "등분산성 위배")
print()

# Cook's distance: 개별 데이터 포인트가 회귀 모델의 추정치에 미치는 영향력을 측정
# 값이 클수록 해당 데이터가 모델 전체에 큰 영향을 주는 '이상치(Outlier)'일 가능성이 높음
# 데이터가 적을 때, 이상치가 의심스러울 때, 모델 결과가 이상하게 나올 때, ...
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
influence = OLSInfluence(lm)
cd, _ = influence.cooks_distance

# cook distance가 가장 큰 5개 확인
print(cd.sort_values(ascending=False)[:5])
print()

# cook's distance가 가장 큰(영향력이 큰) 관측치 원본 확인
print(advdf.iloc[[35, 178, 25, 175, 131]])
# 대부분 tv광고비는 매우 높으나, sales가 낮음 - 모델이 예측하기 어려운 포인트

# 시각화
fig = sm.graphics.influence_plot(lm, alpha=0.05, criterion="cooks")
plt.show()
plt.close()


print("===="*20)

# 다중 선형 회귀 모델 - ols
# x : tv, radio, newspaper
# y : sales

lm_mul = smf.ols('sales ~ tv + radio + newspaper', data=advdf).fit()
print(lm_mul.summary())
print()