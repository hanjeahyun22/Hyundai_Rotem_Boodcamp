from flask import Flask, render_template        # render_template : html 템플렛 파일(Jinja2 템플렛)을 읽어, 필요한 값을 채운 후, 완성된 HTML문을 응답으로 반환해 주는 함수.

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");


if __name__=="__main__":
    app.run(debug=True);