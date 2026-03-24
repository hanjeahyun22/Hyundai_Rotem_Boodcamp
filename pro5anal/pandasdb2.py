# 터미널창 초기화
import os
os.system('cls')

# 원격 DB 연동 - jikwon 자료를 읽어 dataFrame에 저장
# import MySQLdb -> 이거 써도 무방
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
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay
        from jikwon inner join buser on jikwon.busernum = buser.buserno
    """
    cursor.execute(sql)

    # for jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay in cursor:
    #     print(jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay)
    print("=========DataFrame으로 출력=========")
    df1 = pd.DataFrame(cursor.fetchall(), 
                    columns=['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwongen', 'jikwonpay'])
    print(df1.head(3))
    print('연봉의 총합 : ', df1['jikwonpay'].sum())

    print("=========csv 파일로 출력=========")
    
    cursor.execute(sql)
    with open('pandasdb2.csv', mode='w', encoding='utf-8') as fobj:
        writer = csv.writer(fobj)
        for row in cursor.fetchall():
            writer.writerow(row)
    
    df2 = pd.read_csv('pandasdb2.csv', header=None, names=['번호', '이름', '부서', '직급', '성별', '연봉'])
    print(df2.head(3))

    print('\n\npandas의 sql 처리 함수 이용=========')
    df = pd.read_sql(sql, conn)
    df.columns = ['번호', '이름', '부서', '직급', '성별', '연봉']
    print(df.head(2))
    # print(df[:2])와 동일
    print(df['이름'].count(), ' ', len(df))
    print('부서별 인원수: ', df['부서'].value_counts())
    print('연봉 7000 이상 : ', df.loc[df['연봉'] >= 7000])
    ctab = pd.crosstab(df['성별'], df['직급'], margins=True)
    print('교차표\n', ctab)

    print("=========시각화=========")
    jik_ypay = df.groupby(['직급'])['연봉'].mean()     # 직급별 연봉평균
    print('jik_ypay :', jik_ypay)
    
    plt.pie(jik_ypay, explode=(0.2, 0, 0, 0.3, 0),
                labels = jik_ypay.index,
                shadow = True, counterclock = False)
    plt.show()


except Exception as e:
    print('처리 오류 : ', e)
finally:
    cursor.close()
    conn.close()
