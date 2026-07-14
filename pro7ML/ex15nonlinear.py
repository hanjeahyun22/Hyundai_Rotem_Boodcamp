# 비선형회귀(Non-linear-regression)
# : 비선형회귀란 직선의 회귀선을 곡선으로 변환해 보다 더 정확하게 데이터 변화를 예측하는 데 목적이 있다. 
# 선형가정이 어긋날 때(비정규성) 대처할 수 있는 방법으로 다항식 항을 추가한 다항회귀모델을 사용함.
# 입력 데이터 특징 변환으로 선형모델을 개선

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

x = np.array([1,2,3,4,5])
y = np.array([4,2,1,3,7])

plt.scatter(x,y)
plt.show()
print(np.corrcoef(x,y)[0,1])  # 0.48076

# 선형회귀모델 적용
from sklearn.linear_model import LinearRegression
x = x[:, np.newaxis]  # 차원 확대 : 1차원 -> 2차원
model = LinearRegression().fit(x,y)
ypred = model.predict(x)
print('예측값 : ', ypred)   # 예측값 : [2.  2.7 3.4 4.1 4.8]
print('결정계수 : ', r2_score(y,ypred))  # 0.23113207547169834

plt.scatter(x,y)
plt.plot(x, ypred, c='r')
plt.show()


# 비선회귀모델 적용
# 여러 방법 중 가장 일반적인 방법을 사용(PolynomialFeatures, log 변환, curve fit ...)
from sklearn.preprocessing import PolynomialFeatures  # 다항식 특징을 추가
poly = PolynomialFeatures(degree=2, include_bias=False)  # degree = 열 수
x2 = poly.fit_transform(x) # 특징 행렬을 만듦
print(x)  # 5행 1열
print(x2) # 5행 2열

model2 = LinearRegression().fit(x2,y)  # 특징 행렬값으로 모델을 생성
ypred2 = model2.predict(x2)
print('예측값 : ', np.round(ypred2,2))    # [4.14 1.63 1.26 3.03 6.94]
print('결정계수 : ', r2_score(y,ypred2))  # 0.9892183288409704

plt.scatter(x,y)
plt.plot(x, ypred2, c='r')
plt.show()