# Flask app의 Entry point
# Routing, 서버 실행 담당

# Jinja2 : Flask에서 html 을 동적으로 렌더링할 때, 사용하는 템플렛 엔진       -->>  HTML + Python 데이터를 합쳐서 HTML을 만들어주는 도구
# 웹 서버에서 html문을 완성한 후, Client에게 전송
# html 안에 Python 변수를 넣고, 반복/조건문 등을 사용할 수 있게 하는 도구
"""
클라이언트      : 브라우저, 서버에 요청
서버            : Flask 애플리케이션
라우팅          : URL → Python 함수 연결
변수            : Python에서 HTML로 전달할 데이터
Jinja2          : HTML 안에서 변수 처리
render_template : HTML 템플릿을 읽어 완성된 HTML 생성
렌더링          : HTML을 완성하는 과정
"""
"""
클라이언트가 URL 요청
→ Flask 라우팅이 함수 실행
→ Python에서 데이터 생성
→ render_template 실행
→ Jinja2가 변수 치환
→ 완성된 HTML 생성
→ 브라우저에 응답
"""

from flask import Flask, render_template        # render_template : html 템플렛 파일(Jinja2 템플렛)을 읽어, 필요한 값을 채운 후, 완성된 HTML문을 응답으로 반환해 주는 함수.

app = Flask(__name__);

@app.route("/")                                 # 라우팅 -> 함수 매핑
def home():                                     # 매핑된 함수
    return render_template("home.html");

@app.route("/hello")
def hello():
    name = "길동아";
    addr = "강남구 테헤란로";

    # 템플렛 변수에 전달할 때는 '변수명=값' 형태로 적어준다.
    return render_template("hello.html", name=name, juso=addr);

@app.route("/world")
def world_image():
    return render_template("my.html")

if __name__=="__main__":
    app.run(debug=True);