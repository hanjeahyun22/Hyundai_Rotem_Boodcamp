### [이론 - 비계층적 군집 분석: K-평균 군집화 (K-Means Clustering)]
# 1. 개념:
#    - 데이터를 미리 정해진 K개의 군집(Cluster)으로 나누는 대표적인 비비계층적(Partitional) 군집 알고리즘
#    - 각 군집의 중심(Centroid)과 데이터 포인트 간의 거리를 최소화하는 방향으로 군집을 형성함
#
# 2. 주요 특징:
#    - K개의 Seed(초기 중심점): 알고리즘 시작 시 K개의 중심점을 임의로 선택하거나 특정 로직으로 배치함
#    - 계산 효율성: 계층적 군집 분석에 비해 계산 복잡도가 낮아 대규모 데이터셋 처리에 유리함
#    - K값 설정: 사용자가 사전에 군집의 개수(K)를 직접 지정해야 함 (Elbow Method 등을 활용)
#
# 3. K-평균 알고리즘의 작동 순서:
#    Step 1. 초기화 (Initialization): 
#           - 데이터 공간에 임의의 K개의 중심점(Seed)을 배치함
#    Step 2. 할당 (Assignment): 
#           - 모든 데이터 포인트를 가장 가까운 중심점에 할당하여 K개의 초기 군집을 형성함
#    Step 3. 업데이트 (Update): 
#           - 각 군집에 속한 데이터들의 산술 평균을 계산하여 새로운 중심점(Centroid)을 설정함
#    Step 4. 반복 (Iteration): 
#           - 다음 조건 중 하나라도 만족하면 알고리즘을 종료함:
#             1) 중심점의 이동이 없을 때: 각 군집의 중심점(Centroid) 위치가 변하지 않을 때 (수렴)
#             2) 할당의 변화가 없을 때: 모든 데이터 포인트의 군집 할당 결과가 이전 단계와 동일할 때
#             3) 최대 반복 횟수 도달: 설정한 max_iter 횟수에 도달했을 때 (무한 루프 방지)
#
# 4. 장단점:
#    - 장점: 알고리즘이 단순하며 속도가 매우 빠름
#    - 단점: 초기 중심점(Seed) 위치에 따라 결과가 달라질 수 있으며, 이상치(Outlier)에 민감함

# 실습1 - make_blobs 사용

import os
os.system("cls")

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np
import pandas as pd

# 1. 데이터 생성
x, _ = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
print(x[:3], ' ', x.shape)

# 2. 데이터 시각화(산점도)
plt.scatter(x[:, 0], x[:, 1], c="gray", marker="o", s=20)
plt.title("데이터 분포 (Scatter Plot)")
plt.grid(True)
plt.show()

# K-Means 모델 생성
# 군집의 중심 선택 방법
# - 'random': 데이터 중에서 무작위로 초기 중심점을 선택 (전통적인 방식)
# - 'k-means++': 초기 중심점들이 서로 멀리 떨어지도록 선택하는 알고리즘 (기본값, 수렴 속도가 빠르고 성능이 안정적임)
# - ndarray: 사용자가 직접 초기 중심점의 좌표를 지정할 때 사용
init_centroid = "random"

# [KMeans 주요 파라미터 설명]
# - n_clusters: 형성할 군집(Cluster)의 개수 (K값)
# - init: 초기 중심점 설정 방식 ('k-means++' 또는 'random')
# - n_init: 초기 중심점 시드(Seed)를 다르게 하여 알고리즘을 반복 실행할 횟수 (가장 낮은 SSE를 가진 결과 선택)
# - random_state: 결과의 재현성을 위한 난수 생성 시드값
k_model = KMeans(n_clusters=3, init=init_centroid, random_state=0)

# K-means로 군집화한 결과물
pred = k_model.fit_predict(x)
print("pred : \n", pred)
print()

# 각 그룹별 보기
print("분류결과 0 : \n", x[pred == 0])
print("분류결과 1 : \n", x[pred == 1])
print("분류결과 2 : \n", x[pred == 2])
print("중심점 : \n", k_model.cluster_centers_)

# 시각화
plt.scatter(x[pred == 0, 0], x[pred == 0, 1], c='red', marker='o', s=50, label='Cluster 1')
plt.scatter(x[pred == 1, 0], x[pred == 1, 1], c='green', marker='s', s=50, label='Cluster 2')
plt.scatter(x[pred == 2, 0], x[pred == 2, 1], c='blue', marker='v', s=50, label='Cluster 3')
plt.scatter(k_model.cluster_centers_[:, 0], k_model.cluster_centers_[:, 1], c='black', marker='+', s=100, label='Centroids')
plt.legend()
plt.grid(True)
plt.show()
plt.close()

# K-Means의 K값 결정 (elbow / shiloutte 기법)

# [Elbow Method: 최적의 군집 수(K)를 결정하는 방법]
#   1. 역할: 군집 내 오차 제곱합(SSE, Inertia)의 변화를 관찰하여 적절한 K값을 찾음
#   2. 방법: K값을 1부터 순차적으로 늘려가며 모델을 학습시키고 SSE 값을 기록함
#   3. 판단 기준: K가 증가할수록 SSE는 감소하며, 그래프가 '팔꿈치(Elbow)'처럼 
#       급격하게 꺾이는 지점이 정보 손실 대비 효율이 가장 좋은 최적의 K값임
#   4. SSE(Inertia) 구하는 법: 각 데이터 포인트와 해당 군집 중심(Centroid) 사이의 거리를 제곱하여 모두 합산함
#   5. SSE(Inertia) 구하는 이유: 군집 내 데이터들이 얼마나 밀집되어 있는지(응집도)를 측정하기 위함임
#       - 값이 작을수록 데이터들이 중심에 가깝게 모여 있어 군집화가 잘 되었다고 판단함
#       - Scikit-learn의 KMeans 모델에서는 'inertia_' 속성을 통해 이 값을 제공함
def elbow(x):
    sse = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init=init_centroid, random_state=0)
        kmeans.fit(x)
        sse.append(kmeans.inertia_)
    plt.plot(range(1, 11), sse, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.title('Elbow Method')
    plt.show()

elbow(x)

'''
실루엣(silhouette) 기법
  클러스터링의 품질을 정량적으로 계산해 주는 방법이다.
  클러스터의 개수가 최적화되어 있으면 실루엣 계수의 값은 1에 가까운 값이 된다.
  실루엣 기법은 k-means 클러스터링 기법 이외에 다른 클러스터링에도 적용이 가능하다
'''
import numpy as np
from sklearn.metrics import silhouette_samples
from matplotlib import cm

# 데이터 X와 X를 임의의 클러스터 개수로 계산한 k-means 결과인 y_km을 인자로 받아 각 클러스터에 속하는 데이터의 실루엣 계수값을 수평 막대 그래프로 그려주는 함수를 작성함.
# y_km의 고유값을 멤버로 하는 numpy 배열을 cluster_labels에 저장. y_km의 고유값 개수는 클러스터의 개수와 동일함.

def plotSilhouette(x, pred):
    cluster_labels = np.unique(pred)
    n_clusters = cluster_labels.shape[0]   # 클러스터 개수를 n_clusters에 저장
    sil_val = silhouette_samples(x, pred, metric='euclidean')  # 실루엣 계수를 계산
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []

    for i, c in enumerate(cluster_labels):
        # 각 클러스터에 속하는 데이터들에 대한 실루엣 값을 수평 막대 그래프로 그려주기
        c_sil_value = sil_val[pred == c]
        c_sil_value.sort()
        y_ax_upper += len(c_sil_value)

        plt.barh(range(y_ax_lower, y_ax_upper), c_sil_value, height=1.0, edgecolor='none')
        yticks.append((y_ax_lower + y_ax_upper) / 2)
        y_ax_lower += len(c_sil_value)

    sil_avg = np.mean(sil_val)         # 평균 저장

    plt.axvline(sil_avg, color='red', linestyle='--')  # 계산된 실루엣 계수의 평균값을 빨간 점선으로 표시
    plt.yticks(yticks, cluster_labels + 1)
    plt.ylabel('클러스터')
    plt.xlabel('실루엣 개수')
    plt.show() 

'''
그래프를 보면 클러스터 1~3 에 속하는 데이터들의 실루엣 계수가 0으로 된 값이 아무것도 없으며, 실루엣 계수의 평균이 0.7 보다 크므로 잘 분류된 결과라 볼 수 있다.
'''
X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
km = KMeans(n_clusters=3, random_state=0) 
y_km = km.fit_predict(X)

plotSilhouette(X, y_km)
