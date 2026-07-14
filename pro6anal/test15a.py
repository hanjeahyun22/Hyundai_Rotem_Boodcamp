# 일원 분산 분석으로 평균 차이 검정
# 강남구에 있는 GS편의점 3개 지역 일

# 귀무 : GS편의점 3개 지역의 매출액 평균에 차이가 없다.
# 대립 : GS편의점 3개 지역 중 적어도 한 지역의 매출액 평균에 차이가 있다.

import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import koreanize_matplotlib
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

uri = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3.txt"

# 읽기 1
# data = pd.read_csv(uri)
# print(data.head())

# 읽기 2
data = np.genfromtxt(urllib.request.urlopen(uri), delimiter=',', skip_header=1)
print(data, type(data))  # <class 'numpy.ndarray'>
print(data.shape)  # (22, 2)

# 세개의 집단 
gr1 = data[data[:, 1] == 1, 0]
gr2 = data[data[:, 1] == 2, 0]
gr3 = data[data[:, 1] == 3, 0]

print(f"\n[그룹1] {gr1}  평균: {np.mean(gr1):.2f}")
print(f"[그룹2] {gr2}  평균: {np.mean(gr2):.2f}")
print(f"[그룹3] {gr3}  평균: {np.mean(gr3):.2f}")

print()
# 정규성 확인 (Shapiro-Wilk test)
print(f"그룹1 정규성 p-value: {stats.shapiro(gr1).pvalue:.4f}")
print(f"그룹2 정규성 p-value: {stats.shapiro(gr2).pvalue:.4f}")
print(f"그룹3 정규성 p-value: {stats.shapiro(gr3).pvalue:.4f}")

# 등분산성 확인
print(stats.levene(gr1, gr2, gr3).pvalue)
print(stats.bartlett(gr1, gr2, gr3).pvalue)

# 데이터 퍼짐 정도 시각화
plt.boxplot([gr1, gr2, gr3], showmeans=True)
plt.show()

# 일원분산분석 방법1 : anova_lm()
df = pd.DataFrame(data=data, columns=['pay','group'])
print(df)
lmodel = ols('pay ~ C(group)', data=df).fit() # C(group)은 group 변수를 범주형(Categorical)으로 취급함을 의미
print(anova_lm(lmodel, typ=1))

# 일원분산분석 방법2 : f_oneway()
f_stat, p_val = stats.f_oneway(gr1, gr2, gr3)
print(f"f-통계량: {f_stat:.4f}")  # f-통계량: 5.3739
print(f"p-value: {p_val:.4f}")    # p-value: 0.0148

# [최종 판정] 유의수준 0.05 기준
# p-value(0.0148) < 0.05 이므로 귀무가설을 기각한다.
# 결론: GS편의점 3개 지역 중 적어도 한 지역의 매출액 평균에 차이가 있다.

# 사후 검정 (Post Hoc Test): 어떤 그룹들 간에 구체적으로 차이가 있는지 확인
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukeyResult = pairwise_tukeyhsd(df['pay'], df['group'])
print(tukeyResult)
# Multiple Comparison of Means - Tukey HSD, FWER=0.05
# 1.0 vs 2.0: p-adj(0.0126) < 0.05 이므로 유의미한 차이가 있음 (reject=True)
# 1.0 vs 3.0, 2.0 vs 3.0: 유의미한 차이가 없음 (reject=False)

# 시각화 
tukeyResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()

# 참고
# anova_lm() : 정규성, 등분성이 깨지면 p-value 신뢰 불가
# f_oneway() : 정규성 깨지면 stats.kruskal(), 등분산성이 깨지면 welch ANOVA 사용