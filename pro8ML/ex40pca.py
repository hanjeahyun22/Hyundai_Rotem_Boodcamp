# PCA(주성분 분석) : 선형대수 관점에서 입력데이터의 공분산 행렬을 고유값 분해하고 
# 이렇게 구한 고유벡터의 입력 데이터를 선형변환하는 것이다.
# 이 고유벡터가 PCA의 주성분 벡터로서 데이터의 분산이 큰 방향을 나타낸다.
# 입력 데이터의 성질을 최대한 유지한 상태로 고차원을 저차원 데이터로 변환하는 기법

# iris dataset으로 차원 축소
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
import seaborn as sns
import numpy as np

iris = load_iris()
n = 10
x = iris.data[:n, :2] # sepal length, width 열만 선택
print('차원 축소 전 데이터 : \n', x, x.shape, type(x))
print(x.T)

# 시각화1 : 각 샘플의 두 특성값을 선으로 연결해 비교
"""
plt.plot(x.T, 'o:')
plt.xticks(range(2), ['꽃받침 길이','꽃받침 너비'])
plt.grid(True)
plt.title('아이리스 크기 특성')
plt.xlabel('특성의 종류')
plt.ylabel('특성값')
plt.xlim(-0.5, 2)
plt.ylim(2.5, 6)
plt.legend(['표본 {}'.format(i+1) for i in range(n)])
plt.show()
"""

# 시각화2 : 산점도(scatter)
df = pd.DataFrame(x)
print(df)
# sns.scatterplot(x=df[0], y=df[1], data=df, marker='s', s=100, color='b')
ax = sns.scatterplot(x=0, y=1, data=df, marker='s', s=100, color='b')
# 각 점에 대해 text 표시
for i in range(n):
    ax.text(x[i,0]-0.05, x[i,1] + 0.03, '표본 {}'.format(i+1))
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.title('아이리스 특성')
plt.axis('equal')
plt.show()

# 시각화 결과 두 변수 간 상관관계가 확인되므로 차원 축소 가능성이 높음
# PCA 수행 단계:
# 1. 입력 데이터의 공분산 행렬 생성
# 2. 공분산 행렬의 고유벡터와 고유값(분산의 크기) 계산
# 3. 고유값이 큰 순서대로 k개의 주성분(고유벡터) 선택
# 4. 선택된 고유벡터를 사용하여 데이터를 새로운 저차원 공간으로 투영(선형 변환)

pca1 = PCA(n_components=1) # 2차원 -> 1차원 축소
x_low = pca1.fit_transform(x)
print('차원 축소 후 데이터 : \n', x_low[:3], x_low.shape)

# 축소된 데이터를 다시 원래 차원으로 복구 (정보 손실 발생 확인용)
x2 = pca1.inverse_transform(x_low)
print('복구된 데이터 : \n', x2[:3], x2.shape)

# 시각화 3 : 원본 데이터와 차원 축소 후 복구된 데이터 비교
sns.scatterplot(x=0, y=1, data=df, marker='s', s=100, color='b', alpha=0.3, label='원본')
for i in range(n):
    plt.text(x[i,0]-0.05, x[i,1] + 0.03, '표본 {}'.format(i+1))

df2 = pd.DataFrame(x2)
sns.scatterplot(x=0, y=1, data=df2, marker='o', s=100, color='r', label='차원축소 후 복구')

# 차원 축소된 데이터들이 놓인 선(주성분 방향) 그리기
plt.plot(x2[:, 0], x2[:, 1], 'r--', alpha=0.5)

plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.title('PCA 차원 축소 결과')
plt.axis('equal')
plt.legend()
plt.show()

# 주성분이 설명하는 분산 비율 (정보 유지량)
print('주성분 벡터(고유벡터) : \n', pca1.components_) 
print('설명 가능한 분산 비율 : ', pca1.explained_variance_ratio_)
# [0.89393856] -> 1차원으로 줄여도 원본 데이터 분산의 약 89%를 설명함

print('-'*40)
# 원본 열 4개를 차원축소해 2개의 열로 변환 후 SVM 분휴모델 작성
x = iris.data
print(x[0,:])  # [5.1 3.5 1.4 0.2]
pca2 = PCA(n_components=2)
x_low2 = pca2.fit_transform(x)
print(x_low2[0, :], x_low2.shape) # (150, 2)

# 변동성 비율 확인
print('설명 가능한 분산 비율 : ', pca2.explained_variance_ratio_)  # [0.92461872 0.05306648]
x4 = pca2.inverse_transform(x_low2)
print('최조 자료 : ', x[0])
print('차원 축소 : ', x_low2[0])
print('차원 복귀 : ', x4[0, :])

print('-'*40)
iris1 = pd.DataFrame(x, columns=['sepal length', 'sepal width', 'petal length', 'petal width'])
iris2 = pd.DataFrame(x_low2, columns=['PC1', 'PC2'])
iris2['target'] = iris.target
print(iris2.head())

from sklearn import svm, metrics
feature1 = iris1.values
print(feature1[:3])
label = iris2['target']
print(label[:3])

print('\n원본데이터로 SVM 분류 모델 작성')
model1 = svm.SVC(C=0.1, random_state=0).fit(feature1, label)
pred1 = model1.predict(feature1)
print('정확도 : ', metrics.accuracy_score(label, pred1)) # 0.94

print('\n차원축소데이터로 SVM 분류 모델 작성')
feature2 = iris2.values
print(feature2[:3])
print(label[:3])

model2 = svm.SVC(C=0.1, random_state=0).fit(feature2, label)
pred2 = model2.predict(feature2)
print('정확도 : ', metrics.accuracy_score(label, pred2))  # 0.9933