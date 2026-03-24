# 터미널창 초기화
import os
os.system('cls')

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv
import sqlite3
import MySQLdb

config = {
    'host':"127.0.0.1",
    "user":"root",
    "password":"123",
    "database":"test",
    "port":3306,
    "charset":"utf8"
}

"""
pandas 문제 7)

    a) MariaDB에 저장된 jikwon, buser, gogek 테이블을 이용하여 아래의 문제에 답하시오.
        - 사번 이름 부서명 연봉, 직급을 읽어 DataFrame을 작성
        - DataFrame의 자료를 파일로 저장
        - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
        - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))
        - 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시
        - 연봉 상위 20% 직원 출력  : quantile()
        - SQL로 1차 필터링 후 pandas로 분석 
                - 조건: 연봉 상위 50% (df['연봉'].median() ) 만 가져오기  후 직급별 평균 연봉 출력
        - 부서명별 연봉의 평균으로 가로 막대 그래프를 작성
"""

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    # 사번 이름 부서명 연봉, 직급을 읽어 DataFrame을 작성
    sql = "select jikwonno, jikwonname, busername, jikwonpay, jikwonjik from jikwon inner join buser on jikwon.busernum = buser.buserno"
    cursor.execute(sql)
    df_a = pd.DataFrame(cursor.fetchall(),
                        columns=["사번", "이름", "부서명", "연봉", "직급"])
    print(df_a)

    # DataFrame의 자료를 파일로 저장
    cursor.execute(sql)
    with open ("pandasdb_2026_03_24.csv", mode="w", encoding="utf-8") as fobj:
        writer = csv.writer(fobj)
        for row in cursor.fetchall():
            writer.writerow(row)
    
    # 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
    print("부서명 별 연봉의 합 : \n", df_a.groupby(["부서명"])["연봉"].sum())
    print("부서명 별 최대 연봉 : \n", df_a.groupby(["부서명"])["연봉"].max())
    print("부서명 별 최소 연봉 : \n", df_a.groupby(["부서명"])["연봉"].min())
    print()

    # 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))
    ctab = pd.crosstab(df_a["부서명"], df_a["직급"], margins=True)
    print("교차 테이블[(부서명) * (직급)]\n", ctab)
    print()

    # 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시
    sql = """
        select jikwonname as 직원, ifnull(gogekno, "담당 고객 X") as 고객번호, gogekname as 고객명, gogektel as 고객전화 
            from gogek right outer join jikwon on jikwon.jikwonno = gogek.gogekdamsano 
            group by jikwonname;    
        """
    df = pd.read_sql(sql, conn)
    print("직원별 담당 고객 자료(고객 번호, 고객 명, 고객 전화)\n",df)

    # 연봉 상위 20% 직원 출력  : quantile()
    print("연봉 상위 20% 직원 출력\n", df_a.quantile(q=0.8, interpolation="nearest"))

    #- SQL로 1차 필터링 후 pandas로 분석
    #   - 조건: 연봉 상위 50% (df['연봉'].median() ) 만 가져오기  후 직급별 평균 연봉 출력
    median_pay = df_a["연봉"].median()
    sql = """
        select jikwonno, jikwonname, busername, jikwonpay, jikwonjik
            from jikwon inner join buser on jikwon.busernum = buser.buserno
            where jikwonpay >= %s
    """
    df_top50 = pd.read_sql(sql, conn, params=[median_pay])
    df_top50.columns = ["사번", "이름", "부서명", "연봉", "직급"]
    print("직급별 평균 연봉 (상위 50% 필터링 후):")
    print(df_top50.groupby("직급")["연봉"].mean())

    # 부서명별 연봉의 평균으로 가로 막대 그래프를 작성
    buser_pay = df_a.groupby("부서명")["연봉"].mean()

    plt.figure()
    plt.barh(buser_pay.index, buser_pay.values)
    plt.xlabel("평균 연봉")
    plt.title("부서명별 평균 연봉")
    plt.show()

except Exception as e:
    print("err : ", e)
finally:
    cursor.close()
    conn.close()


"""
    b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
        - pivot_table을 사용하여 성별 연봉의 평균을 출력
        - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
        - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))
"""

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = "select * from jikwon"
    cursor.execute(sql)
    df_b = pd.DataFrame(cursor.fetchall(),
                        columns=["직원번호", "직원명", "부서번호", "직급", "연봉", "입사일", "성별", "등급"])
    print(df_b)

    # pivot_table을 사용하여 성별 연봉의 평균을 출력
    print(df_b.pivot_table(values="연봉", index="성별", aggfunc="mean"))

    # 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
    sex_pay = df_b.groupby("성별")["연봉"].mean()

    plt.figure()
    plt.bar(sex_pay.index, sex_pay.values)
    plt.xlabel("평균 연봉")
    plt.title("성별 별 평균 연봉")
    plt.show()

    # 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))
    sql = "select jikwongen, busername from jikwon inner join buser on jikwon.busernum = buser.buserno"
    df_ctab = pd.read_sql(sql, conn)
    df_ctab.columns = ["성별", "부서"]
    ctab = pd.crosstab(df_ctab["성별"], df_ctab["부서"], margins=True)
    print('교차표\n', ctab)
except Exception as e:
    print("err : ", e)
finally:
    cursor.close()
    conn.close()



"""
    c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
        조건 :  try ~ except MySQLdb.OperationalError as e:      사용
        사번  직원명  부서명   직급  부서전화  성별
        ...
        인원수 : * 명
        - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
        - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력
"""

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    num_input = input("직원 번호를 입력하시오. [type : int]")
    name_input = input("직원 이름을 입력하시오. [type : varchar(10)]")

    # 1단계: 로그인 확인용 SQL (WHERE 있음)
    login_sql = """
        select jikwonno from jikwon
        where jikwonno = %s and jikwonname = %s
    """
    df_login = pd.read_sql(login_sql, conn, params=[num_input, name_input])

    if df_login.empty:
        print("로그인 실패: 사번 또는 직원명이 일치하지 않습니다.")
    else:
        print("=== 로그인 성공 ===")

    sql="""
        select jikwonno, jikwonname, busername, jikwonjik, busertel, jikwongen 
        from jikwon inner join buser on jikwon.busernum = buser.buserno;
    """
    df_c = pd.read_sql(sql, conn, params=[num_input, name_input])
    df_c.columns=["사번", "직원명", "부서명", "직급", "부서전화", "성별"]
    print(df_c)
except MySQLdb.OperationalError as e:
    print("err : ", e)
finally:
    cursor.close()
    conn.close()
