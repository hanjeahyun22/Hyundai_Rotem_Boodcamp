import os
import uuid    # Universally Unique Identifier의 약자로 '고유한 문자열 ID' 생성
from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql
from werkzeug.utils import secure_filename
from PIL import Image     # Python Imaging Library로 이미지 열기/저장, 크기 변경, 포맷 변환(JPG ↔ PNG ↔ WEBP), 썸네일 작성(비율 유지 축소) 등 작업 가능

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "DEV_SECRET_KEY")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "mydb")

def get_conn():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, 
	password=DB_PASSWORD, database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

# ===== 업로드 설정 =====
UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
THUMB_DIR = os.path.join(app.root_path, "static", "uploads", "thumbs")
ALLOWED_EXT = {"jpg", "jpeg", "png", "gif", "webp"}
THUMB_MAX_SIZE = (240, 240)  # 썸네일 최대 크기

# 원본 이미지 경로(file_path)를 받아서, 썸네일 이미지의 상대경로를 규칙으로 만들어 주는 함수
# 원본 경로 → 썸네일 경로로 자동 변환해주는 함수
# 핵심은 DB에 ‘원본 경로’만 저장해두고, 썸네일 경로는 규칙으로 계산해서 쓰자는 아이디어.
# 썸네일은 static/uploads/thumbs 폴더에 저장한다고 규칙(약속)을 정한다.
# 즉 파일 구조가 static/uploads/abcd.jpg (원본),  static/uploads/thumbs/abcd.jpg (썸네일)
# 그러면 썸네일 URL은 /static/uploads/thumbs/abcd.jpg
# 즉 DB에 썸네일 경로를 따로 저장하지 않아도, 원본경로만 있으면 언제든지 썸네일경로를 만들 수 있다는 뜻.
def thumb_rel_from_file_pathFunc(file_path: str) -> str:
    # file_path: "uploads/xxxx.jpg" -> thumb: "uploads/thumbs/xxxx.jpg"
    base = os.path.basename(file_path)
    return f"uploads/thumbs/{base}"  # base가 "abcd.jpg"면 → "uploads/thumbs/abcd.jpg"
    # 왜 이렇게 하냐? DB에는 원본만 uploads/xxxx.jpg 형태로 저장해도,
    # 썸네일 경로는 DB 컬럼 없이 규칙으로 항상 계산할 수 있게 만들기 위해서.

# 업로드한 파일명이 허용된 확장자인지를 검사하는 간단한 필터 함수
def allowed_fileFunc(filename: str) -> bool:
    # 파일명에 확장자가 있고, 그 확장자가 허용 목록에 있으면 True를 반환
    # filename.rsplit(".", 1) → 오른쪽에서 . 기준으로 딱 1번만 나눔
    # → 예: "my.photo.JPG" → ["my.photo", "JPG"]  → [1]은 확장자 부분("JPG")
    # in ALLOWED_EXT → 미리 정해둔 허용 확장자 집합에 포함되면 True
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# 업로드된 이미지파일을 (1)원본으로저장, (2)썸네일도 만들어 저장, (3)DB에 넣기좋은 상대경로2개 반환 함수
def save_image_and_thumbFunc(file_storage):
    # 업로드 파일저장 + 썸네일 생성.   return: (file_path, thumb_path)  -> 둘 다 "uploads/..." 형태의 상대경로
    # 사용자가 올린 파일명은 위험할 수 있어(공백/한글/특수문자/경로침입 ../ 등).
    # secure_filename()이 안전한 형태로 정리한 파일명을 만들어줌. 예: "../a b.png" → "a_b.png" 같은 식
    orig = secure_filename(file_storage.filename)
    ext = orig.rsplit(".", 1)[1].lower()   # 파일 확장자만 뽑아 소문자로 바꿈. 예:"cat.JPG" → "jpg"
        # 실제 저장 파일명은 원본 이름을 쓰지 않고 UUID(고유한 문자열 ID)로 새로 만든다.
        # 이유: 중복 방지(같은 이름 업로드해도 덮어쓰기 안 됨), 보안/관리 편함. 예: a3f1...9c.jpg
    saved_name = f"{uuid.uuid4().hex}.{ext}"

    file_abs = os.path.join(UPLOAD_DIR, saved_name) # 서버 내부에서 원본 파일을 저장할 절대경로 만든다.
    file_storage.save(file_abs)      # 실제로 업로드된 파일을 위 경로에 저장

    file_rel = f"uploads/{saved_name}"     # 원본 상대경로를 규칙으로 바꿔서 썸네일 상대경로를 만든다.
    thumb_rel = thumb_rel_from_file_pathFunc(file_rel)
    thumb_abs = os.path.join(app.root_path, "static", thumb_rel)    # 썸네일을 저장할 절대 경로

    make_thumbnailFunc(file_abs, thumb_abs)   # 원본 파일을 읽어서 썸네일 파일을 생성
    return file_rel, thumb_rel   # DB 저장/HTML 출력에 쓰기 좋은 상대 경로 2개를 반환한다.
                                    # 원본: uploads/uuid.jpg, 썸네일: uploads/thumbs/uuid.jpg

# 원본 이미지 파일(src_abs)을 열어서 썸네일(작은 이미지) 파일(thumb_abs)로 저장해주는 역할
# 원본을 비율 유지한 채로 작은 이미지로 만들어 저장
def make_thumbnailFunc(src_abs: str, thumb_abs: str):
    # 이미지 열어서 비율 유지 + 축소
    with Image.open(src_abs) as ima:       # Pillow(PIL)로 원본 이미지 파일을 연다.
        ima.thumbnail(THUMB_MAX_SIZE)  # 비율 유지
        # PNG/GIF 등도 저장되지만, 포맷은 확장자 기반으로 Pillow가 판단
        ima.save(thumb_abs)    # 축소된 이미지를 thumb_abs 경로에 파일로 저장

def safe_removeFunc(rel_path: str):
    abs_path = os.path.join(app.root_path, "static", rel_path)
    # rel_path는 예를 들어 "uploads/a.jpg" 같은 상대경로.
    # 이걸 실제 파일 위치(절대경로)로 합쳐서 만듦. 예: .../프로젝트폴더/static/uploads/a.jpg
    try:
        if os.path.exists(abs_path):  # 파일이 실제로 존재할 때만 삭제하도록 체크.
            os.remove(abs_path)
    except:
        pass
    # 왜 필요한가? 사진 삭제/교체할 때는 DB 행은 이미 삭제됐는데 파일 삭제가 실패하거나, 반대로 파일이 이미 없을 수도 있다. 이때 삭제는 시도하되, 실패해도 앱은 정상 동작하도록 하는 안전장치.

# 폴더 준비
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

@app.get("/")
def home():
    # return redirect("/albums")   # url_for("albums_list") 대신 하드코딩
    # 하드코딩은 라우트가 바뀌면 문자열도 같이 바꿔야 함. 
    # url_for는 라우트가 바뀌어도 엔드포인트 이름만 유지하면 자동으로 따라가서 안전
    return redirect(url_for("albums_list"))

# ##############################################################################################
#                                           Albums
# ##############################################################################################

# 앨범 목록 + 추가
@app.get("/albums")
def albums_list():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM albums ORDER BY id DESC")
            albums = cur.fetchall()
        return render_template("albums.html", albums=albums)
    finally:
        conn.close()

@app.post("/albums/add")
def albums_add():
    name = (request.form.get("name") or "").strip()
    if not name:
        flash("앨범 이름은 필수입니다.")
        return redirect(url_for("albums_list"))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO albums(name) VALUES (%s)", (name,))
        return redirect(url_for("albums_list"))
    finally:
        conn.close()


# 앨범 수정
@app.get("/albums/edit/<int:album_id>")
def albums_edit_form(album_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM albums WHERE id=%s", (album_id,))
            album = cur.fetchone()
        if not album:
            flash("해당 앨범이 없습니다.")
            return redirect(url_for("albums_list"))
        return render_template("album_edit.html", album=album)
# redirect: 다른 URL로 가! (요청 2번, URL 바뀜)
        # render_template: 이 HTML을 지금 보여줘 (200, 요청 1번, URL 그대로)
    finally:
        conn.close()


@app.post("/albums/edit/<int:album_id>")
def albums_edit_save(album_id: int):
    name = (request.form.get("name") or "").strip()
    if not name:
        flash("앨범 이름은 필수입니다.")
        return redirect(url_for("albums_edit_form", album_id=album_id))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE albums SET name=%s WHERE id=%s", (name, album_id))
        return redirect(url_for("albums_list"))
    finally:
        conn.close()




# 앨범 삭제 (사진 있으면 막기)
@app.post("/albums/delete/<int:album_id>")
def albums_delete(album_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 해당 앨범명(카테고리)에 사진들이 있으면 앨범명 삭제 불가
            cur.execute("SELECT COUNT(*) AS cnt FROM photos WHERE album_id=%s", (album_id, ))
            if cur.fetchone()["cnt"] > 0:
                flash("이 앨범에는 사진이 있어 삭제할 수 없습니다. (먼저 사진을 삭제하세요)")
                return redirect(url_for("albums_list"))
            cur.execute("DELETE FROM albums WHERE id=%s", (album_id,))
        return redirect(url_for("albums_list"))
    finally:
        conn.close()


# 사진 목록 + 업로드
@app.get("/albums/<int:album_id>/photos")
def photos_list(album_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM albums WHERE id=%s", (album_id,))
            album = cur.fetchone()
            if not album:
                flash("해당 앨범이 없습니다.")
                return redirect(url_for("albums_list"))

            cur.execute("""
                SELECT id, album_id, title, file_path, created_at FROM photos
                WHERE album_id=%s ORDER BY id DESC
            """, (album_id,))
            photos = cur.fetchall()

        # 템플릿에서 thumb 경로도 쓰기 좋게 같이 넘김(규칙 기반)
        for p in photos:
            p["thumb_path"] = thumb_rel_from_file_pathFunc(p["file_path"])

        return render_template("photos.html", album=album, photos=photos)
    finally:
        conn.close()


@app.post("/albums/<int:album_id>/photos/add")
def photos_add(album_id: int):
    title = (request.form.get("title") or "").strip()
    file = request.files.get("photo")
    print(title, file)
    if not title:
        flash("사진 제목(title)은 필수입니다.")
        return redirect(url_for("photos_list", album_id=album_id))

    if not file or file.filename == "":
        flash("업로드할 파일을 선택하세요.")
        return redirect(url_for("photos_list", album_id=album_id))

    if not allowed_fileFunc(file.filename):
        flash("허용 확장자: jpg, jpeg, png, gif, webp")
        return redirect(url_for("photos_list", album_id=album_id))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM albums WHERE id=%s", (album_id,))
            if not cur.fetchone():
                flash("앨범이 존재하지 않습니다.")
                return redirect(url_for("albums_list"))

        file_rel, _thumb_rel = save_image_and_thumbFunc(file)

        with conn.cursor() as cur:
            # 썸네일 이미지는 DB에 저장 안함. Static/uploads/thumbs 폴더에 저장
            cur.execute(
                "INSERT INTO photos(album_id, title, file_path) VALUES (%s, %s, %s)",
                (album_id, title, file_rel)
            )
        return redirect(url_for("photos_list", album_id=album_id))
    finally:
        conn.close()


# ##############################################################################################
#                                       photos
# ##############################################################################################

# 사진 수정 (제목 수정 + 파일 교체)
@app.get("/photos/edit/<int:photo_id>")
def photo_edit_form(photo_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, album_id, title, file_path FROM photos WHERE id=%s", (photo_id, ))
            photo = cur.fetchone()

        if not photo:
            flash("해당 사진이 없습니다.")
            return redirect(url_for("albums_list"))

        photo["thumb_path"] = thumb_rel_from_file_pathFunc(photo["file_path"])
        return render_template("photo_edit.html", photo=photo)
    finally:
        conn.close()


@app.post("/photos/edit/<int:photo_id>")
def photo_edit_save(photo_id: int):
    title = (request.form.get("title") or "").strip()
    new_file = request.files.get("photo")  # 선택 업로드(있으면 교체)

    if not title:
        flash("제목은 필수입니다.")
        return redirect(url_for("photo_edit_form", photo_id=photo_id))

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, album_id, title, file_path FROM photos WHERE id=%s", (photo_id,))
            old = cur.fetchone()
        if not old:
            flash("해당 사진이 없습니다.")
            return redirect(url_for("albums_list"))

        album_id = old["album_id"]
        old_file_path = old["file_path"]
        old_thumb_path = thumb_rel_from_file_pathFunc(old_file_path)

        # 1) 파일 교체가 없는 경우: 제목만 수정
        if not new_file or new_file.filename == "":
            with conn.cursor() as cur:
                cur.execute("UPDATE photos SET title=%s WHERE id=%s", (title, photo_id))
            return redirect(url_for("photos_list", album_id=album_id))

        # 2) 파일 교체가 있는 경우
        if not allowed_fileFunc(new_file.filename):
            flash("허용 확장자: jpg, jpeg, png, gif, webp")
            return redirect(url_for("photo_edit_form", photo_id=photo_id))

        new_file_rel, _new_thumb_rel = save_image_and_thumbFunc(new_file)

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE photos SET title=%s, file_path=%s WHERE id=%s",
                (title, new_file_rel, photo_id)
            )

        # 교체 성공했으면 이전 파일/썸네일 삭제
        safe_removeFunc(old_file_path)
        safe_removeFunc(old_thumb_path)
        return redirect(url_for("photos_list", album_id=album_id))
    finally:
        conn.close()

# 사진 삭제 (DB + 파일 + 썸네일)
@app.post("/photos/delete/<int:photo_id>")
def photos_delete(photo_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, album_id, file_path FROM photos WHERE id=%s", (photo_id,))
            row = cur.fetchone()
            if not row:
                flash("해당 사진이 없습니다.")
                return redirect(url_for("albums_list"))

            album_id = row["album_id"]
            file_path = row["file_path"]
            thumb_path = thumb_rel_from_file_pathFunc(file_path)

            cur.execute("DELETE FROM photos WHERE id=%s", (photo_id,))

        # 파일 삭제
        safe_removeFunc(file_path)
        safe_removeFunc(thumb_path)
        return redirect(url_for("photos_list", album_id=album_id))
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
