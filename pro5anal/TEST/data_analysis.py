# 터미널창 초기화
import os
os.system('cls')

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import urllib
# BeautofulSoup 객체를 이용한 웹 문서 처리
import requests
from bs4 import BeautifulSoup
import MySQLdb

'''
[문항1] 아래와 같은 numpy 배열을 작성하였다. "실행결과"와 같이 보일 수 있도록 아래의 빈칸에 적당한 배열 슬라이싱을 적으시오.
주의 : 수업 시간에 설명한 내용과 상이한 코드를 적으면 0점. 예를 들어 np.flip() 함수 사용 X.
(배점:5)
import numpy as np
data = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
print(___________________________)

실행결과 :
[[16 15 14 13]
[12 11 10  9]
[ 8  7  6  5]
[ 4  3  2  1]]
'''

# data = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
# print(data[::-1,::-1])

'''
[문항2] 네이버 사이트가 제공하는 실시간 인기 검색어 자료를 읽어, 사람들에게 관심 있는 주제는 무엇인지 알아보려 한다.
title을 얻기 위해 ol tag 내의 li tag 값을 얻기 위한 코드를 작성하였다.
프로그램이 제대로 수행될 수 있도록 아래의 빈 칸을 채우시오.
(배점:5)
try:
    url = "http://www.naver.com"
    page = urllib.request.urlopen(url)
        
    soup = BeautifulSoup(page.read(), "1)___________") 
    title = soup.2)_____.find_all('li')
    for i in range(0, 10):
            print(str(i + 1) + ") " + title[i].a['title'])
3)_________ Exception as e:
    print('에러:', e)
'''

# try:
#     url = "http://www.naver.com"
#     page = urllib.request.urlopen(url)
        
#     soup = BeautifulSoup(page.read(), "html.parser") 
#     title = soup.find("ol").find_all('li')
#     # title = soup.2)_____.find_all('li')
#     for i in range(0, 10):
#             print(str(i + 1) + ") " + title[i].a['title'])
# except Exception as e:
#     print('에러:', e)

"""

[문항3] sqlite3 DB를 사용하여 DataFrame의 자료를 db에 저장하려 한다. 아래의 빈칸에 알맞은 코드를 적으시오.
조건 : index는 저장에서 제외한다.
(배점:5)
data = {
    'product':['아메리카노','카페라떼','카페모카'],
    'maker':['스벅','이디아','엔젤리너스'],
    'price':[5000,5500,6000]
}

df = pd.DataFrame(data)
df.①__________('test', conn, if_exists='append', ②________________)
"""
# data = {
#     'product':['아메리카노','카페라떼','카페모카'],
#     'maker':['스벅','이디아','엔젤리너스'],
#     'price':[5000,5500,6000]
# }
# df = pd.DataFrame(data)
# df.to_sql('test', conn, if_exists='append', index=False)

"""
[문항4] DataFrame의 결과가 아래와 같이 출력 되었다. 밑줄과 [ ] 안에 필요한 코드를 작성하시오.

강남 강북 서초
1월 0 1 2
2월 3 4 5
3월 6 7 8
4월 9 10 11
(배점:5)
DataFrame(np.arange(12).reshape((__, __)), _______=[              ],  _______ = [            ])
"""

# pd.DataFrame(np.arange(12).reshape((4,3)), columns=["강남", "강북", "서초"], index=["1월", "2월", "3월", "4월"])

"""
[문항5] matplotlib.pyplot을 사용해 그래프를 그리는 과정에서, plt.plot(), plt.title() 등의 함수는
그래프 요소를 백그라운드에 누적시키는 역할을 한다.
하지만 실제로 이 누적된 결과가 화면에 렌더링되어 사용자에게 시각적으로 표시되기 위해서는
반드시 마지막에 __________ 함수를 호출해야 한다.
빈칸에 가장 적당한 matplotlib가 지원하는 함수를 적으시오.
(배점:5)
"""
# plt.show()

"""
[문항6] pandas 모듈을 이용하여 DataFrame 객체 타입의 데이터를 "test.csv" 파일로 저장하려 한다.
index와 header는 저장 작업에서 제외한다. 아래의 소스 코드를 순서대로 완성하시오.
(배점:5)
data = DataFrame(items)
data.to_csv(              , index=        , header=          )
"""
# data = DataFrame(items)
# data.to_csv("test.csv", index=False, header=False)


"""
[문항7] 아래의 DataFrame에 대해 "실행결과 1" 이 나오도록 빈칸 ①에 적당한 명령문을 적으시오.
또한 열 삭제를 한 후 새로운 DataFrame type의 frame2를 만드는 명령을 빈칸 ②에 적으시오.

"실행결과 2" 와 같이 결과가 보일 수 있도록 한다.
(배점:5)
from pandas import DataFrame
frame = DataFrame({'bun':[1,2,3,4], 'irum':['aa','bb','cc','dd']}, index=['a','b', 'c','d'])
print(①___________)
frame2 = ②__________________    # 인덱스가 'd'인 행 삭제
print(frame2)

실행결과 1 :
        a  b  c  d
bun    1  2  3  4
irum  aa  bb  cc  dd

실행결과 2 :
    bun irum
a    1  aa
b    2  bb
c    3  cc
"""
# frame = pd.DataFrame({'bun':[1,2,3,4], 'irum':['aa','bb','cc','dd']}, index=['a','b', 'c','d'])
# print(frame.T)
# frame2 = frame.drop('d')
# print(frame2)

"""
[문항8] 하드 디스크에 저장된 "ex.csv" 파일을 읽어 칼럼명이 있는 Dataframe type의 자료를 얻으려고 한다.
판다스의 csv 파일 읽기 전용 함수를 사용하여 읽을 수 있도록 할 예정이다.
칼럼명은 a, b, c, d라고 하겠다. 아래의 빈칸에 적당한 소스 코드를 적으시오.
(배점:5)
--- 현재 모듈과 같은 경로에 ex.csv 파일의 내용은 다음과 같다. ----
1,2,3,4
5,6,7,8

import pandas as pd
df = ①________________(②___________ , ③___________________________) 
"""
# df = pd.read_csv("ex.csv", names=["a", "b", "c", "d"])


"""
[문항9] 다음과 같은 DataFrame이 있을 때, juso 컬럼의 문자열을 분리하여 0번째 요소만 추출하고, 
이를 Series로 반환하는 코드를 작성하시오. 빈칸(_____)에 들어갈 코드를 완성하시오.
(배점:5)
data = {
    'juso':['강남구 역삼동', '중구 신당동', '강남구 대치동'],
    'inwon':[23, 25, 15]
}
df = DataFrame(data)
results = ①________([x.split()[0] for x in ②_______.juso])
print(results)

출력 결과 :
0    강남구
1    중구
2    강남구
dtype: object
"""
# data = {
#     'juso':['강남구 역삼동', '중구 신당동', '강남구 대치동'],
#     'inwon':[23, 25, 15]
# }
# df = pd.DataFrame(data)
# results = pd.Series([x.split()[0] for x in df.juso])
# print(results)


"""
	
[문항10] 크기가 다른 두 NumPy 배열 x, y에 대해 아래 연산 결과가 출력된다.
이와 같이 서로 다른 shape의 배열 간 연산 시 자동으로 크기가 맞춰지는 현상을 무엇이라고 하는가? 
(용어를 적으시오)

x = np.array([1,2,3,4,5])
y = np.arange(1, 4).reshape(3, 1)
print(x + y)

연산결과
[[2 3 4 5 6]
[3 4 5 6 7]
[4 5 6 7 8]]
(배점:5)
"""
# BroadCasting

"""

[문항11] MariaDb에 저장된 jikwon 테이블을 사용한다.
담당 고객이 없는 직원의 수, 연봉 평균, 표준편차를 출력하는 프로그램을 작성하려고 한다.

조건 :
1) DB의 자료를 SQL문으로 읽어, DataFrame에 저장한다.
2) 아래의 main() 함수에 적당한 코드를 완성하시오.
(배점:10)
import MySQLdb
import pandas as pd
import numpy as np
import sys

def main():
    CONFIG = {"host": "127.0.0.1", "user": "root", "passwd": "123", "db": "test", "port": 3306, "charset": "utf8" }

    sql = '''
        sql 문은 여기에 작성
    '''

    나머지 코드는 여기에 작성하시오.

if __name__ == "__main__":
    main()
"""
# def main():
#     CONFIG = {"host": "127.0.0.1", 
#                 "user": "root", 
#                 "passwd": "123", 
#                 "db": "test", 
#                 "port": 3306, 
#                 "charset": "utf8" }

#     sql = """
#         select jikwonpay 
#         from jikwon 
#         left outer join gogek on jikwon.jikwonno = gogek.gogekdamsano 
#         where gogekdamsano is null;
#     """
#     conn = MySQLdb.connect(**CONFIG)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     df = pd.DataFrame(cursor.fetchall(), columns=["연봉"])

#     print("담당 고객이 없는 직원의 수", len(df), "명")
#     print("연봉 평균 : ", df["연봉"].mean(), "만원")
#     print("연봉 표준편차 : ", df["연봉"].std())
#     conn.close()

# if __name__ == "__main__":
#     main()

"""

[문항12] 표준정규분포를 따르는 난수로 9 by 4 형태의 DataFrame을 생성하시오. 변수명은 df라고 주자.
생성한 DataFrame의 칼럼 이름을 "가격1, 가격2, 가격3, 가격4"로 지정해 출력한다.
그리고 각 컬럼의 평균을 출력하는 코드를 작성하시오.

출력결과 :
가격1 가격2 가격3 가격4
0 -0.170009 0.539772 0.190635 0.789348
1 2.329343 0.798612 0.507198 0.276083
2 0.360988 0.869521 -0.496902 -0.150631
3 1.915679 -0.178226 -2.168088 1.087044
4 -1.001024 0.191449 -2.210461 0.233456
5 -2.111664 -0.223952 -0.536790 -0.003607
6 0.413132 -0.175507 -0.999601 1.045065
7 0.594383 -1.315871 -1.651703 -0.428549
8 1.203476 2.071813 -2.264859 0.631219
가격1 0.392700
가격2 0.286401
가격3 -1.070063
가격4 0.386603
(배점:10)
"""
# df = pd.DataFrame(np.random.randn(9,4), columns=["가격1", "가격2", "가격3", "가격4"])
# print(df)
# print()
# print(df.mean())

"""
[문항13] 아래의 코드를 참조해서 내용에 맞는 소스 코드를 적으시오.
from pandas import DataFrame
data = {"a": [80, 90, 70, 30], "b": [90, 70, 60, 40], "c": [90, 60, 80, 70]}

칼럼(열)의 이름을 순서대로 "국어", "영어", "수학"으로 변경한다.
아래 문제는 제시한 columns와 index 명을 사용한다.
1) 모든 학생의 수학 점수를 출력하기
2) 모든 학생의 수학 점수의 표준편차를 출력하기
3) 모든 학생의 국어와 영어 점수를 Series 타입이 아니라 DataFrame type으로 출력하기
(배점:10)
출력 결과 :
0    90
1    60
2    80
3    70
Name: 수학, dtype: int64

12.909944487358056     

    국어  영어
0   80  90
1   90  70
2   70  60
3   30  40
"""
# data = {"a": [80, 90, 70, 30], "b": [90, 70, 60, 40], "c": [90, 60, 80, 70]}
# df = pd.DataFrame(data=data)
# df.columns=["국어", "영어", "수학"]

# print(df)

# # 1) 모든 학생의 수학 점수를 출력하기
# print("1) 모든 학생의 수학 점수를 출력하기\n", df["수학"])
# print()

# # 2) 모든 학생의 수학 점수의 표준편차를 출력하기
# print("2) 모든 학생의 수학 점수의 표준편차를 출력하기\n", df["수학"].std())
# print()

# # 3) 모든 학생의 국어와 영어 점수를 Series 타입이 아니라 DataFrame type으로 출력하기
# print("3) 모든 학생의 국어와 영어 점수를 Series 타입이 아니라 DataFrame type으로 출력하기\n", df[["국어", "영어"]])

"""
[문항14] 정규분포를 따르는 데이터 1000개를 생성하고, 히스토그램을 그리는 코드를 작성하시오.

요구 조건
- 평균 : 0, 표준편차: 1
- 구간 : 20개
- 투명도 : 0.7
- 그래프 제목 : good
(배점:10)
"""
# data = np.random.randn(1000)
# plt.hist(data, bins=20, alpha=0.7)
# plt.title("good")
# plt.show()

"""
[문항15] CSV 파일을 Pandas로 읽고, 데이터를 요약(날짜/제품별 판매수량 합)하는 코드를 작성하시오.

예제 파일명 : sales_data.csv
날짜,제품,판매수량,가격
2025-08-01,노트북,5,1200000
2025-08-01,마우스,10,25000
2025-08-02,노트북,7,1150000
2025-08-02,마우스,8,23000
2025-08-03,노트북,6,1190000
2025-08-03,마우스,12,24000

힌트 : df.pivot_table
(배점:10)
출력 결과 :
제품          노트북  마우스
날짜
2025-08-01    5  10
2025-08-02    7    8
2025-08-03    6  12
"""

# df = pd.read_csv("sales_data.csv")
# print(df)
# print(df.pivot_table(index="날짜", columns="제품", aggfunc="sum"))