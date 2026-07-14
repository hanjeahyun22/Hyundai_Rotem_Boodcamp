#################################################################################
### [실습 - DBSCAN을 이용한 복합 고객 행동 패턴 군집화]
#################################################################################
# 1. 분석 목적:
#    - 단순 원형 분포가 아닌 비선형(초승달 등), 밀집도 차이, 이상치가 포함된 복합 데이터 분석
#    - 고객의 지출액, 방문 횟수, 평균 구매액을 바탕으로 자연스러운 군집 형성 및 노이즈 탐지
#
# 2. 주요 이론 (DBSCAN):
#    - 밀도 기반 군집화: 일정 거리(eps) 내에 최소 개수(min_samples) 이상의 데이터가 있으면 하나의 군집으로 인식
#    - 노이즈(Noise) 처리: 어떤 군집에도 속하지 않는 밀도가 낮은 데이터는 -1(Outlier)로 분류
#    - 비선형 구조: K-Means와 달리 기하학적이고 복잡한 형태의 군집도 효과적으로 찾아냄
#
# 3. 분석 순서:
#    Step 1. 다양한 패턴(VIP, 일반, 저활동, 비선형, 이상치)을 가진 가상 데이터 생성
#    Step 2. 데이터 표준화(StandardScaler): 거리 기반 알고리즘이므로 필수 전처리
#    Step 3. DBSCAN 모델 학습 및 하이퍼파라미터(eps, min_samples) 설정
#    Step 4. 군집 결과 시각화 및 노이즈 데이터 확인
#################################################################################

#################################################################################
### [주요 메소드 및 옵션 설명]
#################################################################################
# 1. DBSCAN(eps=0.5, min_samples=5):
#    - eps (epsilon): 이웃을 정의하는 반지름 거리. 너무 작으면 노이즈가 많아지고, 너무 크면 군집이 합쳐짐
#    - min_samples: 핵심 포인트(Core Point)가 되기 위해 eps 내에 존재해야 하는 최소 데이터 개수
# 2. StandardScaler():
#    - 데이터의 평균을 0, 표준편차를 1로 변환. 변수 간의 단위(Scale) 차이로 인한 왜곡 방지
# 3. fit_predict():
#    - 모델 학습과 군집 할당을 동시에 수행. 결과값 -1은 어느 군집에도 속하지 않는 '노이즈'를 의미함
#################################################################################

import os
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# ---------------------------------------------------------
# [STEP 1] 가상의 복합 고객 데이터 생성 (Simulation)
# ---------------------------------------------------------
np.random.seed(42)

# 데이터 로드
# vip 고객
vip = pd.DataFrame({
    "annual_spending":np.random.normal(700, 40, 80),
    "visit_per_month":np.random.normal(20, 2, 80),
    "avg_purchase":np.random.normal(80, 10, 80),
    "group":"vip"
    })

# 일반 고객  -->>  평균적인 소비 패턴
normal = pd.DataFrame({
    "annual_spending":np.random.normal(300, 100, 150),
    "visit_per_month":np.random.normal(10, 4, 150),
    "avg_purchase":np.random.normal(30, 15, 150),
    "group":"normal"
    })

# 저활동 고객  -->>  방문 적음, 구매 적음
low = pd.DataFrame({
    "annual_spending":np.random.normal(100, 30, 70),
    "visit_per_month":np.random.normal(3, 1, 70),
    "avg_purchase":np.random.normal(10, 5, 70),
    "group":"low"
    })

# 특이 패턴 고객(비선형 패턴)  -->>  일정하지 않은 소비 패턴
t = np.linspace(0, 3*np.pi, 60)
non_lin = pd.DataFrame({
    "annual_spending":np.random.normal(0, 10, len(t)) +200+100*np.cos(t),
    "visit_per_month":np.random.normal(0, 1, len(t)) +10+5*np.sin(t),
    "avg_purchase":40+10*np.sin(t),
    "group":"non_lin"
    })

# 이상치 고객  -->>  너무 많이 사거나 안사거나
outliers = pd.DataFrame({
    "annual_spending":[900, 50, 850],
    "visit_per_month":[10, 1, 25],
    "avg_purchase":[120, 5, 100],
    "group":"outlier"
    })

# 데이터 합치기
df = pd.concat([vip, normal, low, non_lin, outliers], ignore_index=True)
print()

# ---------------------------------------------------------
# [STEP 2] 원본 데이터 시각화 (분포 확인)
# ---------------------------------------------------------
plt.figure(figsize=(6,5))
sns.scatterplot(data=df, x="annual_spending", y="visit_per_month", hue="group", palette="Set2")
plt.title("원본 데이터")
plt.xlabel("연간 지출액")
plt.ylabel("월별 방문 횟수")
plt.legend(title="소비 패턴")
plt.show()

# ---------------------------------------------------------
# [STEP 3] 데이터 전처리 및 DBSCAN 모델 학습
# ---------------------------------------------------------
# [StandardScaler] 거리 기반 알고리즘의 성능 향상을 위해 필수
scaler = StandardScaler()
x_scaled = scaler.fit_transform(df.drop(columns=["group"]))

# [DBSCAN 모델 생성] eps와 min_samples는 데이터의 밀도에 따라 조정이 필요함
dbscan = DBSCAN(eps=0.5, min_samples=5, metric="euclidean")
clusters = dbscan.fit_predict(x_scaled)
df["cluster"] = clusters
print(df.head())

# ---------------------------------------------------------
# [STEP 4] 군집 결과 시각화 (DBSCAN 결과)
# ---------------------------------------------------------
# -1로 표시된 데이터는 DBSCAN이 찾아낸 이상치(Noise)임
plt.figure(figsize=(6,5))
sns.scatterplot(data=df, x="annual_spending", y="visit_per_month", hue="cluster", palette="Set1")
plt.title("군집 분석 결과")
plt.xlabel("연간 지출액")
plt.ylabel("월별 방문 횟수")
plt.legend(title="소비 패턴")
plt.show()

print()
print("군집 평균 : \n", df.groupby("cluster")[["annual_spending", "visit_per_month", "avg_purchase"]].mean())
