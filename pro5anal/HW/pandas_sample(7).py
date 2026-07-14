# a) MariaDB에 저장된 jikwon, buser, gogek 테이블을 이용하여 아래의 문제에 답하시오.
#      - 사번 이름 부서명 연봉, 직급을 읽어 DataFrame을 작성
#      - DataFrame의 자료를 파일로 저장
#      - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
#      - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))
#      - 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시
#      - 연봉 상위 20% 직원 출력  : quantile()
#      - SQL로 1차 필터링 후 pandas로 분석 
#             - 조건: 연봉 상위 50% (df['연봉'].median() ) 만 가져오기  후 직급별 평균 연봉 출력
#      - 부서명별 연봉의 평균으로 가로 막대 그래프를 작성

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv

config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
#      - 사번 이름 부서명 연봉, 직급을 읽어 DataFrame을 작성
    sql = """
        select jikwonno, jikwonname, busername, jikwonpay, jikwonjik
        from jikwon inner join buser on jikwon.busernum=buser.buserno
    """
    cursor.execute(sql)

    df = pd.DataFrame(cursor.fetchall(),
                    columns=['사번', '이름','부서명', '연봉', '직급'])
    print(df.head(3))
    print()

#      - DataFrame의 자료를 파일로 저장
    with open('jikwoninfo.csv', mode='w', encoding='utf-8') as fobj:
        writer = csv.writer(fobj)
        writer.writerow(df.columns)
        writer.writerows(df.values)

    df2 = pd.read_csv('jikwoninfo.csv')
    print(df2.head(3))
    print()

#      - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
    result = pd.pivot_table(df2, index='부서명', values='연봉', aggfunc=['sum', 'max', 'min'])
    result.columns=['연봉합', '최대', '최소']
    print(result)
    print()

#      - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))
    ctab = pd.crosstab(df['부서명'], df['직급'], margins=True)
    print('교차표\n', ctab)
    print()
    
#      - 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시
    sql = """select jikwonno, jikwonname, gogekno, gogekname, gogektel
        from jikwon left outer join gogek on jikwon.jikwonno=gogek.gogekdamsano
    """
    df3 = pd.read_sql(sql, conn)
    df3 = df3.fillna("담당 고객 X")
    print(df3)
    print()

#      - 연봉 상위 20% 직원 출력  : quantile()
    threshold = df2['연봉'].quantile(0.8)
    print(df2[df2['연봉']>=threshold])
    print()

#      - SQL로 1차 필터링 후 pandas로 분석 
#             - 조건: 연봉 상위 50% (df['연봉'].median() ) 만 가져오기  후 직급별 평균 연봉 출력
    sql = "select jikwonjik as 직급, jikwonpay as 연봉 from jikwon"
    df4 = pd.read_sql(sql, conn)
    pay_median = df4['연봉'].median()
    df4 = df4[df4['연봉'] >= pay_median]
    df4_pivot = df4.pivot_table(values='연봉', index='직급', aggfunc='mean')
    print(df4_pivot)
    print()

#      - 부서명별 연봉의 평균으로 가로 막대 그래프를 작성
    buser_ypay = df.groupby(['부서명'])['연봉'].mean()  # 직급별
    print(buser_ypay)
    plt.barh(range(len(buser_ypay)), buser_ypay, alpha=0.4)     # 가로 막대
    plt.yticks(range(len(buser_ypay)), buser_ypay.index)
    plt.xlabel('평균 연봉')
    plt.ylabel('부서별')
    plt.show()

except Exception as e:
    print('처리 오류 : ', e)
    
finally:
    cursor.close()
    conn.close()

#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
#      - pivot_table을 사용하여 성별 연봉의 평균을 출력
#      - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
#      - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8'
}

try:
    conn   = pymysql.connect(**config)
    cursor = conn.cursor()

    sql = """
        SELECT j.jikwonno   AS 사번,
            j.jikwonname AS 직원명,
            b.busername  AS 부서명,
            j.jikwongen  AS 성별,
            j.jikwonpay  AS 연봉
        FROM   jikwon j
        INNER JOIN buser b ON j.busernum = b.buserno
    """
    df = pd.read_sql(sql, conn)
    print(df.head(3))
    print()


    pt = pd.pivot_table(df, index='성별', values='연봉', aggfunc='mean')
    print('성별 연봉 평균 (pivot_table)')
    print(pt)
    print()


    pt.plot(kind='bar', legend=False, color=['steelblue', 'coral'], rot=0)
    plt.title('성별 평균 연봉')
    plt.xlabel('성별')
    plt.ylabel('연봉')
    plt.tight_layout()
    plt.show()


    ct = pd.crosstab(df['부서명'], df['성별'])
    print('부서명 성별 교차 테이블')
    print(ct)

except pymysql.OperationalError as e:
    print('DB 오류 :', e)
except Exception as e:
    print('처리 오류 :', e)
finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import os

config = {
    'host':'127.0.0.1',
    'password':'123',
    'user':'root',
    'database' : 'test',
    'port':3306,
    'charset':'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql="""
        select 
            jikwonno, jikwonname, busername, jikwonjik, busertel, jikwongen, jikwonpay, 
            gogekno, gogekname, gogektel 
        from jikwon 
        inner join buser on jikwon.busernum=buser.buserno
        left outer join gogek on jikwon.jikwonno=gogek.gogekdamsano
    """
    cursor.execute(sql)
    df_raw = pd.DataFrame(cursor.fetchall(), columns=['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉', '고객번호', '고객명', '고객전화'])
    df = df_raw.drop_duplicates(subset=['사번'])
    
except pymysql.OperationalError as e:
    print(e)

finally:
    cursor.close()
    conn.close()

# print(df)
# os._exit(0)

#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#   조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#   사번  직원명  부서명   직급  부서전화  성별
#   ...
#   인원수 : * 명
dfc = df[['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉']]
dfc = dfc.rename(columns={'이름': '직원명'})
# print(dfc)

while True:
    jikwonno = input('사번을 입력하세요. 종료:q\t')

    if jikwonno == 'q':
        break

    if not jikwonno.isdigit(): 
        print('사번은 숫자만 입력하세요\n')
        continue

    jikwonname = input('이름을 입력하세요. 종료:q\t')
    if jikwonname == 'q':
        break

    if any(dfc['사번'] == int(jikwonno)):
        name = dfc[dfc['사번'] == int(jikwonno)]['직원명'].iloc[0]
        if name == jikwonname:
            # 전직원 출력
            print(dfc.drop(columns=['연봉'], axis=1))
            print("인원수 : ", dfc['사번'].count(), "명")

            male = dfc[dfc['성별']=='남']['연봉']
            female = dfc[dfc['성별']=='여']['연봉']

            figure, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
            figure.set_size_inches(15,10)

            # - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
            sns.boxplot(y=male, ax=ax1)
            sns.boxplot(y=female, ax=ax2)

            ax1.set(xlabel='남성', ylabel='연봉[원]', title='남성 연봉 분포')
            ax2.set(xlabel='여성', ylabel='연봉[원]', title='여성 연봉 분포')

            # - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력
            sns.histplot(data=male, bins=10, ax=ax3)
            sns.histplot(data=female, bins=10, ax=ax4)

            ax3.set(xlabel='연봉[원]', ylabel='인원수[명]', title='남성 연봉 분포 비교')
            ax4.set(xlabel='연봉[원]', ylabel='인원수[명]', title='여성 연봉 분포 비교')

            plt.show()
            break
        else:
            print("사번과 이름 정보가 일치하지 않습니다.\n")
    else: print("존재하지 않는 사번 입니다.\n")