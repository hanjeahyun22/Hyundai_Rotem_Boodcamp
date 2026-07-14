"""
MLP(다층 퍼셉트론) - 딥러닝의 기초 신경망 구조
--------------------------------------------------------------------------------------------------------------------------------
1. 정의 (Definition): 
    - 입력층(Input Layer)과 출력층(Output Layer) 사이에 하나 이상의 은닉층(Hidden Layer)이 존재하는 신경망
    - 단층 퍼셉트론의 한계인 비선형 분리 문제(XOR 등)를 해결하기 위해 고안됨

2. 핵심 구성 요소 (Key Components):
    - 노드(Node/Neuron): 각 층을 구성하는 기본 단위로, 가중합을 계산하고 활성화 함수를 적용함
    - 가중치(Weights) & 편향(Bias): 입력 신호의 중요도를 조절하는 파라미터
    - 활성화 함수(Activation Function): 선형 결합을 비선형 신호로 변환 (ReLU, Sigmoid, Tanh 등)

3. 학습 메커니즘 (Learning Mechanism):
    - 순전파(Forward Propagation): 입력 데이터를 층을 거쳐 출력층까지 전달하여 예측값을 계산
    - 손실 함수(Loss Function): 실제값과 예측값의 차이(오차)를 측정
    - 역전파(Backpropagation): 출력층에서 발생한 오차를 입력층 방향으로 거꾸로 전파하며 가중치를 업데이트
    - 최적화(Optimizer): 경사하강법(Gradient Descent) 등을 통해 손실을 최소화하는 가중치를 탐색

4. 주요 하이퍼파라미터 (Hyperparameters):
    - hidden_layer_sizes: 은닉층의 개수와 각 층의 노드 수를 결정 (예: (100, 50)은 2개 층)
    - activation: 은닉층에서 사용할 활성화 함수 ('relu', 'logistic', 'tanh' 등)
    - solver: 가중치 최적화를 위한 알고리즘 ('adam', 'sgd', 'lbfgs')
    - alpha: L2 규제(Regularization) 강도 (과적합 방지용)
    - learning_rate_init: 초기 학습률

5. 특징 및 한계:
    - 특징: 비선형 관계를 학습할 수 있어 복잡한 패턴 인식에 강력함
    - 한계: 하이퍼파라미터 튜닝이 까다롭고, 데이터가 적으면 과적합(Overfitting) 위험이 큼
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# logic_gates = {
#     "AND": np.array([0, 0, 0, 1]),
#     "OR":  np.array([0, 1, 1, 1]),
#     "XOR": np.array([0, 1, 1, 0])
# }

label = np.array([0, 1, 1, 0])

# =========================================================================
# [STEP 1] MLP 모델 생성 및 학습 (XOR 문제 해결)
# -------------------------------------------------------------------------
# [MLPClassifier 주요 파라미터 설명]
# - hidden_layer_sizes: 은닉층의 구조. (10,)은 10개의 노드를 가진 1개의 은닉층을 의미
# - solver: 가중치 최적화 알고리즘. 'adam'은 데이터가 많을 때, 'lbfgs'는 적을 때 유리
# - learning_rate_init: 가중치 업데이트 시 적용되는 학습률의 초기값
# - max_iter: 최대 학습 반복 횟수 (Epoch)
# - activation: 활성화 함수. 'relu'가 기본이며 비선형성을 부여함
# =========================================================================

model = MLPClassifier(
    hidden_layer_sizes=(10,), 
    solver="adam", 
    learning_rate_init=0.01, 
    max_iter=1000,
    verbose=1
).fit(feature, label)

# =========================================================================
# [STEP 2] 예측 및 결과 확인
# -------------------------------------------------------------------------
# [이론: 왜 MLP인가?]
# - 단층 퍼셉트론은 직선 하나로 데이터를 나누기 때문에 XOR를 해결할 수 없음
# - MLP는 은닉층을 통해 입력 공간을 왜곡/변환하여 비선형 결정 경계를 생성함
# - 역전파(Backpropagation)를 통해 출력층의 오차를 은닉층으로 전달하며 학습함
# - max_iter는 500~1000의 값으로 추천.
# =========================================================================

pred = model.predict(feature)

print(f"XOR 학습 결과 예측값: {pred}")
print(f"실제 정답 레이블: {label}")
print(f"최종 정확도: {accuracy_score(label, pred)}")
