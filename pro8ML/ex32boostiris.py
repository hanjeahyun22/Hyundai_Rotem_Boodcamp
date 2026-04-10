"""
XGBoost & LightGBM (부스팅 앙상블 학습)
--------------------------------------------------------------------------------------------------------------------------------
1. 정의 (Definition): 
    - 여러 개의 약한 학습기(Weak Learner)를 순차적으로 학습시켜 앞선 모델의 오차를 보완하는 방식
    - 부스팅(Boosting)은 이전 트리의 오차를 다음 트리가 학습하는 '순차적' 구조를 가짐

2. XGBoost (eXtreme Gradient Boosting):
    - Gradient Boosting 기반으로 병렬 처리와 과적합 방지(L1, L2 규제) 기능이 강화된 모델
    - 트리 기반 알고리즘 중 성능과 자원 효율성이 뛰어나 가장 널리 사용됨

3. LightGBM (Light Gradient Boosting Machine):
    - 리프 중심 트리 분할(Leaf-wise) 방식을 사용하여 속도가 매우 빠르고 메모리 사용량이 적음
    - 대량의 데이터를 처리할 때 XGBoost보다 빠르지만, 데이터 양이 적을 경우 과적합 위험이 있음

4. 특징 (Features):
    - 성능이 매우 우수하여 캐글(Kaggle) 등 데이터 분석 경진대회에서 가장 많이 사용됨
    - 결측치를 자체적으로 처리하며, 대규모 데이터셋에서 효율적임
--------------------------------------------------------------------------------------------------------------------------------
"""

"""
[주요 하이퍼파라미터 설명]
- n_estimators: 생성할 결정 트리의 개수 (반복 횟수)
- max_depth: 트리의 최대 깊이 (과적합 제어용)
- learning_rate: 학습률 (이전 오차를 얼마나 반영할지 결정, 보통 0.01~0.2)
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
import xgboost as xgb
from lightgbm import LGBMClassifier # xgboost보다 성능은 우수하지만, 자료가 적으면 X
import warnings ; warnings.filterwarnings('ignore')
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

# =========================================================================
# [STEP 3] 모델 생성 및 학습
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] LightGBM 모델 학습")
print("="*60)

# LightGBM 모델 설정
# - boosting_type: 실행할 부스팅 알고리즘 (gbdt: 일반적인 경사 하강 결정 트리)
# - num_leaves: 하나의 트리가 가질 수 있는 최대 리프 개수 (LGBM의 핵심 파라미터)
# - verbose: 학습 과정 출력 여부 (-1은 출력 안 함)
# - n_jobs: 사용할 CPU 코어 수 (-1은 전체 사용)
lgb_clf = LGBMClassifier(boosting_type='gbdt', max_depth=6, n_estimators=100, random_state=42, verbose=-1)

lgb_clf.fit(x_train, y_train)

print("LightGBM 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 비교 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가 결과")
print("="*60)

pred_lgb = lgb_clf.predict(x_test)

print(f"[LightGBM] 정확도 : {accuracy_score(y_test, pred_lgb):.4f}")
print("\n상세 분류 보고서:")
print(classification_report(y_test, pred_lgb))

# =========================================================================
# [STEP 5] 특성 중요도(Feature Importance) 분석 및 비교
# -------------------------------------------------------------------------
# 1. Gain(이득): 해당 특성이 모델의 예측 오차를 줄이는 데 기여한 총 합계
# 2. 계산 방식: 각 모델에서 제공하는 get_score(gain) 또는 feature_importance(gain) 사용
# 3. 정규화: 각 특성의 중요도를 전체 합으로 나누어 백분율(%)로 변환하여 비교 용이성 확보
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] LightGBM 특성 중요도(Gain) 분석")
print("="*60)

# LightGBM 피처 중요도 추출 (Gain 기준)
lgb_gain = pd.Series(lgb_clf.booster_.feature_importance(importance_type='gain'), index=x.columns)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)
lgb_importance_df = lgb_gain_pct.sort_values(ascending=False)

print(lgb_importance_df)
print("="*60)

# 시각화
plt.figure(figsize=(8, 5))
sns.barplot(x=lgb_importance_df.values, y=lgb_importance_df.index)
plt.title("LightGBM Feature Importance (Gain %)")
plt.xlabel("Importance (%)")
plt.ylabel("Features")
plt.tight_layout()
plt.show()
plt.close()