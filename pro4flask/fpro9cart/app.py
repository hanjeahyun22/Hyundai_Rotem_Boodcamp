'''
fpro9cart - 장바구니 항목을 session에 담으려는 예제
'''


from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "abcdef123456"
app.permanent_session_lifetime = timedelta(minutes=5)

products = [
    {"id":1, "name":"노트북", "price":3500000},
    {"id":2, "name":"키보드", "price":50000},
    {"id":3, "name":"마우스", "price":35000},
    {"id":4, "name":"모니터", "price":1500000}
]

@app.route("/")
def product_list():
    return render_template("products.html", products=products)

# 클라이언트가 상품을 장바구니에 담음
# 서버의 세션에 '클라이언트가 장바구니에 담은 상품' 저장
# Flask의 특성 : 클라이언트에 '세션의 id' 정보 저장.
@app.route("/cart")
def show_cart():
    cart = session.get("cart", {})                      # cart : python 객체        #"cart" : session의 product
    return render_template("cart.html", cart = cart)    # 매개변수 = 객체


@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    # print(product_id)                     # 잘 넘어오고 있는지 확인
    # 세션 cart가 없으면 빈 dict 생성
    cart = session.get("cart", {})

    # next() : 묶음형 자료에서 다음 값 1개를 꺼내는 함수.
    # -> iterator(반복 가능한 객체)에서 다음 값을 하나 꺼내는 함수 ->  next(iterator, default)
    # 주문 상품이 product에  기억됨.
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return "상품을 찾을 수 없어요", 404
    
    # 주문 상품이 상품목록에 있으면 장바구니에 추가  ->  클릭이 아닌, 직접 주소창에 키보드로 id 를 입력한 경우
    item_name = product["name"]

    # 주문한 상품이 이미 카트에 담겨져 있다면, 상품 개수를 추가     cart = session.get("cart", {})
    if item_name in cart:
        cart[item_name]["qty"] += 1
    else:
        # 카트에 최초로 담는 물건인 경우, 수량을 1로 설정(qty 요소(key) 생성)
        cart[item_name] = {"price":product["price"], "qty":1}

    # 클라이언트 RAM의 변수 cart를 Server의 Session "cart" key에 값으로 저장.
    session["cart"] = cart

    # 5분 만료 적용 다시 시작
    session.permanent = True

    # cart에 품목을 저장하면, 장바구니를 보기 위해서 show_cart 함수를 실행.
    return redirect(url_for("show_cart"))

if __name__=="__main__":
    app.run(debug=True)