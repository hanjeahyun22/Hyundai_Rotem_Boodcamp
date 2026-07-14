### [이론 - 계층적 군집 분석 (Hierarchical Clustering)]
# - 데이터 간의 유사성(거리)을 바탕으로 개별 객체들을 계층적인 트리 구조로 묶어가는 비지도 학습 알고리즘
# - 특징:
#   1. 덴드로그램(Dendrogram)을 통해 군집 형성 과정을 시각적으로 파악할 수 있음
#   2. 초기 군집 수(K)를 설정할 필요가 없으며, 덴드로그램을 보고 적절한 수준에서 절단하여 군집 수를 결정함
#   3. 한 번 군집에 속한 데이터는 다른 군집으로 이동할 수 없는 결정적(Deterministic) 방식임
# - 주요 방식: 응집형(Bottom-up, 가까운 것부터 병합)과 분리형(Top-down, 전체에서 세분화)이 있음

# 계층적 군집분석 : 데이터를 단계적으로 묶어 군집을 형성하는 알고리즘
# 거리가 가까운 데이터부터 계속 묶어가는 방식
# 군집 수를 미리 정하지 않아도 됨.
# 구조는 덴드로그램으로 확인

### [라이브러리 비교: Scipy vs Scikit-learn]
# 1. Scipy (scipy.cluster.hierarchy)
#    - 통계적 접근: 상세한 군집 형성 과정(거리, 계층 구조)을 분석할 때 유리함
#    - 시각화: 덴드로그램(Dendrogram)을 생성하는 표준 도구를 제공함
# 2. Scikit-learn (sklearn.cluster)
#    - 머신러닝 접근: 다른 ML 알고리즘(분류, 회귀)과 파이프라인 연결이 용이함
#    - 대규모 데이터: Scipy보다 대용량 데이터 처리에 최적화되어 있으며 일관된 API(fit, predict)를 제공함

### [데이터 전처리: StandardScaler]
# 1. 개념: 데이터의 평균을 0, 표준편차를 1로 변환하여 표준정규분포 형태로 만드는 스케일링 기법
# 2. 필요성: 군집 분석은 '거리' 기반 알고리즘임. 변수마다 단위(cm, kg, 원 등)가 다르면 
#    값이 큰 변수가 거리에 압도적인 영향을 미치므로, 모든 변수의 영향력을 동등하게 맞추기 위해 필수임
# 3. 계산 방식: (측정값 - 평균) / 표준편차 -> 각 데이터가 평균으로부터 몇 표준편차만큼 떨어져 있는지 계산함
# 4. 추천 경우: 
#    - 데이터의 특성이 정규분포를 따를 때 효과적임
#    - 이상치(Outlier)가 너무 많지 않은 일반적인 상황에서 가장 우선적으로 추천되는 방식

import os
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import adjusted_mutual_info_score, normalized_mutual_info_score

# ---------------------------------------------------------
# 1. 데이터 로드 및 탐색
# ---------------------------------------------------------
iris_data = load_iris()                             # 붓꽃(Iris) 데이터셋 로드
x = iris_data.data                                  # feature: 독립 변수 (꽃받침/꽃잎의 길이와 너비 등 학습에 사용되는 특징 데이터)
y = iris_data.target                                # label: 타겟 숫자 (0, 1, 2) - clusters와 길이를 맞추기 위해 target 사용

# 분석을 위해 feature 데이터를 데이터프레임으로 변환
df = pd.DataFrame(x, columns=iris_data.feature_names)
print(df.head())
print(df.info())
print(df.describe())

# ---------------------------------------------------------
# 2. 데이터 전처리 (스케일링)
# ---------------------------------------------------------
# [데이터 스케일링 (Data Scaling)]
# 1. 개념: 서로 다른 변수(Feature)들의 값의 범위를 일정한 수준으로 맞추는 작업
# 2. 이유: 변수마다 단위(cm, kg, 원 등)가 다르면 수치가 큰 변수가 분석 결과에 지배적인 영향을 미치기 때문
# 3. 군집 분석에서의 필요성: 군집 분석은 데이터 간의 '거리'를 기반으로 그룹을 나눔. 
#    스케일링을 하지 않으면 단위가 큰 변수가 거리에 미치는 영향이 비정상적으로 커져 왜곡된 결과가 나올 수 있음
# 4. 작동 원리: 모든 특성(Feature)의 평균을 0, 분산을 1로 만들어 데이터의 분포를 표준화함
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# ---------------------------------------------------------
# 3. 계층적 군집 분석 수행 (Linkage)
# ---------------------------------------------------------
# [linkage 함수 설명]
# 1. 기능: 데이터 포인트들 간의 거리를 계산하여 가장 유사한(가까운) 군집들을 순차적으로 병합함
# 2. 이유: 모든 데이터 사이의 거리 관계를 파악하여 계층적인 트리 구조(Dendrogram)를 형성하기 위함
# 3. 역할: 각 단계에서 어떤 군집이 합쳐졌는지, 그때의 거리는 얼마인지를 담은 연결 행렬(Z)을 생성함
#    - method="ward": 군집 내 분산을 최소화하는 방식으로 뭉침
z = linkage(x_scaled, method="ward", metric="euclidean")

# ---------------------------------------------------------
# 4. 군집 구조 시각화 (Dendrogram)
# ---------------------------------------------------------
plt.figure(figsize=(12,5))
dendrogram(z)
plt.title("계층적 군집 분석 결과 (Dendrogram)")
plt.xlabel("Sample")
plt.ylabel("Distance(유클리드)")
plt.show()

# ---------------------------------------------------------
# 5. 군집 할당 및 결과 저장 (fcluster)
# ---------------------------------------------------------
# [fcluster 함수 설명] 
# - 개념: linkage 함수로 생성된 계층 구조(Z)를 특정 기준에 따라 잘라 실제 군집 번호를 할당하는 함수
# - z: linkage 함수를 통해 계산된 군집 계층 구조 데이터
# - t: 군집을 나누는 임계값 (criterion에 따라 거리 혹은 개수를 의미함)
# - criterion: t를 적용하는 기준
#   * 'maxclust': 최대 군집의 개수를 t개로 제한하여 나눔
#   * 'distance': 군집 간의 거리가 t 이하인 것들끼리 묶음
clusters = fcluster(Z=z, t=3, criterion="maxclust")
df["cluster"] = clusters
print(df.head())
print(df.tail())

# ---------------------------------------------------------
# 6. 군집 결과 시각화 (Scatter Plot)
# ---------------------------------------------------------
# [산점도(Scatter Plot) 시각화]
# 1. 산점도: 두 변수 간의 관계를 좌표평면 상의 점으로 나타낸 그래프. 데이터의 분포와 군집 형태를 파악하기 용이함
# 2. 데이터 선택:
#    - x_scaled[:, 0]: 스케일링된 'sepal length (cm)' (꽃받침 길이) 데이터
#    - x_scaled[:, 1]: 스케일링된 'sepal width (cm)' (꽃받침 너비) 데이터
#    - 4개의 특성 중 시각화를 위해 가장 기본적인 앞의 2개 특성을 x, y축으로 선택함
# 3. sns.scatterplot 옵션:
#    - x, y: 그래프의 축이 될 데이터
#    - hue: 데이터를 구분할 기준 변수 (여기서는 fcluster로 나눈 군집 번호)
#    - palette: 군집별로 적용할 색상 테마
plt.figure(figsize=(12,6))
sns.scatterplot(x=x_scaled[:, 0], y=x_scaled[:, 1], hue=clusters, palette="Set1")
plt.title("군집 분석 결과 산점도 (Sepal 기준)")
plt.xlabel("꽃받침 길이")
plt.ylabel("꽃받침 너비")
plt.show()
plt.close()

# ---------------------------------------------------------
# 7. 결과 비교 및 검증
# ---------------------------------------------------------
# [결과 비교 및 검증]
# - 실제 label: 데이터셋 제작자가 미리 정의해둔 정답(품종). 0은 Setosa를 의미함
# - 군집 결과: 비지도 학습 알고리즘이 데이터의 유사성만으로 스스로 묶은 그룹 번호
# - 해석: 실제 라벨 0번 그룹이 군집 결과 1번으로 일관되게 묶였다면, 모델이 해당 품종의 특징을 잘 파악하여 분류했다는 뜻임
#   * 실제 라벨 (Actual): 0(Setosa), 1(Versicolor), 2(Virginica) - 데이터의 원래 품종
#   * 군집 결과 (Cluster): 1, 2, 3 - 알고리즘이 유사도에 따라 임의로 부여한 그룹 번호
print("\n--- 군집 결과 검증 ---")
print("실제 label : ", iris_data.target[:10]) # [0 0 0 0 0 0 0 0 0 0] (정답 데이터: Setosa 품종)
print("군집 결과 : ", clusters[:10])        # [1 1 1 1 1 1 1 1 1 1] (예측된 군집: 1번 그룹으로 분류됨)
print("\n교차표 - 실제 라벨 vs. 군집 결과")
ct = pd.crosstab(iris_data.target, clusters, rownames=['Actual'], colnames=['Cluster'])
print(ct)

print("각 실제 class가 가장 많이 속한 군집")
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i, :].idxmax()
    print("실제 class", i, "가 가장 많이 속한 군집:", max_cluster, "(갯수 : ", ct.iloc[i, :].max(), ")")

# 정량적 평가 : 군집 결과가 실제 정답과 얼마나 유사한지를 수치로 표현
# [정량적 평가 지표 설명]
# 1. 외부 평가 지표 (External Evaluation): 실제 정답(Label)이 있는 경우 사용하는 상위 개념의 평가 방식
# 2. ARI (Adjusted Rand Index): '쌍(Pair)' 기반의 일치도를 측정하는 외부 평가 하위 지표
#    - 두 데이터가 같은 군집에 속하는지 여부를 실제 정답과 비교하여 계산함
#    - 우연히 일치할 확률을 보정(Adjusted)하여 신뢰도가 높음
# 3. NMI (Normalized Mutual Information): '정보량' 기반의 유사도를 측정하는 외부 평가 하위 지표
#    - 두 그룹 간에 얼마나 많은 정보를 공유하는지(상호 의존성)를 측정함
#    - 군집의 크기가 불균형해도 안정적인 결과를 제공하며, 0~1 사이의 값을 가짐
# 4. 해석 기준 (범위: -1 ~ 1, NMI는 0 ~ 1):
#    - 1.0: 완벽한 일치
#    - 0.9 이상: 매우 높은 유사성
#    - 0.7 ~ 0.9: 우수한 군집화 결과
#    - 0.4 ~ 0.7: 양호한 수준
#    - 0.0 이하: 무작위 할당과 다를 바 없음 (예측 가치 없음)

from sklearn.metrics import adjusted_rand_score
ari = adjusted_rand_score(iris_data.target, clusters)
nmi = normalized_mutual_info_score(iris_data.target, clusters)

print(f"\nARI (Adjusted Rand Index): {ari:.4f}")
print(f"NMI (Normalized Mutual Information): {nmi:.4f}")
