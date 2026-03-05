from flask import Flask, render_template, request, redirect, url_for, session

# Python 세션(Session)
# 웹에서 사용자 정보를 서버에 저장하는 기능(쿠키를 통해 세션 운영)
# 일정 시간 동안 동일 사용자(브라우저)와 일련의 요청을 하나의 상태로 보고, 그 상태를 유지시키는 기술
# 쿠키에 비해 상대적으로 안전

# 실습 : 사용자가 os를 선택하면 세션에 저장하고 읽기
from datetime import timedelta      # timedetla : 시간의 “차이(기간)”을 표현하는 객체 -> 즉, 몇 초 / 몇 분 / 몇 시간 / 며칠 같은 시간 길이를 나타낼 때 사용

# Flask는 세션 사용을 위해 secret_key 설정 필요 (session은 쿠키 기반이기 때문.)
app = Flask(__name__)

# secret key값 설정
# key 값 자동 생성 -> python -c "import secrets; print(secrets.token_hex(32))"
app.secret_key = "abcdef123456"     # 위조 방지용 임의 secret key 값 설정.

app.permanent_session_lifetime = timedelta(seconds=5)       # session 만료 시간 : 5초

@app.get("/")
def home():
    return render_template("main.html")

@app.route("/setos")
def setos():
    # args. : GET 방식으로 받겠다.
    # form. : POST 방식으로 받겠다.
    favorite_os = request.args.get("favorite_os")

    # favorite_os가 있다면 session을 만들고 showos로 이동, 없으면 setos.html로 만들러감.
    if favorite_os:
        session.permanent = True        # Session 만료 시간(5초) 적용
        session["f_os"] = favorite_os
        return redirect(url_for("showos"))
    else:
        return render_template("setos.html")

@app.route("/showos")
def showos():
    # dict 형태로 session값을 받을 객체 선언
    context = {}

    # 만약 'f_os' key가 session에 있다면, session 에 저장.
    if "f_os" in session:
        context["f_os"] = session["f_os"]
        context["message"] = f"당신이 선택한 운영체제는 '{session['f_os']}'"
    else:
        context["f_os"] = None
        context["message"] = "운영체제를 선택하지 않았거나 세션이 만료됨."

    # 묶음형 자료형(context(dict type))를 return함.             # (dict)는 중괄호({}) 내에 {Key: Value}
    return render_template("showos.html", context=context)

if __name__=="__main__":
    app.run(debug=True)