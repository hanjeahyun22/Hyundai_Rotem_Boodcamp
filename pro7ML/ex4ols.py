# 최소제곱해를 선형 행렬 방정식으로 얻기

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

x = np.array([0, 1, 2, 3])
y = np.array([-1, 0.2, 0.5, 2.1])

plt.scatter(x, y)
plt.show()
plt.close()

A = np.vstack([x, np.ones(len(x))]).T
print(A)
print()

# 본래 데이터를 1차원 추세선으로 표현하기 위해서, 선형대수학 이용
import numpy.linalg as lin

# y = wx + b        (w : weight,  b : residual)

w, b = lin.lstsq(A, y)[0]       # 최소제곱법 연산(내부적으로 편미분)
print(w,' ', b)                 # 기울기 : 0.96,  절편 : -0.9899999999999998
print()

# 회귀식 : y_hat = 0.96x - 0.9899999999999998

print(0.96 * 0 + -0.9899999999999998)           # 실제값 : -1            # 예측값 : -0.9899999999999998
print(0.96 * 1 + -0.9899999999999998)           # 실제값 : 0.2           # 예측값 : -0.029999999999999805
print(0.96 * 2 + -0.9899999999999998)           # 실제값 : 0.5           # 예측값 : 0.9300000000000002
print(0.96 * 3 + -0.9899999999999998)           # 실제값 : 2.1           # 예측값 : 1.8900000000000001
print()

y_hat = w*x + b
print(y_hat)

plt.scatter(x, y,marker='o', label='실제값')
plt.plot(x, y_hat, '-r', label='회귀분석 추세선')
plt.grid(True)
plt.show()
plt.close()