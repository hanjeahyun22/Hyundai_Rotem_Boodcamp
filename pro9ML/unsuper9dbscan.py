#################################################################################
### [이론 - 밀도 기반 군집 분석: DBSCAN]
#################################################################################
# 1. 개념 (Definition):
#    - DBSCAN: Density-Based Spatial Clustering of Applications with Noise
#    - 데이터가 세밀하게 몰려 있는 '밀도(Density)'가 높은 영역을 하나의 군집으로 인식함
#    - 기하학적인 모양을 가진 데이터셋(예: 초승달 모양)에서도 군집화를 매우 잘 수행함
#
# 2. 주요 파라미터 (Hyperparameters):
#    - eps (epsilon): 이웃을 정의하는 반지름 거리. 이 거리 안에 데이터가 몇 개 있는지 확인
#    - min_samples: 한 핵심 포인트(Core Point)가 되기 위해 eps 내에 존재해야 하는 최소 데이터 개수
#
# 3. 데이터 포인트의 분류:
#    - 핵심 포인트 (Core Point): eps 내에 min_samples 이상의 이웃이 있는 점
#    - 경계 포인트 (Border Point): 핵심 포인트의 이웃이지만, 스스로는 핵심 포인트가 아닌 점
#    - 노이즈/이상치 (Noise/Outlier): 어떤 핵심 포인트와도 이웃이 아닌 점 (군집에서 제외)
#
# 4. 장점 (Advantages):
#    - 군집의 개수(K)를 미리 정할 필요가 없음 (데이터 분포에 따라 자동 결정)
#    - 원형이 아닌 복잡한 기하학적 형상의 군집도 잘 찾아냄
#    - 이상치(Noise)를 명확하게 구분하여 제거할 수 있음
#
# 5. 단점 (Disadvantages):
#    - 데이터의 밀도가 부위별로 크게 다를 경우 성능이 떨어짐
#    - 차원이 높아질수록(High Dimension) 적절한 eps 값을 찾기 어려움
#    - eps와 min_samples 설정값에 따라 결과가 매우 민감하게 변함
#################################################################################

#################################################################################
### [DBSCAN vs K-Means 비교 분석]
#################################################################################
# - K-Means: 
#   * 중심점 기반. 군집이 원형(Spherical)이라고 가정함
#   * 초승달 모양이나 겹쳐진 데이터 구조에서는 성능이 낮음
#   * 모든 데이터를 반드시 특정 군집에 할당함 (이상치에 취약)
#   * 설정한 K개의 군집 개수 형성
#
# - DBSCAN:
#   * 밀도 기반. 데이터의 실제 형상을 따라 군집을 형성함
#   * 비선형적인 데이터 구조에서 압도적인 성능을 보임
#   * 밀도가 낮은 데이터는 '노이즈(-1)'로 분류하여 분석의 신뢰도를 높임
#   * 밀도에 따른 군집 개수 형성
#################################################################################

import os
os.system("cls")
os.environ["OMP_NUM_THREADS"] = "1"

import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN, KMeans
import koreanize_matplotlib

# =========================================================================
# [STEP 1] 데이터 생성 및 시각화
# -------------------------------------------------------------------------
# - make_moons: 초승달 모양의 두 개의 클러스터를 생성하는 데이터셋 생성 함수
# - noise=0.05: 데이터에 추가되는 가우시안 노이즈의 표준편차
# =========================================================================
x, y = make_moons(n_samples=200, noise=0.05, shuffle=True, random_state=0)
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.title("원본 데이터 분포 (Moon Dataset)")
plt.show()

# ---------------------------------------------------------
# [함수 정의] 군집화 결과 시각화
# ---------------------------------------------------------
def plotResult(x, pr):
    plt.scatter(x[pr == 0, 0], x[pr == 0, 1], c="blue", marker="o", s=40, label="Cluster 1")
    plt.scatter(x[pr == 1, 0], x[pr == 1, 1], c="red", marker="s", s=40, label="Cluster 2")
    
    # 노이즈 데이터 시각화 (DBSCAN 결과에서 -1인 경우)
    if -1 in pr:
        plt.scatter(x[pr == -1, 0], x[pr == -1, 1], c="gray", marker="x", s=40, label="Noise")
        
    plt.legend()
    plt.grid(True)

# =========================================================================
# [STEP 2] K-Means를 이용한 군집화 (중심점 기반)
# -------------------------------------------------------------------------
# [이론 설명]
# - K-Means는 데이터가 원형으로 분포되어 있다고 가정하고 중심점과의 거리를 계산함
# - 초승달 모양처럼 비선형적인 구조에서는 데이터를 수직/수평으로 가로지르며 잘못 분류함
# =========================================================================
print("=" * 60)
print("[STEP 2] K-Means 군집화 수행")
print("=" * 60)

k_means_model = KMeans(n_clusters=2, init='k-means++', random_state=0)
pred1 = k_means_model.fit_predict(x)
print("K-Means 예측 군집 id : \n", pred1[:10])

plotResult(x, pred1)
# K-Means의 중심점 표시
plt.scatter(k_means_model.cluster_centers_[:, 0], k_means_model.cluster_centers_[:, 1], c="black", marker="+", s=200, label="Centroids")
plt.title("Clustering Result [K-Means]")
plt.show()

# =========================================================================
# [STEP 3] DBSCAN을 이용한 군집화 (밀도 기반)
# -------------------------------------------------------------------------
# [옵션 설명]
# - eps=0.2: 이웃을 판별하는 반지름 거리
# - min_samples=5: 핵심 포인트가 되기 위한 최소 이웃 데이터 수
# - metric="euclidean": 거리 측정 방식 (유클리드 거리)
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 3] DBSCAN 군집화 수행")
print("=" * 60)

dbscan_model = DBSCAN(eps=0.2, min_samples=5, metric="euclidean")
pred2 = dbscan_model.fit_predict(x)
print("DBSCAN 예측 군집 id : \n", pred2[:10])
print("군집 종류 (포함된 ID) : ", set(pred2))

plt.title("Clustering Result [DBSCAN]")
plotResult(x, pred2)
plt.show()