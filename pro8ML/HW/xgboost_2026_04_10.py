'''
[XGBoost 문제] 
kaggle.com이 제공하는 'glass datasets'          testdata 폴더 : glass.csv
유리 식별 데이터베이스로 여러 가지 특징들에 의해 7 가지의 label(Type)로 분리된다.
RI	Na	Mg	Al	Si	K	Ca	Ba	Fe	Type

glass.csv 파일을 읽어 분류 작업을 수행하시오.
'''


import os
os.system('cls')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings ; warnings.filterwarnings('ignore')

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 (Glass Dataset)")
print("="*60)

# 데이터 로드 (경로는 환경에 맞춰 수정 가능)
df = pd.read_csv("glass.csv")

print(df.head(3))
print(f"\n데이터 크기: {df.shape}")
print("\n레이블(Type) 분포:\n", df['Type'].value_counts().sort_index())

# 독립변수(X)와 종속변수(y) 분리
X = df.drop('Type', axis=1)
y = df['Type']

# XGBoost는 레이블이 0부터 시작해야 하므로 LabelEncoding 수행
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# =========================================================================
# [STEP 2] 데이터 분할 (Train 8 : Test 2)
# =========================================================================
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# =========================================================================
# [STEP 3] XGBoost 모델 생성 및 학습
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] XGBoost 모델 학습")
print("="*60)

# 다중 분류(Multi-class) 설정을 위한 XGBClassifier
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    objective='multi:softmax',
    random_state=42,
    eval_metric='mlogloss'
)

xgb_model.fit(X_train, y_train)
print("XGBoost 모델 학습 완료")

# =========================================================================
# [STEP 4] 예측 및 성능 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가")
print("="*60)

y_pred = xgb_model.predict(X_test)

print(f"최종 정확도 : {accuracy_score(y_test, y_pred):.4f}")
print("\n상세 분류 보고서:")
# 원래 레이블 클래스 명시
print(classification_report(y_test, y_pred, target_names=[str(c) for c in le.classes_]))

print("\n혼돈 행렬(Confusion Matrix):")
print(confusion_matrix(y_test, y_pred))
print("="*60)