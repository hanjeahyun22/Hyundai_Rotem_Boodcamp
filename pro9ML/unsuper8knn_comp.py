#################################################################################
### [실습 - 지도학습(KNN) vs 비지도학습(K-Means) 비교 분석]
#################################################################################
# 1. 분석 목적
#    - 동일한 Iris 데이터셋에 대해 라벨(정답) 유무에 따른 학습 방식의 차이 이해
#    - 분류(Classification)와 군집화(Clustering)의 성능 및 예측 결과 비교
#
# 2. 주요 이론
#    - KNN (지도학습): 새로운 데이터와 가장 가까운 K개의 이웃 라벨을 참조하여 분류
#    - K-Means (비지도학습): 라벨 없이 데이터 간의 거리를 기반으로 K개의 그룹을 형성
#
# 3. 주요 파라미터
#    - n_neighbors: KNN에서 참조할 이웃의 수
#    - n_clusters: K-Means에서 형성할 군집의 개수
#    - weights='distance': 가까운 이웃에게 더 높은 가중치 부여 (KNN)
#################################################################################

import os
os.system('cls')
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

# =========================================================================
# [STEP 1] 데이터 로드 및 탐색
# =========================================================================
print("=" * 60)
print("[STEP 1] 데이터 로드 (Iris)")
print("=" * 60)

iris_data = load_iris()
x = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y = pd.Series(iris_data.target)

print(f"데이터 크기: {x.shape}")
print("레이블 분포:")
print({name: (y == i).sum() for i, name in enumerate(iris_data.target_names)})

# =========================================================================
# [STEP 2] 데이터 전처리 및 분할 (Train / Test Split)
# =========================================================================
print("\n" + "=" * 60) 
print("[STEP 2] 데이터 분할 (8:2)")
print("=" * 60)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=12, stratify=y
)
print("데이터 분할 완료")

# =========================================================================
# [STEP 3] 지도학습 - KNN (K-Nearest Neighbors)
# -------------------------------------------------------------------------
# [이론 설명]
# - KNN은 '유유상종' 원리에 기반하여 새로운 데이터와 가장 가까운 K개의 이웃 라벨을 참조함
# - 특징: 데이터의 라벨(y_train)을 직접 학습에 사용하는 대표적인 지도학습 알고리즘
# [옵션 설명]
# - n_neighbors=3: 참조할 이웃의 개수 설정
# - weights='distance': 거리가 가까운 이웃에게 더 높은 가중치를 부여하여 예측력 향상
# =========================================================================
print("=" * 60)
print("[STEP 3] 지도학습: KNN 모델 학습 및 평가")
print("=" * 60)

knnModel = KNeighborsClassifier(n_neighbors=3, weights="distance", metric="euclidean")
knnModel.fit(x_train, y_train)

knn_pred = knnModel.predict(x_test)
print("KNN 예측값 : ", knn_pred)
print("실제 정답  : ", y_test.values)
print(f"KNN 정확도  : {accuracy_score(y_test, knn_pred):.4f}")

# =========================================================================
# [STEP 4] 비지도학습 - K-Means Clustering
# -------------------------------------------------------------------------
# [이론 설명]
# - K-Means: 라벨 없이 데이터 간의 거리를 계산하여 유사한 특성끼리 K개의 그룹으로 묶음
# - 특징: 학습 시 정답(y_train)을 전혀 사용하지 않고 데이터 자체의 구조적 분포만 파악
# [옵션 설명]
# - n_clusters=3: 형성할 군집(Cluster)의 개수 지정
# - init='k-means++': 초기 중심점을 멀리 배치하여 수렴 속도와 성능을 최적화
# =========================================================================
print("=" * 60)
print("[STEP 4] 비지도학습: K-Means 모델 학습 및 평가")
print("=" * 60)

kmeansModel = KMeans(n_clusters=3, init="k-means++", random_state=0)
kmeansModel.fit(x_train)                # y_train(라벨) 없이 학습 진행
print(kmeansModel.labels_)
print()

# ---------------------------------------------------------
# [STEP 5] 군집별 실제 라벨 분포 확인 (비지도학습 검증)
# ---------------------------------------------------------
print("=" * 60)
print("[STEP 5] 군집별 실제 라벨 분포 확인 (비지도학습 검증)")
print("=" * 60)
print("0번 군집 내 실제 라벨 분포 : \n", y_train[kmeansModel.labels_ == 0].value_counts())
print("1번 군집 내 실제 라벨 분포 : \n", y_train[kmeansModel.labels_ == 1].value_counts())
print("2번 군집 내 실제 라벨 분포 : \n", y_train[kmeansModel.labels_ == 2].value_counts())

# =========================================================================
# [STEP 6] 신규 데이터 예측 및 성능 비교 (지도 vs 비지도)
# -------------------------------------------------------------------------
# - KNN: 학습된 라벨(품종)을 바탕으로 명확한 클래스 분류 결과 반환
# - K-Means: 라벨 없이 중심점과의 거리에 따라 군집 번호(Cluster ID) 반환
# =========================================================================
print("\n" + "=" * 60)
print("[STEP 6] 신규 데이터 예측 결과 비교")
print("=" * 60)

new_input = pd.DataFrame([[6.1, 2.8, 4.7, 1.2]], columns=x.columns)

# [6-1] KNN 예측 및 근거 확인
knn_pred = knnModel.predict(new_input)
print(f"[KNN] 새로운 값은 {knn_pred} (Versicolor)로 분류됨")
dist, index = knnModel.kneighbors(new_input)
print(f"KNN 이웃 거리: {dist}")
print(f"KNN 이웃 인덱스: {index}")
# [해석] 가장 인접한 3개 데이터의 라벨을 확인하여 다수결로 품종을 결정함

# [6-2] K-Means 예측 및 근거 확인
clu_pred = kmeansModel.predict(new_input)
print(f"[K-Means] 새로운 값은 {clu_pred}번 군집으로 분류됨")
# [해석] 새로운 데이터의 좌표가 특정 군집의 중심점(Centroid)과 가장 가깝기 때문에 해당 ID 부여

# [6-3] 비지도학습 성능 정량화를 위한 라벨 재매핑 및 정확도 산출
pred_cluster = kmeansModel.predict(x_test)
print("\n테스트 데이터 군집 결과 : \n", pred_cluster)

# 임시 저장용 라벨(3, 4, 5)
np_arr = np.array(pred_cluster)
np_arr[np_arr == 0], np_arr[np_arr == 1], np_arr[np_arr == 2] = 3, 4, 5

# 실제 품종 라벨과 매칭 (0:Setosa, 1:Versicolor, 2:Virginica)
np_arr[np_arr == 3] = 0
np_arr[np_arr == 4] = 1
np_arr[np_arr == 5] = 2
print("매핑 완료된 군집 라벨 : \n", np_arr)

predict_label = np_arr.tolist()
print(f"K-Means 최종 테스트 정확도 : {np.mean(predict_label == y_test):.4f}")