import os
os.system('cls')

# ROC(Receiver OPerating Characteristic) Curve
#   모든 분류 임계값에서 분류 모델의 성능을 보여주는 그래프
#   x축 : FPR(1-특이도)
#   y축 : TPR(민감도)
#   AUC(Area Under Curve - 그래프 아래의 면적)을 이용해 모델 성능 평가
#   AUC가 클 수록, 정확히 분류
# FPR(1-특이도 : 위양성률)이 변할 때, TPR(민감도)의 변화율

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================================
#           분류용 가상 데이터 생성 (학습을 위한 데이터셋 준비)
# =========================================================================
# n_samples: 생성할 표본 데이터의 총 개수
# n_features: 독립변수(특성)의 전체 개수
# n_redundant: 다른 독립변수들의 선형 조합으로 만들어지는 중복된 특성의 개수
# x: 독립변수 데이터
# y: 종속변수(레이블) 데이터
x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=123)
print(x[:3], x.shape)
print(y[:3], y.shape)
print()
# 샘플 데이터 시각화
# plt.scatter(x[:, 0], x[:, 1])
# plt.show()


# =========================================================================
#                   Logistic Regression Modeling
# =========================================================================
model = LogisticRegression().fit(x, y)
y_hat = model.predict(x)
print("예측값(y_hat)\t", y_hat[:5])
print("실제값(y)\t", y[:5])


# =========================================================================
#                   ROC curve의 판별경계선 설정용 결정함수
# =========================================================================
f_value = model.decision_function(x)
print("f_value", f_value[:10])
print()
df = pd.DataFrame(np.vstack([f_value, y_hat, y]).T, columns=["f_value", "y_hat", "y"])
print(df.head(3))
print()

# =========================================================================
#                   모델 성능 파악
# =========================================================================
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y, y_hat))
'''
[[44  4]
[ 8 44]]
'''
# =========================================================================
#                   모델 성능 파악 및 ROC 지표 계산
# =========================================================================
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

# 혼돈 행렬(Confusion Matrix) 추출
# [[TN, FP]
#  [FN, TP]]
tn, fp, fn, tp = confusion_matrix(y, y_hat).ravel()
print(f"TN(진음성): {tn}, FP(위양성): {fp}\nFN(위음성): {fn}, TP(진양성): {tp}\n")

# 1. 정확도 (Accuracy)
#    - 전체 샘플 중 맞게 예측한 비율
#    - 공식: (TP + TN) / (TP + TN + FP + FN)
accuracy = (tp + tn) / (tp + tn + fp + fn)

# 2. 재현율 (Recall) 또는 민감도 (Sensitivity) = TPR(True Positive Rate)
#    - 실제 True인 것 중에서 모델이 True라고 예측한 비율 (놓치지 말아야 할 때 중요)
#    - 공식: TP / (TP + FN)
sensitivity = tp / (tp + fn)

# 3. 정밀도 (Precision)
#    - 모델이 True라고 예측한 것 중에서 실제 True인 비율 (정확하게 예측했는지 중요)
#    - 공식: TP / (TP + FP)
precision = tp / (tp + fp)

# 4. 특이도 (Specificity) = TNR(True Negative Rate)
#    - 실제 False인 것 중에서 모델이 False라고 예측한 비율 (정상인을 정상으로 판별)
#    - 공식: TN / (TN + FP)
specificity = tn / (tn + fp)

# 5. 위양성률 (Fall-out) = FPR(False Positive Rate)
#    - 실제 False인 것 중에서 모델이 True라고 잘못 예측한 비율 (1 - 특이도)
#    - 공식: FP / (FP + TN)
fallout = fp / (fp + tn)

print(f"정확도(Accuracy): {accuracy}\n재현율(Recall, Sensitivity): {sensitivity:.3f}")
print(f"정밀도(Precision): {precision}\n특이도(Specificity): {specificity:.3f}\n위양성률(Fall-out): {fallout:.3f}")
print()

from sklearn import metrics
acc_score = metrics.accuracy_score(y, y_hat)
print("모델 정확도 : ", acc_score)

cl_rep = metrics.classification_report(y, y_hat)
print(cl_rep)
print()


fpr, tpr, thresholds = metrics.roc_curve(y, model.decision_function(x))
print("fpr : ", fpr)
print("tpr : ", tpr)
print("thresholds : ", thresholds)  # 분류 결정 임계값(결정함수값)
print()



# =========================================================================
#                   ROC Curve 및 AUC 시각화
# =========================================================================

# ROC curve
plt.plot(fpr, tpr, 'o-', label='Logistic Regression')
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess Classification Line(AUC=0.5)')
plt.plot([fallout], [sensitivity], 'ro', ms=6)
plt.xlabel('FPR (1 - Specificity)')
plt.ylabel('TPR (Sensitivity)')
plt.title('ROC Curve')
plt.legend()
plt.grid(True)
plt.show()

# AUC
print("AUC(Area Under the Curve) : ROC 곡선 아래 면적 (1에 근접할수록 모델 성능 좋음)")
print("AUC : ", metrics.auc(fpr, tpr))