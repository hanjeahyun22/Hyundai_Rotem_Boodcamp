'''
env 파일을 이용한 DB
.env 파일 : 환경 변수(Environment Variables)를 저장해 두는 설정 파일
주로 웹 애플리케이션에서 DB 접속 정보나 비밀 키 같은 민감한 설정을 코드 밖으로 분리할 때 사용

웹 프로그래밍에서 DB를 연결할 때 보통 이런 정보가 필요합니다.
DB Host
DB Port
DB Name
DB User
DB Password
Secret Key

이걸 코드에 직접 쓰면 문제가 생김.

* 보안 문제
- GitHub에 올리면 비밀번호가 그대로 노출됨
- 환경 분리 어려움
- 개발 / 테스트 / 운영 DB가 다른데 코드 수정해야 함

--> 그래서 환경 변수 파일(.env)을 사용.

'''
# evv 파일을 읽을 때 필요한 모듈 설치 필요
# pip install python-dotenv
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
import pymysql          # pip install pymysql
import os



app = Flask(__name__)
app.secret_key = "abcdef123456"         # session/flash 를 위한 cookie 서명 용 secret_key

load_dotenv()                           # .env 파일에 저장된 환경변수 읽기 함수             # 리눅스에서는 안보이는 hidden file

# MariaDB 연결 정보 -->> .env파일에 DB연동 정보를 입력해놓고, main 코드에서는 정보 비공개.
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",                          # utf8mb4 : '전 세계 문자 (한글 포함) + 이모지'까지 처리
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )



# ##############################################################################################
#                                       login / logout
# ##############################################################################################


@app.get("/")
def root():
    return redirect(url_for("login_form"))


# 로그인 Form - GET 방식
@app.get("/login")
def login_form():
    return render_template("login.html")


# 로그인 Form - HOST 방식
@app.post("/login")
def login_post():
    jikwonno_raw = (request.form.get("jikwonno") or "").strip()
    jikwonname = (request.form.get("jikwonname") or "").strip()

    # 만약 직원 번호가 숫자가 아니거나, 직원 이름이 입력되지 않은 경우 에러메세지
    if not jikwonno_raw.isdigit() or not jikwonname:            # isdigit : 값이 숫자인지 확인
        flash("직원 번호는 숫자, 직원 이름은 필수")
        return redirect(url_for("login_form"))
    
    jikwonno = int(jikwonno_raw)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 로그인 체크
            cur.execute("""
                select jikwonno, jikwonname from jikwon    
                where jikwonno=%s and jikwonname=%s    
            """, (jikwonno, jikwonname))

            me = cur.fetchone()

            if not me:
                flash("로그인 실패. 직원 정보 불일치.")
                return redirect(url_for("login_form"))
            
            # 로그인 성공인 경우
            cur.execute("""
                select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as jikwonibsail_year
                from jikwon
                inner join buser on jikwon.busernum = buser.buserno    
                order by jikwonno
            """)
            rows = cur.fetchall()

        # 세션 생성
        session["jikwonno"] = me["jikwonno"]
        session["jikwonname"] = me["jikwonname"]

        return render_template("jikwonlist.html", rows=rows, login_user=me)

    except Exception as e:
        print('에러  : ', e)
    finally:
        conn.close()

# 로그아웃 Form - POST 방식
@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_form"))


# ##############################################################################################
#                                       DataBase
# ##############################################################################################

# 로그인 확인 후, 고객 정보를 확인하도록 기능.
@app.get("/gogek/<int:jikwonno>")
def gogek_list(jikwonno:int):
    if "jikwonno" not in session:
        flash("로그인 후 고객정보 이용하세요")
        return redirect(url_for("login_form"))
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            
            # 고객 정보
            cur.execute("""
                select gogekno, gogekname, gogektel
                from gogek
                where gogekdamsano=%s order by gogekno
                """, (jikwonno, ))

            customers = cur.fetchall()

            # 직원 정보
            cur.execute("""
                    select jikwonname from jikwon
                    where jikwonno=%s
                """, (jikwonno, ))
            
            emp = cur.fetchone()
        
        return render_template("gogek_list.html", customers=customers, empno=jikwonno,
                                empname=(emp["jikwonname"] if emp else ""))

    finally:
        conn.close()

# 직원 리스트
@app.get("/jikwons")
def jikwon_list():
    if "jikwonno" not in session:
        flash("로그인 후 고객정보 이용하세요")
        return redirect(url_for("login_form"))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as jikwonibsail_year
                from jikwon
                inner join buser on jikwon.busernum = buser.buserno    
                order by jikwonno
            """)

            rows = cur.fetchall()

        # 이미 로그인이 된 상황이기 때문에, 직원 정보를 session에서 가져옴.
        login_user = {"jikwonno":session["jikwonno"], "jikwonname":session["jikwonname"]}
        return render_template("jikwonlist.html", rows=rows, login_user=login_user)
    
    finally:
        conn.close()

if __name__=="__main__":
    app.run(debug=True)