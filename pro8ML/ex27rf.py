"""
Bagging vs Boosting (앙상블 학습의 두 축)
--------------------------------------------------------------------------------------------------------------------------------
1. 배깅 (Bagging - Bootstrap Aggregating):
    - 원리: 전체 데이터에서 무작위 복원 추출(Bootstrap)한 여러 샘플로 모델들을 '병렬'로 학습시킨 후 결과를 집계(Voting/Average)함
    - 목적: 모델의 분산(Variance)을 줄여 과적합(Overfitting)을 방지함
    - 대표 알고리즘: Random Forest

2. 부스팅 (Boosting):
    - 원리: 여러 개의 약한 학습기(Weak Learner)를 '순차적'으로 학습시킴. 앞선 모델이 틀린 데이터에 가중치를 부여하여 다음 모델이 보완함
    - 목적: 편향(Bias)과 오차를 줄여 강력한 예측 성능을 도출함
    - 대표 알고리즘: AdaBoost, Gradient Boosting, XGBoost, LightGBM

3. 주요 차이점:
    - 배깅은 병렬 처리(속도 빠름), 부스팅은 순차 처리(성능 우수하나 과적합 위험 및 속도 느림)
--------------------------------------------------------------------------------------------------------------------------------
"""

"""
RandomForest 분류 알고리즘
--------------------------------------------------------------------------------------------------------------------------------
1. 정의: 여러 개의 의사결정나무(Decision Tree)를 결합하여 성능을 높이는 대표적인 배깅(Bagging) 방식의 앙상블 알고리즘
2. 핵심 원리:
    - 부트스트랩 샘플링(Bootstrap Sampling): 전체 데이터에서 중복을 허용하여 무작위로 데이터를 추출해 여러 개의 학습 데이터셋 생성
    - 무작위 특징 선택(Random Feature Selection): 각 노드를 분할할 때 모든 특성이 아닌 무작위로 선택된 일부 특성만을 고려하여 나무들 간의 상관관계를 줄임
3. 장점:
    - 과적합(Overfitting) 방지 효과가 탁월함
    - 데이터의 스케일에 영향을 거의 받지 않음 (StandardScaler 불필요)
    - 특성 중요도(Feature Importance)를 통해 어떤 변수가 예측에 중요한지 파악 가능
4. 주요 파라미터:
    - n_estimators: 결정 나무의 개수 (많을수록 성능이 좋아질 수 있으나 속도가 느려짐)
    - max_features: 최적의 분할을 위해 고려할 특성의 개수
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# ================================================================================================================================
# [STEP 1] 데이터 로드 및 전처리 (Data Loading & Cleaning)
# 1. 타이타닉 생존자 데이터를 로드하고 분석에 필수적인 컬럼의 결측치를 제거함
# 2. 분석에 사용할 주요 특성(객실등급, 나이, 성별) 중 결측치가 있는 행은 제거
# ================================================================================================================================
print("="*60)
print("[STEP 1] 데이터 로드 및 전처리 (Data Loading & Cleaning)")
print("="*60)
# 1. 타이타닉 생존자 데이터를 로드하고 분석에 필수적인 컬럼의 결측치를 제거함
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv")

# 2. 분석에 사용할 주요 특성(객실등급, 나이, 성별) 중 결측치가 있는 행은 제거
df = df.dropna(subset=["Pclass", "Age", "Sex"])
print(f"결측치 제거 후 데이터 크기: {df.shape}")

# 3. 독립변수(Feature)와 종속변수(Target: Survived) 분리
df_x = df[["Pclass", "Age", "Sex"]]
df_y = df["Survived"]

# ================================================================================================================================
# [STEP 2] 범주형 데이터 인코딩 및 데이터 분할
# 1. Label Encoding: 문자열('male', 'female')을 숫자로 변환 (모델 학습용)
# 2. 학습용(Train)과 평가용(Test) 데이터 분리 (8:2 비율)
# ================================================================================================================================
print("\n" + "="*60)
print("[STEP 2] 범주형 데이터 인코딩 및 데이터 분할")
print("="*60)
# 1. Label Encoding: 문자열('male', 'female')을 숫자로 변환 (모델 학습용)
encoder = LabelEncoder()
df_x.loc[:, "Sex"] = encoder.fit_transform(df_x["Sex"])  # female: 0, male: 1
print("성별 인코딩 완료 (female: 0, male: 1)")

# 2. 학습용(Train)과 평가용(Test) 데이터 분리 (8:2 비율)
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.2, random_state=42)
print(f"Train Data: {train_x.shape}, Test Data: {test_x.shape}")

# ================================================================================================================================
# [STEP 3] RandomForest 모델 생성 및 학습
# - n_estimators: 생성할 의사결정나무의 개수 (앙상블 크기)
# ================================================================================================================================
print("\n" + "="*60)
print("[STEP 3] RandomForest 모델 생성 및 학습")
print("="*60)
# n_estimators: 생성할 의사결정나무의 개수 (앙상블 크기)
model = RandomForestClassifier(criterion="gini", n_estimators=500, random_state=12)
model.fit(train_x, train_y)
print("모델 학습 완료 (n_estimators=500)")

# ================================================================================================================================
# [STEP 4] 모델 예측 및 성능 평가
# 1. 테스트 데이터를 이용한 예측
# 2. 정확도 지표 확인
# 3. 교차 검증(Cross Validation) 수행
# ================================================================================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 예측 및 성능 평가")
print("="*60)
# 1. 테스트 데이터를 이용한 예측
pred = model.predict(test_x)
print(f"예측 값(샘플 5개) : {pred[:5]}")
print(f"실제 값(샘플 5개) : {np.array(test_y[:5].values)}")
print("-" * 30)

# 2. 정확도 지표 확인
print(f"총 테스트 개수 : {len(test_y)}, 맞춘 개수 : {sum(pred == test_y)}")
print(f"최종 분류 정확도 : {accuracy_score(test_y, pred):.4f}")

# 3. 교차 검증(Cross Validation) 수행
cross_validation = cross_val_score(model, df_x, df_y, cv=5)
print(f"5-Fold 교차 검증 개별 정확도: {cross_validation}")
print(f"교차 검증 평균 정확도 : {np.round(np.mean(cross_validation), 5)}")

# ================================================================================================================================
# [STEP 5] 특성 중요도(Feature Importance) 분석
# - 어떤 변수가 생존 예측에 가장 큰 영향을 주었는지 확인 및 시각화
# ================================================================================================================================
print("\n" + "="*60)
print("[STEP 5] 특성 중요도(Feature Importance) 분석")
print("="*60)
# 어떤 변수가 생존 예측에 가장 큰 영향을 주었는지 확인
for name, value in zip(df_x.columns, model.feature_importances_):
    print(f"{name} : {value:.4f}")

# 특성 중요도 시각화
n_features = df_x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align="center")
plt.yticks(np.arange(n_features), df_x.columns)
plt.xlabel("특성 중요도")
plt.ylabel("특성")
plt.title("타이타닉 생존 예측 주요 변수")
plt.ylim([-1, n_features])
plt.show()
plt.close()

# ================================================================================================================================
# [STEP 6] 전체 변수 대상 재학습 및 중요도 분석
# 1. 분석 범위를 확장하여 더 많은 특성(Fare, SibSp, Parch 등)을 포함
# 2. 문자형 데이터(Sex) 재인코딩 및 모델 재학습 수행
# ================================================================================================================================
print("\n" + "="*60)
print("[STEP 6] 전체 변수 대상 재학습 및 중요도 분석")
print("="*60)

# 1. 확장된 독립변수(Feature) 선택 (Ticket, Cabin 등 인코딩 까다로운 변수 제외)
df_imsi = df[["Pclass", "Age", "Sex", "Fare", "SibSp", "Parch"]]
df_imsi_y = df["Survived"]

# 2. 범주형 데이터(Sex) 재인코딩
df_imsi.loc[:, "Sex"] = encoder.fit_transform(df_imsi["Sex"])

# 3. 확장된 데이터로 모델 재학습
model_all = RandomForestClassifier(n_estimators=500, random_state=12)
model_all.fit(df_imsi, df_imsi_y)

# 4. 특성 중요도 데이터프레임 생성 및 출력
importances = model_all.feature_importances_
features_df = pd.DataFrame({
    "feature": df_imsi.columns, 
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("[전체 변수별 중요도 순위]")
print(features_df)

# 5. 확장된 변수 중요도 시각화
plt.figure(figsize=(8, 5))
sns.barplot(x="importance", y="feature", data=features_df, orient="h")
plt.xlabel("특성 중요도")
plt.ylabel("특성")
plt.tight_layout()
plt.show()
print("="*60)