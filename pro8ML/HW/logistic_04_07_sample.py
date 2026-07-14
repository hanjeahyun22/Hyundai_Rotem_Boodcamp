'''
문1] 소득 수준에 따른 외식 성향을 나타내고 있다. 
주말 저녁에 외식을 하면 1, 외식을 하지 않으면 0으로 처리되었다. 
다음 데이터에 대하여 소득 수준이 외식에 영향을 미치는지 로지스틱 회귀분석을 실시하라.
키보드로 소득 수준(양의 정수)을 입력하면 외식 여부 분류 결과 출력하라.
'''
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import accuracy_score

# data 정제
df = pd.read_csv("logitest1.csv")
print(df.info())
print(df.요일.unique())
# 주말 데이터 추출
df_weekend = df[df['요일'].isin(['토', '일'])]
df_weekend.reset_index(inplace=True, drop=True)
print(df_weekend.요일.unique())     # ['토' '일']
print(df_weekend.외식유무.unique()) # [0 1] - 외식O 1, 외식X 0
print(df_weekend.head(2))

#=======================================================================================
# 모델 1 : logit()
#=======================================================================================
formula = '외식유무 ~ 소득수준'

#  logit() 모델 생성
logit_model = smf.logit(formula=formula, data=df_weekend).fit()
print(logit_model.summary())
print()

# 예측값 확인하기
logit_pred = logit_model.predict(df_weekend[:10])
print('logit_model 예측값 :',np.around(logit_pred.values)) # [1. 0. 0. 0. 1. 1. 0. 0. 1. 1.]
print('실제값 :',df_weekend['외식유무'][:10].values)       # [0 0 0 0 1 1 0 0 1 1]
print()

# logit_model 정확도 확인하기1 - accuracy_score 사용
logit_pred2 = logit_model.predict(df_weekend['소득수준'])
print('분류 정확도 :', accuracy_score(df_weekend['외식유무'], np.around(logit_pred2))) # 0.90476

# logit_model 정확도 확인하기2 - Confusion matrix 사용
conf_tab = logit_model.pred_table()
print(conf_tab)
# [[10.  1.]
# [ 1.  9.]]
print('분류 정확도 :', (conf_tab[0][0] + conf_tab[1][1]) / len(df_weekend)) # 0.9047
print()

#======================================================================================
# 모델 2 : glm()
#=====================================================================================
# glm 모델 생성
glm_model = smf.glm(formula=formula, data=df_weekend, family=sm.families.Binomial()).fit() 
print(glm_model.summary())
print()

# 예측값 확인하기
glm_pred = glm_model.predict(df_weekend['소득수준'][:10]) 
print("glm 예측값 :", np.around(glm_pred.values))    # [1. 0. 0. 0. 1. 1. 0. 0. 1. 1.]
print('실제값 :',df_weekend['외식유무'][:10].values) # [0 0 0 0 1 1 0 0 1 1]

# glm_model 정확도 확인하기 - accuracy_score 사용
glm_pred2 = glm_model.predict(df_weekend['소득수준'])
print('분류 정확도 :', accuracy_score(df_weekend['외식유무'], np.around(glm_pred2))) # 0.9047

#==================================================================================
# 입력값 예측하기
#==================================================================================
data = int(input("소득수준을 입력하세요 : "))
if not isinstance(data, int) or data < 0:
    print("0보다 작거나 정수가 아닙니다.양의 정수 값을 입력해 주세요")
else:
    newdf = pd.DataFrame({'소득수준':[data]})
    new_pred = glm_model.predict(newdf)
    if np.around(new_pred.values) == 1 :
        print('새로운 값 예측결과 :', np.around(new_pred.values))
        print("주말 저녁 외식을 합니다.")
    else:
        print('새로운 값 예측결과 :', np.around(new_pred.values))
        print("주말 저녁 외식을 안합니다.")

    
