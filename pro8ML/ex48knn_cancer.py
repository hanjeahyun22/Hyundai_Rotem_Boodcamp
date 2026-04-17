# KNN - breast_cancer dataset 사용

import os
os.system('cls')

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib


# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 (Breast Cancer)")
print("="*60)

data = load_breast_cancer()

# feature
x = data.data

# label
y = data.target     # 0 : malignant, 1 : benign

print(x[:2], ' ', x.shape)
print(y[:2], ' ', np.unique(y))

# =========================================================================
# [STEP 2] 데이터 분할 및 스케일링 (Preprocessing)
# -------------------------------------------------------------------------
# - KNN은 거리 기반 알고리즘이므로 특성 간의 단위(Scale) 차이를 맞추는 것이 필수적임
# - StandardScaler: 평균 0, 표준편차 1로 변환하여 모든 특성이 동등한 기여를 하게 함
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] 데이터 분할 및 표준화 스케일링")
print("="*60)

# 학습용/테스트용 데이터 분리 (8:2 비율)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# 데이터 표준화 (Standardization)
# 스케일링(Scaling)은 데이터의 범위를 일정하게 맞추는 작업이며, 
# 여기서 사용하는 StandardScaler는 '표준화' 방식입니다.
# 표준화: 각 특성의 평균을 0, 분산을 1로 변경하여 데이터가 가우시안 정규 분포를 따르도록 변환합니다.
# KNN은 거리 기반 알고리즘이므로 특성 간의 단위 차이를 없애기 위해 필수적입니다.

# [fit_transform vs transform 차이]
# - fit_transform(): 학습 데이터(Train)의 평균과 표준편차를 '계산(fit)'하고 동시에 '변환(transform)'함
# - transform(): 학습 데이터에서 계산된 통계량을 그대로 사용하여 테스트 데이터(Test)를 '변환'만 함 (테스트 데이터의 정보가 모델에 유출되는 것을 방지)
scalar = StandardScaler() 
x_train_scaled = scalar.fit_transform(x_train)
x_test_scaled = scalar.transform(x_test)

print("데이터 전처리 및 스케일링 완료")

# =========================================================================
# [STEP 3] 최적의 K값 탐색 (Hyperparameter Tuning)
# -------------------------------------------------------------------------
# - n_neighbors: 예측 시 고려할 이웃의 수. 너무 작으면 과적합, 크면 과소적합 발생
# - k값의 변화에 따른 정확도 비교를 통해 모델의 일반화 성능이 가장 좋은 지점을 탐색
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] 최적의 K값(n_neighbors) 탐색 및 성능 분석")
print("="*60)

train_accuracy = []
test_accuracy = []
k_range = range(3, 12)

for k in k_range:
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(x_train_scaled, y_train)

    # 예측
    y_train_pred = knn_model.predict(x_train_scaled)
    y_test_pred = knn_model.predict(x_test_scaled)

    # 정확도 계산
    train_accuracy.append(accuracy_score(y_train, y_train_pred))
    test_accuracy.append(accuracy_score(y_test, y_test_pred))


# 시각화
plt.figure()
plt.plot(k_range, train_accuracy, marker='o', label='Train Accuracy')
plt.plot(k_range, test_accuracy, marker='s', label='Train Accuracy')
plt.xlabel("k value")
plt.ylabel("Accuracy")
plt.legend()
plt.title("K-NN accuracy comparison")
plt.grid(True)
plt.show()
plt.close()

"""
[최적의 K값 선택 근거]
1. 그래프 확인 시 k=3에서 Test Accuracy가 가장 높게 나타남.
2. 하지만 k=3은 Train Accuracy와의 격차가 커서 과적합(Overfitting)의 위험이 있음.
3. k=9 지점은 Test Accuracy가 여전히 높은 수준을 유지하면서도, 
    Train Accuracy와의 차이가 줄어들어 모델의 일반화 성능이 더 안정적이라고 판단됨.
4. 따라서 단순 정확도 수치보다 '과적합 최소화'와 '일반화'를 고려하여 k=9를 최종 선택함.
"""

print(f"단일 Test Accuracy 기준 최적 k: {k_range[np.argmax(test_accuracy)]}")

# 최종 선택된 k값 적용
besk_k = 9

final_model = KNeighborsClassifier(n_neighbors=besk_k)
final_model.fit(x_train_scaled, y_train)

# 성능 확인
y_pred = final_model.predict(x_test_scaled)
print("-" * 60)
print(f"최종 모델(k={besk_k}) 테스트 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[Confusion Matrix]")
print(confusion_matrix(y_test, y_pred))
print("-" * 60)

# 새로운 자료로 예측
new_data = x[0].copy()
new_data = new_data + np.random.normal(0, 0.1, size=new_data.shape)
new_data_scaled = scalar.transform([new_data])
new_pred = final_model.predict(new_data_scaled)
proba = final_model.predict_proba(new_data_scaled)

print("새로운 데이터 예측 결과")
print("예측 label : ", new_pred[0], "[0:악성, 1:양성]")
print("클래스별 예측 확률 : ", proba[0])
print("-" * 60)