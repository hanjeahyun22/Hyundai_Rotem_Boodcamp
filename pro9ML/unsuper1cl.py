### [이론 - 군집 분석(Clustering)]
# - 데이터간의 유사도를 정의하고, 그 유사도에 가까운 것 부터 순서대로 합쳐가는 방법 -> 거리, 상관계수 등 이용
# - 비슷한 특성을 가진 개체를 그룹으로 만들고, 군집 분리 후, t-test, ANOVA 분석 등을 통해 그룹간 평균의 차이 확인
# - 비지도 학습 (Unsupervised Learning): 타겟 변수(Label) 없이 데이터의 특징만으로 패턴을 파악

# [계층적 군집 분석(Hierarchical Clustering)]
# 1. 응집형(Agglomerative) : 각 데이터를 하나의 군집으로 보고 가까운 것부터 합쳐가는 상향식 방식
# 2. 분리형(Divisive) : 전체 데이터를 하나의 군집으로 보고 세부적으로 나누어가는 하향식 방식

# [통계 분석 설명]
# - t-test: 두 집단 간의 평균 차이가 통계적으로 유의미한지 검정하는 방법
# - ANOVA (분산 분석): 세 개 이상의 집단 간 평균 차이를 비교하기 위해 분산을 이용하는 검정 방법

# [옵션 설명]
# - np.random.seed: 동일한 난수 발생을 위한 설정
# - random_sample: 0~1 사이의 균등 분포에서 난수 생성

import os
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# ---------------------------------------------------------
# 1. 데이터 생성 및 초기화 (5개의 점 생성)
# ---------------------------------------------------------
np.random.seed(123)
var = ["X", "Y"]
labels = ["점0", "점1", "점2", "점3", "점4"]

# 샘플 데이터셋 구성 (5행 2열: X, Y 좌표값)
x = np.random.random_sample([5, 2])
df = pd.DataFrame(x, columns=var, index=labels)
print("--- 생성된 데이터셋 ---\n", df)

# 데이터 시각화 (산점도)
plt.scatter(x[:, 0], x[:, 1], c="blue", marker="o")
for i, txt in enumerate(labels):
    plt.text(x[i, 0], x[i, 1], txt) # 각 점에 라벨 표시

plt.title("데이터 분포 (Scatter Plot)")
plt.grid(True)
plt.show()

# ---------------------------------------------------------
# 2. 거리 행렬 계산 (Distance Matrix)
# ---------------------------------------------------------
from scipy.spatial.distance import pdist, squareform

# pdist: 모든 점들 사이의 유클리드 거리를 계산 (벡터 형태 반환)
dist_vec = pdist(df, metric="euclidean")
print("\n두 점간의 거리 벡터: ", dist_vec)

# squareform: 벡터 형태의 거리를 보기 편하게 행렬(Matrix) 형태로 변환
row_dist = pd.DataFrame(squareform(dist_vec), columns=labels, index=labels)
print("\n--- 거리 행렬 (Distance Matrix) ---\n", row_dist)

# ---------------------------------------------------------
# 3. 계층적 군집 분석 수행 (Hierarchical Clustering)
# ---------------------------------------------------------
# linkage: 응집형 계층적 군집화 수행
# - method='ward': 워드 연결법 (군집 내 오차 제곱합을 최소화하는 방식)
# - metric='euclidean': 거리 측정 방식
from scipy.cluster.hierarchy import linkage

row_clusters = linkage(dist_vec, method='ward', metric='euclidean')

# 군집 결과 데이터프레임 구성
# Cluster ID_1, 2: 합쳐지는 군집 번호 / Distance: 군집 간 거리 / Cluster member: 군집 내 샘플 수
df2 = pd.DataFrame(row_clusters, columns=["Cluster ID_1", "Cluster ID_2", "Distance", "Cluster member"])

print(df2)

# Cluster의 계층 구조를 계통도(Dendogram)로 출력
from scipy.cluster.hierarchy import dendrogram

row_dend = dendrogram(row_clusters, labels=labels)
plt.title("계층적 군집 분석 결과 (Dendrogram)")
plt.tight_layout()
plt.ylabel("유클리드 거리")
plt.show()