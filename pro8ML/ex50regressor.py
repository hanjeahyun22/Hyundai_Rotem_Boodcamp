"""
Scikit-learn 제공 Regressor 성능 비교 실습
---------------------------------------------------------------------------------------------------
1. 개요: 다양한 회귀 알고리즘(Linear, RF, XGB, SVR, KNN)의 성능을 동일한 조건에서 비교
2. 주요 기법:
    - Pipeline: 데이터 스케일링과 모델 학습 과정을 하나로 묶어 관리
    - GridSearchCV: 각 모델별 최적의 하이퍼파라미터를 탐색
    - 교차 검증(Cross Validation): 데이터 편향을 방지하고 일반화 성능 측정
---------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
import seaborn as sns

# =========================================================================
# [STEP 1] 데이터 로드 및 분할 (Diabetes Dataset)
# =========================================================================
print("="*70)
print("[STEP 1] 데이터 로드 및 학습/테스트 세트 분리")
print("="*60)

data = load_diabetes()
x = data.data
y = data.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
print(f"학습 데이터 크기: {x_train.shape}, 테스트 데이터 크기: {x_test.shape}")

# =========================================================================
# [STEP 2] 모델별 파이프라인 및 하이퍼파라미터 설정
# -------------------------------------------------------------------------
# - Pipeline: StandardScaler를 포함하여 거리 기반 모델(SVR, KNN)의 성능 보장
# - param: GridSearchCV에서 탐색할 파라미터 그리드 정의
# =========================================================================
print("\n" + "="*70)
print("[STEP 2] 모델별 파이프라인 및 하이퍼파라미터 딕셔너리 구성")
print("="*60)

models = {
    # 1. LinearRegression (선형 회귀)
    # - 특징: 종속 변수와 하나 이상의 독립 변수 간의 선형 상관관계를 모델링함.
    # - 장점: 모델이 직관적이며 예측 속도가 매우 빠르고, 계수(Coefficient)를 통해 변수의 영향력을 파악하기 쉬움.
    # - 단점: 데이터가 비선형 구조일 경우 성능이 떨어지며, 이상치(Outlier)에 민감하게 반응함.
    # - 필수 전처리: 특성 간의 단위가 다를 경우 StandardScaler 등을 통한 스케일링이 권장됨.
    "LinearRegression": {
        "pipiline": Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())]),
        "param": {
            "model__fit_intercept": [True, False] # 절편 사용 여부
        }
    },

    # 2. RandomForestRegressor (랜덤 포레스트 회귀)
    # - 특징: 여러 개의 의사결정나무를 독립적으로 학습시킨 후 그 결과의 평균을 취하는 배깅(Bagging) 방식의 앙상블 모델.
    # - 장점: 무작위성을 통해 과적합을 효과적으로 방지하며, 데이터의 스케일에 영향을 거의 받지 않아 전처리가 간소함.
    # - 단점: 트리의 개수가 많아질수록 모델의 크기가 커지고 예측 속도가 느려질 수 있음.
    # - 주요 파라미터: n_estimators(나무 개수), max_depth(최대 깊이) 등을 통해 복잡도 조절.
    "RandomForest": {
        "pipiline": Pipeline([("model", RandomForestRegressor(random_state=42))]),
        "param": {
            "model__n_estimators": [100, 200],      # 결정 트리 개수
            "model__max_depth": [None, 5, 10],      # 트리 최대 깊이
            "model__min_samples_split": [2, 5]      # 노드 분할 최소 샘플 수
        }
    },

    # 3. XGBoostRegressor (eXtreme Gradient Boosting)
    # - 특징: 이전 트리의 오차를 다음 트리가 보완하는 부스팅(Boosting) 알고리즘을 병렬 처리가 가능하도록 최적화함.
    # - 장점: 규제(L1, L2)를 포함하여 과적합 방지 능력이 뛰어나며, 정교한 하이퍼파라미터 튜닝을 통해 최상급의 성능을 도출함.
    # - 단점: 파라미터가 많아 튜닝이 까다롭고, 학습 데이터가 적을 경우 과적합 위험이 있음.
    # - 핵심 원리: 잔차(Residual)를 줄여나가는 방향으로 순차적으로 학습함.
    "XGBoost": {
        "pipiline": Pipeline([("model", XGBRegressor(random_state=42, verbosity=0))]),
        "param": {
            "model__n_estimators": [100, 200],      # 부스팅 반복 횟수
            "model__learning_rate": [0.01, 0.05],   # 학습률
            "model__max_depth": [3, 5]              # 트리 깊이
        }
    },

    # 4. SVR (Support Vector Regression)
    # - 특징: 데이터 포인트들이 결정 경계 내의 마진(Margin) 안에 최대한 많이 들어오도록 학습하는 서포트 벡터 머신의 회귀 버전.
    # - 장점: 커널 트릭(Kernel Trick)을 사용하여 복잡한 비선형 관계를 효과적으로 학습할 수 있음.
    # - 단점: 데이터셋이 커질수록 학습 시간이 기하급수적으로 증가하며, C와 Gamma 파라미터에 매우 민감함.
    # - 필수 전처리: 거리 기반 알고리즘이므로 반드시 표준화(StandardScaler)를 수행해야 함.
    "SVR": {
        "pipiline": Pipeline([("scaler", StandardScaler()), ("model", SVR())]),
        "param": {
            "model__C": [0.1, 1, 10],               # 규제 강도
            "model__gamma": ["scale", "auto"],      # 커널 계수
            "model__kernel": ["rbf"]                # 커널 종류
        }
    },

    # 5. KNeighborsRegressor (K-최근접 이웃 회귀)
    # - 특징: 새로운 데이터와 가장 가까운 K개의 학습 데이터를 찾아 그들의 평균값(또는 가중 평균)으로 값을 예측함.
    # - 장점: 모델이 매우 단순하며 데이터의 분포를 가정하지 않는 비모수적(Non-parametric) 모델임.
    # - 단점: 데이터가 많아지면 검색 속도가 느려지고, 차원이 높아질수록 성능이 급격히 저하됨(차원의 저주).
    # - 필수 전처리: 변수 간의 거리 계산이 핵심이므로 스케일링이 필수적임.
    "KNN": {
        "pipiline": Pipeline([("scaler", StandardScaler()), ("model", KNeighborsRegressor())]),
        "param": {
            "model__n_neighbors": [3, 5, 7],        # 이웃의 수
            "model__weights": ["uniform", "distance"] # 가중치 방식
        }
    }
}

# =========================================================================
# [STEP 3] GridSearchCV를 이용한 모델별 최적화 및 학습
# -------------------------------------------------------------------------
# - 각 모델별로 정의된 파라미터 그리드를 사용하여 5-Fold 교차 검증 수행
# - R2 Score(결정 계수)를 기준으로 최적의 파라미터 조합을 탐색
# =========================================================================
print("\n" + "="*70)
print("[STEP 3] 모델별 하이퍼파라미터 튜닝 및 성능 측정")
print("="*60)

results = []
best_models = {}

for name, config in models.items():
    print(f"[{name}] 최적 파라미터 탐색 중...")
    
    # GridSearchCV 설정
    grid = GridSearchCV(config["pipiline"], config["param"], cv=5, scoring="r2", n_jobs=-1)
    grid.fit(x_train, y_train)

    # 최적 모델 추출 및 테스트 데이터 예측
    best_model = grid.best_estimator_
    y_pred = best_model.predict(x_test)

    # 성능 지표 계산 (RMSE, R2 Score)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # 결과 저장
    results.append({
        "Model": name,
        "Best Params": grid.best_params_,
        "RMSE": rmse,
        "R2 Score": r2
    })
    best_models[name] = best_model # 추후 사용을 위해 모델 객체 저장

print("\n" + "="*70)
print("[STEP 4] 모델별 최종 성능 비교 결과")
print("="*60)

df_results = pd.DataFrame(results, columns=["Model", "RMSE", "R2 Score"])
df_results = df_results.sort_values(by="R2 Score", ascending=False)
print("[최종 성능 비교]\n", df_results)
print("="*60)

# =========================================================================
# [STEP 4] 성능 지표 시각화 (R2 Score & RMSE)
# =========================================================================
plt.figure(figsize=(12, 5))

# 1. R2 Score 비교 (높을수록 좋음)
plt.subplot(1, 2, 1)
sns.barplot(x="Model", y="R2 Score", data=df_results)
plt.title("모델별 결정 계수 (R2 Score) 비교")

# 2. RMSE 비교 (낮을수록 좋음)
plt.subplot(1, 2, 2)
sns.barplot(x="Model", y="RMSE", data=df_results)
plt.title("Regression Models' RMSE Comparison")
plt.xlabel("Model")
plt.ylabel("RMSE")

plt.tight_layout()
plt.show()
plt.close()

# =========================================================================
# [STEP 5] Best Model의 Prediction 시각화
# =========================================================================

# 1. Best Model 선택
best_model_name = df_results.iloc[0]["Model"]
best_model = best_models[best_model_name]

# 2. 예측
best_pred = best_model.predict(x_test)

# 3. 시각화
plt.figure(figsize=(10, 6))
plt.scatter(y_test, best_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("True Values")
plt.ylabel("Predicted Values")
plt.title(f"Best model : {best_model_name}")
plt.show()
plt.close()