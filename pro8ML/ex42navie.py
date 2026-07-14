"""
Naive Bayes(나이브 베이즈) 분류 실습
---------------------------------------------------------------------------------------------------
1. 개요 (Overview): 
    - 베이즈 정리(Bayes' Theorem)를 기반으로 한 조건부 확률 기반의 분류 알고리즘
    - 모든 특성(Feature)들이 서로 독립적이라는 '나이브(순진한)' 가정 하에 계산을 단순화함
    - 텍스트 분류(스팸 메일 필터링) 및 실시간 예측에 매우 효율적임

2. 주요 특징 (Key Features):
    - 계산 속도가 매우 빠르고 고차원 데이터에서도 잘 작동함
    - 데이터의 양이 적어도 비교적 준수한 성능을 보임

3. 나이브 베이즈 종류 (Types):
    - GaussianNB: 연속형 변수(정규분포 가정)에 사용
    - MultinomialNB: 텍스트 데이터(단어 빈도수)에 사용
    - BernoulliNB: 이진 데이터(특성 존재 여부 0/1)에 사용
---------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import koreanize_matplotlib


# =========================================================================
# [STEP 1] 데이터 로드 및 탐색 (Data Loading)
# =========================================================================
print("="*70)
print("[STEP 1] 데이터 로드 및 탐색 (Weather Dataset: 날씨에 따른 강수 여부)")
print("="*60)

df = pd.read_csv('weather.csv')
print(f"전체 데이터 크기: {df.shape}")
print(df.head(5))

# =========================================================================
# [STEP 2] 데이터 전처리 (Data Preprocessing)
# =========================================================================
print("\n" + "="*70)
print("[STEP 2] 데이터 전처리 및 변수 분리")
print("="*60)

# 1. 불필요한 컬럼 제거 (시계열 특성인 날짜 데이터 제외)
df = df.drop("Date", axis=1)

# 2. 범주형(문자열) 데이터를 수치형으로 변환 (Yes/No -> 1/0)
df["RainToday"] = df["RainToday"].map({"Yes": 1, "No": 0})
df["RainTomorrow"] = df["RainTomorrow"].map({"Yes": 1, "No": 0})

# 3. 결측치 처리 (일조량 데이터의 결측치를 평균값으로 대체)
df["Sunshine"] = df["Sunshine"].fillna(df["Sunshine"].mean())

# 3. 독립변수(Feature)와 종속변수(Label) 분리
x = df.drop("RainTomorrow", axis=1)         # 내일 강수 여부를 제외한 나머지
y = df["RainTomorrow"]                      # 내일 강수 여부 (Target)

# 4. 학습용/테스트용 데이터 분할 (8:2 비율)
# stratify=y: 타겟 클래스의 비율을 유지하며 분할하여 편향 방지
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# =========================================================================
# [STEP 3] 모델 생성 및 학습 (Modeling)
"""
[나이브 베이즈 모델 및 GaussianNB 옵션 설명]
1. GaussianNB: 특성들이 정규 분포(가우시안 분포)를 따른다고 가정할 때 사용 (연속형 변수에 적합)
2. priors: 각 클래스의 사전 확률(Prior Probability)을 직접 지정. None이면 데이터에서 자동으로 계산
3. var_smoothing: 모든 특성의 최대 분산 부분만큼 분산에 더해지는 값. 
   - 계산 시 분모가 0이 되는 것을 방지하고, 곡선을 부드럽게 만들어 수치적 안정성을 높임 (기본값: 1e-9)
"""

# =========================================================================
print("\n" + "="*70)
print("[STEP 3] Gaussian Naive Bayes 모델 학습 및 평가")
print("="*60)

model = GaussianNB()
model.fit(x_train, y_train)

# 1. 예측 및 기본 평가
pred = model.predict(x_test)
print(f"테스트 데이터 예측값(10개): {pred[:10]}")
print(f"테스트 데이터 실제값(10개): {y_test[:10].values}")
print(f"최종 분류 정확도: {accuracy_score(y_test, pred):.4f}")

# 2. 상세 성능 지표 (Precision, Recall, F1-score)
print("\n[상세 분류 보고서]")
print(classification_report(y_test, pred))
print("\n[혼동 행렬 (Confusion Matrix)]")
print(confusion_matrix(y_test, pred))

# 3. 교차 검증 (일반화 성능 확인)
scores = cross_val_score(model, x, y, cv=5)
print(f"\n5-Fold 교차 검증 정확도: {scores}")
print(f"평균 검증 정확도: {scores.mean():.4f}")
print("="*60)


# =========================================================================
# [STEP 4] 특성 중요도 분석 (Feature Importance)
# -------------------------------------------------------------------------
# GaussianNB는 각 클래스별 특성의 평균(theta_) 차이를 통해 중요도를 유추할 수 있음
# =========================================================================
print("\n" + "="*70)
print("[STEP 4] 특성 중요도 분석 (클래스별 평균 차이 기반)")
print("="*60)

mean_0 = model.theta_[0] # 비 안 오는 날(0)의 특성 평균
mean_1 = model.theta_[1] # 비 오는 날(1)의 특성 평균

# 두 클래스 간의 평균 차이가 클수록 분류에 중요한 특성으로 판단
importance = np.abs(mean_1 - mean_0)
feature_importance = pd.DataFrame({"feature": x.columns, "importance": importance}).sort_values("importance", ascending=False)
print("[특성 중요도 순위]\n", feature_importance)

# [시각화] 특성 중요도 막대 그래프
plt.figure(figsize=(10, 5))
plt.bar(feature_importance["feature"], feature_importance["importance"], color='skyblue')
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.title("Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()
print("="*60)

# =========================================================================
# [STEP 5] 새로운 데이터 예측 (Prediction)
# =========================================================================
print("\n" + "="*70)
print("[STEP 5] 가상 데이터를 활용한 강수 예측 테스트")
print("="*60)
newdata = pd.DataFrame([{
    "MinTemp": 12.3,
    "MaxTemp": 27.0,
    "Rainfall": 0.0,
    "Sunshine": 10.0,
    "WindSpeed": 8.0,
    "Humidity": 40,
    "Pressure": 1005,
    "Cloud": 1.0,
    "Temp": 20.0,
    "RainToday": 0
}])

new_pred = model.predict(newdata)
print(f"새로운 데이터 예측 결과: {'[비 옴]' if new_pred[0] == 1 else '[비 안 옴]'}")
print(f"클래스별 예측 확률 (0: 안 옴, 1: 옴): {model.predict_proba(newdata)}")
print("="*60)