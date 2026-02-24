# 개인용 Database : SQLITE3 - 파이썬에 기본 모듈로 제공
# http:///www.sqlite.org
# 모바일 기기, 임베디드 시스템 주로 사용.

import sqlite3
print(sqlite3.sqlite_version)

# conn = sqlite3.connect('exam.db')
conn = sqlite3.connect(':memory:')      # RAM(주기억장치)에만 db저장 -> 휘발성

try:
    cur = conn.cursor()                 # SQL문 처리를 위한 cursor 객체 생성
    
    # 테이블 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)")         # SQL문은 큰따움표"" 안에 작성 -> SQL문이 길어지면 """ """ 안에 적으면 됨.

    # 자료 입력
    cur.execute("insert into friends values('홍길동', '222-2222', '서초1동')")                                          # 트랜젝션 시작
    cur.execute("insert into friends values(?, ?, ?)", ('신기해', '333-3333', '역삼2동'))           # tuple 자료형
    inputdatas = ('신기한', '333-4444', '역삼2동')
    cur.execute("insert into friends values(?, ?, ?)", inputdatas)
    conn.commit()                                                                                                       # 트랜젝션 종료
    
    # 자료 보기
    cur.execute("select * from friends")
    # print(cur.fetchone())               # 한 개의 레코드(행)만 읽기
    print(cur.fetchall())
    print()
    cur.execute("select name, addr, phone from friends")            # 원본 테이블과 무관하게, select 시, column 순서 무작위로 가능
    for r in cur:
        # print(r)
        print(r[0] + ' ' + r[1] + ' ' + r[2])

except Exception as e:
    print('err : ', e)
    conn.rollback()
finally:
    conn.close()


