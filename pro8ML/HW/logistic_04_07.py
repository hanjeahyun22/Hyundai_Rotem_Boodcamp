'''
[로지스틱 분류분석 문제1]
문1] 소득 수준에 따른 외식 성향을 나타내고 있다. 주말 저녁에 외식을 하면 1, 외식을 하지 않으면 0으로 처리되었다. 
다음 데이터에 대하여 소득 수준이 외식에 영향을 미치는지 로지스틱 회귀분석을 실시하라.
키보드로 소득 수준(양의 정수)을 입력하면 외식 여부 분류 결과 출력하라.
'''

import os
os.system('cls')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("eat.csv")
# print(data.head(3))

# 외식 유무 예측할 소득 수준 입력
income = int(input('소득 수준 입력: '))

# Logistic regression 모델링
# 종속변수(y) : "외식유무"
# 독립변수(x) : "소득수준"
model = smf.logit(formula='외식유무 ~ 소득수준', data=data).fit()
print(model.summary())

# 예측
new_data = pd.DataFrame({'소득수준': [income]})
y_pred = model.predict(new_data)
print("예측된 y : \n", y_pred)       # Series 형태

print(f"\n소득 수준 {income}에 대한 외식 확률: {y_pred.values[0]}")

result = "외식함" if y_pred.values[0] > 0.5 else "외식 안 함"
print(f"분류 결과: {result}")
