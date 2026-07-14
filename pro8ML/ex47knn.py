"""
KNN(K-Nearest Neighbors) 알고리즘 실습
---------------------------------------------------------------------------------------------------
1. 개요 (Overview): 
    - 새로운 데이터가 주어졌을 때, 기존 데이터 중 가장 가까운 K개의 이웃을 찾아 
      그 이웃들의 다수결(Classification)이나 평균(Regression)으로 값을 예측하는 알고리즘
    - '유유상종': 비슷한 특징을 가진 데이터들은 서로 가까이 모여 있다는 가정에 기반함

2. 주요 특징 (Key Features):
    - Instance-based Learning: 모델을 미리 생성하지 않고 데이터를 저장해 두었다가 예측 시점에 계산함
    - Lazy Learner: 학습 단계가 매우 빠르지만(단순 저장), 예측 단계에서 계산량이 많음
    - 거리 기반 알고리즘이므로 데이터 정규화(Scaling)가 성능에 큰 영향을 미침
---------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier 

# =========================================================================
# [STEP 1] 학습용 데이터 준비 (Training Data)
# -------------------------------------------------------------------------
# 3개의 특성(Feature)을 가진 3개의 샘플 데이터 생성
# =========================================================================
print("="*70)
print("[STEP 1] 학습용 데이터 및 레이블 생성")
print("="*60)

# 독립변수 (X): [특성1, 특성2, 특성3]
train = [
    [5, 3, 2],
    [1, 3, 5],
    [4, 5, 7]
]

# 종속변수 (y): 0(감소), 1(증가)
label = [0, 1, 1]

print(f"학습 데이터:\n{np.array(train)}")
print(f"레이블: {label}")

# 데이터 분포 시각화
plt.plot(train, 'o')
plt.xlim([-1, 5])
plt.ylim([0, 8])
plt.title("Training Data Distribution")
plt.show()

# =========================================================================
# [STEP 2] KNN 모델 생성 및 학습 (Modeling)
# -------------------------------------------------------------------------
# [KNeighborsClassifier 주요 파라미터 설명]
# - n_neighbors: 예측 시 고려할 최근접 이웃의 개수 (K값)
# - weights: 예측에 사용되는 가중치 함수
#   * 'uniform': 모든 이웃에 동일한 가중치 부여 (기본값)
#   * 'distance': 거리가 가까운 이웃에게 더 높은 가중치 부여
# - metric: 거리 측정 방식 (기본값 'minkowski'는 유클리드 거리와 유사)
# =========================================================================
print("\n" + "="*70)
print("[STEP 2] KNN 모델 생성 및 학습 (K=3, weights='distance')")
print("="*60)

kmodel = KNeighborsClassifier(n_neighbors=3, weights='distance')
kmodel.fit(train, label)

print("KNN 모델 학습 완료")

# =========================================================================
# [STEP 3] 새로운 데이터 예측 (Prediction)
# =========================================================================
print("\n" + "="*70)
print("[STEP 3] 새로운 데이터를 활용한 예측 테스트")
print("="*60)

new_data = [[1, 2, 9], [6, 2, 1]]
new_pred = kmodel.predict(new_data)
new_prob = kmodel.predict_proba(new_data)

print(f"새로운 데이터: {new_data}")
print(f"예측 결과: {new_pred}")
print(f"클래스별 예측 확률 (0: 감소, 1: 증가): {new_prob}")
print("="*60)
