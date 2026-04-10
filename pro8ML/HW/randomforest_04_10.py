'''
[Randomforest 문제1] 
kaggle.com이 제공하는 'Red Wine quality' 분류 ( 0 - 10)
dataset은 winequality-red.csv 
https://www.kaggle.com/sh6147782/winequalityred?select=winequality-red.csv
Input variables (based on physicochemical tests):
    1 - fixed acidity
    2 - volatile acidity
    3 - citric acid
    4 - residual sugar
    5 - chlorides
    6 - free sulfur dioxide
    7 - total sulfur dioxide
    8 - density
    9 - pH
    10 - sulphates
    11 - alcohol
    Output variable (based on sensory data):
    12 - quality (score between 0 and 10)
'''

"""
RandomForest 분류 알고리즘 - Red Wine Quality 데이터셋
--------------------------------------------------------------------------------------------------------------------------------
1. 정의:
    - 여러 개의 의사결정나무(Decision Tree)를 결합하여 성능을 높이는 대표적인 배깅(Bagging) 방식의 앙상블 알고리즘
    - 와인의 화학적 특성을 기반으로 품질 등급(0~10점)을 예측하는 다중 분류 문제

2. RandomForest 특징:
    - 여러 개의 트리를 병렬로 학습하여 과적합을 줄임
    - 각 트리는 서로 다른 부트스트랩 샘플로 학습
    - 각 노드 분할 시 일부 특성만 무작위 선택
    - 스케일링의 영향이 거의 없으므로 StandardScaler는 생략 가능
    - feature_importances_ 속성으로 중요 변수 확인 가능

3. 주요 하이퍼파라미터:
    - n_estimators: 생성할 트리 개수
    - max_depth: 트리 최대 깊이
    - min_samples_split: 노드 분할 최소 샘플 수
    - min_samples_leaf: 리프 노드 최소 샘플 수
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 및 탐색")
print("="*60)

wine = pd.read_csv("winequality-red.csv")

print(wine.head(3))
print(f"\n데이터 크기 : {wine.shape}")
print("\n데이터 정보")
print(wine.info())

print("\n품질 등급 분포")
print(wine['quality'].value_counts().sort_index())

# 독립변수 / 종속변수 분리
x = wine.drop('quality', axis=1)
y = wine['quality']

print("\n독립변수 컬럼")
print(list(x.columns))

# =========================================================================
# [STEP 2] 학습용 / 평가용 데이터 분할
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] 데이터 분할")
print("="*60)

train_x, test_x, train_y, test_y = train_test_split(
    x,
    y,
    test_size=0.3,
    random_state=12,
    stratify=y
)

print(f"Train Data : {train_x.shape}, {train_y.shape}")
print(f"Test Data  : {test_x.shape}, {test_y.shape}")

# =========================================================================
# [STEP 3] RandomForest 모델 생성 및 하이퍼파라미터 탐색
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] RandomForest 모델 생성 및 GridSearchCV")
print("="*60)

# RandomForest 기본 모델
model = RandomForestClassifier(random_state=12)

# 하이퍼파라미터 후보
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

# 교차검증 설정
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)

# GridSearchCV
grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy',
    n_jobs=-1
)

# 모델 학습
grid.fit(train_x, train_y)

print(f"최적 파라미터 : {grid.best_params_}")
print(f"최고 교차검증 정확도 : {grid.best_score_:.4f}")

# 최적 모델 저장
best_model = grid.best_estimator_

# =========================================================================
# [STEP 4] 테스트 데이터 예측 및 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 테스트 데이터 평가")
print("="*60)

pred = best_model.predict(test_x)

print(f"예측값(샘플 10개) : {pred[:10]}")
print(f"실제값(샘플 10개) : {np.array(test_y[:10])}")

print("\n최종 테스트 정확도")
print(f"{accuracy_score(test_y, pred):.4f}")

print("\n상세 분류 보고서")
print(classification_report(test_y, pred))

# =========================================================================
# [STEP 5] 교차검증(Cross Validation)
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] 교차검증")
print("="*60)

cross_validation = cross_val_score(
    best_model,
    x,
    y,
    cv=5,
    scoring='accuracy'
)

print(f"5-Fold 교차검증 정확도 : {cross_validation}")
print(f"교차검증 평균 정확도 : {np.mean(cross_validation):.4f}")

# =========================================================================
# [STEP 6] 특성 중요도(Feature Importance) 분석
# =========================================================================
print("\n" + "="*60)
print("[STEP 6] 특성 중요도 분석")
print("="*60)

for name, value in zip(x.columns, best_model.feature_importances_):
    print(f"{name} : {value:.4f}")

feature_df = pd.DataFrame({
    'feature': x.columns,
    'importance': best_model.feature_importances_
}).sort_values(by='importance', ascending=False)

print("\n[특성 중요도 순위]")
print(feature_df)

# =========================================================================
# [STEP 7] 특성 중요도 시각화
# =========================================================================
print("\n" + "="*60)
print("[STEP 7] 특성 중요도 시각화")
print("="*60)

plt.figure(figsize=(8, 6))

sns.barplot(
    data=feature_df,
    x='importance',
    y='feature',
    orient='h'
)

plt.xlabel('특성 중요도')
plt.ylabel('변수명')
plt.title('Red Wine Quality 예측 주요 변수')
plt.tight_layout()
plt.show()