from flask import Flask, render_template, request, make_response, redirect, url_for

COOKIE_AGE = 60*60*24*7         # 일주일
app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/login")
def loginfunc():
    name = request.cookies.get("name")
    visits = request.cookies.get("visits")

    if name:        # 만약 name에 값이 있다면 ~
        visits = int(visits or "0") + 1     # 초기 방문을 안했을 때, 초기값으로 문자열 "0"을 int로 바꾸고 저장.
        msg = f"안녕하세요. {name}님 {visits}번째 방문입니다."
    else:
        visits = None
        msg = "이름을 입력하면 방문 횟수를 쿠키로 기억합니다"

    resp = make_response(render_template("login.html", msg=msg, name=name, visits = visits))
    
    # 로그인 상태면 visits 쿠키 갱신
    if name:
        resp.set_cookie("visits", str(visits), max_age=COOKIE_AGE, samesite="Lax")
    return resp
    

@app.post("/login")
def loginfunc2():
    name = (request.form.get("name") or "").strip()

    resp = make_response(redirect(url_for("loginfunc")))
    resp.set_cookie("name", name, max_age=COOKIE_AGE, samesite="Lax")
    resp.set_cookie("visits", "0", max_age=COOKIE_AGE, samesite="Lax")
    return resp

@app.post("/logout")
def logoutfunc3():
    # 쿠키 삭제 후, /login(GET방식)으로 이동
    resp = make_response(redirect(url_for("loginfunc")))
    resp.delete_cookie("name")
    resp.delete_cookie("visits")
    return resp

if __name__=="__main__":
    app.run(debug=True)