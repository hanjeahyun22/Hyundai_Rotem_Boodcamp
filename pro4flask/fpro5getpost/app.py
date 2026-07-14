from flask import Flask, render_template, request

app = Flask(__name__);

@app.route("/get_form")
def get_form():
    return render_template("get_form.html");

@app.route("/get_result")
def get_result():
    name = request.args.get("username");            # args : argument       # get("usernmae") : username argument를 받을 거다.
    age = request.args.get("age");                  # !!!!! '23' 문자 타입으로만 받음 !!!!
    age = age + "살";
    return render_template("get_result.html", name=name, age=age);

@app.route("/post_form")
def post_form():
    return render_template("post_form.html");

@app.route("/post_result", methods=['POST'])
def post_result():
    name = request.form.get("username");
    email = request.form.get("email");
    return render_template("post_result.html", name = name, email=email);

if __name__=="__main__":
    app.run(debug=True)