# Logistic Regression - 다항 분류
# ex) iris dataset

import os
os.system('cls')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler            # 표준화(Standardization)
from sklearn.preprocessing import MinMaxScaler              # 정규화(Normalization)
from sklearn import datasets

# 1. Standardization (표준화): StandardScaler
# - 데이터를 평균 0, 표준편차 1이 되도록 변환. (Z-score 정규화)
# - 이상치(Outlier)에 덜 민감하며, 데이터가 가우시안 분포(정규분포)를 따를 때 유용.

# 2. Normalization (정규화): MinMaxScaler
# - 데이터를 0과 1 사이의 범위로 변환.
# - 데이터의 최소/최대값을 알 때 유용하며, 이상치에 매우 민감함.

# softmax regression(multinomial logistic regression)
from sklearn.linear_model import LogisticRegression         #  LogisticRegression : 다중 종속변수(class / label)을 지원하도록 일반화 됨.

iris = datasets.load_iris()
print(iris.keys())
print(iris.target())
print(iris.data[:3])
print(np.corrcoef(iris.data[:, 2], iris.target[:, 3]))


# 독립변수(x) : petal length, petal width / 종속변수(y) : iris 종류
x = iris.data[:, [2, 3]] 
y = iris.target
print(x.shape, ' ', y.shape)
print(x[:3], ' ', y[:3], set(map(int, y)))

# 데이터 분리
print("\ntrain/test split (7 : 3)")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)


# Scaling : 데이터 크기 표준화 - 최적화 과정에서 안정성, 수렵속도 향상, 과적합/과소적합 방지 등의 효과
# 하지만, iris dataset은 크기의 차이가 거의 없으므로, 표준화 의미 X

# 모델 생성
print("============ 분류 모델 생성 ===============")
model = LogisticRegression(C = 0.1, solver='lbfgs', multi_class='multinomial', random_state=0)
# C : 규제 강도 (Inverse of regularization strength). 값이 작을수록 규제가 강해짐(과적합 방지)
# solver : 최적화 알고리즘 선택
#   - lbfgs : Limited-memory Broyden–Fletcher–Goldfarb–Shanno. 기본값, 다항 분류와 L2 규제에 적합
#   - liblinear : 작은 데이터셋에 적합. 다항 분류 시 OvR(One-vs-Rest) 방식 사용
# multi_class : 다중 클래스 분류 전략 설정
#   - 'multinomial': 소프트맥스 회귀를 사용하여 직접 다항 분류 수행 (클래스가 3개 이상일 때 권장)
#   - 'ovr' (One-vs-Rest): 각 클래스마다 이진 분류 모델을 만들어 결합하는 방식
#   - 'auto': solver나 데이터 특성에 따라 자동으로 선택 (기본값)
#   - lbfgs : Limited-memory Broyden–Fletcher–Goldfarb–Shanno. 기본값, 다항 분류와 L2 규제에 적합
#   - liblinear : 작은 데이터셋에 적합. 다항 분류 시 OvR(One-vs-Rest) 방식 사용
print(model)
model.fit(x_train, y_train)

# 분류 예측
y_pred = model.predict(x_test)
print("예측값 : ", y_pred)
print("실제값 : ", y_test)
print("총 갯수 : ", len(y_test), "\n오류 수 : ", (y_test != y_pred).sum())

# 분류 정확도 확인
# 방법 1) sklearn.metrics의 accuracy_score 함수 사용 : (실제값, 예측값)을 인자로 받아 정확도 계산
print("(방법1) 분류 정확도 : ", accuracy_score(y_test, y_pred))
print()

# 방법 2) confusion matrix(혼동 행렬) 사용 : 판정 테이블을 생성하여 정답 수의 합계를 전체 개수로 나눔
con_mat = pd.crosstab(y_test, y_pred, rownames=["예측값"], colnames=["관측값"])
print("(방법2) 분류 정확도 : ", (con_mat.values.diagonal().sum()) / len(y_test))
print()

# 방법 3) model.score() 사용 : (독립변수, 실제값)을 인자로 받아 내부적으로 예측 후 정확도 계산
print("(방법3) 분류 정확도 : ", model.score(x_test, y_test))
print()

# test score, train score간에 차이가 크면, overfitting 의심
print("test score : ", model.score(x_test, y_test))
print("train score : ", model.score(x_train, y_train))
print()

# 학습 후, 검증이 된 모델 저장
import joblib
joblib.dump(model, "logimodel.pkl")
del model                                       # 이미 피클 파일로 저장했으므로, 모델 삭제해도 무관
read_model = joblib.load("logimodel.pkl")       # 이 이후로는 read_model만 사용
print(read_model.predict(x_test))


# 데이터 예측
print("새로운 값으로 예측하기")
new_data = np.array[[5.5, 2.2], [0.6, 0.3], [1.1, 0.5]]
new_pred = read_model.predict(new_data)
print("예측 결과 : ", new_pred)
print(read_model.predict_proba(new_data))

# iris dataset 분류 연습용 시각화 코드
import matplotlib.pyplot as plt
import koreanize_matplotlib
from matplotlib.colors import ListedColormap

def plot_decision_regionFunc(X, y, classifier, test_idx=None, resolution=0.02, title=''):
    markers = ('s', 'x', 'o', '^', 'v')      # 마커 표시 모양 5개 정의
    colors = ('r', 'b', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    #print('cmap : ', cmap.colors[0], cmap.colors[1], cmap.colors[2])

    # decision surface 그리기
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    # xx, yy를 ravel()를 이용해 1차원 배열로 만든 후 전치행렬로 변환하여 퍼셉트론 분류기의 
    # predict()의 인자로 입력하여 계산된 예측값을 Z로 둔다.
    Z = classifier.predict(np.array([xx.ravel(), yy.ravel()]).T)
    Z = Z.reshape(xx.shape)   # Z를 reshape()을 이용해 원래 배열 모양으로 복원한다.

    # X를 xx, yy가 축인 그래프 상에 cmap을 이용해 등고선을 그림
    plt.contourf(xx, yy, Z, alpha=0.5, cmap=cmap)   
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    X_test = X[test_idx, :]
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], color=cmap(idx), marker=markers[idx], label=cl)

    if test_idx:
        X_test = X[test_idx, :]
        plt.scatter(X_test[:, 0], X_test[:, 1], c=[], linewidth=1, marker='o', s=80, label='testset')

    plt.xlabel('꽃잎 길이')
    plt.ylabel('꽃잎 너비')
    plt.legend(loc=2)
    plt.title(title)
    plt.show()

x_combined_std = np.vstack((x_train, x_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regionFunc(X=x_combined_std, y=y_combined, classifier=read_model, test_idx=range(105, 150), title='scikit-learn제공')
