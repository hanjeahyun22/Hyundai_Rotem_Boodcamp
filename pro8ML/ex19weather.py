# Logistic Regression - Train Data / Test Data
# ex) 날씨 예보 (강수 O/X)


import os
os.system('cls')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv")
data2 = pd.DataFrame()
data2 = data.drop(["Date", "RainToday"], axis=1)
data2["RainTomorrow"] = data2["RainTomorrow"].map({"Yes": 1, "No": 0})

# 모델의 성능을 객관적으로 파악.
# 모델학습과 검증에 사용된 자료가 같으면, Overfitting 우려.
train, test = train_test_split(data2, test_size=0.3, random_state=42)

print(data2.head(3), data2.shape)
print(data2["RainTomorrow"].unique())

# 종속변수(label / class)   : RainTomorrow
# 독립변수(feature)         : 나머지 열
print("데이터 분리 : Train Data, Test Data")

# 모델 생성
col_select = "+".join(train.columns.difference(["RainTomorrow"]))
print(col_select)
my_fomula = "RainTomorrow ~ " + col_select
model = smf.logit(formula=my_fomula, data=train).fit()
print(model.summary())
print(model.params)
print()

print("예측값 : ", np.rint(model.predict(test)[:5]).values)
print("실제값 : ", test["RainTomorrow"])
print()

# 분류 정확도
conf_mat = model.pred_table()
print(conf_mat)
print("분류 정확도 : ", (conf_mat[0][0] + conf_mat[1][1]) / len(test))
print()

from sklearn.metrics import accuracy_score
pred = model.predict(test)
print("분류 정확도 : ", accuracy_score(test["RainTomorrow"], np.rint(pred)))
print()
