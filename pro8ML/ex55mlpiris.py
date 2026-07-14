"""
MLP(Multi-Layer Perceptron) - Iris 데이터 분류 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요:
    - 붓꽃(Iris)의 꽃받침/꽃잎 길이와 너비 데이터를 이용해 3개 품종을 분류하는 다중 분류 문제
    - 입력층, 은닉층, 출력층으로 구성된 인공 신경망 구조를 사용함

2. 주요 특징:
    - 비선형 결정 경계를 학습할 수 있어 퍼셉트론보다 복잡한 패턴 분류에 유리함
    - 역전파(Backpropagation)와 경사하강 기반 최적화를 통해 가중치를 학습함
    - 특성 간 스케일 차이에 민감하므로 StandardScaler 전처리가 중요함

3. 주요 하이퍼파라미터:
    - hidden_layer_sizes: 은닉층 개수 및 노드 수
    - activation: 활성화 함수
    - solver: 최적화 알고리즘
    - learning_rate_init: 초기 학습률
    - max_iter: 최대 반복 횟수(Epoch)
--------------------------------------------------------------------------------------------------------------------------------
"""

# [STEP 0] 환경 설정 및 라이브러리 임포트
import os
os.system('cls')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("=" * 60)
print("[STEP 1] 데이터 로드 (Iris)")
print("=" * 60)

data = load_iris()
x = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print(f"데이터 크기: {x.shape}")
print("레이블 분포:")
print({name: (y == i).sum() for i, name in enumerate(data.target_names)})

# =========================================================================
# [STEP 2] 데이터 분할 및 스케일링
# -------------------------------------------------------------------------
# - MLP는 특성값 크기에 민감하므로 표준화가 중요함
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 2] 데이터 분할 및 표준화 스케일링")
print("=" * 60)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=12, stratify=y
)

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

print("데이터 전처리 및 스케일링 완료")

# =========================================================================
# [STEP 3] MLP 모델 생성 및 학습
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 3] MLP 모델 학습")
print("=" * 60)

model = MLPClassifier(
    hidden_layer_sizes=(50, 30),   # 은닉층 2개: 50개, 30개 노드
    activation='relu',             # 활성화 함수
    solver='adam',                 # 최적화 알고리즘
    learning_rate_init=0.001,      # 초기 학습률
    max_iter=1000,                 # 최대 학습 반복 횟수
    random_state=0,                # 결과 재현성
    verbose=True                   # 학습 과정 출력
)

model.fit(x_train_scaled, y_train)

print("MLP 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 평가
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 4] 모델 성능 평가 결과")
print("=" * 60)

pred = model.predict(x_test_scaled)

print(f"[MLP] 정확도 : {accuracy_score(y_test, pred):.4f}")
print("\n상세 분류 보고서:")
print(classification_report(y_test, pred, target_names=data.target_names))

# =========================================================================
# [STEP 5] 혼동 행렬 시각화
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 5] 혼동 행렬 시각화")
print("=" * 60)

cm = confusion_matrix(y_test, pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=data.target_names,
    yticklabels=data.target_names
)
plt.title("Iris Dataset - MLP Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# =========================================================================
# [STEP 6] 학습 손실 곡선(Loss Curve) 시각화
# -------------------------------------------------------------------------
# - model.loss_curve_ : 각 epoch마다의 손실값 저장
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 6] 학습 손실 곡선 시각화")
print("=" * 60)

plt.figure(figsize=(8, 5))
plt.plot(model.loss_curve_)
plt.title("MLP Training Loss Curve - Iris")
plt.xlabel("Iterations (Epochs)")
plt.ylabel("Loss")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"최종 손실 값(Loss): {model.loss_:.4f}")
print(f"학습 반복 횟수: {model.n_iter_}")

print("\n" + "=" * 60)
print("MLP Iris 분류 실습 종료")
print("=" * 60)

# =========================================================================
# [STEP 7] 결정 경계(Decision Boundary) 시각화
# -------------------------------------------------------------------------
# - 꽃잎 길이(petal length), 꽃잎 너비(petal width) 2개 feature만 사용
# - 모델이 실제로 어떻게 분류하는지 2D 평면에서 확인
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 7] 결정 경계 시각화 (Petal Length vs Width)")
print("=" * 60)

# 사용할 feature 선택 (index 기준)
# petal length: 2, petal width: 3
X_2d = x.iloc[:, [2, 3]].values
y_2d = y.values

# train/test split
X_train_2d, X_test_2d, y_train_2d, y_test_2d = train_test_split(
    X_2d, y_2d, test_size=0.2, random_state=12, stratify=y_2d
)

# scaling
scaler_2d = StandardScaler()
X_train_2d_scaled = scaler_2d.fit_transform(X_train_2d)
X_test_2d_scaled = scaler_2d.transform(X_test_2d)

# MLP 모델 (2D용)
model_2d = MLPClassifier(
    hidden_layer_sizes=(50, 30),
    max_iter=500,
    random_state=0
)
model_2d.fit(X_train_2d_scaled, y_train_2d)

# mesh grid 생성
x_min, x_max = X_train_2d_scaled[:, 0].min() - 1, X_train_2d_scaled[:, 0].max() + 1
y_min, y_max = X_train_2d_scaled[:, 1].min() - 1, X_train_2d_scaled[:, 1].max() + 1

xx, yy = np.meshgrid(
    np.arange(x_min, x_max, 0.02),
    np.arange(y_min, y_max, 0.02)
)

# grid 데이터 예측
Z = model_2d.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 시각화
plt.figure(figsize=(8, 6))

# decision boundary
plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Set1)

# 실제 데이터 scatter
scatter = plt.scatter(
    X_train_2d_scaled[:, 0],
    X_train_2d_scaled[:, 1],
    c=y_train_2d,
    cmap=plt.cm.Set1,
    edgecolor='k'
)

plt.xlabel("Petal Length (scaled)")
plt.ylabel("Petal Width (scaled)")
plt.title("MLP Decision Boundary (Iris - Petal Features)")

plt.legend()

plt.grid(True)
plt.show()