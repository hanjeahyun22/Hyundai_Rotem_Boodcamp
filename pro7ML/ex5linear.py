# 선형 회귀 분석 (Linear Regression)
# - 독립변수(X)와 종속변수(Y) 간의 선형적 상관관계를 모델링하는 기법
# - 최소제곱법(Ordinary Least Squares, OLS)을 사용하여 잔차제곱합(RSS)을 최소화하는 회귀계수(기울기 w, 절편 b)를 추정

# - 주요 라이브러리: 
#   1. Scikit-learn: 머신러닝 모델 구축 및 예측에 최적화
#   2. Statsmodels: 통계적 유의성 검정 및 상세한 모델 요약 보고서 제공에 최적화
# - 전제 조건: 선형성, 독립성, 등분산성, 정규성

# - 주요 기능:
#   1. 모델 생성(fit): 데이터를 학습하여 최적의 회귀계수 도출
#   2. 예측(predict): 학습된 모델을 바탕으로 새로운 데이터의 결과값 추정
#   3. 평가(summary/score): 모델의 설명력(R-squared) 및 통계적 유의성 확인

# 전통적 방법의 선형회귀(기계학습 중 지도 학습)
# 각 데이터에 대한 잔차제곱합이 최소가 되는 추세선(회귀선)을 만들고,
# 이를 통해 독립변수가 종속변수에 얼마나 영향을 주는지 인과관계를 분석.
# 독립변수 : 연속형, 종속변수 : 연속형 - 두 변수는 상관관계 및 인과관계가 있어야 함.
# 정량적인 모델을 생성

import statsmodels.api as sm
import pandas as pd
from sklearn.datasets import make_regression
import numpy as np

np.random.seed(12)

# 모델 맛보기
print('\n방법1 : make_regression 사용. model 생성 X')
x, y, coef = make_regression(n_samples=50, n_features=1, bias=100 , coef=True)
print(x)
# 예측되는 x값
# [[-1.70073563]
#  [-0.67794537]
#  [ 0.31866529]
# ...
print()
print(y)  # 예측되는 y값 : [ -52.17214291   39.34130801  128.51235594  112.42316554
print()
print(coef)  # 기울기 : 89.47430739278907
# y = wx + b  => y^ = 89.47430739278907 * x + 100

y_pred = coef * -1.70073563 + 100
print('예측값 : ', y_pred)  # -52.17214255248879

xx = x
yy = y

print('\n방법2 : LinearRegression 사용. model 생성 O')
from sklearn.linear_model import LinearRegression
model = LinearRegression()
fit_model = model.fit(xx,yy)  # 최소 제곱법으로 기울기 절편을 반환
print('기울기(slope) : ', fit_model.coef_)   # 기울기 :  [89.47430739]
print('절편(bias) : ', fit_model.intercept_) # 절편 :  100.0
y_newpred = fit_model.predict(xx[[0]])
print('예측값1 : ', y_newpred)  # 예측값1 :  [-52.17214291]
y_newpred2 = fit_model.predict(np.array([[0.12345],[0.3],[0.5]]))
print('예측값2 : ', y_newpred2) # 예측값2 :  [111.04560325 126.84229222 144.7371537 ]

print('\n방법3 : ols 사용. model 생성 O')
# 잔차 제곱합(RSS)을 최소화하는 가중치 벡터를 행렬 미분으로 구하는 방법.
import statsmodels.formula.api as smf
print(xx.ndim)  # 2차원
x1 = xx.flatten()  # 차원축소   xx.ravel() -> 차원축소
print(x1.ndim)  # 1차원 # ols는 낮은 차원에서 더 유용함.
y1 = yy

data = np.array([x1,y1])
df = pd.DataFrame(data.T)
df.columns = ['x1','y1']
print(df.head(3))

model2 = smf.ols(formula="y1 ~ x1",data=df).fit()
print(model2.summary()) 
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                     y1   R-squared:                       1.000
# Model:                            OLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 1.905e+32
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):               0.00
# Time:                        11:01:18   Log-Likelihood:                 1460.6
# No. Observations:                  50   AIC:                            -2917.
# Df Residuals:                      48   BIC:                            -2913.
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    100.0000   7.33e-15   1.36e+16      0.000     100.000     100.000
# x1            89.4743   6.48e-15   1.38e+16      0.000      89.474      89.474
# ==============================================================================
# Omnibus:                        7.616   Durbin-Watson:                   1.798
# Prob(Omnibus):                  0.022   Jarque-Bera (JB):                8.746
# Skew:                           0.516   Prob(JB):                       0.0126
# Kurtosis:                       4.770   Cond. No.                         1.26
# ==============================================================================
print(model2.params['x1'])       # 89.47430739278903
print(model2.params['Intercept'])  # 99.99999999999999

new_df = pd.DataFrame({'x1': [-1.7007353, -0.67794537]})  # 기존자료 검증
print('예측값1 : ', model2.predict(new_df))
new_df2 = pd.DataFrame({'x1': [0.1234, 0.2345]})  # 새로운 자료
print('예측값2 : ', model2.predict(new_df2))

