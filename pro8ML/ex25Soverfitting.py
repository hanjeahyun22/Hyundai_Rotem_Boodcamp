import os
os.system('cls')

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score

# ================================================================================================================================
# [공통] 데이터 로드 및 모델 초기화
# ================================================================================================================================
iris = sns.load_dataset('iris')
features = iris.drop('species', axis=1).values  # 독립변수 (4개 특성)
label = iris['species'].values                  # 종속변수 (붓꽃 종류)

# 의사결정나무 모델 생성
dt_clf2 = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=12)
print(f"전체 데이터 크기: {features.shape[0]}")


# ================================================================================================================================
# [방법 1] Train/Test Split (데이터 분할)
# 1. 목적: 모델이 학습하지 않은 '새로운 데이터'에 대해 얼마나 잘 작동하는지(일반화 성능)를 확인하기 위함
# 2. 원리: 전체 데이터를 학습용(Train)과 평가용(Test)으로 분리하여, 학습 시에는 평가 데이터를 절대 보지 못하게 함
# 3. 특징: 가장 기본적인 과적합 방지 및 성능 평가 방법임
# ================================================================================================================================
from sklearn.model_selection import train_test_split

print("\n" + "="*50)
print("1. Train/Test Split을 이용한 과적합 방지")
print("="*50)

# 데이터를 8:2 비율로 분할
x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=12)

dt_clf2.fit(x_train, y_train)
train_acc = accuracy_score(y_train, dt_clf2.predict(x_train))
pred = dt_clf2.predict(x_test)
test_acc = accuracy_score(y_test, pred)

print(f"학습 데이터 정확도: {train_acc:.4f}")
print(f"테스트 데이터 정확도: {test_acc:.4f}")
print("※ 두 정확도의 차이가 크면 과적합(Overfitting)을 의심해야 함")
print("="*50)

# ================================================================================================================================
# [방법 2] K-fold Cross Validation (K-폴드 교차 검증)
# 1. 목적: 데이터 편향을 방지하고 모델의 일반화 성능을 객관적으로 평가하기 위함 (과적합 방지)
# 2. 원리: 전체 데이터를 K개의 데이터 폴드 세트로 나누고, K번만큼 학습과 검증 평가를 반복 수행
# 3. 장점: 모든 데이터를 학습과 검증에 사용할 수 있어 데이터 부족 문제를 보완함
# ================================================================================================================================
from sklearn.model_selection import KFold

# 5개의 폴드 세트로 분리하는 KFold 객체 생성
kfold = KFold(n_splits=5) 
cv_accuracy = []  # 각 폴드별 정확도를 저장할 리스트

print("\n" + "="*50)
print("2. K-Fold 교차 검증 시작 (5-Fold)")
print("="*50)

n_iter = 0
# kfold.split()은 학습용/검증용 데이터의 '인덱스'를 반환함
for train_index, test_index in kfold.split(features):
    
    # 인덱스를 이용해 실제 데이터 추출
    x_train, x_test = features[train_index], features[test_index]
    y_train, y_test = label[train_index], label[test_index]
    dt_clf2.fit(x_train, y_train)
    pred = dt_clf2.predict(x_test)
    n_iter += 1

    # 반복할 때 마다 정확도 출력
    accuracy = np.round(accuracy_score(y_test, pred), 5)

    train_size = x_train.shape[0]
    test_size = x_test.shape[0]
    print(f"반복 수 : {n_iter}, 교차검증 정확도 : {accuracy}, 학습 데이터 크기 : {train_size}, 검증 데이터 크기 : {test_size}")
    # print(f"검증 세트 인덱스 : {test_index}") # 검증에 사용된 행 번호 확인 시 주석 해제
    cv_accuracy.append(accuracy)

print("="*50)
print(f"각 폴드별 정확도: {np.array(cv_accuracy).astype(float)}")
print(f"최종 평균 검증 정확도: {np.mean(cv_accuracy)}")
print("="*50)


# ================================================================================================================================
# [방법 2-1] Stratified K-fold Cross Validation
# 1. 목적: 불균형한 분포를 가진 레이블(결정 클래스) 데이터 집합을 위한 K-폴드 방식
# 2. 원리: 학습 데이터와 검증 데이터 세트가 가지는 레이블 분포도가 유사하도록 데이터를 분할함
# 3. 특징: 분류(Classification) 모델에서 특정 레이블이 너무 적거나 편중되어 있을 때 반드시 사용해야 함
# ================================================================================================================================
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=3)
n_iter = 0
cv_accuracy = []

print("\n" + "="*50)
print("3. Stratified K-Fold 교차 검증 시작 (3-Fold)")
print("="*50)

for train_index, test_index in skf.split(features, label): # 레이블 데이터(label)가 반드시 인자로 들어가야 함
    n_iter += 1
    x_train, x_test = features[train_index], features[test_index]
    y_train, y_test = label[train_index], label[test_index]
    
    dt_clf2.fit(x_train, y_train)
    pred = dt_clf2.predict(x_test)
    
    accuracy = np.round(accuracy_score(y_test, pred), 4)
    cv_accuracy.append(accuracy)
    print(f"반복 {n_iter} : 정확도 {accuracy}, 학습 데이터 크기 {x_train.shape[0]}, 검증 데이터 크기 {x_test.shape[0]}")

print("="*50)
print(f"최종 평균 검증 정확도: {np.mean(cv_accuracy)}")
print("="*50)


# ================================================================================================================================
# [방법 2-2] cross_val_score
# 1. 목적: KFold의 일련의 과정을 한꺼번에 수행해주는 API (폴드 세트 설정, 반복 학습/검증, 성능 지표 반환)
# 2. 특징: 내부적으로 Stratified K-Fold 방식을 사용함 (분류 모델일 경우)
# ================================================================================================================================
from sklearn.model_selection import cross_val_score

print("\n" + "="*50)
print("4. cross_val_score를 이용한 교차 검증 (cv=5)")
print("="*50)

# cross_val_score(모델, 피처셋, 레이블셋, scoring='평가지표', cv=폴드수)
scores = cross_val_score(dt_clf2, features, label, scoring='accuracy', cv=5)

print(f"교차 검증별 정확도: {np.round(scores, 4)}")
print(f"평균 검증 정확도: {np.round(np.mean(scores), 4)}")
print("="*50)

# ================================================================================================================================
# [방법 3] GridSearchCV (격자 탐색)
# 1. 목적: 모델의 성능을 최적화하기 위해 하이퍼파라미터(Hyperparameter)의 최적 조합을 자동으로 찾아줌
# 2. 원리: 사용자가 지정한 여러 파라미터 값들을 격자(Grid) 형태로 조합하여 모두 학습/평가해보고 최상의 결과를 반환
# 3. 특징: 교차 검증(Cross Validation)을 기반으로 하므로, 데이터 편향 없이 안정적인 최적 파라미터를 찾을 수 있음
# 4. 주요 속성:
#    - param_grid: 탐색할 파라미터 명칭과 값들을 딕셔너리 형태로 설정
#    - best_params_: 학습 후 찾아낸 최적의 파라미터 조합
#    - best_score_: 최적 파라미터일 때의 평균 정확도
# ================================================================================================================================
from sklearn.model_selection import GridSearchCV

print("\n" + "="*50)
print("5. GridSearchCV를 이용한 하이퍼파라미터 최적화")
print("="*50)

# 1. 하이퍼파라미터 후보군 설정 (딕셔너리 형태)
# max_depth: 트리의 최대 깊이
# min_samples_split: 노드 분할을 위한 최소 샘플 수 (과적합 제어용)
# min_samples_leaf: 리프 노드가 되기 위한 최소 샘플 수
# criterion: 불순도 측정 지표 ('gini' 또는 'entropy')
# max_features: 최적의 분할을 위해 고려할 특성(Feature)의 수
# splitter: 각 노드에서 분할을 선택하는 전략 ('best' 또는 'random')
parameters = {'max_depth': [1, 2, 3], 'min_samples_split': [2, 3]}

# 2. GridSearchCV 객체 생성
# refit=True: 최적의 파라미터로 모델을 재학습시킴 (기본값) : 내부적으로 cv를 설정한 개수만큼 생성 후, 이를 실행시켜, 최적의 파라미터 출력
grid_dtree = GridSearchCV(estimator=dt_clf2, param_grid=parameters, cv=3, refit=True)

# 3. 학습 및 최적 파라미터 탐색
grid_dtree.fit(features, label)

# 4. 결과 출력
print(f"최적 파라미터: {grid_dtree.best_params_}")
print(f"최고 정확도: {grid_dtree.best_score_}")

# 5. 상세 결과 확인 (DataFrame 변환)
scores_df = pd.DataFrame(grid_dtree.cv_results_)
print("\n[상세 파라미터별 성능 결과]")
print(scores_df[['params', 'mean_test_score', 'rank_test_score']])

# 6. 최적의 모델(Best Estimator) 꺼내어 예측하기
best_model = grid_dtree.best_estimator_

# 가상의 데이터로 예측 테스트
new_sample = [[5.1, 3.5, 1.4, 0.2]] # setosa 샘플 데이터
best_pred = best_model.predict(new_sample)
print(f"\n새로운 데이터 예측 결과: {best_pred}")
print("="*50)