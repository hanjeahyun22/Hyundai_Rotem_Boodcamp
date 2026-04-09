# 참여 칼럼 : 
#    - Daily Time Spent on Site : 사이트 이용 시간 (분)
#    - Age : 나이,
#    - Area Income : 지역 소득,
#    - Daily Internet Usage :일별 인터넷 사용량(분),
#    - Clicked Ad : 광고 클릭 여부 ( 0 : 클릭x , 1 : 클릭o )
# 광고를 클릭('Clicked on Ad')할 가능성이 높은 사용자 분류.
# 데이터 간 단위가 큰 경우 표준화 작업을 시도한다.
# 모델 성능 출력 : 정확도, 정밀도, 재현율, ROC 커브와 AUC 출력
# 새로운 데이터로 분류 작업을 진행해 본다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/advertisement.csv')

print(df.head())
print(df.info())

df = df[['Daily Time Spent on Site', 'Age', 'Area Income',
        'Daily Internet Usage', 'Clicked on Ad']]

# X / y 분리
X = df.drop('Clicked on Ad', axis=1)
y = df['Clicked on Ad']

# train / test 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 표준화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 모델 학습
model = LogisticRegression()
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# 성능 평가
acc = metrics.accuracy_score(y_test, y_pred)
pre = metrics.precision_score(y_test, y_pred)
rec = metrics.recall_score(y_test, y_pred)

print("정확도:", acc)
print("정밀도:", pre)
print("재현율:", rec)
print(metrics.confusion_matrix(y_test, y_pred))

print("\n--- Classification Report ---")
print(metrics.classification_report(y_test, y_pred))

# 시각화
fpr, tpr, thresholds = metrics.roc_curve(y_test, y_prob)
roc_auc = metrics.auc(fpr, tpr)

print("AUC:", roc_auc)

plt.plot(fpr, tpr, label='LogisticRegression (AUC = %.3f)' % roc_auc)
plt.plot([0,1], [0,1], 'k--', label='Random (AUC=0.5)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

# 예측
new_data = [[70, 30, 60000, 200]]

new_data_scaled = scaler.transform(new_data)

pred = model.predict(new_data_scaled)

print("예측: ", pred[0])