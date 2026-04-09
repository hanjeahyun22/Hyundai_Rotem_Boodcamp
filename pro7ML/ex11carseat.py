# 터미널창 초기화 (Windows 환경)
import os
os.system('cls')

'''
회귀분석 문제 3)    
kaggle.com에서 carseats.csv 파일을 다운 받아 Sales 변수에 영향을 주는 변수들을 선택하여 선형회귀분석을 실시한다.
변수 선택은 모델.summary() 함수를 활용하여 타당한 변수만 임의적으로 선택한다.
회귀분석모형의 적절성을 위한 조건도 체크하시오.
완성된 모델로 Sales를 예측.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm

# 데이터 로드
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Carseats.csv")
df = df.drop([df.columns[6], df.columns[9], df.columns[10]], axis=1)

lm = smf.ols(formula="Sales ~ Income+Advertising+Price+Age", data=df).fit()
print(lm.summary())
print()

# 유의한 모델이므로 생성된 모델을 파일로 저장하고, 이를 재사용
import pickle
# piclke 파일 저장
with open("carseat.pickle", "wb") as obj:
    pickle.dump(lm, obj)

# pickle 파일 로드
# with open("carseat.pickle", "rb") as obj:
#     mymodel = pickle.load(lm, obj)
# pickle은 binary로 i/o 해야하므로, 번거로움.
import joblib
joblib.dump(lm, "carseat.model")
mymodel = joblib.load("carseat.model")
print(mymodel.summary())
print()


print("===="*20)

print("\n선형회귀 모델의 적절성 조건 체크 후, 모델 사용")
print(df.columns)       # ['Sales', 'CompPrice', 'Income', 'Advertising', 'Population', 'Price', 'Age', 'Education']
df_lm = df.iloc[:, [0, 2, 3, 5, 6]]

# residual 항 구하기
fitted = lm.predict(df_lm)
residual = df_lm.Sales - fitted
print("residual : ", residual)
print("residual mean : ", np.mean(residual))

# Q-Q plot으로 잔차의 정규성 시각화
sm.qqplot(residual, line='s')
plt.title("Q-Q Plot으로 정규성 만족 확인")
plt.show()
plt.close()

import statsmodels.api as sm
from statsmodels.stats.diagnostic import linear_reset       # linearity 확인 모듈
reset_result = linear_reset(lm, power=2, use_f=True)
print("reset_result 결과 : ", reset_result, "p_value : ", reset_result.pvalue)
print("linearity 만족" if reset_result.pvalue > 0.05 else "linearity 위배")
print()

from statsmodels.stats.diagnostic import het_breuschpagan
# Linearity 검정
bp_test = het_breuschpagan(residual, sm.add_constant(df_lm.iloc[:, 1:]))
bp_stat, bp_p_value = bp_test[0], bp_test[1]
print(f"bp_stat : {bp_stat}, bp_p_value : {bp_p_value}")
print("등분산성 만족" if bp_p_value > 0.05 else "등분산성 위배")
print()

# Durbin-Watson 검정: 잔차의 독립성(자기상관)을 확인하는 척도       -->>> model.summary()로 확인 가능
# - 0에 가까우면 양의 상관관계 (Positive Autocorrelation)
# - 4에 가까우면 음의 상관관계 (Negative Autocorrelation)
# - 2에 가까울수록 자기상관이 없는 독립성을 만족한다고 판단함.
# - 일반적으로 1.5 ~ 2.5 사이이면 독립성 가정을 만족하는 것으로 봄.
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm
residual = lm.resid
print(f"Durbin-Watson 통계량: {sm.stats.stattools.durbin_watson(residual)}")
# Durbin-Watson 통계량: 1.9314981270829592 -> residual의 자기상관은 없음.

print("다중 공선성 검정 : 다중회귀 분석 시, 두 개 이상의 독립변수 간, 강한 상관관계가 있으면 안됨.")
from statsmodels.stats.outliers_influence import variance_inflation_factor
df_ind = df[["Income", "Advertising", "Price", "Age"]]
vifdf = pd.DataFrame()
vifdf["변수"] = df_ind.columns
vifdf["vif_value"] = [variance_inflation_factor(df_ind.values, i) for i in range(df_ind.shape[1])]
print(vifdf)

# 시각화
sns.barplot(x="변수", y="vif_value", data=vifdf)
plt.title("VIF")
plt.show()
plt.close()


import joblib
joblib.dump(lm, "carseat.model")
mymodel = joblib.load("carseat.model")
print("새로운 값으로 Sales 예측")
new_df = pd.DataFrame({"Income": [35, 62], "Advertising" : [6, 3], "Price" : [105, 88], "Age" : [32, 55]})
pred = mymodel.predict(new_df)
print("Sales 예측 결과", pred.values)
print()