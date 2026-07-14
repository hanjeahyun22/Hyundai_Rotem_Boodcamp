### [실습 - K-Means를 이용한 쇼핑몰 고객 세분화 (Customer Segmentation)]
# 1. 분석 목적:
#    - 고객의 연간 지출액과 월간 방문 횟수 데이터를 바탕으로 유사한 성향의 고객 그룹을 추출
#    - 그룹별 특징을 파악하여 타겟 마케팅 전략 수립 (예: 우수 고객 관리, 휴면 고객 활성화)
#
# 2. 주요 개념:
#    - 비지도 학습: 정답(Label) 없이 데이터의 분포와 거리만을 이용하여 군집을 형성
#    - K-Means: 각 데이터와 군집 중심점(Centroid) 간의 거리를 최소화하는 방향으로 학습
#
# 3. 데이터 전처리:
#    - np.clip(): 데이터의 범위를 제한하여 음수 등 분석에 부적절한 값을 보정
#    - StandardScaler (권장): 거리 기반 알고리즘이므로 변수 간 단위 차이가 클 경우 스케일링이 필요함

### [주요 메소드 및 속성 설명]
# 1. KMeans(n_clusters=K): 데이터를 K개의 군집으로 나누는 모델 생성
# 2. fit_predict(data): 모델 학습과 동시에 각 데이터가 속한 군집 번호를 반환
# 3. cluster_centers_: 학습 완료 후 계산된 각 군집의 중심점 좌표 (Centroid)
# 4. inertia_: 군집 내 데이터들과 중심점 간의 거리 제곱합 (SSE), 값이 작을수록 응집도가 높음
# 5. random_state: 결과의 재현성을 위해 난수 시드를 고정


import os
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans

# ---------------------------------------------------------
# 1. 가상의 고객 데이터 생성 (Simulation)
# ---------------------------------------------------------
np.random.seed(0)
n_customers = 200

# 연간 지출액 (평균 5만, 표준편차 1.5만)
annual_spending = np.random.normal(50000, 15000, n_customers)
# 월간 방문 횟수 (평균 5회, 표준편차 2회)
monthly_visits = np.random.normal(5, 2, n_customers)

# [데이터 보정 - np.clip]
# - 개념: 배열의 요소가 지정된 최소값보다 작으면 최소값으로, 최대값보다 크면 최대값으로 치환
# - 이유: 지출액이나 방문 횟수는 음수가 될 수 없으므로 하한선을 0으로 고정
annual_spending = np.clip(annual_spending, 0, None)
monthly_visits = np.clip(monthly_visits, 0, None)

# 분석용 데이터프레임 구성
data = pd.DataFrame({'annual spending':annual_spending,
                        'monthly visits':monthly_visits})

print(data.head(), data.shape)

# ---------------------------------------------------------
# 2. 데이터 시각화 (원본 데이터 분포 확인)
# ---------------------------------------------------------
plt.scatter(data['annual spending'], data['monthly visits'])
plt.xlabel('연간 지출액')
plt.ylabel('월간 방문 횟수')
plt.title('고객 데이터 분포')
plt.show()

# ---------------------------------------------------------
# 3. K-Means 모델 생성 및 학습
# ---------------------------------------------------------
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(data)

# ---------------------------------------------------------
# 4. 군집 결과 시각화 및 중심점 표시
# ---------------------------------------------------------
# 군집 결과 시각화
data["cluster"] = clusters
# print(data.head())

for cluster_id in np.unique(clusters):
    cluster_data = data[data["cluster"] == cluster_id]
    
    print(data[data["cluster"] == cluster_id])

    plt.scatter(cluster_data["annual spending"], cluster_data["monthly visits"], label=f"군집 {cluster_id}")

# [cluster_centers_ 의 역할]
# - K-Means 알고리즘이 학습을 통해 최종적으로 결정한 각 군집의 중심점(Centroid) 좌표를 반환함
# - 각 행은 하나의 군집 중심을 나타내며, 열은 입력 데이터의 특성(Feature) 개수와 동일함
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='black', marker='X', s=200, label='Centroids')

plt.xlabel('연간 지출액')
plt.ylabel('월간 방문 횟수')
plt.title('K-Means 고객 세분화 결과')
plt.legend()
plt.show()
plt.close()
