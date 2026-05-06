# 비용 함수(Cost Function)는 머신러닝 모델의 예측값과 실제 정답의 차이(오차)를
# 수치화하여 모델의 성능을 평가하는 함수입니다.
# 목적은 비용 함수 값을 최소화하는 파라미터 W(weight)와 b(bias)를 찾는 것입니다.
#
# 인공 신경망은 손실 함수의 값을 줄이기 위해
# 역전파(backpropagation)로 기울기(gradient)를 계산하고,
# 경사하강법 기반 옵티마이저를 사용하여 W(weight)와 b(bias)를 갱신합니다.
# 선형회귀에서는 보통 평균제곱오차(MSE, Mean Squared Error)를 손실 함수로 사용합니다.
# MSE 수식:  cost = (1 / n) * Σ(예측값 - 실제값)^2
# PyTorch에서는 torch.mean(torch.square(pred - real)) 형태로 MSE를 직접 계산할 수 있습니다.

# 1. 비용 함수 구하기 - NumPy + math 사용
import math
import numpy as np

real = np.array([10, 9, 3, 2, 11])     # 실제값, 정답값
# pred = np.array([11, 5, 2, 4, 3])    # 모델 예측값: 실제값과 차이가 큰 경우
pred = np.array([10, 8, 3, 4, 10])     # 모델 예측값: 실제값과 차이가 작은 경우

cost = 0

for i in range(len(real)):
    cost += math.pow(pred[i] - real[i], 2)
    print(cost)

print('cost : ', cost / len(real))
# 실제값과 예측값의 차이가 작을수록 cost는 0에 가까워짐.
# 선형회귀 모델 y = Wx + b 에서는
# cost가 최소가 되도록 W(weight)와 b(bias)를 학습 과정에서 갱신.

print('\n최적의 W(weight, 가중치) 얻기의 이해 -------')
import torch
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 입력 데이터와 정답 데이터
# PyTorch 연산을 위해 list가 아니라 torch.tensor로 변환합니다.
x = torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32)
y = torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32)
b = 0   # bias는 편의상 0으로 고정.

# 선형회귀 모델 수식  :   hypothesis = W * x + b
# 비용 함수 MSE:  cost = torch.mean(torch.square(hypothesis - y))
# 여기서는 W를 자동으로 학습시키는 것이 아니라,
# W 값을 -3.0부터 4.9까지 직접 바꿔가며 각 W에서 cost가 어떻게 변하는지 확인.

# 시각화를 위한 리스트
w_val = []
cost_val = []

for i in range(-30, 50):
    feed_w = i * 0.1

    # hypothesis = W * x + b
    hypothesis = feed_w * x + b

    # MSE 비용 함수 계산
    cost = torch.mean(torch.square(hypothesis - y))

    # 그래프를 그리기 위해 Python 숫자 형태로 변환
    cost_val.append(cost.item())
    w_val.append(feed_w)

    print(f'{i}, cost:{cost.item()}, weight:{feed_w}')

# W 값에 따른 Cost 변화 시각화
plt.plot(w_val, cost_val, marker='o')
plt.xlabel('W(가중치)')
plt.ylabel('Cost(손실, 비용)')
plt.title('가중치 W 변화에 따른 비용 함수 Cost 변화')
plt.grid(True)
plt.show()