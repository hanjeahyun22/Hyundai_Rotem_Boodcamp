import os
os.system("cls")

'''[문항1] 아래의 설명에 해당하는 가장 적합한 통계 용어를 적으시오.
데이터 값들이 평균으로부터 얼마나 퍼져 있는지(흩어져 있는지)를 나타내는 지표 중 하나로, 이것은 관측 값에서 평균을 뺀 값을 제곱하고, 그것을 모두 더한 후 전체 갯수로 나눠서 구한다.
즉, 차이 값의 제곱의 평균이다. 관측 값에서 평균을 뺀 값인 편차를 모두 더하면 0이 나오므로 제곱해서 더한다.
(배점:5)
'''
# 분산

'''
[문항2] 척도에 따라 통계 분석방법의 적용방식이 달라진다.
통계 처리를 위해 문자의 경우는 숫자 처리를 하게 되며, 숫자로 표현된 경우라 하더라도 무조건 사칙연산이 가능하지는 않다. 그 숫자의 의미(=척도)를 이해해야 한다.
예를 들어 남자:1, 여자:2로 표현하는 경우에 수치로 표현되었지만 1 + 1 = 2 와 같이 계산해서 남자 2명이 여자 1명과 같다는 이상한 해석결과를 얻을 수 있다.
그러므로 가능하면 비율척도나 등간척도의 형태로 자료 수집을 하는 것이 분석에 도움이 된다.
어찌되었든 자료에 대한 측정 척도는 통계 분석 방법을 결정하기 때문에 중요하다.
아래의 예는 인구조사표를 작성한 예이다. 밑줄에 가장 적당한 척도의 종류(명목, 서열, 등간, 비율)를 적으시오.
(배점:5)

id          성별              나이          가구주와관계      학력                  키(cm)
1(순서)  여(1) ______  33(2) ______  처(명목)        대졸(3) _______  175(4) _______
'''

# (1) : 명목
# (2) : 비율
# (3) : 서열
# (4) : 등간

'''

[문항3] 아래 질문 ①, ②에 답하시오.
① 실제 타겟의 클래스와 분류모형이 예측한 클래스가 서로 일치하는지 여부를 개수로 정리하여 표로 나타낸 것을 무엇이라 하는가?
② 위 표를 이용하여 정확도(accuracy)를 구하는 수식을 작성하시오.
(배점:5)
'''
# (1) : Confusion Matrix
# (2) : (TP + TN) / (TP + TN + FP + FN)


'''
[문항4] 아래의 설명에 해당하는 가장 적합한 추론통계 모델의 이름을 적으시오.
(배점:5)
예를 들어 윤희는 졸업논문으로 주택 임대료를 예측하는 모델을 작성하기로 하였다.
이 때, 주택의 면적만 고려하지 않고, 지어진지 얼마나 오래 되었는지, 지하철 역과 거리가 얼마나 가까운지 등 다양한 요소의 영향을 확인하는 것이 효과적일 것이라는 판단을 하였다.
결국 윤희는 "주택 임대료를 예측하려면 여러 개의 확률변수를 포함해야 한다." 는 결론에 다다르게 된 것이다.
방정식을 사용한다면 y = b + w1*x1 + w2*x2 + ... wn*xn 와 같이 나타낼 수 있다.
과연 윤희는 어떤 추론통계 알고리즘 모델을 사용하였을까?
'''
# 회귀 분석 모델


'''
[문항5] 기술 통계란 자료를 그래프나 숫자 등으로 요약하는 통계적 행위 및 관련 방법을 말한다.
중심경향값(분포의 중심)을 표현하는 대표값으로 평균, 중위수, 최빈값 등이 있다.
그렇다면 산포도(분포의 퍼짐정도)를 표현하는 측정치는 어떤 것들이 있는지 3가지 이상 적으시오.
(배점:5)
'''
# 범위, 분산, 표준편차

'''
[문항6] 관찰된 빈도가 기대되는 빈도와 의미 있게 다른가(적합성, 독립성, 동질성)의 여부를 검정하기 위해 사용되는 가설검정 방법이다.
이 설명에 해당되는 검정 방법의 이름을 적으시오.
(배점:5)
'''
# 카이제곱 검정

'''
[문항7] 정규성을 따르며 등간척도, 비율 척도의 수치형 데이터에 대한 상관관계분석은 아래의 종류 중 어디에 해당하는가?
1) pearson
2) spearman
3) kendall
4) fisher
(배점:5)
'''

# pearson correlation 분석

'''
활용	
[문항8] 머신러닝 분류모델을 이용해 두 개의 집단이 만들어졌다.
이 두 집단에 대해 가설검정을 한다고 할 때, 아래의 빈 칸에 적합한 용어를 적으시오.
(배점:5)
①___________ :  오류를 허용할 범위를 말하다. (95 % 신뢰수준)
②___________ :  귀무가설을 기각할 수 최소한의 확률 값을 말한다.
이들을 통해 해당 귀무가설을 채택/기각할 수 있다.
'''

# (1) : alpha(오류 허용 범위)
# (2) : p-value


'''
[문항9] 범생이 진원이와 수진이는 모델 준비 작업으로 아래와 같은 데이터를 준비하였다.
과연 이들은 빈 칸에 Numpy가 지원하는 함수의 이름을 무엇이라 적었을까?
(배점:5)
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 7]
print(‘공분산 : ‘, np.①___________(x, y))
print(‘상관계수: ‘, np.②______________(x, y))
'''
# (1) : cov
# (2) : corrcoef
import numpy as np
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 7]
print('공분산 : ', np.cov(x, y))
print('상관계수: ', np.corrcoef(x, y))

'''
[문항10] 표준화(standardization)는 각 관찰값이 평균에서의 이탈 정도를 표준편차 단위로 환산하여,
스케일이 다른 변수들 간 비교를 가능하게 하는 변환이다. 표준화의 수식을 쓰시오.
(배점:5)
'''
# (x_origin_data - mu_mean) / sigma_standard_deviation

'''
[문항11] 아래 지문의 빈칸에 가장 알맞는 용어를 적으시오.
(배점:10)
앙상블 기법의 ②_________은 training dataset을 만들어 그냥 계속 가지고 있는 반면, ①________은 training dataset을 만든 후에 업데이트 및 조정하는 과정이 추가가 된다.
모델의 성능면에서는 ①_________이 우수하나, 과적합이 우려스럽다면 ②_________을 사용하는 좋을 것 같다.
'''
# (1) : Boosting
# (2) : Bagging

'''
	
[문항12] 에이콘 기업에서 행정직 직원들의 '지각횟수'와 '판매횟수' 간에 관계가 있는지 알아보려고 한다.
직원 5명을 대상으로 한 달 동안 '지각횟수'와 '판매횟수'를 조사했더니 아래와 같은 결과를 얻었다.
둘 사이의 상관계수를 출력하고 상관관계가 있는지 설명하시오.
(배점:10)
지각횟수(x) = 1,2,3,4,5
판매횟수(y) = 8,7,6,4,5

import numpy as np
'''
x = [1, 2, 3, 4, 5]
y = [8, 7, 6, 4, 5]
print('상관계수: \n', np.corrcoef(x, y))
# 상관계수: 
#  [[ 1.  -0.9]
#  [-0.9  1. ]]

# --> r이 -1에 근접하므로, 음의 상관관계, 즉 x와 y가 반비례 관계에 있음

'''
[문항13] 다음 데이터는 어느 교육센터에서 실시하고 있는 파이썬 과정 중 두 명의 강사에 따른 성적에 대한 자료이다.
강사에 따라 성적에 차이가 있는지 평균 차이 검정을 하시오.
(배점:10)
강사1 : 71 58 92 78 71 68 67 88 88 60 80 70 68 82 78
강사2 : 50 65 75 91 67 39 81 68 97 86 66 60 65 55 58

① 귀무가설 : 
② 대립가설 :
③ 검정을 위한 소스 코드
'''
# (1) 귀무가설 : 강사에 따른 성적은 차이가 없다.
# (2) 대립가설 : 강사에 따른 성적은 차이가 있다.
# (3)

import numpy as np
import scipy.stats as stats
score_1 = [71, 58, 92, 78, 71, 68, 67, 88, 88, 60, 80, 70, 68, 82, 78]
score_2 = [50, 65, 75, 91, 67, 39, 81, 68, 97, 86, 66, 60, 65, 55, 58]

t_stat, p = stats.ttest_ind(score_1, score_2)
print("통계량 : ",t_stat)
print("p_value : ",p)
# 통계량 :  1.3273661364910396
# p_value :  0.19510952906686385    -->> p_value > 0.05     -->>    귀무가설 채택
# -->> 강사에 따른 성적은 차이가 없다.

'''
	
[문항14] titanic data를 사용하여 아래의 지시문에 따라 의사결정나무분류 모델을 작성하고 결과를 출력하시오.
(배점:10)
import pandas as pd
data = pd.read_csv('titanic_data.csv', usecols=['Survived', 'Pclass', 'Sex', 'Age','Fare'])
print(data.head(2), data.shape)    # (891, 12)
data.loc[data["Sex"] == "male","Sex"] = 0
data.loc[data["Sex"] == "female", "Sex"] = 1
print(data["Sex"].head(2))
print(data.columns)

feature = data[["Pclass", "Sex", "Fare"]]
label = data["Survived"]

이하 소스 코드를 적으시오.
1) train_test_split (7:3), random_state=12
2) 의사결정나무 클래스를 사용해 분류 모델 작성
3) 예측결과로 분류 정확도를 출력
'''
import pandas as pd
data = pd.read_csv('titanic_data.csv', usecols=['Survived', 'Pclass', 'Sex', 'Age','Fare'])
print(data.head(2), data.shape)    # (891, 12)
data.loc[data["Sex"] == "male","Sex"] = 0
data.loc[data["Sex"] == "female", "Sex"] = 1
print(data["Sex"].head(2))
print(data.columns)

feature = data[["Pclass", "Sex", "Fare"]]
label = data["Survived"]

# 1) train_test_split (7:3), random_state=12
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(feature, label, test_size=0.3, random_state=12)
print("훈련 feature : \n", x_train[:2])
print("훈련 label : \n", y_train[:2])

# 훈련 feature : 
#       Pclass Sex    Fare
# 832       3   0   7.2292
# 391       3   0   7.7958    

# 훈련 label : 
# 832    0
# 391    1
# Name: Survived, dtype: int64


# 2) 의사결정나무 클래스를 사용해 분류 모델 작성
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(x_train, y_train)
pred = model.predict(x_test)
print("예측 모델 : \n", pred[:5])
# 예측 모델 : 
#  [1 0 0 0 0]


# 3) 예측결과로 분류 정확도를 출력
from sklearn.metrics import accuracy_score
print("분류 정확도 : ", accuracy_score(y_test, pred))
# 분류 정확도 :  0.7798507462686567         -->>  예측 모델이 약 80% 정확도를 가짐


'''
[문항15] https://www.kaggle.com/c/bike-sharing-demand/data 에서 train.csv를 다운받아 bike_dataset.csv 으로 파일명을 변경한다.
이 데이터는 어느 지역의 2011년 1월 ~ 2012년 12월 까지 날짜/시간. 기온, 습도, 풍속 등의 정보를 바탕으로 1시간 간격의 자전거 대여횟수가 기록되어 있다.
train / test로 분류 한 후 대여횟수에 중요도가 높은 칼럼을 판단하여 feature를 선택한 후, 대여횟수에 대한 회귀 예측(RandomForestRegressor)을 하시오.
(배점:10)
칼럼 정보 :
'datetime', 'season'(사계절:1,2,3,4),  'holiday'(공휴일(1)과 평일(0)), 'workingday'(근무일(1)과 비근무일(0)),
'weather'(4종류:Clear(1), Mist(2), Snow or Rain(3), Heavy Rain(4)),
'temp'(섭씨온도), 'atemp'(체감온도), 'humidity'(습도), 'windspeed'(풍속),
'casual'(비회원 대여량), 'registered'(회원 대여량), 'count'(총대여량)
참고 : casual + registered 가 count 임.

출력 사항 : 예측값 / 실제값, 결정계수, 예측 결과
'''
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# 데이터 로드
df = pd.read_csv("bike_dataset.csv")
# print(df.head(2))
#               datetime  season  holiday  workingday  weather  temp   atemp  humidity  windspeed  casual  registered  count
# 0  2011-01-01 00:00:00       1        0           0        1  9.84  14.395        81        0.0       3          13     16
# 1  2011-01-01 01:00:00       1        0           0        1  9.02  13.635        80        0.0       8          32     40

# feature, label 분리
x = df.drop(["datetime","casual", "registered", "count"], axis=1)
y = df["count"]

# 훈련 / 테스트 데이터 생성
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# RandomForest 회귀 모델 생성 -->> n_estimators=100 임의 설정
rf_model = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1)
rf_model.fit(x_train, y_train)

importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

ranking = pd.DataFrame({
    "feature": x.columns[indices],
    "importance": importances[indices]
})
print("feature 중요도 : \n", ranking)
#       feature  importance
# 0    humidity    0.256634
# 1       atemp    0.234963
# 2   windspeed    0.193771
# 3        temp    0.144183
# 4      season    0.070292
# 5     weather    0.051554
# 6  workingday    0.042182
# 7     holiday    0.006422

# 중요특성 5개(["feature", "humidity", "atemp", "windspeed", "temp"]) 로 다시 RandomForest 모델링
rf_model2 = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1)
rf_model2.fit(x_train[["humidity", "atemp", "windspeed", "temp"]], y_train)

# 예측 및 성능 평가
y_pred = rf_model2.predict(x_test[["humidity", "atemp", "windspeed", "temp"]])
print(f"예측값(샘플 5개): {np.round(y_pred[:5], 3)}")
print(f"실제값(샘플 5개): {np.array(y_test[:5])}")

print(f"\nMSE (평균 제곱 오차) : {mean_squared_error(y_test, y_pred):.4f}")
print(f"R2 Score (결정 계수) : {r2_score(y_test, y_pred):.4f}")
# MSE (평균 제곱 오차) : 29495.2609
# R2 Score (결정 계수) : 0.1123     -->>  11%의 신뢰도이므로, 좋지 않은 회귀 모델