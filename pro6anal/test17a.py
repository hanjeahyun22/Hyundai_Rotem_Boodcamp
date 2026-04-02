# [이원분산분석(Two-way ANOVA)]
# 두 개의 독립변수(범주형)가 하나의 종속변수(연속형)에 미치는 영향을 분석하는 방법이다.
# 각 독립변수의 개별 효과인 '주효과(Main Effect)'와 두 변수가 결합하여 나타나는 '교호작용(Interaction Effect)'을 동시에 검정한다.


# 1. 주효과 가설
# 귀무 : 태아 수와 태아의 머리둘레 평균은 차이 X
# 대립 : 태아 수와 태아의 머리둘레 평균은 차이 O

# 2. 주효과 가설
# 귀무 : 관측자 수와 태아의 머리둘레 평균은 차이 X
# 대립 : 관측자 수와 태아의 머리둘레 평균은 차이 O

# 3. 교호작용 가설
# 귀무 : 교호작용 X (태아수와 관측자 수는 관련 X)
# 대립 : 교호작용 O (태아수와 관측자 수는 관련 O)

# 터미널창 초기화
import os
os.system('cls')

import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
from scipy.stats import wilcoxon
import pandas as pd
import pymysql
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3_2.txt")

# 시각화
# data.boxplot(column = "머리둘레", by = "태아수")
# plt.show()
# data.boxplot(column = "머리둘레", by = "관측자수")
# plt.show()

lin_regression = ols('머리둘레 ~ C(태아수) + C(관측자수)', data=data).fit()         # 교호작용 X
# print(lin_regression.summary())
lin_regression = ols("머리둘레 ~ C(태아수) * C(관측자수)", data=data).fit()         # 교호작용 O
pd.set_option('display.max_columns', None)
result = anova_lm(lin_regression)
print(result)

'''
                            df         sum_sq             mean_sq                    F               PR(>F)
C(태아수)                   2.0     324.008889          162.004444          2113.101449         1.051039e-27
C(관측자수)                 3.0       1.198611            0.399537             5.211353         6.497055e-03
C(태아수):C(관측자수)       6.0       0.562222            0.093704             1.222222         3.295509e-01
Residual                    24.0       1.840000            0.076667              NaN                  NaN
'''

# [이원분산분석(Two-way ANOVA) 결과 해석]

# 1. 태아수(C(태아수))에 대한 검정
# p-value(1.051039e-27) < 0.05 이므로 귀무가설을 기각한다.
# 결론: 태아 수에 따라 태아의 머리둘레 평균은 통계적으로 유의미한 차이가 있다. (주효과 존재)

# 2. 관측자수(C(관측자수))에 대한 검정
# p-value(6.497055e-03) < 0.05 이므로 귀무가설을 기각한다.
# 결론: 관측자 수에 따라 태아의 머리둘레 측정값의 평균은 통계적으로 유의미한 차이가 있다. (주효과 존재)

# 3. 교호작용(C(태아수):C(관측자수))에 대한 검정
# p-value(3.295509e-01) > 0.05 이므로 귀무가설을 채택한다.
# 결론: 태아 수와 관측자 수 간에는 상호작용(교호작용)이 존재하지 않는다.
# 즉, 태아 수에 따른 머리둘레의 차이는 관측자가 누구냐에 따라 달라지지 않는다.





# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
print('='*40)

# 실습 : Poision과 Treat가 독 퍼짐 시간의 평균에 영향을 주나?

# 1. 주효과 가설
# 귀무 : Poision 종류와 독 퍼짐 시간의 평균은 차이 X
# 대립 : Poision 종류와 독 퍼짐 시간의 평균은 차이 O

# 2. 주효과 가설
# 귀무 : Treat 방법과 독 퍼짐 시간의 평균은 차이 X
# 대립 : Treat 방법과 독 퍼짐 시간의 평균은 차이 O

# 3. 교호작용 가설
# 귀무 : 교호작용 X (Poision 종류와 Treat 방법은 관련 X)
# 대립 : 교호작용 O (Poision 종류와 Treat 방법은 관련 O)

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv", index_col=0)

result2 = ols("time ~ C(poison) + C(treat)", data=data2).fit()
print(anova_lm(result2, typ=1))
'''
            df    sum_sq   mean_sq          F        PR(>F)
C(poison)   2.0  1.033013  0.516506  20.643293  5.703728e-07
C(treat)    3.0  0.921206  0.307069  12.272669  6.696971e-06
Residual   42.0  1.050863  0.025021        NaN           NaN
'''
# [이원분산분석(Two-way ANOVA) 결과 해석]
# 1. Poison(C(poison))에 대한 검정
# p-value(5.703728e-07) < 0.05 이므로 귀무가설을 기각한다.
# 결론: Poison 종류에 따라 독 퍼짐 시간의 평균은 통계적으로 유의미한 차이가 있다. (주효과 존재)

# 2. Treat(C(treat))에 대한 검정
# p-value(6.696971e-06) < 0.05 이므로 귀무가설을 기각한다.
# 결론: Treat 방법에 따라 독 퍼짐 시간의 평균은 통계적으로 유의미한 차이가 있다. (주효과 존재)

# 3. 교호작용에 대한 검정 (typ=1 기준, 모델에 교호작용 항을 추가하여 확인 가능)
# 위 분석 결과(typ=1)는 각 변수의 주효과만을 보여주고 있으며, 두 변수 모두 독 퍼짐 시간에 유의미한 영향을 미침을 알 수 있다.


# [사후 분석]
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tkResult1 = pairwise_tukeyhsd(data2['time'], data2['poison'])
print(tkResult1)
tkResult1.plot_simultaneous(xlabel='mean of time', ylabel='poision')
plt.show()
plt.close()

tkResult2 = pairwise_tukeyhsd(data2['time'], data2['treat'])
print(tkResult2)
tkResult2.plot_simultaneous(xlabel='mean of time', ylabel='treat')
plt.show()
plt.close()