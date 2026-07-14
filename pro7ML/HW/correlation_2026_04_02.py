# 터미널창 초기화 (Windows 환경)
import os
os.system('cls')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from pandas.plotting import scatter_matrix
import seaborn as sns

'''
상관관계 문제)
https://github.com/pykwon/python 에 있는 Advertising.csv 파일을 읽어
tv,radio,newspaper 간의 상관관계를 파악하시오. 

또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후
TV, radio, newspaper에 대한 영향을 해석하시오.
그리고 이들의 관계를 heatmap 그래프로 표현하시오. 
'''


data = pd.read_csv("Advertising.csv")
print(data.head())
print(np.corrcoef(data.tv, data.radio))
'''
[[1.         0.05480866]
[0.05480866 1.        ]]
해석: 약 0.055로 상관관계가 거의 없음. TV 광고비와 라디오 광고비는 독립적으로 집행됨을 알 수 있음.
'''

print(np.corrcoef(data.tv, data.newspaper))
'''
[[1.         0.05664787]
[0.05664787 1.        ]]
해석: 약 0.057로 상관관계가 거의 없음. TV 광고비와 신문 광고비 간의 연관성이 매우 낮음.
'''

print(np.corrcoef(data.radio, data.newspaper))
'''
[[1.         0.35410375]
[0.35410375 1.        ]]
해석: 약 0.354로 뚜렷한 양의 상관관계를 보임. 라디오 광고를 많이 하는 경우 신문 광고도 병행하는 경향이 있음.
'''
print()

print(data.corr())
'''
                no        tv     radio  newspaper     sales
no         1.000000  0.017715 -0.110680  -0.154944 -0.051616
tv         0.017715  1.000000  0.054809   0.056648  0.782224
radio     -0.110680  0.054809  1.000000   0.354104  0.576223
newspaper -0.154944  0.056648  0.354104   1.000000  0.228299
sales     -0.051616  0.782224  0.576223   0.228299  1.000000
'''

print("\n[Sales 기준 상관관계 정렬]")
print(data.corr()["sales"].sort_values(ascending=False))
'''
[Sales 기준 상관관계 정렬]
sales        1.000000
tv           0.782224
radio        0.576223
newspaper    0.228299
no          -0.051616
Name: sales, dtype: float64

[해석]
1. TV (0.782): 매출(Sales)과 가장 강한 양의 상관관계를 가짐. TV 광고비 투입이 매출 증대에 가장 큰 영향을 미침.
2. Radio (0.576): 매출과 뚜렷한 양의 상관관계를 가짐. 라디오 광고 또한 매출 상승의 주요 요인임.
3. Newspaper (0.228): 매출과 약한 양의 상관관계를 가짐. 다른 매체에 비해 매출 기여도가 상대적으로 낮음.
'''

# Heatmap 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".3f")
plt.title("Advertising Data Correlation Heatmap")
plt.show()