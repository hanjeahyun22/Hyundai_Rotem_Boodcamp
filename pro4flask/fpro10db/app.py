'''
DB & Flask 연동
'''

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
# flash : 임시 메세지 출력용 (내부적으로 session에 저장해 둠  --->>  secret_key 필요)
# get_flashed_messages : 저장해 둔 메세지를 꺼내는 함수
# ex) flash("~에러~") : 메세지를 세션에 잠시 저장 후, get_flashed_messages()를 하면 메세지를 읽음.
import pymysql          # pip install pymysql
import os


app = Flask(__name__)
app.secret_key = "abcdef123456"         # session/flash 를 위한 cookie 서명 용 secret_key


# MariaDB 연결 정보
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",                          # utf8mb4 : '전 세계 문자 (한글 포함) + 이모지'까지 처리
        # DictCursor : SELECT 결과를 'dict type'으로 받게 해줌.
        # {'code':1, 'sang':마우스, ...}    -->>    row['code'], row['sang']
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )


@app.get("/")
def root():
    return redirect(url_for("show_list"))


@app.get("/show/")
def show_list():
    # DB와 연결
    conn = get_conn()

    # 배열 보기
    try:
        # cursor : DB와 대화하는 통로
        # curosr도 열고 닫아야 함.  ->  with 문을 통해서 자동으로 열고 닫도록 함.
        with conn.cursor() as cur:
            # execute : SQL 실행, 즉 DB에게 실제 명령을 보내는 함수
            cur.execute("select code, sang, su, dan from sangdata order by code")
            # fetch : execute로 SQL을 실행하면 결과가 DB 서버 안에 있습니다. 그걸 Python으로 가져오는 함수입니다.
            # fetchall() : 전부 가져옴
            rows = cur.fetchall()
        messages = list(get_flashed_messages())
        return render_template("list.html", rows=rows, messages=messages)

    # 에러 보기
    # except pymysql.err.IntegrityError as e:
    #     ...
    except Exception as e:
        # flash(f"DB 자료 읽기 오류 : {e}")
        # return redirect(url_for("show_list"))
        pass
    
    # 작업이 끝나면 DB 연결 중지 
    finally:
        conn.close()

# ##############################################################################################
#                                       add
# ##############################################################################################
@app.get("/add/")
def add_form():
    messages = list(get_flashed_messages())
    return render_template("form_add.html", messages=messages)  # 추가 form 호출


# 추가 처리
@app.post("/add/")
def add_save():
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip()         # su_raw, 즉 network를 타고 넘어온 데이터는 문자열.  ex) "23"
    dan_raw = (request.form.get("dan") or "").strip()

    # 다시 한번 검사 -> sang이 값이 없거나 su_raw, dan_raw가 숫자가 아니라면, ...
    if not sang or not su_raw.isdigit or not dan_raw.isdigit:
        flash("sang은 필수. su, dan은 숫자만 허용")
        return redirect(url_for("add_form"))

    # su나 dan으로 연산을 하진 않으므로, 굳이 할 필요는 X
    su = int(su_raw)
    dan = int(dan_raw)

    # DB 연결
    conn = get_conn()
    
    try:
        with conn.cursor() as cur:
            """
            code는 DB에 지금 있는 code 중, 가장 큰 값을 찾고, 그 값에 +1 을 해서 자동 증가
            """
            cur.execute("select max(code) as max_code from sangdata")
            
            # max_code 단 한개 값만 넘어오므로, fetchone() 사용
            row = cur.fetchone()
            max_code = row["max_code"] if row else None
            # 만약 상품이 없어서, code 자체가 존재하지 않는 경우, 1을 받아옴.
            next_code = (max_code + 1) if max_code is not None else 1

            # 추가하기
            cur.execute("insert into sangdata(code, sang, su, dan) values (%s, %s, %s, %s)", (next_code, sang, su, dan))
        conn.commit()
        return redirect(url_for("show_list"))

    except Exception as e:
        conn.rollback()
        flash("저장 실패 : {e}")
        return redirect(url_for("add_form"))
    
    # 정상적인 작업 후에는 DB 연결 해제
    finally:
        conn.close()


# ##############################################################################################
#                                       edit
# ##############################################################################################


@app.get("/eidt/<int:code>")                # code를 get방식으로 들고옴.  http://localhost:5000/eidt/1
def edit_form(code:int):                            # 수정 form 호출 필요
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select * from sangdata where code=%s", (code, ))
            row = cur.fetchone()
        if not row:
            flash("해당 자료가 없어요")
            return redirect(url_for("show_list"))
        
        messages = list(get_flashed_messages())
        return render_template("form_edit.html", row=row, messages=messages)


    finally:
        conn.close()

# 수정 처리
@app.post("/edit/<int:code>/")          # int:code  -  Flask 문법
def edit_save(code:int):                # code:int  -  Python 문법
    sang = (request.form.get("sang") or "").strip()
    su_raw = (request.form.get("su") or "").strip()         # su_raw, 즉 network를 타고 넘어온 데이터는 문자열.  ex) "23"
    dan_raw = (request.form.get("dan") or "").strip()

    # 다시 한번 검사 -> sang이 값이 없거나 su_raw, dan_raw가 숫자가 아니라면, ...
    if not sang or not su_raw.isdigit or not dan_raw.isdigit:
        flash("sang은 필수. su, dan은 숫자만 허용")
        return redirect(url_for("edit_form"))

    # su나 dan으로 연산을 하진 않으므로, 굳이 할 필요는 X
    su = int(su_raw)
    dan = int(dan_raw)

    # DB 연결
    conn = get_conn()
    
    try:
        with conn.cursor() as cur:
            # 수정하기
            cur.execute("update sangdata set sang=%s, su=%s, dan=%s where code=%s", (sang, su, dan, code))
        conn.commit()                                       # commit을 했으므로, DB의 데이터 자체가 변함.
        return redirect(url_for("show_list"))

    except Exception as e:
        conn.rollback()
        flash("수정 실패 : {e}")
        return redirect(url_for("edit_form"))
    
    # 정상적인 작업 후에는 DB 연결 해제
    finally:
        conn.close()


# ##############################################################################################
#                                       delete
# ##############################################################################################

@app.post("/delete/<int:code>")
def delete_row(code:int):
    conn = get_conn()
    
    try:
        with conn.cursor() as cur:
            # 삭제하기
            cur.execute("delete from sangdata where code=%s", (code, ))
        conn.commit()                                       # commit을 했으므로, DB의 데이터 자체가 변함.
        return redirect(url_for("show_list"))

    except Exception as e:
        conn.rollback()
        flash("삭제 실패 : {e}")
        return redirect(url_for("edit_form"))
    
    # 정상적인 작업 후에는 DB 연결 해제
    finally:
        conn.close()



if __name__=="__main__":
    app.run(debug=True)