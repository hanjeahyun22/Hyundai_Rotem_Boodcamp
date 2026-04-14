# PCA(Principle Component Analysis)
# : 선형대수 관점에서, 입력 데이터의 공분산 행렬을 eigenvalue로 분해하고,
# eigen vecor에 입력 데이터를 선형변환.
# 이 eigen vector가 PCA의 Principle Vector로서, 입력 데이터의 분산이 큰 방향을 나타냄.
# 목적 : 입력 데이터의 성질을 최대한 유지한 채로, 고차원을 저차원 데이터로 변환하는 기법
# -->> 입력데이터의 분산이 가장 큰 방향(Eigen Vector)을 찾음.

# ex) iris data로 차원 축소
import os
os.system('cls')

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
n = 10
x = iris.data[:n, :2]
print("차원 축소 전 x : \n", x, x.shape, type(x))
print(x.T)

# 시각화
plt.plot(x.T, 'o:')
plt.xticks(range(2), ["꽃받침길이", "꽃받침너비"])
plt.grid(True)
plt.legend(["표본 {}".format(i+1) for i in range(n)])
plt.title("iris 크기 특성")
plt.xlabel("특성의 종류")
plt.ylabel("특성값")
plt.xlim(-0.5, 2)
plt.ylim(2.5, 6)
plt.show()
plt.close()