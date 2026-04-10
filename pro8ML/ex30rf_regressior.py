"""
RandomForestRegressor (랜덤 포레스트 회귀)
--------------------------------------------------------------------------------------------------------------------------------
1. 정의: 
    - 여러 개의 의사결정나무(Decision Tree)를 생성하여 각 트리의 예측값의 '평균'을 최종 결과로 사용하는 앙상블 회귀 모델
    - 분류(Classifier)와 달리 종속변수가 연속형 숫자일 때 사용함

2. 특징:
    - 비선형 데이터 관계를 잘 포착하며, 이상치(Outlier)에 강건함
    - 과적합(Overfitting) 방지 능력이 뛰어나며, 별도의 스케일링 없이도 준수한 성능을 보임
    - RandomizedSearchCV: 모든 조합을 다 찾는 GridSearchCV와 달리, 정해진 횟수만큼 랜덤하게 파라미터를 조합하여 효율적으로 최적점을 찾음
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import randint

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 및 탐색 (California Housing)")
print("="*60)

housing = fetch_california_housing(as_frame=True)
df = housing.frame

print(df.head(3))
print(f"\n데이터 크기: {df.shape}")

# 독립변수(Feature) / 종속변수(Target) 분리
x = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# =========================================================================
# [STEP 2] 데이터 분할
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] 데이터 분할 (Train 7 : Test 3)")
print("="*60)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
print(f"Train Data: {x_train.shape}, Test Data: {x_test.shape}")

# =========================================================================
# [STEP 3] 기본 모델 생성 및 학습
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] RandomForestRegressor 모델 학습")
print("="*60)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(x_train, y_train)
print("기본 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가")
print("="*60)

y_pred = rf_model.predict(x_test)
print(f"예측값(샘플 5개): {np.round(y_pred[:5], 3)}")
print(f"실제값(샘플 5개): {np.array(y_test[:5])}")

print(f"\nMSE (평균 제곱 오차) : {mean_squared_error(y_test, y_pred):.4f}")
print(f"R2 Score (결정 계수) : {r2_score(y_test, y_pred):.4f}")

# =========================================================================
# [STEP 5] 특성 중요도 분석 및 시각화
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] 특성 중요도 분석")
print("="*60)

importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

ranking = pd.DataFrame({
    "feature": x.columns[indices],
    "importance": importances[indices]
})
print(ranking)

plt.figure(figsize=(10, 6))
sns.barplot(x="importance", y="feature", data=ranking)
plt.title("California 주택 가격 예측 주요 변수 (RF Regressor)")
plt.tight_layout()
plt.show()

# =========================================================================
# [STEP 6] 하이퍼파라미터 튜닝 (RandomizedSearchCV)
# =========================================================================
print("\n" + "="*60)
print("[STEP 6] RandomizedSearchCV를 이용한 튜닝")
print("="*60)

param_dist = {
    'n_estimators': [200, 400, 800],
    'max_depth': [None, 10, 20, 30],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2', 1.0, 0.8, 0.6]
}

rand_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    cv=3,
    scoring='r2',
    random_state=42,
    verbose=1
)

print("최적 파라미터 탐색 중...")
rand_search.fit(x_train, y_train)

print(f"최적 파라미터 : {rand_search.best_params_}")

best = rand_search.best_estimator_
print(f"최고 R2 Score : {rand_search.best_score_:.4f}")
print(f"final model : {best}")
print("="*60)
