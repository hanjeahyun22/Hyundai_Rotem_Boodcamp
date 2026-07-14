from flask import Flask, render_template, request, jsonify
import pymysql
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime

app = Flask(__name__)

model = None
r2 = 0
coef = 0
intercept = 0
jik_avg = []


def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123',
        database='test',
        port=3306,
        charset='utf8'
    )


def make_model():
    global model, r2, coef, intercept, jik_avg

    # DB 연결
    conn = get_connection()
    cur = conn.cursor()

    # 직원 테이블에서 입사일과 연봉을 조회
    cur.execute("""
        select jikwonibsail, jikwonpay
        from jikwon
        where jikwonibsail is not null and jikwonpay is not null
    """)

    # 조회 결과를 DataFrame으로 변환
    df = pd.DataFrame(cur.fetchall(), columns=['jikwonibsail', 'jikwonpay'])

    # 직급별 평균 연봉 조회
    cur.execute("""
        select ifnull(jikwonjik, '직급없음') as jikwonjik,
        round(avg(jikwonpay), 0) as avg_pay
        from jikwon
        group by jikwonjik
    """)

    # 직급별 평균 연봉 결과를 DataFrame으로 변환
    avg_df = pd.DataFrame(cur.fetchall(), columns=['jikwonjik', 'avg_pay'])

    # DB 연결 종료
    conn.close()

    # 입사일 컬럼을 datetime 형식으로 변환
    df['jikwonibsail'] = pd.to_datetime(df['jikwonibsail'], errors='coerce')

    # NaN, NaT가 들어있는 행 제거
    df = df.dropna()

    # 현재 연도 - 입사 연도 = 근무년수 계산
    df['years'] = datetime.now().year - df['jikwonibsail'].dt.year

    # 근무년수가 0 이상인 데이터만 사용
    # 이상한 데이터가 있으면 제외
    df = df[df['years'] >= 0]

    # 독립변수(x) 설정
    # 근무년수(years)를 사용
    x = df[['years']]

    # 종속변수(y) 설정
    # 연봉(jikwonpay)을 사용
    y = df['jikwonpay']

    # 선형회귀 모델 객체 생성
    model = LinearRegression()

    # x를 이용해 y를 예측하도록 학습
    model.fit(x, y)

    # 회귀계수(기울기) 저장
    # coef_는 배열 형태라 첫 번째 값 사용
    coef = round(float(model.coef_[0]), 4)

    # 절편 저장
    intercept = round(float(model.intercept_), 4)

    # 결정계수(R²) 계산
    # 실제 y값과 예측값 비교 후 백분율 형태로 저장
    r2 = round(r2_score(y, model.predict(x)) * 100, 2)

    # 직급별 평균 연봉 DataFrame을
    # HTML에서 사용하기 쉽게 딕셔너리 리스트 형태로 변환
    jik_avg = avg_df.to_dict(orient='records')


# 메인 페이지 라우팅
# 브라우저에서 / 주소로 접속하면 실행
@app.route('/')
def index():
    # 기본 화면에 보여줄 예측값 계산
    # 근무년수 3년을 넣어 예측
    pred = round(float(model.predict(pd.DataFrame({'years': [3]}))[0]), 2)

    # 예측값이 음수면 0으로 보정
    # 연봉은 음수가 될 수 없기 때문
    if pred < 0:
        pred = 0

    # index.html 파일을 화면에 보여주고
    # 예측값, 설명력, 회귀식, 직급별 평균연봉 데이터 전달
    return render_template(
        'index.html',
        pred=pred,
        r2=r2,
        coef=coef,
        intercept=intercept,
        jik_avg=jik_avg
    )


# 예측 처리 라우팅
# axios가 /predict 주소로 POST 요청을 보내면 실행
@app.route('/predict', methods=['POST'])
def predict():
    # axios는 보통 JSON 형태로 데이터를 전송하므로
    # request.get_json()으로 전달값을 받음
    data = request.get_json()

    # 사용자가 입력한 근무년수를 가져옴
    # 문자열일 수 있으므로 float로 변환
    years = float(data['years'])

    # 입력된 근무년수로 연봉 예측
    # DataFrame 형태로 컬럼명을 맞춰서 예측
    pred = model.predict(pd.DataFrame({'years': [years]}))

    # 예측 결과를 소수점 둘째 자리까지 반올림
    pred_value = round(float(pred[0]), 2)

    # 예측값이 음수면 0으로 보정
    # 실제 연봉은 음수가 될 수 없으므로 처리
    if pred_value < 0:
        pred_value = 0

    # 예측 결과를 JSON 형식으로 반환
    # axios의 response.data로 받을 수 있음
    return jsonify({
        'pred': pred_value,
        'r2': r2,
        'coef': coef,
        'intercept': intercept
    })


if __name__ == '__main__':
    make_model()

    app.run(debug=True)