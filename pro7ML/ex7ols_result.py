# 단순선형회귀 : ols의 Regression Result의 이해

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")
print(df.head())
print(df.corr())
#           친밀도   적절성    만족도
# 친밀도  1.000000  0.499209  0.467145
# 적절성  0.499209  1.000000  0.766853
# 만족도  0.467145  0.766853  1.000000

model = smf.ols(formula="만족도 ~ 적절성", data=df).fit()
print(model.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                    만족도   R-squared:                       0.588
# Model:                            OLS   Adj. R-squared:                  0.586
# Method:                 Least Squares   F-statistic:                     374.0
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):           2.24e-52
# Time:                        14:42:07   Log-Likelihood:                -207.44
# No. Observations:                 264   AIC:                             418.9
# Df Residuals:                     262   BIC:                             426.0
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      0.7789      0.124      6.273      0.000       0.534       1.023
# 적절성         0.7393      0.038     19.340      0.000       0.664       0.815
# ==============================================================================
# Omnibus:                       11.674   Durbin-Watson:                   2.185
# Prob(Omnibus):                  0.003   Jarque-Bera (JB):               16.003
# Skew:                          -0.328   Prob(JB):                     0.000335
# Kurtosis:                       4.012   Cond. No.                         13.4
# ==============================================================================
print('parameters : ', model.params)
# parameters :  
# Intercept    0.778858
# 적절성       0.739276

# R-squared(결정계수)
# 1. 모델의 설명력을 나타냄 (0 ~ 1 사이의 값).
# 2. 종속변수(만족도)의 전체 변동성 중 독립변수(적절성)가 설명하는 비율.
# 3. 현재 모델은 약 58.8%의 설명력을 가짐을 의미함.
# 4. 1에 가까울수록 모델이 데이터를 잘 설명한다고 판단함.
print('R-squared : ', model.rsquared)
# R-squared : 0.5880630629464404


print('p-value : ', model.pvalues)
# p-value : 2.235345e-52

print('예측값 : ', model.predict()[:5])
print('실제값 : ', df.만족도[:5].values)
# 예측값 :  [3.73596305 2.99668687 3.73596305 2.25741069 2.25741069]
# 실제값 :  [3 2 4 2 2]

plt.scatter(df.적절성, df.만족도)
slope, intertcept = model.params = np.polyfit(df.적절성, df.만족도, 1)
plt.plot(df.적절성, slope * df.적절성 + intertcept, c='b')
plt.show()