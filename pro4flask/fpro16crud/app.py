from flask import Flask, jsonify, request, render_template
from db import get_connFunc

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")


# 1) 전체 조회
@app.get("/api/sangdata")
def list_sangdata():
    sql = "SELECT code, sang, su, dan FROM sangdata ORDER BY code"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    return jsonify({"ok": True, "data": rows})   # dict, list 등을 JSON 응답으로 만들어 반환


# 2) 1건 조회(선택)
@app.get("/api/sangdata/<int:code>")
def get_one(code: int):
    sql = "SELECT code, sang, su, dan FROM sangdata WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (code, ))
            row = cur.fetchone()
    if not row:
        return jsonify({"ok": False, "error": "NOT_FOUND"}), 404
    return jsonify({"ok": True, "data": row})


# 3) 추가 (POST / JSON)
@app.post("/api/sangdata")
def create_sangdata():
    data = request.get_json(silent=True) or {}

    # 필수값 체크
    try:
        code = int(data.get("code"))
    except Exception:
        return jsonify({"ok": False, "error": "code is required(int)"}), 400

    sang = (data.get("sang") or "").strip()
    if not sang:
        return jsonify({"ok": False, "error": "sang is required"}), 400

    try:
        su = int(data.get("su", 0))
        dan = int(data.get("dan", 0))
    except Exception:
        return jsonify({"ok": False, "error": "su/dan must be int"}), 400

    sql = "INSERT INTO sangdata(code, sang, su, dan) VALUES(%s, %s, %s, %s)"
    try:
        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (code, sang, su, dan))
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400    # 예: PK 중복 등

    return jsonify({"ok": True, "message": "CREATED", "code": code}), 201


# 4) 수정 (PUT / JSON)
@app.put("/api/sangdata/<int:code>")
def update_sangdata(code: int):
    data = request.get_json(silent=True) or {}

    sang = (data.get("sang") or "").strip()
    if not sang:
        return jsonify({"ok": False, "error": "sang is required"}), 400

    try:
        su = int(data.get("su", 0))
        dan = int(data.get("dan", 0))
    except Exception:
        return jsonify({"ok": False, "error": "su/dan must be int"}), 400

    sql = "UPDATE sangdata SET sang=%s, su=%s, dan=%s WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (sang, su, dan, code))
            if cur.rowcount == 0:
                return jsonify({"ok": False, "error": "NOT_FOUND"}), 404

    return jsonify({"ok": True, "message": "UPDATED", "code": code})


# 5) 삭제 (DELETE)
@app.delete("/api/sangdata/<int:code>")
def delete_sangdata(code: int):
    sql = "DELETE FROM sangdata WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (code,))
            if cur.rowcount == 0:
                return jsonify({"ok": False, "error": "NOT_FOUND"}), 404

    return jsonify({"ok": True, "message": "DELETED", "code": code})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)