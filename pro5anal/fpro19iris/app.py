from flask import Flask, render_template, request
import pandas as pd
import numpy as np  
import seaborn as sns
import matplotlib
matplotlib.use('Agg')       
# Agg(Anti Grain Geometry) : matplotlib의 렌더링 엔진 중 하나 
# 이미지 저장 시 오류 방지 - 차트 출력 없이 저장할 때 사용
import matplotlib.pyplot as plt
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent      # 현재 파일의 경로 의미
STATIC_DIR = BASE_DIR / 'static' / 'images'
STATIC_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/showdata')
def showdata():
    df = sns.load_dataset('iris')
    # print(df.head())

    # pie chart 생성 및 저장(서버에서 자체 출력 X)
    counts = df['species'].value_counts().sort_index()
    plt.figure()
    counts.plot.pie(autopct='%1.1f%%', startangle=90, ylabel='')
    plt.tight_layout()

    img_path = STATIC_DIR / 'fpro19.png'
    plt.savefig(img_path, dpi=130)
    plt.close()

    irishtml = df.to_html(
        classes='table table-striped table-sm', index=False
    )
    return render_template(
        'show.html',
        table = irishtml,
        img_path = 'images/fpro19.png'
        )

if __name__ == '__main__':
    app.run(debug=True)