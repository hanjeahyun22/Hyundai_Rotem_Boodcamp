#################################################################################
### [실습 - K-Means를 이용한 Iris 데이터 군집화 및 성능 평가]
#################################################################################
# 1. 분석 목적
#    - 붓꽃(Iris)의 4가지 특성 데이터를 활용하여 유사한 특성을 가진 품종끼리 그룹화
#    - 실제 품종(Label)과 군집 결과의 일치도를 정량적으로 평가하여 모델 성능 확인
#
# 2. 주요 이론
#    - K-Means: 데이터 간의 유클리드 거리를 기반으로 K개의 군집 중심점을 최적화하는 알고리즘
#    - PCA (주성분 분석): 고차원(4D) 데이터를 정보 손실을 최소화하며 저차원(2D)으로 축소하여 시각화에 활용
#
# 3. 분석 순서
#    Step 1. 데이터 로드 및 표준화(StandardScaler) 수행
#    Step 2. 시각화를 위한 PCA 차원 축소
#    Step 3. K-Means 모델 생성 및 학습 (K=3)
#    Step 4. 군집 결과 시각화 및 정량적 지표(ARI, NMI, Silhouette) 계산
#
# 4. 평가 방법
#    - ARI/NMI: 실제 정답이 있을 때 사용하는 외부 평가 지표 (1에 가까울수록 우수)
#    - Silhouette Score: 정답이 없을 때 군집의 응집도와 분리도를 측정하는 내부 평가 지표
#
# 5. 주요 파라미터 및 옵션 설명
#    - n_clusters: 형성할 군집의 개수 (Iris 품종 수인 3으로 설정)
#    - init='k-means++': 초기 중심점을 멀리 떨어뜨려 배치하여 수렴 속도와 성능 개선
#    - n_init=10: 서로 다른 초기값으로 10번 반복 실행하여 가장 낮은 SSE를 가진 결과 선택
#    - n_components=2: PCA를 통해 유지할 주성분의 개수
#    - explained_variance_ratio_: 각 주성분이 원본 데이터의 분산을 얼마나 설명하는지 나타내는 비율
#################################################################################

import os
os.system("cls")
os.environ["OMP_NUM_THREADS"] = "1"

#################################################################################
### [라이브러리 임포트 및 모듈 상세 설명]
#################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 1. sklearn.datasets.load_iris
#    - 붓꽃의 4가지 특성(꽃받침/꽃잎의 길이와 너비)과 3가지 품종 라벨 데이터를 제공
#
# 2. sklearn.preprocessing.StandardScaler
#    - 각 특성의 평균을 0, 분산을 1로 변환하여 거리 기반 알고리즘의 왜곡 방지
#
# 3. sklearn.cluster.KMeans
#    - K개의 중심점을 설정하고 데이터와의 거리를 최소화하며 그룹화하는 비지도 학습 알고리즘
#
# 4. sklearn.metrics (평가 지표)
#    - adjusted_rand_score (ARI): 타겟(정답)이 있을 때, 무작위 일치 확률을 보정한 군집화 정확도 지표 (-1 ~ 1)
#    - normalized_mutual_info_score (NMI): 데이터 간의 상호 정보량을 이용한 유사도 측정 지표 (0 ~ 1)
#    - silhouette_score: 정답이 없을 때, 군집 내 응집도와 군집 간 분리도를 계산하여 품질을 평가하는 지표
#
# 5. sklearn.decomposition.PCA (주성분 분석)
#    - 고차원 데이터를 정보 손실을 최소화하면서 저차원(2D)으로 투영하여 시각화 지원

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.decomposition import PCA

# ---------------------------------------------------------
# Step 1. 데이터 로드 및 탐색
# ---------------------------------------------------------
iris_Data = load_iris()
x = iris_Data.data
y = iris_Data.target
feature_names = iris_Data.feature_names

df = pd.DataFrame(x, columns=feature_names)
print("iris data shape : ", x.shape)        # (150, 4)
print()

# ---------------------------------------------------------
# Step 2. 데이터 전처리 (Scaling)
# ---------------------------------------------------------
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
print(x_scaled[:2])

# ---------------------------------------------------------
# Step 3. PCA 차원 축소 (시각화용)
# ---------------------------------------------------------
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
print("pca 분산 비율 : ", pca.explained_variance_ratio_)        # pca 분산 비율 :  [0.72962445 0.22850762]

# ---------------------------------------------------------
# Step 4. K-Means 모델 생성 및 학습
# ---------------------------------------------------------
k = 3           # Iris 품종 수에 맞춰 K=3 설정

# n_init=10: 초기 중심점 시드를 다르게 하여 10번 반복 실행 후 최적 결과 선택
kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)

clusters = kmeans.fit_predict(x_scaled)
df["cluster"] = clusters

print("군집 중심 값 : \n", kmeans.cluster_centers_)

# ---------------------------------------------------------
# Step 5. 군집 결과 시각화 (PCA 기반)
# ---------------------------------------------------------
plt.figure(figsize=(6, 5))
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette="Set1")
plt.title("군집 분석 결과 산점도")
plt.xlabel("주성분 1")
plt.ylabel("주성분 2")
plt.show()
plt.close()

# ---------------------------------------------------------
# Step 6. 실제 label과 군집 비교(crosstab)
# ---------------------------------------------------------
ct = pd.crosstab(y, clusters)
print(ct)

### [Crosstab 결과 해석]
# col_0   0   1   2
# row_0            
# 0       0  50   0  -> 실제 0번 품종(Setosa)은 모두 1번 군집으로 완벽하게 분류됨 (정확도 100%)
# 1      39   0  11  -> 실제 1번 품종(Versicolor)은 대부분 0번 군집(39개)으로 분류되었으나, 일부(11개)는 2번으로 혼동됨
# 2      14   0  36  -> 실제 2번 품종(Virginica)은 대부분 2번 군집(36개)으로 분류되었으나, 일부(14개)는 0번으로 혼동됨
#
# * 결론: 
# 1. Setosa는 다른 품종과 물리적 거리가 멀어 군집화가 매우 명확함.
# 2. Versicolor와 Virginica는 특성 데이터가 겹치는 부분이 있어 일부 오분류가 발생함.
# 3. 전체적으로 실제 품종의 경향성을 잘 반영하여 그룹화되었음을 알 수 있음.

# ---------------------------------------------------------
# Step 6-1. 정량적 성능 평가
# ---------------------------------------------------------
### [성능 지표 설명]
# ARI: 실제 라벨과 군집 결과의 일치도 (1에 가까울수록 완벽한 일치)
ari = adjusted_rand_score(y, clusters)
# NMI: 상호 정보량 기반 유사도 (0~1 사이, 1에 가까울수록 우수)
nmi = normalized_mutual_info_score(y, clusters)
# Silhouette: 군집 내 응집도와 군집 간 분리도 (정답 없이 모델 자체의 품질 측정)
sil = silhouette_score(x_scaled, clusters)

print(f"\n--- 성능 평가 지표 ---")
print(f"ARI (Adjusted Rand Index): {ari:.4f}")
print(f"NMI (Normalized Mutual Information): {nmi:.4f}")
print(f"Silhouette Score: {sil:.4f}")

#################################################################################
### [분석 결과 요약 및 오차 분석]
# 1. PCA 분산 비율은 '정보 보존량'을 의미하며, 분류 정확도와는 별개의 개념임.
# 2. Versicolor와 Virginica는 물리적 특성이 유사하여 데이터가 겹치는 구간에서 오분류 발생.
#################################################################################
# ---------------------------------------------------------
# Step 7. 클래스별 대표 군집 매핑 확인
# ---------------------------------------------------------
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f"실제 class {i} -> 군집 {max_cluster}")

# ---------------------------------------------------------
# Step 8. 최적의 K 결정 (Elbow Method)
# ---------------------------------------------------------
### [Elbow Method 이론]
# - K가 증가함에 따라 SSE(Inertia)는 감소함.
# - 그래프가 '팔꿈치'처럼 급격히 꺾이는 지점이 효율적인 최적의 K값임.
# - inertia_: 각 데이터와 중심점 간의 거리 제곱합.
initial = []
k_range = range(1, 10)
for k in k_range:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(x_scaled)
    initial.append(kmeans.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(k_range, initial, marker="o")
plt.title("elbow 기법")
plt.xlabel("K")
plt.ylabel("initial")
plt.show()
plt.close()

# ---------------------------------------------------------
# Step 9. 실제 라벨 vs 군집 결과 비교 시각화
# ---------------------------------------------------------
plt.subplot(1, 2, 1)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=y, palette="Set1")
plt.title("실제 라벨")

### [군집 결과 시각화]
plt.subplot(1, 2, 2)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette="Set1")
plt.title("군집 결과")
plt.show()
plt.close()


# -------------------------------------------------------------------------------
# [Step 10. 군집별 특성 분석 및 통계적 검증]
# -------------------------------------------------------------------------------

# 1. 군집별 평균 계산
pd.set_option("display.max_columns", None)
cluster_mean = df.groupby("cluster").mean()
print("군집별 평균 : \n", cluster_mean)

### 2. 통계적 검증 - ANOVA (분산 분석)
# - 목적: 군집 간 특성 차이가 통계적으로 유의미한지 확인
# - 귀무 가설(H0): 모든 군집의 변수별 평균은 동일하다.
# - 대립 가설(H1): 적어도 한 군집의 변수별 평균은 다르다.
from scipy.stats import f_oneway 
# f_oneway(*args): 세 개 이상의 그룹 간 평균 차이를 비교하는 일원 분산 분석 수행

# 각 군집별로 분리
for col in feature_names:
    group0 = df[df["cluster"] == 0][col]
    group1 = df[df["cluster"] == 1][col]
    group2 = df[df["cluster"] == 2][col]

    # ANOVA 실행
    f_stat, p_val = f_oneway(group0, group1, group2)
    print(f"{col} : f-statistic:{f_stat:.4f}, p-value:{p_val:.4f}")

    # 해석
    if p_val < 0.05:
        print("군집 간 평균에 차이가 없다(유의하지 않다. 유연이다.)")
    else:
        print("군집간 평균에 차이가 있다.(유의하다. 우연이 아니다.)")

# 결과 : K-Means가 꽃잎 길이/너비, 꽃받침을 제대로 군집분석함.


### 3. 사후 검정 (Post-hoc Test)
from statsmodels.stats.multicomp import pairwise_tukeyhsd
# pairwise_tukeyhsd: ANOVA 결과 유의미한 차이가 있을 때, 구체적으로 어떤 군집끼리 차이가 나는지 검정
# - endog: 분석할 데이터 (종속 변수)
# - groups: 그룹을 나눌 기준 (독립 변수)
# - alpha: 유의 수준 (기본값 0.05)

# petal Length로 작업
feature = "petal length (cm)"
tukey = pairwise_tukeyhsd(
    endog=df[feature],
    groups=df["cluster"],
    alpha=0.05
)

print("tukeyhsd 결과(petal length) : \n", tukey)

# plot_simultaneous(): 군집별 평균과 신뢰구간을 시각화하여 차이를 직관적으로 확인
tukey.plot_simultaneous(figsize=(6, 4))
plt.title(f"tukeyhsd : {feature}")
plt.xlabel("평균 차이")
plt.show()
plt.close()
print()

### 4. 군집별 시각화 (Boxplot)
for col in feature_names:
    plt.figure(figsize=(6, 4))
    sns.boxplot(x="cluster", y=col, data=df)
    plt.title(f"{col} by cluster")
    plt.show()

print()

### 5. 최종 군집 특성 요약
cluster_mean["label"] = ["Type A", "Type B", "Type C"]
print(cluster_mean)
