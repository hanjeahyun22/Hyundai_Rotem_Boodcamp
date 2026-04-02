#2
"""
DB에 저장된 buser와 jikwon 테이블을 이용하여 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있는지 검정하시오. 
만약에 연봉이 없는 직원이 있다면 작업에서 제외한다.

귀 : 부서에 따른 연봉 평균은 차이가 없다.
대 : 부서에 따른 연봉 평균은 차이가 있다.
"""
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt 
import koreanize_matplotlib
from pingouin import welch_anova
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pymysql

config = {
    'host':'127.0.0.1', 'user':'root', 'password':'123',
    'database':'test', 'port':3306, 'charset':'utf8mb4'
}
try:
    conn = pymysql.connect(**config)
    sql = """
        select b.busername, j.jikwonpay 
        from jikwon j 
        join buser b on j.busernum = b.buserno
    """
    df = pd.read_sql(sql,conn)
except Exception as e:
    pass
finally:
    conn.close()
df = df.dropna(subset=['jikwonpay']) # jikwonpay Na 제거
gc = df[df['busername'] == '총무부']['jikwonpay']
gy = df[df['busername'] == '영업부']['jikwonpay']
gj = df[df['busername'] == '전산부']['jikwonpay']
gg = df[df['busername'] == '관리부']['jikwonpay']
print(gg)
# 정규성
print(stats.shapiro(gc).pvalue)
print(stats.shapiro(gy).pvalue)
print(stats.shapiro(gj).pvalue)
print(stats.shapiro(gg).pvalue)
# 0.026044936412817302  <- 정규성 만족 X
# 0.06420810634182218
# 0.41940720517769636
# 0.9078027897950541
print()
# 등분산성
print(stats.levene(gc,gy,gj,gg).pvalue)
# 0.7860663814082607
# p > a 이므로 등분산성 만족
# 정규성 X 등분산성 O -> stats.kruskal()
print()
print(stats.kruskal(gc,gy,gj,gg).pvalue)
# p 0.7869924082758515 > a 이므로 귀무 채택 

# 사후 검정 
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=df.jikwonpay, groups=df.busername)
print(tukResult)
# 시각화 
tukResult.plot_simultaneous(xlabel="mean",ylabel='group')
plt.show()