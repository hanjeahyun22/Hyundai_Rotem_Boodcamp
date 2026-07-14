from flask import Flask, render_template, request, jsonify
from db import get_connFunc

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

# 전체 조회
@app.get("/api/sangdata")
def list_sangdata():
    sql = "select code, sang, su, dan from sangdata order by code asc"
    # with 문을 쓰면 자동으로 conn.close() 처럼 닫힘.
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    return jsonify({"ok":True, "data":rows})


# 새 상품 추가
@app.post("/api/sangdata")
def create_sangdata():
    data = request.get_json()
    # print("data : ", data)
    code = int(data["code"])
    sang = data["sang"]
    su = int(data["su"])
    dan = int(data["dan"])
    isql = "insert into sangdata(code, sang, su, dan) values (%s, %s, %s, %s)"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(isql, (code, sang, su, dan))        # (%s, %s, %s, %s) -> tuple 형식으로 입력
    return jsonify({"ok":True})

# 상품 수정
@app.put("/api/sangdata/<int:code>")
def update_sangdata(code): 
    data = request.get_json()

    sang = data["sang"]
    su = int(data["su"])
    dan = int(data["dan"])

    usql = "update sangdata set sang=%s, su=%s, dan=%s where code=%s"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(usql, (sang, su, dan, code))        # tuple형식, 차례 지켜서 입력값
    return jsonify({"ok":True})


# 상품 삭제
@app.delete("/api/sangdata/<int:code>")
def delete_sangdata(code):
    try:
        dsql = "delete from sangdata where code = %s"

        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(dsql, (code, ))        # tuple형식 -> 입력값이 한개 라도, 마지막에 ',' 필요.
                if cur.rowcount == 0:
                    return jsonify({"ok":False, "msg":"해당 자료 없음"})
        return jsonify({"ok":True, "msg":"삭제 완료"})
    except Exception as err:
        return jsonify({"ok":False, "msg":str(err)})
    


if __name__=="__main__":
    app.run(debug=True)