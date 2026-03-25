from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
from markupsafe import escape
import matplotlib.pyplot as plt
import koreanize_matplotlib

app = Flask(__name__)

db_config = {
    'host':'127.0.0.1', 'user':'root', 'password':'123',
    'database':'test', 'port':3306, 'charset':'utf8mb4'
}

def get_connection():
    return pymysql.connect(**db_config)

def df_8_global():
    sql = """
        select jikwonno as 사번, jikwonname as 직원명, busername as 부서명, jikwonjik as 직급, jikwonpay as 연봉, year(now()) - year(jikwonibsail) as 근무년수, jikwongen as 성별
        from jikwon join buser on jikwon.busernum = buser.buserno
        order by busernum, jikwonname asc
    """

    # SQL 실행
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]  # description : 컬럼 정보 얻기

    return pd.DataFrame(rows, columns=cols)

@app.route('/')
def main():
    return render_template('main.html')

# #######################################################################################################################################################################
# 1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join)
    # : 부서번호, 직원명 순으로 오름 차순 정렬 
# #######################################################################################################################################################################
@app.route('/ans1')
def ans1():
    df = df_8_global()
    # dept = request.args.get("dept", "").strip()

    return render_template('ans1.html', 

                            ans_8_1=df.to_html(index=False))


#######################################################################################################################################################################
# 2) 부서명, 직급 자료를 이용하여  각각 연봉합, 연봉평균을 구하시오.
#######################################################################################################################################################################
@app.route('/ans2')
def ans2():    
    df = df_8_global()
    # print('부서별 총합 : ', df['jikwonpay'].sum())
    # 직급별 연봉 통계
    if not df.empty:
        stats_df_1 = (
            df.groupby("부서명")["연봉"]
            .agg(
                총합 = "sum",
                평균 = "mean"
            )
            .round(2)
            .reset_index()
            .sort_values(by='평균', ascending=False)
        )
        stats_df_2 = (
            df.groupby("직급")["연봉"]
            .agg(
                총합 = "sum",
                평균 = "mean"
            )
            .round(2)
            .reset_index()
            .sort_values(by='평균', ascending=False)
        )
        # dept = request.args.get("dept", "").strip()
        return render_template('ans2.html', 
                            # dept=escape(dept), 
                            ans_8_2_1=stats_df_1.to_html(index=False),
                            ans_8_2_2=stats_df_2.to_html(index=False))

#######################################################################################################################################################################
# 3) 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력하시오.
#######################################################################################################################################################################
@app.route('/ans3')
def ans3(): 
    df = df_8_global()
    ans3_sum = df.groupby('부서명')['연봉'].sum()
    ans3_mean = df.groupby('부서명')['연봉'].mean()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].bar(ans3_sum.index, ans3_sum.values)
    axes[0].set_title('부서명 별 연봉 합')
    axes[0].set_ylabel('연봉')
    axes[0].grid(True)

    axes[1].bar(ans3_mean.index, ans3_mean.values)
    axes[1].set_title('부서명 별 연봉 평균')
    axes[1].set_ylabel('연봉')
    axes[1].grid(True)


    plt.savefig('static/ans3.png')
    return render_template('ans3.html')

    # plt.figure()
    # # plt.bar(df.groupby('부서명')['연봉'].sum().index, df.groupby('부서명')['연봉'].sum().index)
    # plt.show()

#######################################################################################################################################################################
# 4) 성별, 직급별 빈도표를 출력하시오.
#######################################################################################################################################################################
@app.route('/ans4')
def ans4(): 
    df = df_8_global()
    stats = pd.crosstab(df['성별'], df['직급'])
    return render_template('ans4.html', ans_8_4=stats.to_html())


#######################################################################################################################################################################
# 5) 부서별 최고 연봉자 출력 : 부서명별로 가장 연봉이 높은 직원 1명씩 출력 
# 출력 항목: 부서명, 직원명, 연봉
#######################################################################################################################################################################
@app.route('/ans5')
def ans5(): 
    df = df_8_global()
    rich = df.groupby('부서명')['연봉'].max()

    # jikwonno가 PK이므로, 가장 고연봉 -->> PK값 찾음. (단, 고연봉 중복 X 가정)
    rich_jikwon_no = df[df["연봉"].isin(rich)]
    stats = rich_jikwon_no[['부서명', '직원명', '연봉']]
    return render_template('ans5.html', ans_8_5=stats.to_html())

#######################################################################################################################################################################
# 6) 부서별 직원 비율 계산 : 전체 인원 대비 각 부서 인원 비율(%) 
# 비율 계산 (%)은 dept_ratio = (dept_count / total * 100).round(2)
# 결과를 DataFrame으로 출력
# 예: 총 인원: 30명
#             영업부 20%
#             총무부 30%
#             전산부 5%
#######################################################################################################################################################################
@app.route('/ans6')
def ans6(): 
    df = df_8_global()
    dept_count = df.groupby('부서명').size()
    total = len(df)
    dept_ratio = (dept_count / total * 100).round(2)
    ans8_6 = pd.DataFrame({
        '부서명':dept_ratio.index, 
        '비율':dept_ratio.values
        })
    return render_template('ans6.html', ans_8_6=ans8_6.to_html())


if __name__ == '__main__':
    app.run(debug=True)