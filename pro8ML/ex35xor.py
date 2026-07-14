"""
SVM (Support Vector Machine) - XOR 연산 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - 단순 선형 회귀나 로지스틱 회귀로 해결하기 어려운 비선형 문제(XOR)를 SVM을 통해 해결함
    - 커널 트릭(Kernel Trick)을 사용하여 저차원 데이터를 고차원으로 매핑하여 분류 수행

2. 주요 특징:
    - SVC(Support Vector Classifier)는 기본적으로 'rbf'(방사 기저 함수) 커널을 사용하여 비선형 분리가 가능함
--------------------------------------------------------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm, metrics

# =========================================================================
# [STEP 1] 데이터 준비 (AND/XOR 논리 연산 데이터)
# =========================================================================
x_data = [ 
    [0, 0, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 1]
]

# feature, label 분리
# [설명] 리스트 슬라이싱 또는 Pandas DataFrame을 활용하여 독립변수(X)와 종속변수(y)를 추출

# feature = []
# lavel = []
# for row in x_data:
#     p = row[0]
#     q = row[1]
#     r = row[2]
#     feature.append([p, q])
#     lavel.append(r)

x_df = pd.DataFrame(x_data)
feature = np.array(x_df.iloc[:, 0:2])
lavel = np.array(x_df.iloc[:, 2])

print("feature : \n", feature)
print("label : \n", lavel)

# =========================================================================
# [STEP 2] 모델 생성 및 학습
# -------------------------------------------------------------------------
# [SVC 주요 파라미터]
# - kernel: 'linear', 'poly', 'rbf'(기본값), 'sigmoid' 등 결정 경계의 모양 설정
# - C: 규제 강도 (값이 클수록 오차 허용 안 함)
# =========================================================================
logistic_model = LogisticRegression()
svm_model = svm.SVC()

logistic_model.fit(feature, lavel)
svm_model.fit(feature, lavel)

# =========================================================================
# [STEP 3] 예측 및 성능 평가
# =========================================================================
logistic_pred = logistic_model.predict(feature)
svm_pred = svm_model.predict(feature)

pred1 = logistic_model.predict(feature)
print("logistic model 예측값 : \n", pred1)

pred2 = svm_model.predict(feature)
print("svm model 예측값 : \n", pred2)

accuracy1 = metrics.accuracy_score(lavel, pred1)
accuracy2 = metrics.accuracy_score(lavel, pred2)

print("logistic model 정확도 : ", accuracy1)
print("svm model 정확도 : ", accuracy2)
print()