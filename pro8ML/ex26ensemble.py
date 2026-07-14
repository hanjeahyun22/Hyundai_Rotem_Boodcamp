# ================================================================================================================================
# [개념] 앙상블 학습 (Ensemble Learning) : "집단지성의 힘"
# --------------------------------------------------------------------------------------------------------------------------------
# 1. 정의: 여러 개의 분류기를 생성하고 그 예측을 결합하여 보다 정확하고 강력한 최종 예측을 도출하는 기법
# 2. 핵심 원리: 약한 모델(Weak Learner)들을 결합하여 편향과 분산을 감소시키고 일반화 성능을 극대화함
# 3. 주요 방식:
#    - 보팅(Voting)  : 서로 다른 알고리즘을 가진 분류기들의 투표 (Hard: 다수결, Soft: 확률 평균)
#    - 배깅(Bagging) : 같은 알고리즘을 사용하되 데이터를 무작위 샘플링하여 병렬 학습 (예: Random Forest)
#    - 부스팅(Boosting): 순차적 학습을 통해 앞선 모델의 오차에 가중치를 부여하여 보완 (예: XGBoost, LightGBM)
#    - 스태킹(Stacking): 여러 모델의 예측 결과를 다시 학습 데이터로 사용하여 메타 모델(Meta Model) 구축
# ================================================================================================================================

import os
os.system('cls')

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from collections import Counter
import numpy as np

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색 (Breast Cancer Dataset)
# - 위스콘신 유방암 데이터: 유방암 세포의 특징을 바탕으로 악성/양성 여부 분류
# =========================================================================
cancer = load_breast_cancer()
x, y = cancer.data, cancer.target

print(f"진단 결과 클래스(y) : {np.unique(y)} (0:악성, 1:양성)")

# 클래스별 데이터 분포 확인 (불균형 데이터 여부 체크)
counter = Counter(y)
total = sum(counter.values())
print("-" * 30)
for cls, cnt in counter.items():
    print(f"클래스 {cls}: {cnt}개 ({cnt/total*100:.2f}%)")
print()

# =========================================================================
# [STEP 2] 데이터 분할 (Train / Test Split)
# - 학습 데이터와 평가 데이터를 8:2 비율로 분리
# =========================================================================
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print(f"전체 데이터 분포 : {Counter(y)}")
print(f"학습 데이터 분포 : {Counter(y_train)}")
print(f"테스트 데이터 분포: {Counter(y_test)}")
print()

# =========================================================================
# [STEP 3] 개별 모델 생성 및 파이프라인 구축
# - LR, KNN: 거리/경사하강법 기반이므로 StandardScaler(표준화) 필수 적용
# - DT: 트리 기반 모델로 데이터 스케일에 영향을 받지 않아 단독 사용
# =========================================================================
logistic_regression = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, solver='lbfgs', random_state=12))
knn_classifier = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
decision_tree = DecisionTreeClassifier(max_depth=5, random_state=12)

# =========================================================================
# [STEP 4] 보팅(Voting) 앙상블 모델 구축
# - voting='soft': 각 분류기의 예측 확률을 평균내어 결정 (확률 기반의 정교한 판단 가능)
# =========================================================================
voting = VotingClassifier(estimators=[("LR", logistic_regression), ("KNN", knn_classifier), ("DT", decision_tree)], voting="soft")

# =========================================================================
# [STEP 5] 모델 학습 및 성능 평가
# =========================================================================
print("="*50)
print("1. 개별 모델 성능 확인")
print("-"*50)
named_models = [("LR", logistic_regression), ("KNN", knn_classifier), ("DT", decision_tree)]
for name, model in named_models:
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print(f"{name} 개별 모델 정확도: {accuracy_score(y_test, pred):.4f}")

print("\n2. 앙상블(Voting) 모델 성능 확인")
print("-"*50)
voting.fit(x_train, y_train)
v_pred = voting.predict(x_test)
print(f"★ Voting 앙상블 최종 정확도: {accuracy_score(y_test, v_pred):.4f}")

print("\n3. 교차 검증(Cross Validation)을 통한 일반화 성능 확인")
cvfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
cv_score = cross_val_score(voting, x, y, cv=cvfold, scoring="accuracy")
print(f"보팅 5-Fold CV 평균 정확도 : {cv_score.mean():.4f} (표준편차: ±{cv_score.std():.4f})")
print("="*50)

print("\n[보팅 모델 상세 평가지표]")
print(classification_report(y_test, v_pred))
print('Confusion Matrix : \n', confusion_matrix(y_test, v_pred))
print(f"ROC-AUC Score : {roc_auc_score(y_test, voting.predict_proba(x_test)[:, 1]):.4f}")
