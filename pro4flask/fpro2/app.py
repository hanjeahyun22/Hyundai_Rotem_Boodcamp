from flask import Flask, request, make_response
# request : 현재 들어온 http 요청 정보(parameter, form, header, cookie, ...)를 담는 객체
# make_response : 응답(reponse) 객체를 직접 만들어 반환할 때 사용하는 함수

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>홈 페이지</h2><p>/login으로 이동해 보세요</p>"

@app.route("/login", methods=["GET", "POST"])
def login():
    # GET 요청
    if request.method == "GET":
        return """
            <h2>로그인 페이지</h2>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="사용자 이름 입력" value="admin">
                <button type="submit">로그인</button>
            </form>
            <p>POST 요청 시, username 값을 서버가 받아 처리~~</p>
        """
    elif request.method == "POST":
        user = request.form.get("username", "").strip();            # strip() : 문자열 앞, 뒤 공백 삭제

        if not user:
            return "사용자 이름 입력<br><a href='/login'>돌아가기</a>"
        
        # 정상 입력 시 - 로그인 성공 메세지 출력
        message = f"""
            <h2>로그인 성공!</h2>
            <p>안녕하세요 {user} 회원님. 서비스 마음껏 활용</p>
            <a href="/">홈으로 돌아가기</a>
        """
        return make_response(message, 200);
    else:
        return make_response("잘못된 요청", 405);

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port = 5000)
