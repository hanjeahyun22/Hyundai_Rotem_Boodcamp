# 터미널창 초기화
import os
os.system('cls')

'''
카이제곱 문제1) 부모학력 수준이 자녀의 진학여부와 관련이 있는가?를 가설검정하시오
    예제파일 : cleanDescriptive.csv
    칼럼 중 level - 부모의 학력수준, pass - 자녀의 대학 진학여부
    조건 :  level, pass에 대해 NA가 있는 행은 제외한다.
'''
# 귀무가설 : 부모학력 수준이 자녀의 진학여부와 관련이 없다(independent)
# 대립가설 : 부모학력 수준이 자녀의 진학여부와 관련이 있다(dependent)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/cleanDescriptive.csv")
print(data.head())

# level, pass 결측치 제거
data = data[["level", "pass"]].dropna()

ctab = pd.crosstab(index=data["level"], columns=data["pass"])
# print(data["level"].unique())                           # [1:대학원졸 2:대졸 3:고졸]
# print(data["pass"].unique())                             # [1:진학O 2:진학X]

ctab.index = ["대학원졸", "대졸", "고졸"]
ctab.columns = ["진학O", "진학X"]
print(ctab)

# 이원카이제곱 검정
chi_result = [ctab.loc["대학원졸"], ctab.loc["대졸"], ctab.loc["고졸"]]
chi2, p, dof, expected = stats.chi2_contingency(chi_result)
print(f"chi2 : {chi2}, p : {p}, dof : {dof}")               # chi2 : 2.7669512025956684, p : 0.25070568406521365, dof : 2
print("expected : \n", expected) 

print('''
판정 : chi2: 2.7669512025956684, dof:2, critical value : 5.99("카이제곱분포표" 에 의한 값)
chi2 값이 임계치 좌측에 있으므로, 귀무가설(H0) 채택
-->> 부모학력 수준이 자녀의 진학여부와 관련이 없다.
''')

'''
카이제곱 문제2) 지금껏 A회사의 직급과 연봉은 관련이 없다. 
그렇다면 jikwon_jik과 jikwon_pay 간의 관련성 여부를 통계적으로 가설검정하시오.
    예제파일 : MariaDB의 jikwon table 
    jikwon_jik   (이사:1, 부장:2, 과장:3, 대리:4, 사원:5)
    jikwon_pay (1000 ~2999 :1, 3000 ~4999 :2, 5000 ~6999 :3, 7000 ~ :4)
    조건 : NA가 있는 행은 제외한다.
'''
# 귀무가설 : A회사의 직급과 연봉은 관련이 없다.(independent)
# 대립가설 : A회사의 직급과 연봉은 관련이 있다.(dependent)

import pymysql

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
        SELECT
    jikwonjik,
    CASE
        WHEN jikwonpay BETWEEN 1000 AND 2999 THEN '1000~2999'
        WHEN jikwonpay BETWEEN 3000 AND 4999 THEN '3000~4999'
        WHEN jikwonpay BETWEEN 5000 AND 6999 THEN '5000~6999'
        ELSE '7000~'
    END AS pay_group
    FROM jikwon
    WHERE jikwonjik IS NOT NULL AND jikwonpay IS NOT NULL
    """

    data = pd.read_sql(sql, conn)
    ctab = pd.crosstab(index=data["jikwonjik"], columns=data["pay_group"])
    ctab.index = ["이사", "부장", "과장", "대리", "사원"]
    ctab.columns = [1, 2, 3, 4]
    print(ctab)
    
    chi_result = [ctab.loc["이사"], ctab.loc["부장"], ctab.loc["과장"], ctab.loc["대리"], ctab.loc["사원"]]
    chi2, p, dof, expected = stats.chi2_contingency(chi_result)
    print(f"chi2 : {chi2}, p : {p}, dof : {dof}")               #  chi2 : 37.40349394195548, p : 0.00019211533885350577, dof : 12
    print("expected : \n", expected) 
    print('''
    판정 : chi2: 37.40349394195548, dof:12, critical value : 21.03("카이제곱분포표" 에 의한 값)
    chi2 값이 임계치 우측에 있으므로, 귀무가설(H0) 기각
    -->> A회사의 직급과 연봉은 관련이 있다.
    ''')
except pymysql.OperationalError as e:
    print('DB 오류 :', e)
except Exception as e:
    print('처리 오류 :', e)
finally:
    cursor.close()
    conn.close()