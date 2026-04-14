'''
SVM (Support Vector Machine) - 심장병(Heart Disease) 진단 분류 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - 흉부외과 환자 303명의 검진 데이터를 바탕으로 중증 심장질환(AHD) 여부를 예측하는 이진 분류 문제
    - 데이터 출처: https://www.kaggle.com/zhaoyingzhu/heartcsv

2. 주요 특징:
    - SVM의 선형 커널(Linear Kernel)을 사용하여 환자의 건강 지표와 질환 간의 결정 경계 학습
    - 결측치 제거 및 범주형 데이터의 수치화(Mapping) 과정 포함
    - 모델의 일반화 성능 확인을 위한 Train/Test 데이터 분할 및 정확도 평가
--------------------------------------------------------------------------------------------------------------------------------

데이터 구성:
- Age, Sex, RestBP(혈압), Chol(콜레스테롤), Fbs(공복혈당), RestECG(심전도), MaxHR(최대심박수) 등
- label 칼럼 : AHD (Yes: 심장질환 있음, No: 없음)

제약 사항:
feature 칼럼 : 문자 데이터(Object) 칼럼은 제외하고 수치형 데이터만 사용
label 칼럼 : AHD(중증 심장질환)

데이터 예)
"","Age","Sex","ChestPain","RestBP","Chol","Fbs","RestECG","MaxHR","ExAng","Oldpeak","Slope","Ca","Thal","AHD"
"1",63,1,"typical",145,233,1,2,150,0,2.3,3,0,"fixed","No"
"2",67,1,"asymptomatic",160,286,0,2,108,1,1.5,2,3,"normal","Yes"
'''
import os
os.system('cls')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split

# =========================================================================
# [STEP 1] 데이터 로드 및 전처리 (Data Cleaning & Feature Engineering)
# -------------------------------------------------------------------------
# 1. 결측치(NaN)가 포함된 행을 제거하여 데이터의 품질을 확보합니다.
# 2. 문자열 레이블(Yes/No)을 모델이 학습 가능한 숫자(1/0)로 변환합니다.
# 3. 분석에 부적합한 문자열 피처 및 인덱스 컬럼을 필터링합니다.
# =========================================================================
print("="*60)
print("[STEP 1] 데이터 로드 및 전처리")
print("="*60)

data = pd.read_csv("Heart.csv")

# 1. 결측치 처리 (Heart 데이터에는 일부 결측치가 존재하므로 제거하거나 채워줍니다)
data = data.dropna()

# 2. 라벨 데이터(AHD) 수치화 (Yes: 1, No: 0)
data['target'] = data['AHD'].map({'Yes': 1, 'No': 0})

# 3. 문자열(Object) 컬럼 제외 처리
# select_dtypes(exclude=['object'])를 사용하여 수치형 데이터만 추출합니다.
# 이때 첫 번째 의미 없는 인덱스 컬럼("Unnamed: 0")이 있다면 함께 제거합니다.
df_numeric = data.select_dtypes(exclude=['object'])

# 4. 독립변수(X)와 종속변수(y) 분리
# target은 우리가 수치화한 라벨이므로 X에서 제외합니다.
X = df_numeric.drop(['target'], axis=1)
if 'Unnamed: 0' in X.columns:
    X = X.drop('Unnamed: 0', axis=1)

y = df_numeric['target']

# 학습용(Train)과 테스트용(Test) 데이터 분할 (7:3 비율)
# random_state를 고정하여 실행 시마다 동일한 결과를 얻도록 설정
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=12)
print(f"학습 데이터 크기: {x_train.shape}, 테스트 데이터 크기: {x_test.shape}")

# =========================================================================
# [STEP 2] SVM 모델 생성 및 학습 (Model Training & Evaluation)
# -------------------------------------------------------------------------
# SVC(Support Vector Classifier)를 사용하여 데이터를 분류합니다.
# =========================================================================
print("\n" + "="*60)
print("[STEP 2] SVM 모델 학습 및 평가")
print("="*60)

# [SVC 주요 파라미터 설명]
# 1. C (Cost): 규제 강도를 결정하는 파라미터 (가장 중요)
#    - 값이 클수록 (Hard Margin): 오차를 허용하지 않음. 결정 경계가 복잡해지며 과적합(Overfitting) 위험이 있음.
#    - 값이 작을수록 (Soft Margin): 오차를 어느 정도 허용하며 마진을 넓힘. 모델의 일반화 성능이 향상됨.
# 2. kernel: 데이터를 고차원으로 매핑하는 방식
#    - 'linear': 선형 분리. 데이터가 직선으로 나뉠 때 사용.
#    - 'rbf': 방사 기저 함수. 비선형 데이터를 곡선 형태로 분리할 때 사용 (기본값).
# 3. probability=True: 기본 SVM은 거리 기반 모델이라 확률을 제공하지 않지만, 
#    이 옵션을 켜면 predict_proba()를 통해 소속 확률을 확인할 수 있습니다.
model = svm.SVC(kernel='linear', C=0.5, probability=True).fit(x_train, y_train)

# 테스트 데이터를 이용한 예측 및 성능 지표 출력
pred = model.predict(x_test)
print(f"예측값(10개): {pred[:10]}")
print(f"실제값(10개): {y_test[:10].values}")
print(f"최종 분류 정확도: {metrics.accuracy_score(y_test, pred):.4f}")

print("\n[상세 분류 보고서]")
print(metrics.classification_report(y_test, pred))

# =========================================================================
# [STEP 3] 새로운 데이터 예측 (Inference)
# -------------------------------------------------------------------------
# 학습된 모델에 임의의 환자 데이터를 입력하여 심장질환 여부를 예측합니다.
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] 임의의 데이터 예측")
print("="*60)

# 딕셔너리 형태로 임의의 데이터 생성 후 DataFrame으로 변환
sample_dict = {
    'Age': [55],
    'Sex': [1],
    'RestBP': [130],
    'Chol': [250],
    'Fbs': [0],
    'RestECG':[1],
    'MaxHR': [150],
    'ExAng': [0],
    'Oldpeak': [1.2],
    'Slope': [2],
    'Ca': [0]
}

sample_data = pd.DataFrame(sample_dict)
new_pred = model.predict(sample_data)
new_proba = model.predict_proba(sample_data) # 각 클래스별 확률 확인

print(f"입력 데이터 (샘플):\n{sample_data}")
print("-" * 60)
result = "심장질환(Yes)" if new_pred[0] == 1 else "정상(No)"
print(f"분류 결과: {result} (예측값: {new_pred[0]})")
print(f"예측 확률: [정상: {new_proba[0][0]:.4f}, 질환: {new_proba[0][1]:.4f}]")
print("="*60)
