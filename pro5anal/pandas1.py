# 터미널창 초기화
import os
os.system('cls')

# 고수준의 자료 구조(series, DataFrame)와 빠르고 쉬운 데이터 분석용 함수 제공
# 통합된 시계열 연산, 축약연산, 누락 데이터 처리, SQL, 시각화 ... 등을 제공
# Data Wrangling, Data Munging 가능

# 데이터 랭글링(Data Wrangling)의 6단계
# 1. Discovering : 데이터에 대한 깊은 이해를 하는 단계
# 2. Structuring : 필요없는 행/컬럼 삭제 및 분석 가능한 형태로 구조화하는 단계
# 3. Cleaning : 데이터 이상치 결측치를 발견하고 처리하는 단계
# 4. Enriching : 데이터를 풍부하게 하기 위한 전략을 짜는 단계
# 5. Validating : 데이터의 분포 등을 검정하는 단계
# 6. Publishing : 데이터를 분석 모델의 인풋으로 입력하는 단계

# 데이터 멍잉(Data Munging)
# 정의: 원시 데이터를 분석하기 쉬운 포맷으로 변경하는 모든 프로세스.
# 주요 작업:
# 데이터 정제(Cleaning): 결측값(Null) 처리, 이상치 제거, 형식 일치.
# 데이터 변환(Transformation): 데이터 타입 변환, 정규화, 데이터 파싱.
# 데이터 병합/결합(Merging): 여러 소스에서 온 데이터를 하나로 통합.
# 구조화(Structuring): 행과 열의 형태로 정리하여 분석 도구에 적합하게 만듦.
# 중요성: 데이터 분석 작업 시간의 대부분을 차지하며, 분석 결과의 정확성과 직결됩니다.

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# Series : 일련의 객체를 담을 수 있는 1차원 배열과 같은 자료구조로 색인(indexing)
# -->>  차원 데이터 구조 
# 쉽게 말하면 인덱스가 붙은 배열

# DataFrame :  2차원 표(Table) 형태의 자료구조
# 쉽게 말하면 여러 개의 Series가 열(Column)로 합쳐진 것

print("list를 input으로 받는 object")
obj_list = pd.Series([3, 7, -5, 4])
print(obj_list, type(obj_list))
print()

print("tuple을 input으로 받는 object")
obj_tuple = pd.Series((3, 7, -5, 4))
print(obj_tuple, type(obj_tuple))
print()

print("set은 에러 발생")
# obj_set = pd.Series({3, 7, -5, 4})
# print(obj_set)
print()

obj2 = pd.Series([3, 7, -5, 4], index=['a', 'b', 'c', 'd'])
print(obj2)
print()
print('pandas의 sum : ', obj2.sum(), '\nnumpy의 sum : ', np.sum(obj2), '\npython의 sum : ', sum(obj2))
print('\npandas의 표준편차 : ', obj2.std())
print('\nobj2.values : ', obj2.values)
print('\nobj2.index : ', obj2.index)
print("\nobj2['a'] : ", obj2['a'])                  # a번째 index의 value만 출력
print("\nobj2[['a']] : ", obj2[['a']])              # index와 value 모두 출력
print("\n인덱식 : obj2[['a', 'b']] : ", obj2[['a', 'b']])
print("\n슬라이싱 : obj2[['a':'c']] : ", obj2['a':'c'])

print(obj2[2])
print(obj2.iloc[2])
print(obj2[1:4])

print(obj2[[2, 1]])
print(obj2.iloc[[2, 1]])

print('a' in obj2)
print('k' in obj2)

print('파이썬의 Dict 자룔를 Sereies 객체로 생성')
names = {'mouse':5000, 'keyboard':250000, 'monotor':10000000}
print(names)
obj3 = Series(names)
print(obj3, ' ', type(obj3))
obj3.index=['마우스', '키보드', '모니터']
print(obj3, ' ', type(obj3))

obj3.name = "상품가격"
print(obj3)

print('\nDataFrame 객체 --------------------')
df = pd.DataFrame(obj3)
print(df, ' ', type(df))

data = {
    'irum':['홍길동', '한국인', '신기해', '공기밥', '한가해'],
    'juso':('역삼동', '신당동', '역삼동', '역삼동', '신사동'),
    'nai':[23, 25, 44, 23, 34]
}

frame = pd.DataFrame(data)
print(frame)
print()

print(frame['irum'])
print()
print(frame.irum)
print()
print(type(frame.irum))
print()

# column 순서 변경 가능 -->> 관계형 데이터 베이스의 테이블에서와 비슷.
print(DataFrame(data=data, columns=['juso', 'irum', 'nai']))

# NaN (결측치)
frame2 = pd.DataFrame(data=data, columns=['irum', 'nai', 'juso', 'tel'], index=['a', 'b', 'c', 'd', 'e'])
print(frame2)

# coloumn값 Insert/Update 가능
frame2["tel"] = "111-1111"

print(frame2)

val = pd.Series(['222-2222', '333-3333', '444-4444'], index=['b', 'c', 'e'])
print(val)
frame2['tel'] = val
print(frame2)
print()

print(frame2.T)     # 행렬 전치
print()

print(frame2.values)    # 결과는 List type
print(frame2.values[0, 1])
print(frame2.values[0:2])

# 행 삭제
frame3 = frame2.drop('d')
# frame3 = frame2.drop('d', axis=0)
print(frame3)

# 열 삭제
frame4 = frame2.drop('tel', axis=1)
print(frame4)

print('------'*10)
print(frame2)
print(frame2.sort_index)