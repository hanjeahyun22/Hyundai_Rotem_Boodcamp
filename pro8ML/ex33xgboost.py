"""
XGBoost (eXtreme Gradient Boosting) 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - Gradient Boosting 알고리즘을 분산 환경에서 실행할 수 있도록 최적화한 라이브러리
    - Regression, Classification 문제를 모두 지원하며, 성능과 자원 효율성이 매우 뛰어남

2. 주요 특징:
    - 규제(Regularization): L1(Lasso), L2(Ridge) 규제를 통해 모델의 복잡도를 제어하고 과적합을 방지함
    - 조기 종료(Early Stopping): 검증 오차가 더 이상 개선되지 않으면 학습을 중단하여 자원 낭비 방지
    - 결측치 처리: 데이터 내 결측치를 자체적으로 처리하는 로직을 보유함

3. 데이터셋: Kaggle Santander Customer Satisfaction
    - 산탄데르 은행의 고객 만족 여부(Target 0: 만족, 1: 불만족)를 예측하는 이진 분류 문제
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xgboost import XGBClassifier, plot_importance
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import roc_auc_score
from sklearn import metrics

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 및 탐색")
print("="*60)

pd.set_option('display.max_columns', None)

df = pd.read_csv("train.csv", encoding="latin-1")
print(df.shape)
print(df.info())

# 레이블 분포 확인 (불균형 데이터 여부 체크)
print(df["TARGET"].value_counts())
unsatisfied_cnt = df["TARGET"].value_counts()[0]
total_cnt = df.TARGET.count()
print(f"불만족 비율은 {(unsatisfied_cnt/total_cnt)*100:.2f}")

# =========================================================================
# [STEP 2] 데이터 전처리 (Data Cleaning)
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] 데이터 전처리")
print("="*60)

# var3 컬럼의 이상치(-999999)를 최빈값인 2로 대체
df["var3"].replace(-999999, 2, inplace=True)
# 단순 식별자인 ID 컬럼 제거
df.drop("ID", axis=1, inplace=True)

# 피처(X)와 레이블(Y) 분리
x_features = df.iloc[:, :-1]
y_label = df.iloc[:, -1]
print("x_features shape: ", x_features.shape)
print("y_label shape: ", y_label.shape)

# =========================================================================
# [STEP 3] 데이터 분할 (Train / Test Split)
# =========================================================================
x_train, x_test, y_train, y_test = train_test_split(x_features, y_label, test_size=0.2, random_state=0)
train_cnt = y_train.count()
test_cnt = y_test.count()
print(x_train.shape, x_test.shape)
print("학습 데이터 label값 분포 비율 : ", y_train.value_counts()/train_cnt)
print("테스트 데이터 label값 분포 비율 : ", y_test.value_counts()/test_cnt)

# =========================================================================
# [STEP 4] XGBoost 모델 생성 및 학습
# -------------------------------------------------------------------------
# [주요 파라미터 설명]
# - n_estimators: 생성할 결정 트리의 개수
# - random_state: 결과 재현을 위한 난수 시드
# - early_stopping_rounds: 설정한 횟수 동안 성능 개선이 없으면 학습 중단
# - eval_set: 조기 종료를 판단하기 위한 검증 데이터셋
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] XGBoost 모델 학습")
print("="*60)

xgb_clf = XGBClassifier(n_estimators=5, random_state=12,  eval_metric="auc", eval_set=[(x_train, y_train), (x_test, y_test)])

# 학습 수행
# eval_metric: 평가 지표 (logloss: 이진 분류의 손실 함수)
xgb_clf.fit(x_train, y_train, eval_set=[(x_test, y_test)])

xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:, 1])
print(f"ROC AUC: {xgb_roc_score:.4f}")

print("XGBoost 모델 학습 완료")
print("="*60)

pred = xgb_clf.predict(x_test)
print("예측값 : ", pred[:5])
print("실제값 : ", y_test[:5].values)
print("분류 정확도 : ", metrics.accuracy_score(y_test, pred))

# =========================================================================
# [STEP 5] GridSearchCV를 이용한 하이퍼파라미터 튜닝
# -------------------------------------------------------------------------
# [주요 튜닝 파라미터 설명]
# - max_depth: 트리의 최대 깊이 (값이 클수록 모델이 복잡해지고 과적합 위험 증가)
# - min_child_weight: 관측치에 대한 가중치 합의 최솟값 (과적합 조절용)
# - colsample_bytree: 트리 생성 시 사용되는 피처의 샘플링 비율
# - learning_rate: 부스팅 스텝 반복 시 업데이트되는 학습률
# -------------------------------------------------------------------------
# [평가 지표 옵션 설명]
# - average='macro': 각 클래스의 지표를 단순 평균함 (클래스별 샘플 수 불균형을 고려하지 않음)
# - average='micro': 전체 샘플을 대상으로 지표를 계산함 (클래스별 샘플 수가 다를 때 전체적인 성능 파악에 용이)
# - average='weighted': 각 클래스의 샘플 수에 비례하여 가중 평균을 계산함
# -------------------------------------------------------------------------
# [GridSearchCV 특징]
# - 설정한 파라미터의 모든 조합을 교차 검증(CV)을 통해 평가하여 최적의 조합을 찾음
# - refit=True 설정 시 최적 파라미터로 전체 학습 데이터를 재학습함
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] 하이퍼파라미터 튜닝 (GridSearchCV)")
print("="*60)
params = {"max_depth":[5, 7], "min_child_weight":[1, 3], "colsample_bytree":[0.5, 0.75]}

grid_cv = GridSearchCV(xgb_clf, param_grid=params, cv=3, refit=True)
grid_cv.fit(x_train, y_train, eval_set=[(x_test, y_test)])

print(f"최적 파라미터: {grid_cv.best_params_}")
print(f"최고 정확도: {grid_cv.best_score_}")
print("="*60)

xgb_clf2 = XGBClassifier(n_estimators=5, random_state=12, max_depth=5, min_child_weight=3, colsample_bytree=0.5)

xgb_clf2.fit(x_train, y_train, eval_set=[(x_test, y_test)])

xgb_roc_score = roc_auc_score(y_test, xgb_clf2.predict_proba(x_test)[:, 1], average="macro")
print(f"ROC AUC: {xgb_roc_score:.4f}")

pred2 = xgb_clf2.predict(x_test)
print("예측값 : ", pred2[:5])
print("실제값 : ", y_test[:5].values)
print("분류 정확도 : ", metrics.accuracy_score(y_test, pred2))
print("="*60)

# 중요 피쳐 시각화
fig, ax = plt.subplots(figsize=(10, 8))
plot_importance(xgb_clf2, ax=ax, max_num_features=20)
plt.show()