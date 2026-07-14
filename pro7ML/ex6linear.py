# 전통적 방법의 선형회귀(기계학습 중 지도학습)
print('\n방법4 : make_regression 사용. model 생성 X')

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# IQ에 따른 시험점수 예측
score_iq = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/score_iq.csv')
print(score_iq.head(3))
#      sid  score   iq  academy  game  tv
# 0  10001     90  140        2     1   0
# 1  10002     75  125        1     3   3
# 2  10003     77  120        1     0   4
print(score_iq.info())
x = score_iq.iq
y = score_iq.score
print(x[:3])
# 0    140
# 1    125
# 2    120
print(y[:3])
# 0    90
# 1    75
# 2    77

print('상관계수 : ', np.corrcoef(x,y)[0,1])  # 상관계수 :  0.8822
print(score_iq[['iq','score']].corr())
#             iq    score
# iq     1.00000  0.88222
# score  0.88222  1.00000


print('-'*40)
# 단순 선형회귀 분석 (인과관계가 있다는 가정하에 진행)
model = stats.linregress(x,y)
print(model)   # slope = 0.6514309527270075, intercept = -2.8564471221974657
# linregress_results
# slope = 0.6514309527270075
# intercept = -2.8564471221974657
print('기울기 : ', model.slope)
print('절편 : ', model.intercept)
print('p-value : ', model.pvalue)

plt.scatter(x,y)
plt.plot(x, model.slope * x + model.intercept, c='r')
plt.show()
# predict 메소드를 지원하지 않음.
# print('점수예측 : ', np.polyval([model.slope, model.intercept],np.array(score_iq.iq)))  # 전체 예측
new_df = pd.DataFrame({'iq':[55,66,77,88,150]})
print('점수예측 : \n', np.polyval([model.slope, model.intercept],new_df))
# 점수예측 :  
#  [[32.97225528]
#  [40.13799576]
#  [47.30373624]
#  [54.46947672]
#  [94.85819579]]