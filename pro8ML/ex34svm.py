"""
SVM (Support Vector Machine) 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - 데이터들 사이의 거리를 최대화하는 '결정 경계(Hyperplane)'를 찾아 분류를 수행하는 알고리즘
    - 이진 분류에 매우 강력하며, 커널 트릭을 통해 비선형 분류도 가능함

2. 주요 용어:
    - 서포트 벡터(Support Vectors): 결정 경계와 가장 가까이 있는 데이터 포인트들
    - 마진(Margin): 결정 경계와 서포트 벡터 사이의 거리 (이 거리를 최대화하는 것이 목표)
    - C (Cost): 오차를 얼마나 허용할지 결정하는 규제 파라미터 (값이 클수록 하드 마진, 작을수록 소프트 마진)
    - Kernel: 데이터를 고차원으로 보내 선형 분리가 가능하게 만드는 함수 (linear, poly, rbf 등)
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')


from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', family='malgun gothic')

# =========================================================================
# [STEP 1] 데이터 생성 및 시각화
# =========================================================================
print("[STEP 1] 데이터 생성 중...")
# [make_blobs 옵션 설명]
# - n_samples: 생성할 총 데이터 샘플의 개수
# - centers: 생성할 클러스터(집단)의 개수 (여기서는 이진 분류를 위해 2개 설정)
# - cluster_std: 클러스터 내 데이터의 표준편차 (값이 작을수록 데이터가 뭉쳐 있고, 클수록 흩어짐)
# - random_state: 데이터 생성을 위한 난수 시드 (결과 재현성 보장)
# - n_features: 데이터의 특성(차원) 개수 (기본값 2)
X, y = make_blobs(n_samples=50, centers=2, cluster_std=0.5, random_state=4)

# 레이블을 -1과 1로 변환 (SVM의 전형적인 레이블링 방식)
y = 2 * y - 1

plt.scatter(X[y == -1, 0], X[y == -1, 1], marker='o', label="-1 클래스")
plt.scatter(X[y == +1, 0], X[y == +1, 1], marker='x', label="+1 클래스")
plt.xlabel("x1")
plt.ylabel("x2")
plt.legend()
plt.title("학습용 데이터")
plt.show()

# =========================================================================
# [STEP 2] SVM 모델 생성 및 학습
# =========================================================================
print("\n[STEP 2] SVM 모델 학습 중...")
from sklearn.svm import SVC

# [SVC(Support Vector Classifier) 주요 파라미터 설명]
# - kernel: 데이터를 고차원으로 매핑하는 함수 결정
#   * 'linear': 선형 분리 (가장 단순함)
#   * 'rbf': 방사 기저 함수 (비선형 데이터에 효과적, 기본값)
#   * 'poly': 다항식 커널
# - C (Cost): 오차에 대한 규제 강도 (중요!)
#   * 값이 클수록(Hard Margin): 오차를 허용하지 않음 -> 과적합(Overfitting) 위험 증가
#   * 값이 작을수록(Soft Margin): 오차를 어느 정도 허용하며 마진을 넓힘 -> 일반화 성능 향상
model = SVC(kernel='linear', C=1.0).fit(X, y)

# =========================================================================
# [STEP 3] 결정 경계(Decision Boundary) 계산
# =========================================================================
print("[STEP 3] 결정 경계 계산 중...")
xmin = X[:, 0].min()
xmax = X[:, 0].max()
ymin = X[:, 1].min()
ymax = X[:, 1].max()
xx = np.linspace(xmin, xmax, 10)
yy = np.linspace(ymin, ymax, 10)
X1, X2 = np.meshgrid(xx, yy)

z = np.empty(X1.shape)
for (i, j), val in np.ndenumerate(X1):    # np.ndenumerate: 다차원 배열의 인덱스와 값을 동시에 반환

    x1 = val

    x2 = X2[i, j]

    # 결정 함수(Decision Function): 데이터 포인트가 결정 경계로부터 떨어진 거리와 방향을 계산
    p = model.decision_function([[x1, x2]])

    z[i, j] = p[0]

# =========================================================================
# [STEP 4] 결과 시각화 및 예측
# =========================================================================
print("[STEP 4] 학습 결과 시각화")
# 결과 시각화
plt.scatter(X[y == -1, 0], X[y == -1, 1], marker='o', label="-1 클래스")
plt.scatter(X[y == +1, 0], X[y == +1, 1], marker='x', label="+1 클래스")

# [plt.contour 옵션 설명]
# - levels=[-1, 0, 1]: 결정 경계(0)와 서포트 벡터가 위치하는 마진 경계(-1, 1)를 선으로 표시
plt.contour(X1, X2, z, levels=[-1, 0, 1], colors='k', linestyles=['dashed', 'solid', 'dashed'])
# 서포트 벡터 표시 (결정 경계를 만드는 핵심 데이터)
plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, alpha=0.3)

x_new = [10, 2]
plt.scatter(x_new[0], x_new[1], marker='^', s=100)
plt.text(x_new[0] + 0.03, x_new[1] + 0.08, "테스트 데이터")
plt.xlabel("x1")
plt.ylabel("x2")
plt.legend()
plt.title("SVM 예측 결과")
plt.show()

# =========================================================================
# [STEP 5] 서포트 벡터(Support Vectors) 확인
# =========================================================================
print("="*60)
print("Support Vectors 좌표:")
print(model.support_vectors_)
print("="*60)
print("SVM 실습 완료")