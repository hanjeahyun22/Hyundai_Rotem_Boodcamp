"""
Perceptron(퍼셉트론) - 기초 신경망 알고리즘 실습
---------------------------------------------------------------------------------------------------
1. 개요 (Overview): 
    - 프랑크 로젠블라트가 1957년에 제안한 초기 형태의 인공 신경망
    - 다수의 신호를 입력받아 하나의 신호(0 또는 1)를 출력하는 단층 구조의 이진 분류기
    - 현대 딥러닝의 근간이 되는 '뉴런'의 수학적 모델임

2. 주요 특징 (Key Features):
    - 선형 분리가 가능한 문제(AND, OR, NAND)는 해결할 수 있으나, 비선형 문제(XOR)는 해결 불가
    - 가중치(Weight)와 편향(Bias)을 업데이트하며 학습하는 '초기 학습 규칙'을 따름
    - 틀린 데이터에 대해서만 가중치를 수정하는 방식으로 학습이 진행됨
---------------------------------------------------------------------------------------------------
3. 주요 하이퍼파라미터 (Hyperparameters):
    - max_iter: 학습 반복 횟수(Epoch). 모든 데이터를 몇 번 훑을지 결정함
    - eta0: 학습률(Learning Rate). 가중치 업데이트 시 반영할 변화의 크기
    - tol: 학습 중단 기준. 성능 개선이 이 값보다 작으면 조기 종료함
    - random_state: 데이터 셔플링 및 초기 가중치 설정을 위한 난수 시드

4. 한계점 (Limitations):
    - 선형 분리 가능(Linearly Separable)한 데이터만 완벽히 학습 가능
    - XOR 문제와 같은 비선형 데이터셋에서는 수렴하지 못하거나 성능이 저하됨
    - 이를 해결하기 위해 다층 퍼셉트론(MLP)과 역전파(Backpropagation) 알고리즘이 등장함
---------------------------------------------------------------------------------------------------
"""

"""
=========================================================================
"""

"""
=========================================================================
[핵심 요약] Perceptron의 학습 메커니즘
-------------------------------------------------------------------------
1. 학습 방식: 딥러닝의 일반적인 경사하강법(Gradient Descent)과 달리, 
    '오분류된 데이터'에 대해서만 가중치를 수정하는 'Perceptron Learning Rule'을 따름.
2. 학습 흐름: 데이터 입력 -> 예측 -> 실제값과 비교 -> 틀린 경우에만 가중치(Weight) 
    및 편향(Bias) 업데이트 -> 모든 데이터를 맞출 때까지 반복.
3. 수학적 기반: 선형 회귀식(wX + b)을 기반으로 하며, 로지스틱 회귀와 유사한 
    결정 경계 구조를 가짐. (단, 비선형 XOR 문제는 해결 불가)
4. 순전파(Forward): 입력값과 가중치의 가중합 계산 후 활성화 함수(Step Function) 적용
5. 오차 계산: 실제값과 예측값의 차이 발생 확인
6. 가중치 업데이트: 오차가 발생한 경우에만 학습률(eta0)을 적용하여 가중치와 편향 수정
7. 반복 학습: 전체 데이터에 대해 max_iter(Epoch)만큼 위 과정을 반복
=========================================================================
"""


import os
os.system('cls')

import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt


# =========================================================================
# [STEP 1] 학습용 데이터 준비 (AND, OR, XOR 논리 회로)
# -------------------------------------------------------------------------
# 각 논리 회로별 레이블 정의
# - AND: 둘 다 1일 때만 1
# - OR: 하나라도 1이면 1
# - XOR: 서로 다를 때만 1 (비선형 문제)
# - feature: [x1, x2] 형태의 입력 데이터
# =========================================================================

feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

logic_gates = {
    "AND": np.array([0, 0, 0, 1]),
    "OR":  np.array([0, 1, 1, 1]),
    "XOR": np.array([0, 1, 1, 0])
}

# =========================================================================
# [STEP 2] Perceptron 모델 생성 및 학습
# -------------------------------------------------------------------------
# [Perceptron 주요 파라미터 설명]
# - max_iter: 학습 반복 횟수 (Epoch). 데이터를 몇 번 훑을지 결정
# - tol: 학습 중단 기준 (성능 개선이 이 값보다 작으면 조기 종료)
# - eta0: 학습률 (Learning Rate). 가중치를 한 번에 얼마나 업데이트할지 결정
# - verbose: 학습 과정(가중치 업데이트 등)을 터미널에 출력
# =========================================================================

print("\n" + "="*70)
print("[STEP 2-3] 논리 게이트 학습 및 성능 평가")
print("="*60)

for name, label in logic_gates.items():
    print(f"\n--- [{name} Gate] 학습 시작 ---")
    
    # 모델 생성 및 학습
    model = Perceptron(max_iter=1000)
    model.fit(feature, label)

# =========================================================================
# [STEP 3] 예측 및 성능 평가
# =========================================================================
    pred = model.predict(feature)

    print(f"최종 가중치(Weights): {model.coef_}")
    print(f"최종 편향(Bias): {model.intercept_}")
    print("예측값 : ", pred)
    print("실제값 : ", label)
    print("정확도 : ", accuracy_score(label, pred))

    if name == "XOR" and accuracy_score(label, pred) < 1.0:
        print("※ 참고: 단층 퍼셉트론은 비선형 문제인 XOR를 해결할 수 없습니다.")
        print("   이유: 단층 퍼셉트론은 하나의 직선(선형 결정 경계)으로만 데이터를 분리할 수 있기 때문입니다.")

# =========================================================================
# [STEP 4] 일반 수치 데이터 분류 실습
# =========================================================================
"""
[이론 설명: 결정 경계(Decision Boundary)]
퍼셉트론은 w1*x1 + w2*x2 + b = 0 이라는 직선을 경계로 데이터를 분류합니다.
"""
print("\n" + "="*70)
print("[STEP 4] 일반 수치 데이터 분류 실습")
print("="*60)

x_data = np.array([[2, 3], [3, 3], [1, 1], [5, 2], [6, 1]])
y_data = np.array([1, 1, 1, -1, -1])

# 모델 생성 (eta0: 학습률 설정)
model_custom = Perceptron(max_iter=1000, eta0=0.1, random_state=42)
model_custom.fit(x_data, y_data)

# 결과 출력
pred_custom = model_custom.predict(x_data)
print(f"학습 데이터:\n{x_data}")
print(f"예측값 : {pred_custom}")
print(f"실제값 : {y_data}")
print(f"정확도 : {accuracy_score(y_data, pred_custom)}")

# 새로운 데이터 예측
new_point = [[4, 4]]
new_pred = model_custom.predict(new_point)
print(f"새로운 데이터 {new_point} 예측 결과: {new_pred}")
print("="*70)
print("Perceptron 실습 종료")

# parameter 확인
print(f"가중치(weight) : {model_custom.coef_}")
print(f"편향(bias) : {model_custom.intercept_}")

"""
[Q&A] 가중치(weight)가 [[-0.4, 0.8]]로 두 개가 나오는 이유는?
퍼셉트론의 식은 y = w1*x1 + w2*x2 + ... + wn*xn + b 입니다.
현재 실습 데이터(x_data)의 특성(Feature)이 [x1, x2]로 2개이기 때문에, 
각 입력 특성에 곱해지는 가중치도 w1(-0.4)과 w2(0.8) 두 개가 생성되는 것입니다.
"""

# 결정 경계 시각화
print("\n" + "="*70)
print("[STEP 5] 결정 경계(Decision Boundary) 시각화")
print("="*60)

plt.figure(figsize=(8, 6))
plt.scatter(x_data[:, 0], x_data[:, 1], c=y_data, cmap="bwr")
weight = model_custom.coef_[0]
bias = model_custom.intercept_[0]
x_values = np.linspace(0, 7, 100)
y_values = -(weight[0] * x_values + bias) / weight[1]
plt.plot(x_values, y_values, 'k')
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Sklearn Perceptron Decision Boundary")
plt.show()
plt.close()