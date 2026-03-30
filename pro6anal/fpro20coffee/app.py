from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from db import insert_survey, fetchall_survey
from analysis import analysis_func, save_barchart_func
import time

BASE_DIR = Path(__file__).resolve().parent
IMG_PATH = BASE_DIR / "static" / "images" / "vbar.png"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/coffee/survey")
def survey_view():
    return render_template("coffee/coffeesurvey.html")

@app.post("/coffee/surveyprocess")
def surveyprocess():
    gender = (request.form.get("gender") or "").strip()
    age_raw = (request.form.get("age") or "").strip()
    co_survey = (request.form.get("co_survey") or "").strip()

    # 입력 검증
    if not gender or not age_raw.isdigit() or not co_survey:
        return redirect(url_for("survey_view"))

    age = int(age_raw)

    # db에 자료 저장
    insert_survey(gender=gender, age=age, co_survey=co_survey)

    # 조회 / 분석
    rdata = fetchall_survey()
    # print(rdata)
    crossTab, results, df = analysis_func(rdata)

    # 차트 저장
    if not df.empty:
        save_barchart_func(df, IMG_PATH)

    return render_template(
        "coffee/result.html",
        crossTab=crossTab.to_html() if not crossTab.empty else "데이터가 없음.",
        results=results,
        df=df.to_html(index=False) if not df.empty else "",
        ts=int(time.time())
    )

@app.get("/coffee/surveyshow")
def survey_show():
    # 저장 X, 결과만 출력
    rdata = fetchall_survey()
    crossTab, results, df = analysis_func(rdata)

    # 차트 저장
    if not df.empty:
        save_barchart_func(df, IMG_PATH)

    return render_template(
        "coffee/result.html",
        crossTab=crossTab.to_html() if not crossTab.empty else "데이터가 없음.",
        results=results,
        df=df.to_html(index=False) if not df.empty else "",
        ts=int(time.time())
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)