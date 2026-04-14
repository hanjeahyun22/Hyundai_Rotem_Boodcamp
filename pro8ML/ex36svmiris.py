"""
SVM (Support Vector Machine) - 다중 클래스 ROC 커브 실습
--------------------------------------------------------------------------------------------------------------------------------
1. 개요: 
    - Iris 데이터를 활용하여 SVM 모델의 성능을 ROC(Receiver Operating Characteristic) 커브와 AUC(Area Under Curve)로 평가
    - 다중 클래스(3개) 문제를 해결하기 위해 One-vs-Rest(OvR) 전략과 레이블 이진화(Binarization)를 적용

2. 주요 평가 지표:
    - Micro-average: 모든 클래스의 결과를 합쳐서 전체적인 성능을 측정 (샘플 수가 다를 때 유용)
    - Macro-average: 각 클래스별 지표를 계산한 후 단순 평균 (모든 클래스를 동일한 비중으로 취급)
--------------------------------------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from itertools import cycle

# =========================================================================
# [STEP 1] 데이터 로드 및 전처리
# =========================================================================
iris = datasets.load_iris()
X = iris.data
y = iris.target
# [label_binarize 설명]
# ROC 커브는 기본적으로 이진 분류용이므로, 다중 클래스(0, 1, 2)를 
# [1,0,0], [0,1,0], [0,0,1] 형태의 이진 벡터로 변환(One-Hot Encoding과 유사)함
y = label_binarize(y, classes=[0, 1, 2]) 
n_classes = y.shape[1] # 클래스 개수 (3개)

# [데이터 확장] 학습을 어렵게 만들기 위해 가상의 노이즈 피처 추가
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]
# 데이터 분할 (학습 50% : 테스트 50%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)

# =========================================================================
# [STEP 2] 모델 생성 및 학습 (One-vs-Rest 전략)
# -------------------------------------------------------------------------
# [OneVsRestClassifier]
# - 각 클래스를 다른 모든 클래스와 구분하는 이진 분류기를 개별적으로 생성
# [SVC 옵션]
# - kernel='linear': 선형 분리 수행
# - probability=True: 확률값을 계산하여 ROC 커브 계산 시 활용
# =========================================================================
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=random_state))

# 결정 함수(Decision Function) 값을 계산하여 예측 점수 획득
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

# =========================================================================
# [STEP 3] ROC 커브 및 AUC 면적 계산
# =========================================================================
fpr = dict()
tpr = dict()
roc_auc = dict()

# 1. 클래스별 ROC/AUC 계산
for i in range(n_classes):
    # roc_curve: 실제값과 판별함수 값을 넣어 FPR, TPR 반환
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i]) 
    roc_auc[i] = auc(fpr[i], tpr[i])
# 2. Micro-average 계산 (전체 샘플 대상)
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
# 3. Macro-average 계산 (클래스별 평균)
# 모든 FPR 값들을 병합하여 고유값 추출
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# 선형 보간법(Interpolation)을 사용하여 평균 TPR 계산
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

mean_tpr /= n_classes
fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# =========================================================================
# [STEP 4] 결과 시각화 - 특정 클래스 (Class 2)
# =========================================================================
plt.figure()
lw = 2
plt.plot(fpr[2], tpr[2], color='darkorange', lw=lw, label='ROC curve of class 2 (area = %0.2f)' % roc_auc[2])
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Single Class ROC (Class 2)')
plt.legend(loc="lower right")
plt.show()

# =========================================================================
# [STEP 5] 결과 시각화 - 전체 다중 클래스 확장
# =========================================================================
plt.figure()
# Micro-average 시각화
plt.plot(fpr["micro"], tpr["micro"],
        label='micro-average ROC curve (area = {0:0.2f})'.format(roc_auc["micro"]),
        color='deeppink', linestyle=':', linewidth=4)

# Macro-average 시각화
plt.plot(fpr["macro"], tpr["macro"],
        label='macro-average ROC curve (area = {0:0.2f})'.format(roc_auc["macro"]),
        color='navy', linestyle=':', linewidth=4)

# 개별 클래스별 커브 시각화
colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
            label='ROC curve of class {0} (area = {1:0.2f})'.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Multi-class ROC Extensions')
plt.legend(loc="lower right")
plt.show()

print("SVM 다중 클래스 ROC 분석 완료")