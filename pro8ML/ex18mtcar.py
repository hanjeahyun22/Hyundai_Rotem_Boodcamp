# 로지스틱 회귀 (Logistic Regression)
# - 선형 결합의 결과를 로짓(Logit) 변환을 통해 확률(0~1)로 변환하여 분류를 수행하는 알고리즘
# - 종속변수가 범주형(이항/다항)일 때 사용하며, 신경망(ANN)의 기본 단위인 퍼셉트론의 핵심 원리임
# - 독립변수: 연속형 / 종속변수: 범주형(예: 0 또는 1)

# mtcars dataset 사용
import statsmodels.api as sm

mtcars = sm.datasets.get_rdataset('mtcars')
print(mtcars.keys())    
# ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
mtcars = sm.datasets.get_rdataset('mtcars').data
print(mtcars.head(3))
print(mtcars.info())

# 연비와 마력 수에 따른 변속기 분류(수동 자동)
mtcar = mtcars.loc[:,['mpg', 'hp', 'am']] 
print(mtcar.head(2))
print(mtcar['am'].unique()) # [1(수동), 0(자동)]

# 모델 작성 방법1 : logit()
import numpy as np
import statsmodels.formula.api as smf
formula='am ~ mpg + hp'
result = smf.logit(formula=formula, data=mtcar).fit()
print(result.summary())
#                            Logit Regression Results
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32
# Model:                          Logit   Df Residuals:                       29
# Method:                           MLE   Df Model:                            2
# Date:                Tue, 07 Apr 2026   Pseudo R-squ.:                  0.5551
# Time:                        15:43:49   Log-Likelihood:                -9.6163
# converged:                       True   LL-Null:                       -21.615
# Covariance Type:            nonrobust   LLR p-value:                 6.153e-06
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -33.6052     15.077     -2.229      0.026     -63.156      -4.055
# mpg            1.2596      0.567      2.220      0.026       0.147       2.372
# hp             0.0550      0.027      2.045      0.041       0.002       0.108
# ==============================================================================

# 예측값
# print('예측값 : ', result.predict())
pred = result.predict(mtcar[:10])
print('예측값 : ', np.round(pred.values,3))
# 예측값 :  [0.25  0.25  0.558 0.356 0.397 0.007 0.108 0.632 0.585 0.066]
print('실제값 : ', mtcar['am'][:10].values)
print('예측값 : ', np.around(pred.values)) # np.around() 0.5를 기준으로 0과 1로 나뉨.
# 실제값 :  [1  1  1  0  0  0  0  0  0  0]
# 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.]
print()
print('수치에 대한 집계표(confusion matrix, 혼돈행렬) 확인 ---')
conf_tab = result.pred_table()
print(conf_tab)
# [[16.  3.]
#  [ 3. 10.]]

# 혼돈 행렬(Confusion Matrix) 해석:
# [[TN, FP]
#  [FN, TP]]
# - TN(True Negative): 0을 0으로 맞춘 경우 (16개)
# - FP(False Positive): 0을 1로 틀린 경우 (3개)
# - FN(False Negative): 1을 0으로 틀린 경우 (3개)
# - TP(True Positive): 1을 1로 맞춘 경우 (10개)

# 현재 모델의 분류 정확도
accuracy = (conf_tab[0, 0] + conf_tab[1, 1]) / len(mtcar)
print('분류 정확도(Accuracy):', accuracy) # (16 + 10) / 32 = 0.8125

# 모듈로 확인 2 - confusion matrix 이용
from sklearn.metrics import accuracy_score
pred2 = result.predict(mtcar)
print('분류 정확도(Accuracy):', accuracy_score(mtcar['am'], np.around(pred2)))


print('-'*40)
# 모델 작성 방법 2 : glm() - 일반화된 선형모델
result2 = smf.glm(formula=formula, data=mtcar, family=sm.families.Binomial()).fit()
# Binomial() : 이항분포 , Gaucian() : 정규분포
print(result2.summary())

glm_pred = result2.predict(mtcar[:10])
print('실제값 : ', mtcar['am'][:10].values)
print('예측값 : ', np.around(glm_pred.values))
# 실제값 :  [1 1 1 0 0 0 0 0 0 0]
# 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.]

glm_pred2 = result2.predict(mtcar)
print('분류 정확도(Accuracy):', accuracy_score(mtcar['am'], np.around(glm_pred2)))
# 분류 정확도(Accuracy): 0.8125

# logit()은 변환 함수, glm()은 logit()을 포함한 전체 모델

print('새로운 값으로 분류 ----')
import pandas as pd
new_df = pd.DataFrame()
new_df['mpg'] = [10, 30, 120, 200]
new_df['hp'] = [100, 110, 80, 130]
print(new_df)
new_pred = result.predict(new_df)
# print('예측값 : ', np.around(new_pred.values))
print('예측값 : ', np.rint(new_pred.values))  # np.rint() 반올림
# 예측값 :  [0. 1. 1. 1.]