### [이론 - 비계층적 군집 분석: K-평균 군집화 (K-Means Clustering)]
# 1. 개념:
#    - 데이터를 미리 정해진 K개의 군집(Cluster)으로 나누는 대표적인 비계층적 군집 알고리즘
#    - 각 군집의 중심(Centroid)과 데이터 포인트 간의 거리를 최소화하는 방향으로 군집을 형성함
#
# 2. K-평균 알고리즘의 작동 순서:
#    Step 1. 초기화: 데이터 공간에 임의의 K개의 중심점(Seed)을 배치
#    Step 2. 할당: 모든 데이터 포인트를 가장 가까운 중심점에 할당하여 군집 형성
#    Step 3. 업데이트: 각 군집에 속한 데이터들의 산술 평균을 계산하여 새로운 중심점 설정
#    Step 4. 반복: 중심점 변화가 없거나 최대 반복 횟수에 도달할 때까지 Step 2~3 반복
#
# 3. 주요 파라미터 및 옵션 설명:
#    - n_clusters: 형성할 군집의 개수 (K값)
#    - init='k-means++': 초기 중심점이 서로 멀리 떨어지도록 선택하여 수렴 속도와 성능을 높이는 방식
#    - random_state: 결과의 재현성을 위해 난수 생성 시드를 고정
#
# 4. 왜 하는가? (목적):
#    - 방대한 데이터에서 정답(Label) 없이도 유사한 특징을 가진 그룹을 빠르게 찾아내기 위함
#    - 고객 세분화, 이미지 압축, 이상치 탐지 등 다양한 분야에서 활용

### [데이터 전처리 및 형태 변환]
# - reshape(-1, 1): 1차원 배열을 2차원 행렬(N행 1열)로 변환
#   * Scikit-learn의 모든 모델은 입력 데이터로 2차원 배열을 요구하기 때문에 필수적인 과정임
# - flatten() vs ravel(): 2차원 배열을 다시 1차원으로 펼칠 때 사용
#   1. flatten(): '복사본(Copy)'을 생성. 원본 배열과 독립적인 메모리 공간을 가짐 (안전함)
#   2. ravel(): '뷰(View)'를 생성. 원본 배열의 메모리를 공유하여 속도가 빠르고 메모리 효율적임
#      * ravel로 만든 배열의 값을 수정하면 원본 배열의 값도 함께 변경될 수 있음에 유의
#   * 데이터프레임 생성 시에는 두 방식 모두 1차원 배열을 요구하는 규격을 맞추기 위해 사용됨

### [최적의 K(군집 수) 결정 방법]
# - Elbow Method: SSE(오차 제곱합)가 급격히 줄어드는 지점을 선택
# - Silhouette Score: 군집 간의 거리와 군집 내의 밀집도를 계산하여 품질을 평가

import os
os.system("cls")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import koreanize_matplotlib

# ---------------------------------------------------------
# 1. 데이터 준비 (학생 10명의 시험 점수)
# ---------------------------------------------------------
students = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"]
scores = np.array([76, 95, 65, 85, 60, 92, 55, 88, 83, 72]).reshape(-1, 1)
print("점수 : \n", scores)

# ---------------------------------------------------------
# 2. K-Means 모델 생성 및 학습
# ---------------------------------------------------------
# K=3으로 설정 (고득점, 중위권, 하위권 그룹 예상)
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
km_clusters = kmeans.fit_predict(scores)

# ---------------------------------------------------------
# 3. 결과 출력 및 데이터프레임 구성
# ---------------------------------------------------------
print("학생 별 군집 결과\n", km_clusters)
df = pd.DataFrame({'Student': students, 'Score': scores.ravel(), 'Cluster': km_clusters})
print(df)

# 군집별 평균 점수
print("군집별 평균 점수 : \n", df.groupby('Cluster')['Score'].mean())

# 시각화
x_position = np.arange(len(students))
y_scores = scores.ravel()
colors = {0: 'red', 1: 'blue', 2: 'green'}

plt.figure(figsize=(10, 6))
# 학생별 군집을 색으로 구분해 산점도 plot
for i, (x, y, cluster) in enumerate(zip(x_position, y_scores, km_clusters)):
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y+1.5, students[i], fontsize=10, ha='center')

# 중심점
centers = kmeans.cluster_centers_
for center in centers:
    plt.scatter(len(students)//2, center[0], marker="X", c="black", s=200)

plt.xticks(x_position, students)
plt.xlabel("학생명")
plt.ylabel("점수")
plt.title("Clustered Students by Score")
plt.grid(True)
plt.show()
plt.close()