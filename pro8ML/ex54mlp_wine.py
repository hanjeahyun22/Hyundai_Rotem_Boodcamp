"""
MLP(Multi-Layer Perceptron) - Wine 데이터셋 다중 분류 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - 와인의 화학 성분을 분석하여 3가지 품종(Class 0, 1, 2)으로 분류하는 다항 분류 문제
    - 입력층, 은닉층, 출력층으로 구성된 인공 신경망 구조를 활용

2. 주요 특징:
    - 비선형 결정 경계를 학습할 수 있어 복잡한 데이터 구조에 강점이 있음
    - 경사 하강법(Gradient Descent)과 역전파(Backpropagation)를 통해 가중치를 최적화함
    - 특성 간의 스케일 차이에 민감하므로 StandardScaler 등의 전처리가 필수적임

3. 주요 하이퍼파라미터:
    - hidden_layer_sizes: 은닉층의 개수와 각 층의 노드 수 설정
    - activation: 활성화 함수 (기본값 'relu')
    - solver: 가중치 최적화 알고리즘 (기본값 'adam')
    - max_iter: 최대 학습 반복 횟수 (Epoch)
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system("cls")


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 (Wine Dataset)")
print("="*60)

data = load_wine()
x = data.data
y = data.target
print(x[:2], ' ', x.shape)
print(y[:2], ' ', np.unique(y))

# =========================================================================
# [STEP 2] 데이터 분할 및 스케일링 (Preprocessing)
# -------------------------------------------------------------------------
# - MLP는 가중치 업데이트 시 특성값의 크기에 영향을 많이 받음
# - StandardScaler를 통해 평균 0, 표준편차 1로 변환하여 학습의 수렴 속도를 높임
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] 데이터 분할 및 표준화 스케일링")
print("="*60)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

scalar = StandardScaler()
x_train_scaled = scalar.fit_transform(x_train)
x_test_scaled = scalar.transform(x_test)

print("데이터 전처리 및 스케일링 완료")

# =========================================================================
# [STEP 3] MLP 모델 생성 및 학습
# -------------------------------------------------------------------------
# [MLPClassifier 옵션 설명]
# - hidden_layer_sizes=(50, 30): 
#   * 첫 번째 은닉층에 50개, 두 번째 은닉층에 30개의 노드를 배치한 2층 구조
# - solver='adam': 확률적 경사 하강법의 최적화 기법 중 하나로, 학습 속도가 빠르고 효율적임
# - max_iter: 학습 반복 횟수. 데이터가 복잡할수록 충분한 반복이 필요함
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] MLP 모델 생성 및 학습")
print("="*60)

model = MLPClassifier(
    hidden_layer_sizes=(50, 30), # 은닉층 구조: 첫 번째 층 50개, 두 번째 층 30개 노드
    activation="relu",           # 활성화 함수: 비선형성 부여 (기본값 'relu')
    solver="adam",               # 최적화 알고리즘: 가중치 업데이트 방식 (기본값 'adam')
    learning_rate_init=0.001,    # 초기 학습률: 가중치 업데이트 강도 조절
    max_iter=500,                 # 최대 학습 반복 횟수
    random_state=42,             # 결과 재현을 위한 난수 시드
    verbose=1                    # 학습 과정(Loss 등) 출력 여부
)
model.fit(x_train_scaled, y_train)

print("MLP 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가")
print("="*60)

y_pred = model.predict(x_test_scaled)

print(f"최종 분류 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[상세 분류 보고서]")
print(classification_report(y_test, y_pred, target_names=data.target_names))

# =========================================================================
# [STEP 5] 혼동 행렬(Confusion Matrix) 시각화
# =========================================================================
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))

# [sns.heatmap 옵션 설명]
# - annot=True: 각 셀에 숫자 표시
# - fmt='d': 숫자를 정수(Decimal) 형식으로 출력
# - cmap='Blues': 히트맵의 색상 팔레트 설정
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=data.target_names, yticklabels=data.target_names)
plt.title("Wine Dataset - MLP Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

"""
[성능 지표 및 혼동 행렬 상세 설명]
1. 혼동 행렬(Confusion Matrix):
    - TN(True Negative): 음성을 음성으로 맞게 예측
    - TP(True Positive): 양성을 양성으로 맞게 예측
    - FP(False Positive): 음성을 양성으로 틀리게 예측 (Type I error)
    - FN(False Negative): 양성을 음성으로 틀리게 예측 (Type II error)

2. 주요 평가지표:
    - Precision(정밀도): 모델이 Positive라고 예측한 것 중 실제 Positive인 비율 (FP를 줄이는 것이 목표)
    - Recall(재현율): 실제 Positive인 것 중 모델이 Positive라고 맞춘 비율 (FN을 줄이는 것이 목표)
    - F1-score: 정밀도와 재현율의 조화 평균 (데이터 불균형 시 유용한 지표)
    - Support: 각 클래스에 속한 실제 데이터 샘플 개수

3. 결과 분석:
    - 현재 max_iter=10으로 설정되어 학습이 충분하지 않아 class_1의 Recall(0.14)이 매우 낮게 나타남.
    - 성능 향상을 위해서는 max_iter를 늘리거나 hidden_layer_sizes를 조정해야 함.
"""

'''
최종 분류 정확도: 0.6667

[상세 분류 보고서]
                precision    recall  f1-score   support

    class_0       0.60      1.00      0.75        12
    class_1       1.00      0.14      0.25        14
    class_2       0.71      1.00      0.83        10

    accuracy                          0.67        36
    macro avg     0.77      0.71      0.61        36
    weighted avg  0.79      0.67      0.58        36
'''

# =========================================================================
# [STEP 6] 학습 손실 곡선(Loss Curve) 시각화
# -------------------------------------------------------------------------
# - model.loss_curve_: 매 반복(Epoch)마다 계산된 손실 함수(Loss)의 값
# - 그래프가 하향 곡선을 그리며 수렴하는지 확인하여 학습의 적절성을 판단함
# =========================================================================
print("\n" + "="*60)
print("[STEP 6] 학습 손실 곡선 시각화")
print("="*60)

plt.figure(figsize=(8, 5))
plt.plot(model.loss_curve_)
plt.title("MLP Training Loss Curve")
plt.xlabel("Iterations (Epochs)")
plt.ylabel("Loss")
plt.grid(True)
plt.show()

print(f"최종 손실 값(Loss): {model.loss_:.4f}")
print(f"학습 반복 횟수: {model.n_iter_}")

# 참고 : 미분이 MLP에서 어떻게 쓰이는지 -->> 미분으로 오차를 줄여감
# MLP구조 : 입력 -> 신경망(뉴런) -> 출력 후 오차 확인
# ex) 입력(x) -> 모델 -> 예측값(y_hat) -> 실제값(y) -> 오차(loss) 발생
#   오차함수(loss function) : L = (y - y_hat)
#   -> 예측값이 틀린수록 값이 커짐
# 미분을 통해 오차를 줄임 -> 오차가 줄어드는 방향으로 weight 갱신

# [MLP 전체 학습 과정]
# 1. Regression 모델링 및 예측
# 2. 오차 계산
# 3. 미분(기울기 계산)
# 4. 가중치(weight) 갱신
# 5. Back Proergation : 과정 1~4 반복

"""
[이론 정리: MLP의 학습 원리와 미분의 역할]
--------------------------------------------------------------------------------------------------------------------------------
1. MLP의 기본 구조:
    - 입력(x) -> 신경망(뉴런/가중치) -> 예측값(y_hat) 출력

2. 오차 계산 (Loss Function):
    - 예측값(y_hat)과 실제값(y)의 차이를 측정함
    - 식: L = (y - y_hat)^2 (오차가 클수록 손실 함수 값이 커짐)

3. 미분과 가중치 갱신:
    - 미분을 통해 손실 함수(L)의 기울기(Gradient)를 계산함
    - 기울기가 낮아지는 방향(오차가 줄어드는 방향)으로 가중치(Weight)를 조금씩 수정함

4. 전체 학습 프로세스 (Backpropagation):
    4-1. 순전파(Forward): 데이터를 입력하여 예측값 계산
    4-2. 오차 계산: 실제값과 비교하여 손실(Loss) 측정
    4-3. 역전파(Backward): 미분을 통해 각 층의 기울기 계산
    4-4. 가중치 업데이트: 최적화 알고리즘(Adam 등)을 사용하여 가중치 갱신
    4-5. 반복: 위 과정을 max_iter만큼 반복하여 최적의 모델 완성
--------------------------------------------------------------------------------------------------------------------------------
"""

print("\n" + "="*60)
print("MLP Wine 분류 실습 종료")
print("="*60)

