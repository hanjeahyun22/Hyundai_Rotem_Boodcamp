import os
import pymysql

def get_conn():
    return pymysql.connect(
        host = os.getenv("DB_HOST", "127.0.0.1"),
        user = os.getenv("DB_USER", "root"),
        password = os.getenv("DB_PASSWORD", "123"),
        database = os.getenv("DB_NAME", "coffeedb"),
        port = int(os.getenv("DB_PORT", "3306")),
        charset = "utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def insert_survey(gender:str, age:int, co_survey:str) -> None:
    sql = "insert into survey(gender, age, co_survey) values(%s, %s, %s)"
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (gender, age, co_survey))
    except Exception as e:
        print(e)
    finally:
        conn.close()

def fetchall_survey() -> list[dict]:
    sql = "select rnum, gender, age, co_survey from survey order by rnum asc"
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

if __name__ == "__main__":
    conn = get_conn()
    cursor = conn.cursor(
    )