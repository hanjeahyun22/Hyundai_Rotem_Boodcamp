'''
[로지스틱 분류분석 문제2] 
게임, TV 시청 데이터로 안경 착용 유무를 분류하시오.
안경 : 값0(착용X), 값1(착용O)
예제 파일 : https://github.com/pykwon  ==>  bodycheck.csv
새로운 데이터(키보드로 입력)로 분류 확인. 스케일링X
''' 

import os
os.system('cls')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler            # 표준화(Standardization)
from sklearn.preprocessing import MinMaxScaler              # 정규화(Normalization)
from sklearn.linear_model import LogisticRegression

# =========================================================================
#                               데이터 생성
# =========================================================================
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/bodycheck.csv")
print(data.head(3))
'''
번호  게임   신장  체중  TV시청  안경유무
0   1   2  146  34     2     0
1   2   6  169  57     3     1
2   3   9  160  48     3     1
'''

# =========================================================================
#                               변수 선언
# =========================================================================
# 독립변수 : TV 시청
# 종속변수 : 안경 착용 유무
x = data[["게임", "TV시청"]]
y = data["안경유무"]

# =========================================================================
#                               Train/Test 데이터 분리
# =========================================================================
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# =========================================================================
#                               Scaling
# =========================================================================
# 독립변수(x)만 정규화
scaler = StandardScaler()
x_train_s = scaler.fit_transform(x_train)
x_test_s = scaler.transform(x_test)

# =========================================================================
#                               regression 모델 생성
# =========================================================================
model = LogisticRegression(C = 0.1, solver='lbfgs', random_state=0)
model.fit(x_train_s, y_train)

# =========================================================================
#                               분류 예측
# =========================================================================
y_pred = model.predict(x_test_s)
print("예측값 : ", y_pred)
print("실제값 : ", y_test.values)
print("총 갯수 : ", len(y_test), "\n오류 수 : ", (y_test != y_pred).sum())

# =========================================================================
#                               분류 정확도 확인
# =========================================================================
# sklearn.metrics의 accuracy_score 함수 사용 : (실제값, 예측값)을 인자로 받아 정확도 계산
print("분류 정확도 : ", accuracy_score(y_test, y_pred))
print()

# =========================================================================
#                               새로운 데이터 예측
# =========================================================================
try:
    new_game = float(input("게임 시간을 입력하세요: "))
    new_tv = float(input("TV 시청 시간을 입력하세요: "))
    
    # 새로운 데이터도 학습 때 사용한 scaler로 반드시 transform 해야 함
    new_data = pd.DataFrame([[new_game, new_tv]], columns=["게임", "TV시청"])
    new_data_s = scaler.transform(new_data)
    
    new_pred = model.predict(new_data_s)
    result = "안경 착용" if new_pred[0] == 1 else "안경 미착용"
    print(f"분류 결과: {result} (예측값: {new_pred[0]})")
except Exception as e:
    print("입력 오류:", e)



'''
[로지스틱 분류분석 문제3]
Kaggle.com의 https://www.kaggle.com/truesight/advertisingcsv  file을 사용
얘를 사용해도 됨   'testdata/advertisement.csv' 
참여 칼럼 : 
    - Daily Time Spent on Site : 사이트 이용 시간 (분)
    - Age : 나이,
    - Area Income : 지역 소득,
    - Daily Internet Usage :일별 인터넷 사용량(분),
    - Clicked Ad : 광고 클릭 여부 ( 0 : 클릭x , 1 : 클릭o )
광고를 클릭('Clicked on Ad')할 가능성이 높은 사용자 분류.
데이터 간 단위가 큰 경우 표준화 작업을 시도한다.
모델 성능 출력 : 정확도, 정밀도, 재현율, ROC 커브와 AUC 출력
새로운 데이터로 분류 작업을 진행해 본다.
'''
