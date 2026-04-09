# sigmoid function 적용 연습
# 로지스틱 회귀(Logistic Regression)의 핵심 원리:
# 1. 선형 결합(z = wx + b)의 결과는 (-∞, +∞) 범위를 가짐.
# 2. 이 값을 확률(0 ~ 1)로 변환하기 위해 시그모이드(Sigmoid) 함수를 사용함.
# 3. 로짓(Logit) 함수: log(p / (1 - p)) = wx + b
#    - p는 성공 확률, (1-p)는 실패 확률. p/(1-p)는 오즈(Odds, 승산비)를 의미.
#    - 오즈에 로그를 취한 것이 선형 회귀식과 같다고 정의함.
# 4. 역함수 관계: 로짓 함수의 역함수가 바로 시그모이드 함수임.

# 시그모이드 함수 수식으로 반환된 값 확인
import math
def sigmoidFunc(num):
    # f(x) = 1 / (1 + e^(-x))
    return 1 / (1 + math.exp(-num))

print(sigmoidFunc(3))  # 입력값이 클수록 1에 수렴
# 0.9525741268224334
print(sigmoidFunc(1))
# 0.7310585786300049
print(sigmoidFunc(-5))
# 0.0066928509242848554
print(sigmoidFunc(-10))
# 4.5397868702434395e-05

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

print('\n 로짓(logit) 변환된(가정) 값으로 시그모이드 함수 통과 후 그 결과를 시각화')
x = np.linspace(-10, 10, 50)  # -10부터 10까지 50개의 데이터를 생성 (입력 특성)
print(x)


# 선형결합 (Linear Combination)
w = 1.5  # 가중치(Weight): 기울기 역할을 하며 곡선의 가파른 정도를 결정
b = -2   # 편향(Bias): 절편 역할을 하며 그래프를 좌우로 이동시킴
z = w * x + b  # 결정 경계 함수 (Decision Boundary)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

p = sigmoid(z)  # 0 ~ 1 사이의 확률값(Probability)으로 변환
print('p:\n', p)


# 일부값 받기
print("x[:3](원래 값) : ", np.round(x[:3],3))
# x[:3](원래 값) :  [-10.     -9.592  -9.184]
print("z[:3](logit 변환된 값) : ", np.round(z[:3],3))
# z[:3](logit 변환된 값) :  [-17.    -16.388 -15.776]
print("p[:3](확률) : ", p[:3])
# p[:3](확률) :   [4.13993755e-08 7.63639448e-08 1.40858451e-07]


# 시각화
plt.figure(figsize=(8,5))
plt.plot(x,p, label='sigmoid(z)', color='b')
plt.axhline(0.5, color='r', linestyle='--')  # 임계값(Threshold) 0.5 선 표시
plt.title("시그모이드 함수: z = wx + b를 확률 p로 변환")
plt.xlabel("x(입력값)")
plt.ylabel("p(확률)")
plt.grid(True)
plt.legend()
plt.show()