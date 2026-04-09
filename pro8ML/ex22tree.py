import os
os.system('cls')

# DecisionTree(의사 결정 나무) 분류 모델
# 1. 데이터의 균일도(Impurity)를 기준으로 최적의 질문을 찾아 데이터를 분할하는 모델
# 2. 스무고개 형식의 규칙을 생성하며, 데이터를 직각(수직, 수평) 방향으로 나누어 영역을 구분함
# 3. 장점: 결과 해석이 쉽고 시각화가 가능함 / 단점: 과적합(Overfitting)이 발생하기 쉬움

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
'''
[옵션 상세 설명]
1. criterion: 'gini'는 지니 계수를 사용하여 노드를 분할합니다. 0일 때 가장 순수(Pure)한 상태입니다.
2. max_depth: 트리의 성장을 제한합니다. 가지치기(Pruning)의 가장 기본적인 방법입니다.
3. min_samples_leaf: 리프 노드(끝 노드)가 되기 위한 최소 샘플 수입니다.
4. splitter: 'best'는 최적의 분할을 찾고, 'random'은 무작위 분할 중 최선을 찾습니다.
5. class_weight: 클래스 불균형 데이터일 경우 'balanced'로 설정하여 가중치를 조절할 수 있습니다.
'''
# =========================================================================
#                       분류용 가상 데이터 생성
# =========================================================================
# n_samples: 생성할 데이터 총 개수
# n_features: 독립변수(특성)의 개수
# n_redundant: 다른 특성들의 선형 조합으로 만들어진 중복 특성 수 (0으로 설정하여 독립성 유지)
# n_informative: 종속변수와 상관관계가 있는 유의미한 특성 수
# random_state: 난수 시드값 (결과 재현성 보장)
x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_informative=2, random_state=42)

# =========================================================================
#                   DecisionTreeClassifier 모델 생성 및 학습
# =========================================================================
# criterion: 불순도 측정 지표
#   - 'gini': 지니 불순도 (기본값). 계산이 빠름
#   - 'entropy': 정보 이득(Information Gain) 기반. 좀 더 균형 잡힌 트리를 만듦
# max_depth: 트리의 최대 깊이. 너무 깊으면 과적합(Overfitting), 너무 낮으면 과소적합(Underfitting)
# min_samples_split: 노드를 분할하기 위한 최소 샘플 수
# random_state: 모델 내부의 무작위성 제어
model = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)
model.fit(x, y)

# =========================================================================
#                               시각화
# =========================================================================
# tree구조
plt.figure(figsize=(10, 6))
plot_tree(model, feature_names=["x1", "x2"], class_names=["0", "1"], filled=True)
plt.show()
plt.close()

# 결정 경계 시각화
#   1. x축, y축 값을 조합해서 좌표 격좌 생성(x1, x2범위를 각각 100개 mesh로 나눔)
xx, yy = np.meshgrid(np.linspace(x[:, 0].min(), x[:, 0].max(), 100), np.linspace(x[:, 1].min(), x[:, 1].max(), 100))
#   2. 모든 좌표에 대해 예측값 계산
z = model.predict(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape)
#   3. plot
plt.contour(xx, yy, z, alpha=0.3)
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.title("Decision Boundary")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()
plt.close()