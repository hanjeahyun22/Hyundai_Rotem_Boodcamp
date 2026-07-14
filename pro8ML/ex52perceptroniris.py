"""
Perceptron(퍼셉트론) - Iris 데이터 분류 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 정의 (Definition): 
    - 프랑크 로젠블라트가 제안한 초기 형태의 인공 신경망 구조
    - 입력 값에 가중치를 곱한 합이 임계치를 넘으면 신호를 출력하는 이진 분류기 기반 알고리즘

2. 주요 특징 (Key Features):
    - 선형 결정 경계를 사용하여 데이터를 분류함
    - 학습률(eta0)과 반복 횟수(max_iter)를 통해 가중치 업데이트 강도를 조절함

3. 한계:
    - 선형 분리가 불가능한 데이터셋에 대해서는 수렴하지 못하거나 성능이 낮을 수 있음
--------------------------------------------------------------------------------------------------------------------------------
"""

"""
[주요 하이퍼파라미터 설명]
- max_iter: 학습 반복 횟수 (Epoch)
- eta0: 학습률 (Learning Rate)
"""

# [STEP 0] 환경 설정 및 라이브러리 임포트
# brest_cancer dataset
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
import warnings ; warnings.filterwarnings('ignore')
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 (Iris)")
print("="*60)

data = load_iris()
x = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print(f"데이터 크기: {x.shape}")
print("레이블 분포 : \n", {name:(y==i).sum() for i, name in enumerate(data.target_names)})

# =========================================================================
# [STEP 2] 데이터 분할 (Train 8 : Test 2)
# =========================================================================
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)

# 퍼셉트론은 거리/선형 기반 모델이므로 스케일링 권장
sc = StandardScaler()
x_train_std = sc.fit_transform(x_train)
x_test_std = sc.transform(x_test)

# =========================================================================
# [STEP 3] 모델 생성 및 학습
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] Perceptron 모델 학습")
print("="*60)

model = Perceptron(max_iter=1000, eta0=0.1, random_state=0)
model.fit(x_train_std, y_train)

print("Perceptron 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 비교 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가 결과")
print("="*60)

pred = model.predict(x_test_std)

print(f"[Perceptron] 정확도 : {accuracy_score(y_test, pred):.4f}")
print("\n상세 분류 보고서:")
print(classification_report(y_test, pred))

# =========================================================================
# [STEP 5] 가중치(Weights) 및 편향(Bias) 확인
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] 모델 파라미터 확인")
print("="*60)
print(f"최종 가중치(Weights):\n{model.coef_}")
print(f"최종 편향(Bias): {model.intercept_}")
print("="*60)

# =========================================================================
# [STEP 6] 최종 결정 식(Decision Function) 출력 및 시각화
# =========================================================================
print("\n" + "="*60)
print("[STEP 6] 모델의 최종 수식 및 시각화")
print("="*60)

# 다중 클래스 분류이므로 각 클래스별로 식이 생성됨
features = data.feature_names
for i, name in enumerate(data.target_names):
    w = model.coef_[i]
    b = model.intercept_[i]  # intercept_는 클래스별로 1차원 배열 형태임
    equation = f"y_{name} = " + " + ".join([f"({w[j]:.3f} * {features[j]})" for j in range(len(features))]) + f" + ({b:.3f})"
    print(f"[{name} 결정 식]\n{equation}\n")

# 예측 결과 시각화 (실제값 vs 예측값)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual', alpha=0.5)
plt.scatter(range(len(pred)), pred, color='red', marker='x', label='Predicted', alpha=0.5)
plt.title("Actual vs Predicted Labels")
plt.legend()

plt.subplot(1, 2, 2)
sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt='d', cmap='Blues', 
            xticklabels=data.target_names, yticklabels=data.target_names)
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()