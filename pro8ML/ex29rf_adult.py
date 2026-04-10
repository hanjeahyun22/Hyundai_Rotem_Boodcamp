# RandomForest 분류 알고리즘 - adult dataset (성인 소득 예측 자료)
# 연봉이 50k(약 5만 달러)이상인지 예측(이진 분류)

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline  # 전처리 + 모델 => 실행
from sklearn.compose import ColumnTransformer  # 칼럼별 전처리를 다르게 적용
from sklearn.impute import SimpleImputer   # 결측치 처리
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve

# Adult 데이터셋 불러오기
adult = fetch_openml(name="adult", version=2, as_frame=True)
print(type(adult))  # <class 'sklearn.utils._bunch.Bunch'>

df = adult.frame
print(df.head(2))
print(df.shape)  # (48842, 15)
print(df.info())

# target 변환(인코딩) : class(연봉) > 50K -> 1, <=50K -> 0
df['class'] = df['class'].apply(lambda x: 1 if x == '>50K' else 0)
print(df.head(2))
print(set(df['class']))  # {0, 1}

x = df.drop('class', axis=1)  # feature
y = df['class']
print(x.info())

# 컬럼 분리 : 숫자형, 범주형
num_cols = x.select_dtypes(include=['int64', 'float64']).columns # 숫자형
cat_cols = x.select_dtypes(include=['category','object']).columns # 범주형

# 전처리 파이프라인(숫자형) : 처리 항목들을 연결해 연속적으로 실행
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')), # 결측치 -> 중앙값
    ('scaler', StandardScaler())  # 표준화(평균: 0, 표준편차: 1)
])

# 전처리 파이프라인(범주형) : 처리 항목들을 연결해 연속적으로 실행
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')), # 결측치 -> 최빈값
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # 범주형 -> one-hot encoding
    # OneHotEncoder는 범주형 데이터를 머신러닝 모델이 이해할 수 있도록 0과 1로 구성된 벡터(원-핫 벡터)로 변환하는 기술
])

# 칼럼별 전처리 결합
# 숫자: 스캐일링, 문자: encoding -- 각각 다르게 처리해야 함.
preprocess = ColumnTransformer([
    ('num', num_pipeline, num_cols), # 숫자형 칼럼에 num_pipeline 적용
    ('cat', cat_pipeline, cat_cols)  # 범주형 칼럼에 cat_pipeline 적용
])

# 전체 파이프라인 (전처리 + 모델)
pipeline = Pipeline([
    ('prep', preprocess),  # 전처리 단계
    ('model', RandomForestClassifier(random_state=12))  # 모델 단계
])

# train / test split
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y)  # stratify : 비율 유지

# 하이퍼 파라미터 튜닝 범위 설정
param_grid = {
    'model__n_estimators': [100,200],  # tree 갯수
    'model__max_depth': [5,10, None],  # tree 깊이
    'model__class_weight': [None,'balanced']  # 클래스 불균형 보정
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)

grid = GridSearchCV(
    pipeline, # 전체 파이프라인 사용
    param_grid, # 탐색할 파라미터
    cv=cv, # 교차검증
    scoring='roc_auc', # 평가기준
    n_jobs= -1  # 모든 cpu 사용
)

grid.fit(train_x, train_y)  # 전처리 + 최적의 파라미터 탐색 + 학습 수행 
print('best_params : ', grid.best_params_)
print('best model : ', grid.best_estimator_)

# 예측 
pred = grid.predict(test_x)
proba = grid.predict_proba(test_x)[:,1]  # 클래스 1에 대한 확률값

# 평가
print('정확도 : ', accuracy_score(test_y, pred))
print('roc_auc score : ', roc_auc_score(test_y, proba))
print('classification_report : \n',classification_report(test_y, pred))