from sklearn.linear_model import LinearRegression
import statsmodels.api
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import koreanize_matplotlib
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from flask import Flask, render_template, request, jsonify
import pymysql


app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8mb4'
}

sql = """
    select jikwonjik, jikwonpay, year(now()) - year(jikwonibsail) as year from jikwon
"""

def get_connection():
    return pymysql.connect(**db_config)


def get_model_result():
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()

    # 컬럼명 변경
    df.columns = ['jik', 'pay', 'years']

    # 결측치 제거
    df = df.dropna()

    # 독립변수(X), 종속변수(y)
    x = df[['years']].values
    y = df[['pay']].values

    # 모델 생성
    lmodel = LinearRegression()
    lmodel.fit(x, y)

    # 회귀계수, 절편
    coef = lmodel.coef_[0][0]
    intercept = lmodel.intercept_[0]

    # 예측값
    pred = lmodel.predict(x)

    # 모델 성능 지표
    r2 = r2_score(y, pred)
    mse = mean_squared_error(y, pred)
    rmse = np.sqrt(mse)
    evs = explained_variance_score(y, pred)

    # 직급별 평균 연봉
    jik_avg = df.groupby('jik')['pay'].mean().reset_index()
    jik_avg['pay'] = jik_avg['pay'].round(0).astype(int)

    return {
        'model': lmodel,
        'coef': coef,
        'intercept': intercept,
        'r2': r2,
        'mse': mse,
        'rmse': rmse,
        'evs': evs,
        'jik_avg': jik_avg
    }


@app.route('/')
def index():
    result = get_model_result()

    return render_template(
        'index.html',
        r2=round(result['r2'] * 100, 2),
        mse=round(result['mse'], 2),
        rmse=round(result['rmse'], 2),
        evs=round(result['evs'], 4),
        coef=round(result['coef'], 4),
        intercept=round(result['intercept'], 4),
        jik_avg=result['jik_avg'].values.tolist()
    )


@app.route('/predict', methods=['POST'])
def predict():
    years = float(request.form['years'])

    result = get_model_result()
    model = result['model']

    new_x = [[years]]
    pred = model.predict(new_x)

    pay = int(pred[0][0])

    return jsonify({
        'pay': format(pay, ',')
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)