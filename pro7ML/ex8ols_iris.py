# 단순선형회귀 : iris dataset
# 상관관계가 약한 경우와 강한 경우로 회귀 분석모델을 생성 후 비교

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

iris = sns.load_dataset('iris')
print(iris.head(3))
print(type(iris)) 
#    sepal_length  sepal_width  petal_length  petal_width species
# 0           5.1          3.5           1.4          0.2  setosa
# 1           4.9          3.0           1.4          0.2  setosa
# 2           4.7          3.2           1.3          0.2  setosa
# <class 'pandas.core.frame.DataFrame'>
print(iris.iloc[:,0:4].corr())
#               sepal_length  sepal_width  petal_length  petal_width
# sepal_length      1.000000    -0.117570      0.871754     0.817941
# sepal_width      -0.117570     1.000000     -0.428440    -0.366126
# petal_length      0.871754    -0.428440      1.000000     0.962865
# petal_width       0.817941    -0.366126      0.962865     1.000000

print("\n연습1 : 상관관계가 약한 변수를 사용 -0.117570")
result1 = smf.ols(formula="sepal_length ~ sepal_width", data=iris).fit()
print(result1.summary())
print("R-squared : ", result1.rsquared)
# R-squared :  0.013822654141080859
print("p-value : ", result1.pvalues.iloc[1])
# p-value :  0.15189826071144905 > alpha 0.05 -> 이 모델은 무의미함.

# 시각화
plt.scatter(iris.sepal_width, iris.sepal_length)
plt.plot(iris.sepal_width, result1.predict(), c='r')
plt.show()


print("\n연습2 : 상관관계가 강한 변수를 사용 0.871754")
result2 = smf.ols(formula="sepal_length ~ petal_length", data=iris).fit()
print(result2.summary())
print("R-squared : ", result2.rsquared)
# R-squared :  0.7599546457725151
print("p-value : ", result2.pvalues.iloc[1])
# p-value :  1.0386674194497976e-47 < alpha 0.05 -> 이 모델은 유의미함.

# 시각화
plt.scatter(iris.petal_length, iris.sepal_length)
plt.plot(iris.petal_length, result2.predict(), c='b')
plt.show()

print('실제값 : ', iris.sepal_length[:7].values)
# [5.1 4.9 4.7 4.6 5.0 5.4 4.6]
print()
print('예측값 : ', result2.predict()[:7])
# [4.8790946  4.8790946  4.83820238 4.91998683 4.8790946  5.00177129 4.8790946 ]

# 새로운 값으로 예측
new_data = pd.DataFrame({'petal_length':[1.1, 0.5, 6.0]})
y_pred = result2.predict(new_data)
print('예측값 : ', y_pred.values)
#   [4.75641792 4.51106455 6.76013708]

print("\n연습3 : 독립변수를 복수로 사용(다중선형회귀)")
# result3 = smf.ols(formula="sepal_length ~ petal_length + petal_width", data=iris).fit()
column_select = "+".join(iris.columns.difference(['sepal_length','sepal_width','species']))   # ['sepal_width','species']을 제외한 나머지를 '+'로 묶음.
print(column_select)
result3 = smf.ols(formula="sepal_length ~ " + column_select, data=iris).fit()
print(result3.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:           sepal_length   R-squared:                       0.766
# Model:                            OLS   Adj. R-squared:                  0.763
# Method:                 Least Squares   F-statistic:                     241.0
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):           4.00e-47
# Time:                        16:41:56   Log-Likelihood:                -75.023
# No. Observations:                 150   AIC:                             156.0
# Df Residuals:                     147   BIC:                             165.1
# Df Model:                           2
# Covariance Type:            nonrobust
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# Intercept        4.1906      0.097     43.181      0.000       3.999       4.382
# petal_length     0.5418      0.069      7.820      0.000       0.405       0.679
# petal_width     -0.3196      0.160     -1.992      0.048      -0.637      -0.002
# ==============================================================================
# Omnibus:                        0.383   Durbin-Watson:                   1.826
# Prob(Omnibus):                  0.826   Jarque-Bera (JB):                0.540
# Skew:                           0.060   Prob(JB):                        0.763
# Kurtosis:                       2.732   Cond. No.                         25.3
# ==============================================================================
print("R-squared : ", result3.rsquared)
# R-squared :  0.7662612975425307
print("p-value : ", result3.pvalues.iloc[2])
# p-value :  0.04827245729290487