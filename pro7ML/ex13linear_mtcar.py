# LinearRegression 클래스 사용 : 평가 score - mtcar dataset 사용
from sklearn.linear_model import LinearRegression
import statsmodels.api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score, mean_squared_error

mtcars = statsmodels.api.datasets.get_rdataset('mtcars').data
print(mtcars.head(3))   
print("상관계수 : \n", mtcars.corr(method='pearson'))
print()
# hp가 mpg에 영향을 주는 인과관계
x = mtcars[['hp']].values
print(x[:5])
# [[110]
#  [110]
#  [ 93]
#  [110]
#  [175]]
# => 2차원(사이킷런 유리)
y = mtcars['mpg'].values
print(y[:5])
# [21.  21.  22.8 21.4 18.7] 

# 모델생성
lmodel = LinearRegression().fit(x, y)
print('slope : ', lmodel.coef_)  # [-0.06822828]
print('intercept : ', lmodel.intercept_)  #  30.098860539622496

plt.scatter(x,y)
plt.plot(x, lmodel.coef_ * x + lmodel.intercept_, c='r')
plt.show()


# mpg 예측
pred = lmodel.predict(x)
print('예측값 : ', np.round(pred[:5],1)) #  [22.6 22.6 23.8 22.6 18.2]
print('실제값 : ', y[:5])     # [21.  21.  22.8 21.4 18.7]

# 모델 성늘 지표
# MSE : 모델 내부비교, 계산 편리(단위가 제곱한 값)
# RMSE : 보고/해석용, 해석 용이(원래 단위)
# 회귀 평가 지표는 고정된 점수 범위가 없다.(데이터 스케일에 따라 다름)
# 그래서 모델끼리 상대적인 비교를 한다.

print("MSE : ", mean_squared_error(y, pred))  # 13.9898
print("RMSE : ", np.sqrt(mean_squared_error(y, pred)))  #  3.740297
print("r2_score : ", r2_score(y, pred))  # 0.6024
# r2_score 하나만 보고 모델 판단 X (이상치에 민감, 변수가 많으면 증가.. ), 설명력만  봄.
# 모델 성능은 r2_score과 MSE 또는 r2_score와 RMSE를 사용하도록 한다.

print("새로운 hp로 mpg 예측")
new_hp = [[100],[110,],[120],[130]] # 4행 1열
new_pred = lmodel.predict(new_hp)
print('예측값 : ', np.round(new_pred.flatten(),2))
# 예측값 :   [23.28 22.59 21.91 21.23]
