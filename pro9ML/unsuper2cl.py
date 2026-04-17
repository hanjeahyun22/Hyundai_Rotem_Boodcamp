### [이론 - 군집 분석(Clustering) 및 계층적 군집]
# - 비지도 학습(Unsupervised Learning): 정답(Label) 없이 데이터의 유사성만을 이용하여 그룹화
# - 계층적 군집 분석: 데이터 간의 거리를 계산하여 가까운 것부터 순차적으로 묶어가는 방식
# - Ward's Method: 군집 내 오차 제곱합(SSE)의 증가량을 최소화하는 방식으로, 크기가 비슷한 군집끼리 묶는 경향이 있음

### [옵션 및 함수 설명]
# - linkage(method='ward'): 워드 연결법을 사용하여 계층적 군집 수행
# - fcluster(criterion='maxclust', t=3): 형성된 계층 구조를 바탕으로 최종 군집의 개수를 3개로 제한
# - reshape(-1, 1): 1차원 데이터를 Scikit-learn/Scipy 연산이 가능한 2차원 행렬 형태로 변환
# - flatten() / ravel(): 2차원 배열을 다시 1차원으로 펼쳐서 출력이나 시각화에 사용

### [분류 결과 분석 - 왜 이렇게 나누어졌는가?]
# 1. Cluster 1 (평균 88.60): s2(95), s4(85), s6(92), s8(88), s9(83) -> 80~90점대의 고득점 그룹
# 2. Cluster 2 (평균 74.00): s1(76), s10(72) -> 70점대의 중위권 그룹
# 3. Cluster 3 (평균 60.00): s3(65), s5(60), s7(55) -> 50~60점대의 하위권 그룹
# * 결과 해석: Ward 방식이 점수 차이(유클리드 거리)가 가장 적은 학생들을 묶어 점수대별로 명확히 구분함

### [이론 - 계층적 군집 분석 (Hierarchical Clustering) 상세]
# - 개별 데이터 포인트들을 유사한 것끼리 순차적으로 묶어가는 방식
# - Dendrogram(계통도)을 통해 군집 형성 과정을 시각적으로 파악 가능
# - 비지도 학습의 대표적인 방법으로, 사전에 군집의 개수(K)를 정하지 않아도 됨

### [주요 라이브러리 및 모듈 설명]
# 1. scipy (Scientific Python): 과학 계산 및 통계 분석을 위한 라이브러리
#    - scipy.cluster.hierarchy: 계층적 군집화와 관련된 통계 함수 제공
#    - linkage: 데이터 간의 거리를 계산하여 군집을 형성하는 핵심 함수
#      * method: 군집 간 거리를 구하는 방법 ('single', 'complete', 'average', 'ward' 등)
#      * metric: 거리 측정 방식 ('euclidean', 'cityblock' 등)
#    - dendrogram: 군집 결과를 트리 구조의 그래프로 시각화
#    - fcluster: 형성된 계층 구조에서 특정 기준(거리 혹은 군집 수)으로 군집을 자름
#      * t: 군집을 나누는 임계값 (거리 또는 개수)
#      * criterion: t의 기준 설정 ('distance'는 거리 기준, 'maxclust'는 최대 군집 수 기준)
#
# 2. sklearn (Scikit-learn): 파이썬의 대표적인 머신러닝 라이브러리
#    - AgglomerativeClustering: 응집형 계층적 군집화 모델 제공
#    - fit_predict(): 모델 학습과 동시에 군집 번호를 반환하는 메서드
#    - n_clusters: 미리 지정할 군집의 개수
#
# 3. numpy: 수치 계산 및 배열 처리를 위한 라이브러리
# 4. matplotlib: 데이터 시각화를 위한 라이브러리
import os
os.system("cls")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import koreanize_matplotlib

# ---------------------------------------------------------
# 0. 데이터 준비 및 전처리
# ---------------------------------------------------------

# 학생 10명의 시험점수 데이터 생성
students = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"]
# reshape(-1, 1): 1차원 배열을 2차원 형태(10행 1열)로 변환. Scikit-learn이나 Scipy의 입력 규격에 맞춤
scores = np.array([76, 95, 65, 85, 60, 92, 55, 88, 83, 72]).reshape(-1, 1)
print("점수 : \n", scores)

# ---------------------------------------------------------
# 1. 계층적 군집 수행 (linkage 함수)
# ---------------------------------------------------------
# - method='ward': 워드 연결법. 군집 내 오차 제곱합(SSE)의 증가량을 최소화하는 방향으로 병합
# - metric='euclidean': 두 점 사이의 직선 거리인 유클리드 거리 사용
linked = linkage(scores, method='ward', metric='euclidean')

# ---------------------------------------------------------
# 2. 덴드로그램 시각화 (dendrogram 함수)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
dendrogram(linked, labels=students)
plt.title("학생 점수 군집 분석 (Dendrogram)")
plt.xlabel("학생 ID")
plt.ylabel("거리 (유사도)")
plt.axhline(y=25, color="r", linestyle="--", label="거리 임계값 (y=25)")
plt.legend()
plt.grid(True)
plt.show()

# ---------------------------------------------------------
# 3. 군집 할당 (fcluster 함수)
# ---------------------------------------------------------
# - t: 군집을 나누는 기준 (거리 임계값 또는 군집의 개수)
# - criterion='distance': t값을 거리 기준으로 사용 (t보다 거리가 먼 군집은 합치지 않음)
# - criterion='maxclust': t값을 최대 군집 개수로 사용
labels = fcluster(linked, t=10, criterion='distance')

# scores는 (10, 1) 형태의 2차원 배열입니다. 
# Pandas DataFrame의 컬럼으로 넣기 위해 flatten()을 사용하여 1차원 배열(10,)로 변환합니다.
df = pd.DataFrame({'Student': students, 'Score': scores.flatten(), 'Cluster': labels}) 
print(df)
print()

# 군집 3개로 나누기
clusters = fcluster(linked, t=3, criterion='maxclust')
print("학생 별 군집 결과")
for stu, cluster in zip(students, clusters):
    print(f"{stu} : cluster {cluster}")

# 군집별로 점수와 이름 확인
cluster_info = {}
for student, cluster, score in zip(students, clusters, scores.flatten()):
    if cluster not in cluster_info:
        cluster_info[cluster] = {'students': [], 'scores': []}
    cluster_info[cluster]['students'].append(student)
    cluster_info[cluster]['scores'].append(score)
print(cluster_info)
print()

print("군집별로 평균점수와 이름 확인")
for cluster_id, info in cluster_info.items():
    avg_score = np.mean(info['scores'])
    student_list = ', '.join(info['students'])
    print(f"Cluster {cluster_id} : 평균점수={avg_score:.2f}, 학생들={student_list}")

# 군집별 Scatter Plot
x_positions = np.arange(len(students))
y_scores = scores.ravel()

colors = {1: 'red', 2: 'blue', 3: 'green'}

plt.figure(figsize=(10, 6))
# enumerate와 zip을 사용하여 학생의 인덱스(i), x좌표(x), 점수(y), 소속 군집(cluster)을 동시에 반복문으로 처리
for i, (x, y, cluster) in enumerate(zip(x_positions, y_scores, clusters)):
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y + 1.5, students[i], ha='center') # 학생 이름 표
plt.xticks(x_positions, students)
plt.xlabel("Students")
plt.ylabel("Score")
plt.title("Clustered Students by Score")
plt.grid(True)
plt.show()
plt.close()