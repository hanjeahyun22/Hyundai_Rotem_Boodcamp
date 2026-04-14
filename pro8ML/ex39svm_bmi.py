"""
SVM (Support Vector Machine) - BMI 체질량지수 분류 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - 키와 몸무게 데이터를 바탕으로 저체중, 정상, 비만 여부를 분류하는 다중 클래스 분류 문제
    - BMI 공식: 몸무게(kg) / (키(m)^2)

2. 주요 특징:
    - 대량의 가상 데이터를 생성하여 학습 및 검증 수행
    - SVM의 RBF(방사 기저 함수) 커널을 사용하여 비선형 결정 경계 학습
    - 데이터 정규화(Scaling) 및 교차 검증(Cross Validation) 적용
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import numpy as np
import pandas as pd
from sklearn import svm, metrics, model_selection
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
import koreanize_matplotlib

random.seed(12)

# =========================================================================
# [STEP 1] BMI 계산 함수 정의 및 데이터 생성 로직
# =========================================================================
def cald_bmiFunc(height, weight):
    """키와 몸무게를 입력받아 BMI 카테고리 반환"""
    bmi = weight / (height / 100) ** 2
    if bmi < 18.5:
        return "저체중"
    elif 18.5 <= bmi < 25:
        return "정상"
    else:
        return "비만"
    
# [참고] 데이터 생성 코드 (최초 1회 실행 후 주석 처리)
"""
fp = open("bmi.csv", "w", encoding="utf-8")
fp.write("height,weight,label\n")
for i in range(50000):
    height = random.randint(150, 200)
    weight = random.randint(35, 100)
    label = cald_bmiFunc(height, weight)
    fp.write("{0},{1},{2}\n".format(height, weight, label))
fp.close()
"""

# =========================================================================
# [STEP 2] 데이터 로드 및 전처리 (Data Cleaning & Scaling)
# =========================================================================
print("="*60)
print("[STEP 2] 데이터 로드 및 전처리")
print("="*60)
df = pd.read_csv("bmi.csv")

# 피처(X)와 레이블(y) 분리
label = df["label"]

# 데이터 정규화 (0~1 사이 값으로 스케일링)
weight = df["weight"] / 100
height = df["height"] / 200
wh = pd.concat([weight, height], axis=1)

# 레이블 인코딩 (문자열 -> 숫자)
label = label.map({"저체중": 0, "정상": 1, "비만": 2})

# 학습용/테스트용 데이터 분할 (7:3)
x_train, x_test, y_train, y_test = train_test_split(wh, label, test_size=0.3, random_state=12)

# =========================================================================
# [STEP 3] SVM 모델 생성 및 학습
# =========================================================================
print("\n" + "="*60)
print("[STEP 3] SVM 모델 학습 (Kernel: RBF)")
print("="*60)
model = svm.SVC(C=0.01, kernel='rbf').fit(x_train, y_train)

# =========================================================================
# [STEP 4] 예측 및 성능 평가
# =========================================================================
print("\n" + "="*60)
print("[STEP 4] 모델 성능 평가")
print("="*60)
pred = model.predict(x_test)
print(f"예측값(10개): {pred[:10]}")
print(f"실제값(10개): {y_test[:10].values}")
print(f"최종 분류 정확도: {metrics.accuracy_score(y_test, pred):.4f}")

# 교차 검증 (Cross Validation) 수행
cross_vali = model_selection.cross_val_score(model, wh, label, cv=3)
print(f"\n3-Fold 교차 검증 평균 정확도: {cross_vali.mean():.4f}")
print("="*60)

# =========================================================================
# [STEP 5] 새로운 데이터 예측 및 시각화
# =========================================================================
print("\n" + "="*60)
print("[STEP 5] 새로운 데이터 예측 및 시각화")
print("="*60)

# 1. 새로운 가상 데이터 생성 및 스케일링 적용
new_data = pd.DataFrame({"weight":[66, 88], "height":[188, 160]})
new_data["weight"] = new_data["weight"] / 100  # 학습 시와 동일한 스케일링 적용
new_data["height"] = new_data["height"] / 200
new_pred = model.predict(new_data)
print(f"새로운 데이터 예측 결과 (0:저체중, 1:정상, 2:비만): {new_pred}")

# 2. BMI 데이터 분포 시각화
df2 = pd.read_csv("bmi.csv", index_col=2)
def scatterFunc(lbl, color): # 레이블별로 색상을 다르게 하여 산점도 출력
    b = df2.loc[lbl]
    plt.scatter(b["weight"], b["height"], c=color, label=lbl)

scatterFunc("정상", "yellow")
scatterFunc("비만", "red")
scatterFunc("저체중", "blue")
plt.legend()
plt.xlabel("Weight (kg)")
plt.ylabel("Height (cm)")
plt.title("BMI 체질량지수 데이터 분포")
plt.show()
print("="*60)