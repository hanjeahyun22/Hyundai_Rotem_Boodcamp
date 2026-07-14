"""
[GaussianNB 문제]
독버섯(poisonous)인지 식용버섯(edible)인지 분류
feature는 중요변수를 찾아 선택, label: class
참고 : from xgboost import plot_importance
"""

# Naive Bayes 알고리즘을 이용한 분류 - mushrooms.csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
from xgboost import XGBClassifier, plot_importance
import matplotlib.pyplot as plt
import koreanize_matplotlib


print('mushrooms.csv 데이터 읽기 ----')
df = pd.read_csv("mushrooms.csv")
print(df.head(2))
print(df.shape)  # (8124, 23)

# 범주형(문자) -> 수치 데이터
for col in df.columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])

print(df.head(2))

# feature / label 분리
x = df.drop('class', axis=1)
y = df['class']
print(x.shape, y.shape) # (8124, 22) (8124,)

print('\n데이터 분리 : 학습용(train data), 검증용(test data) ----')
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, stratify=y, random_state=1
)
print(x_train.shape, x_test.shape)   # (5686, 22) (2438, 22)

# 중요 변수 찾기
print('\n중요 변수 찾기 ----')
xgb_model = XGBClassifier(
    n_estimators=50,
    max_depth=3,
    eval_metric='logloss',
    random_state=1
)
xgb_model.fit(x_train, y_train)

feat_impo = pd.DataFrame({
    'feature': x.columns,
    'importance': xgb_model.feature_importances_
}).sort_values(by='importance', ascending=False)

print(feat_impo)

# 중요한 병수 선택
top_features = feat_impo['feature'].values[:5]
print('선택한 중요 변수 5개 :', top_features)

# 중요 변수만 사용
x_train_sel = x_train[top_features]
x_test_sel = x_test[top_features]

# GaussianNB 모델 학습
print('\n분류 모델 생성 ----')
model = GaussianNB()
model.fit(x_train_sel, y_train)

# 예측 및 평가
pred = model.predict(x_test_sel)
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10].values)
# 예측값 :  [0 1 0 1 1 0 0 0 0 0]
# 실제값 :  [0 1 0 1 1 0 0 0 0 0]

print(f"총 갯수: {len(y_test)}, 오류수: {(y_test != pred).sum()}")
# 총 갯수: 2438, 오류수: 356
print('accuracy score : ', accuracy_score(y_test, pred)) # 0.854
print('confusion matrix : \n', confusion_matrix(y_test, pred))
#  [[1149  114]
#  [ 242  933]]

# 교차 검증
cv_score = cross_val_score(model, x[top_features], y, cv=5)
print('교차 검증 점수 : ', cv_score)
# [0.70276923 0.70461538 0.71630769 0.86707692 0.91502463]
print('교차 검증 평균 정확도 : ', np.mean(cv_score))
# 교차 검증 평균 정확도 :  0.7811587722622205

# 중요변수 시각화
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
plot_importance(xgb_model, ax=ax, max_num_features=10)
plt.title('버섯 데이터 중요 변수')
plt.show()

# bar그래프로 시각화
plt.figure(figsize=(10, 8))
plt.bar(feat_impo['feature'][:10], feat_impo['importance'][:10], color='b')
plt.xticks(rotation=45)
plt.xlabel('feature')
plt.ylabel('importance')
plt.title('중요 변수 상위 10개')
plt.tight_layout()
plt.show()
