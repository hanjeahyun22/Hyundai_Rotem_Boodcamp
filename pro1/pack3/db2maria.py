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