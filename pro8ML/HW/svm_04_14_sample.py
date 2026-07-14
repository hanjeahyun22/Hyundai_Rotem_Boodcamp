import pandas as pd
import numpy as np
from sklearn import svm,metrics
from sklearn.model_selection import train_test_split

''' 흉부외과 환자 303명을 관찰한 데이터다. 

각 환자의 나이, 성별, 검진 정보 컬럼 13개와 마지막 AHD 칼럼에 각 환자들이 심장병이 있는지 여부가 기록되어 있다. 

dataset에 대해 학습을 위한 train과 test로 구분하고 분류 모델을 만들어, 모델 객체를 호출할 경우 정확한 확률을 확인하시오. 

임의의 값을 넣어 분류 결과를 확인하시오.     

정확도가 예상보다 적게 나올 수 있음에 실망하지 말자. ㅎㅎ
feature 칼럼 : 문자 데이터 칼럼은 제외

label 칼럼 : AHD(중증 심장질환)'''

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Heart.csv')
print(df.head(2))
print(df.info())
# "","Age","Sex","ChestPain","RestBP","Chol","Fbs","RestECG","MaxHR","ExAng","Oldpeak","Slope","Ca","Thal","AHD"



# 칼럼 feature랑 label이랑 분리
label = df.AHD
feat=df.iloc[:,1:-1]
# print(feat.head(2))
# print(feat.shape)
# print(label.shape)

# pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
# pd.set_option('display.width', None)        # 너비 제한 해제
# pd.set_option('display.max_colwidth', None) # 긴 값도 잘리지 않음

# des=df.describe()
# print(df['ChestPain'].unique())
# print(df['Thal'].unique())

feat.drop('ChestPain',axis=1,inplace=True)
feat.drop('Thal',axis=1,inplace=True)
print(feat.shape)

print(label.unique())
label=label.map({'No':0,'Yes':1})
print(label.unique())


# 정규화

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
feat=scaler.fit_transform(feat)
# print(pd.DataFrame(feat).describe())

na= pd.DataFrame(feat)
print(na.isna().sum())
# Ca결측치 4개


feat= pd.DataFrame(feat)
feat.iloc[:,10]=feat.iloc[:,10].fillna(feat.iloc[:,10].mean())
print(feat.isna().sum())


# 데이터 나누기
x_train,x_test,y_train,y_test=train_test_split(feat,label,test_size=0.2,random_state=12)
print(x_train.shape, x_test.shape)


smodel=svm.SVC(C=0.01, kernel='rbf').fit(x_train,y_train) 
pred=smodel.predict(x_test)

print('실제: ',y_test[:5])
print('예측: ',pred[:5])

score=metrics.accuracy_score(y_test,pred)
print(f'총 갯수:{len(y_test)}, 오류수:{(y_test != pred).sum()}')

print(f'분류 정확도 확인 :{score}')