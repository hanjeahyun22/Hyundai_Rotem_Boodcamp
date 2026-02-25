'''
문1) jikwon 테이블 자료 출력
키보드로부터 부서번호를 입력받아, 해당 부서에 직원 자료 출력
부서번호 입력 : _______
직원번호 직원명 근무지역 직급
1 홍길동 서울 이사
...
인원 수 :
'''

# import MySQLdb
# import pickle

# """
# config = {
#     'host'      : '127.0.0.1',
#     'user'      : 'root',
#     'password'  : '123',
#     'database'  : 'test',
#     'port'      : 3306,
#     'charset'   : 'utf8'
# }
# """

# with open('mydb.dat', mode='rb') as obj:
#     config = pickle.load(obj)

# def chulbal():
#     try:
#         conn = MySQLdb.connect(**config)                    # **객체 : 객체를 dict 형태로 받겠다는 의미
#         cursor = conn.cursor()

#         buserno_input = input('부서 번호를 입력하세요 : ')
#         sql = """
#             select jikwonno as 직원번호, jikwonname as 직원명, buserloc as 근무지역, jikwonjik as 직급 
#             from jikwon
#             inner join buser on buser.buserno = jikwon.busernum
#             where busernum = %s
#         """
        
#         cursor.execute(sql, (buserno_input, ))                                 # cursor : 작성한 SQL문을 DB 서버에 전달하여 실행 요청
        
#         datas = cursor.fetchall()
#         print(datas)
#         print(len(datas))
#         if len(datas) == 0:
#             print(buserno_input + " 번 부서는 없음.")
#             return                                          # sys.exit(0) 를 적어도 같음.

#         for jikwonno, jikwonname, buserloc, jikwonjik in datas:
#             print(jikwonno, jikwonname, buserloc, jikwonjik)

#         print('인원 수 : ', str(len(datas)))                 # len(datas) 자체가 몇 건이 실행됐는지 의미함.

#     except Exception as e:
#         print('err : ', e)
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == "__main__":
#     chulbal()

'''
문2) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
직원번호 입력 : _______
직원명 입력 : _______
직원번호 직원명 부서명 부서전화 직급 성별
1 홍길동 총무부 111-1111 이사 남
'''

# import MySQLdb

# config = {
#     'host' : '127.0.0.1',
#     'user' : 'root',
#     'password' : '123',
#     'database' : 'test',
#     'port' : 3306,
#     'charset' : 'utf8'
# }

# def myFunc():
#     try:
#         conn = MySQLdb.connect(**config)
#         cursor = conn.cursor()

#         jikwonno_input = int(input('직원번호 입력 : '))
#         jikwonname_input = input('직원명 입력 : ')
#         sql = """
#             select jikwonno 직원번호, jikwonname 직원명, busername 부서명, substr(busertel, -8, 8) 부서전화, jikwonjik 직급, jikwongen 성별
#             from jikwon
#             inner join buser on jikwon.busernum = buser.buserno
#             where jikwonno = %s and jikwonname = %s
#             """
#         cou = cursor.execute(sql, (jikwonno_input, jikwonname_input))
        
#         if cou != 0:
#             print('로그인 성공')
#         else:
#             print('로그인 실패')

#         datas = cursor.fetchall()
#         if len(datas) == 0:
#             print('err : 로그인 실패')
#             return
        
#         for jikwonno, jikwonname, busername, busertel,jikwonjik, jikwongen in datas:
#             print(jikwonno, jikwonname, busername, busertel, jikwonjik, jikwongen)
    
#     except Exception as e:
#         print('err : ', e)
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == "__main__":
#     myFunc()


'''
문2-1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.
직원번호 입력 : _______
직원명 입력 : _______
직원번호 직원명 부서명 부서전화 직급 성별
1 홍길동 총무부 111-1111 이사 남
...
직원 수 :
이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.
고객번호 고객명 고객전화 나이
1 사오정 555-5555 34
관리 고객 수 :
'''
# import MySQLdb

# config = {
#     'host' : '127.0.0.1',
#     'user' : 'root',
#     'password' : '123',
#     'database' : 'test',
#     'port' : 3306,
#     'charset' : 'utf8'
# }

# def myFunc():
#     try:
#         conn = MySQLdb.connect(**config)
#         cursor = conn.cursor()

#         jikwonno_input = int(input('직원번호 입력 : '))
#         jikwonname_input = input('직원명 입력 : ')
#         # 해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.
#         sql = """
#             select jikwonno 직원번호, jikwonname 직원명, busername 부서명, substr(busertel, -8, 8) 부서전화, jikwonjik 직급, jikwongen 성별
#             from jikwon
#             inner join buser on jikwon.busernum = buser.buserno
#             where busernum = (select busernum from jikwon where jikwonno = %s and jikwonname = %s)
#             order by jikwonjik ASC, jikwonname ASC; 
#             """

#         cou = cursor.execute(sql, (jikwonno_input, jikwonname_input))
        
#         if cou != 0:
#             print('로그인 성공')
#         else:
#             print('로그인 실패')

#         datas = cursor.fetchall()
#         if len(datas) == 0:
#             print('err : 로그인 실패')
#             return
        
#         for jikwonno, jikwonname, busername, busertel,jikwonjik, jikwongen in datas:
#             print(jikwonno, jikwonname, busername, busertel, jikwonjik, jikwongen)
#         print()
#         print('직원 수 : ', cou)

#         print()
#         # 이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.
#         # 고객번호 고객명 고객전화 나이
#         # 1 사오정 555-5555 34
#         # 관리 고객 수 :

#         sql_gogek = """
#                     select gogekno 고객번호, gogekname 고객명, substr(gogektel, -8, 8) 고객전화,
#                         case substr(gogekjumin, 1, 1)
#                             when 0 or 1 then YEAR(NOW()) - (2000 + substr(gogekjumin, 1, 2))
#                         else YEAR(NOW()) - (1900 + substr(gogekjumin, 1, 2))
#                         end as 나이
#                     from gogek
#                     inner join jikwon on jikwon.jikwonno = gogek.gogekdamsano
#                     where jikwonno = %s;
#                 """

#         gogek_cou = cursor.execute(sql_gogek, (jikwonno_input, ))
#         datas = cursor.fetchall()
#         for a, b, c, d in datas:
#             print(a, b, c, d)
#         print()

#         print('관리 고객 수 : ', gogek_cou)

#     except Exception as e:
#         print('err : ', e)
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == "__main__":
#     myFunc()

'''
문3) 성별 직원 현황 출력 : 성별(남/여) 단위로 직원 수와 평균 급여 출력
성별 직원수 평균급여
남 3 8500
여 2 7800
'''
# import MySQLdb
# import pickle

# with open('mydb.dat', mode='rb') as obj:
#     config = pickle.load(obj)

# def chulbal():
#     try:
#         conn = MySQLdb.connect(**config)                    # **객체 : 객체를 dict 형태로 받겠다는 의미
#         cursor = conn.cursor()

#         sql = """
#             select jikwongen 성별, count(*) 직원수, avg(jikwonpay) from jikwon where jikwongen is not null group by jikwongen
#         """
#         cursor.execute(sql)
#         datas = cursor.fetchall()
#         for a, b, c in datas:
#             print(a, b, c)

#     except Exception as e:
#         print('err : ', e)
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == "__main__":
#     chulbal()


'''
문4)직원별 관리 고객 수 출력 (관리 고객이 없으면 출력에서 제외)
직원번호 직원명 관리 고객 수
1 홍길동 3
2 한송이 1
'''
import MySQLdb
import pickle

with open('mydb.dat', mode='rb') as obj:
    config = pickle.load(obj)

def chulbal():
    try:
        conn = MySQLdb.connect(**config)                    # **객체 : 객체를 dict 형태로 받겠다는 의미
        cursor = conn.cursor()

        sql = """
            select jikwonno 직원번호, jikwonname 직원명, count(*) 관리고객수 from jikwon
            right outer join gogek on jikwon.jikwonno = gogek.gogekdamsano
            group by gogekdamsano;
        """
        cursor.execute(sql)
        datas_4 = cursor.fetchall()
        for a, b, c in datas_4:
            print(a, b, c)

    except Exception as e:
        print('err : ', e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    chulbal()
