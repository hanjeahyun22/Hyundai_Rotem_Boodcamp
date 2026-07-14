# Flast 모듈 설치 -> pip install flask

# Flask 기본 서버는 실무용 X, 개발용 or 학습용 --> Light-weight Server
# 실무용 서버(WSGI) : gunicorn, waitress, nginx, ...

# waitress 서버를 사용한다면, pip install waitress
from waitress import serve;



"""
1. client가 요청
2. routing

"""

from flask import Flask     # 웹 서버(Application Server) 생성에 필요
# Python Application Server : Ptyhon 프로그램 코드를 실행해서 요청을 처리하는 서버

app = Flask(__name__);      # Flask 객체 생성. __name__ : 현재 모듈의 이름

# URL 매핑(라우팅) : 클라이언트 요청이 "/" 일 때, 아래 함수 수행
@app.route("/")
def abc():                  # 클라이언트 요청을 처리하는 함수
    return "<h1>안녕하세요</h1> 반가워요";

@ app.route("/about")
def about():
    return "Flask를 소개하자면 음 만세~~"

@ app.route("/user/<name>") # URL에 변수를 담아 요청 --> <name> 의 값을 함수의 parameter로 취급
def user(name):
    return f"내 친구 {name}";

if __name__ == "__main__":
    # app.run();
    # app.run(debug=True, host = '0.0.0.0', port = 5000)       # 외부에서 코드를 실행하면, 해당 컴퓨터의 ip 자동 할당

    # waitress 실무용 서버 사용시
    print("웹 서버 서비스 시작")
    serve(app=app, host='0.0.0.0', port=8000)
    