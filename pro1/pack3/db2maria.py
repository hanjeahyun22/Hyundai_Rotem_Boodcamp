# 원격 데이터베이스 연동 프로그래밍
# MariaDB : driver file 설치 후 사용
# pip install mysqlclient                   --> 터미널에서 설치
# C:\Users\acorn\anaconda3\envs\myproject\Lib\site-packages 경로에 있는지 확인 필요

import MySQLdb

conn = MySQLdb.connect(
    host = '127.0.0.1',         # window CMD에서 ipconfig 입력 후, ip 확인
    user = 'root',
    password = '123',
    database = 'test',
    port = 3306
    )
print(conn)
conn.close()

# sangdata 자료 CRUD(Insert/Select/Delete/Update)
config = {
    'host'      : '127.0.0.1',
    'user'      : 'root',
    'password'  : '123',
    'database'  : 'test',
    'port'      : 3306,
    'charset'   : 'utf8'
}

def myFunc():
    try:
        conn = MySQLdb.connect(**config)                    # **객체 : 객체를 dict 형태로 받겠다는 의미
        cursor = conn.cursor()

        # 자료 추가
        # isql = "insert into sangdata(code, sang, su, dan) values (5, '신상1', 5, 7800)"         # python은 autocommit이 FALSE로 설정되어 있기 때문에, local 저장소에서만 insert됨.
        # cursor.execute(isql)
        # conn.commit()                                                                           # 이제서야 DB server에도 insert 적용.
        '''
        isql = "insert into sangdata values (%s, %s, %s, %s)"
        # sql_data = 6, '신상2', 11, 5000
        sql_data = (6, '신상2', 11, 5000)
        cursor.execute(isql, sql_data)
        conn.commit()
        '''

        # 자료 수정

        # Insert, Delete는 성공하면 +1 이상, 실패하면 0
        # Update는 성공하면 1, 실패하면 0

        # update를 몇 번 했는지 return값을 사용 안하는 경우
        # cursor.execute(usql, sql_data)
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s"
        sql_data =  ('물티슈', 66, 1000, 5)
        cursor.execute(usql, sql_data)
        conn.commit()
        '''

        # update를 몇 번 했는지 return값을 사용 하는 경우
        # cou = cursor.execute(usql, sql_data)
        # print('수정 건수 : ', cou)
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s"
        sql_data =  ('콜라', 77, 1000, 5)
        cou = cursor.execute(usql, sql_data)
        print('수정 건수 : ', cou)
        conn.commit()
        '''

        # 자료 삭제
        code = '6'

        # -------------------------------------------------
        # ❌ 1. 문자열 직접 결합 방식 (비권장)
        # → SQL Injection 공격에 취약
        # → secure coding 가이드라인 위배
        # dsql = "delete from sangdata where code = " + code


        # -------------------------------------------------
        # ❌ 2. format() 문자열 치환 방식 (비권장)
        # → 단순 문자열 포맷팅일 뿐, DB 바인딩 아님
        # → 사용자가 악의적인 값을 넣으면 SQL Injection 발생 가능
        # dsql = "delete from sangdata where code = '{0}'".format(code)
        # cou = cursor.execute(dsql)


        # -------------------------------------------------
        # ✅ 3. Parameter Binding 방식 (권장, 정석 방법)
        # → %s는 자리표시자(placeholder)
        # → 실제 값은 execute()의 두 번째 인자로 전달
        # → DB 드라이버가 자동으로 escaping 처리
        # → SQL Injection 방지 (Prepared Statement 방식)

        dsql = "delete from sangdata where code = %s"

        # (code,)처럼 쉼표를 붙여야 1개짜리 튜플이 됨
        # (code) 는 그냥 문자열이므로 반드시 쉼표 필요
        cou = cursor.execute(dsql, (code,))

        # execute()의 반환값은 영향받은 행(row) 개수
        if cou != 0:
            print('삭제 성공')
        else:
            print('삭제 실패')

        # 자료 읽기
        sql = "select code, sang, su, dan from sangdata"
        cursor.execute(sql)                                 # DB server의 데이터를 local 컴퓨터의 RAM(주기억장치)로 읽어옴

        for data in cursor.fetchall():
            # print(data)
            print('%s %s %s %s' %data)
        
        print()
        cursor.execute(sql)
        for r in cursor:
            print(r[0], r[1], r[2])

        print()
        cursor.execute(sql)
        for (code, sand, su, dan) in cursor:                # code, sand, su, dan은 column 이름이 아니라, 그냥 변수 -> (a, b, c, d)도 가능 -->> 하지만 가독성을 위함.
            print(code, sand, su, dan)

    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    myFunc()