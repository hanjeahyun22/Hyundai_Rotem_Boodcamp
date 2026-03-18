import os
import pymysql

# 실습용: 환경변수 없으면 기본값 사용
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_connFunc():
    """
    MariaDB 연결 객체 반환
    - cursorclass=DictCursor : 결과를 dict로 받기 (JSON 만들기 편함). autocommit=True : 편의상 자동 커밋
    """
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )