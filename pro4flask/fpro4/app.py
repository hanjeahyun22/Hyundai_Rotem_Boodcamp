from flask import Flask, render_template        # render_template : html 템플렛 파일(Jinja2 템플렛)을 읽어, 필요한 값을 채운 후, 완성된 HTML문을 응답으로 반환해 주는 함수.

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/condition")
def condition():
    score = 85;
    return render_template("condition.html", score=score);      # score값을 서버가 넘겨줌.

@app.route("/loop")
def loop():
    users = ["손오공", "사오정", "저팔계"];
    return render_template("loop.html", users = users);      # score값을 서버가 넘겨줌.

@app.route("/filter")
def filter_ex():
    message = "hello Flask Jinja";
    price = 12345;
    return render_template("filter.html", message = message, price=price);

if __name__=="__main__":
    app.run(debug=True);