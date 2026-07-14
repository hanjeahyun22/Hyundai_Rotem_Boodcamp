# t-test (T-검정) : 
# 검정 통계량이 T-분포를 따르는 통계적 가설 검정 방법이다.
# 주로 두 집단 간의 평균 차이가 통계적으로 유의미한지 확인하기 위해 사용된다.
# 모집단의 분산을 모를 때 표본의 분산을 사용하여 검정하며, 표본의 크기가 작을 때(보통 30개 미만) 유용하다.

# 귀무가설(H0): 집단 간의 평균 차이가 없다.
# 대립가설(H1): 집단 간의 평균 차이가 있다.

# 1. 단일표본 t-검정 (One-sample t-test): 한 집단의 평균이 특정 값과 차이가 있는지 검정
# 정규분포의 표본에 대한 기대값을 조사하는 검정방법이다. 
# 예상 평균값과 표본 자료 간의 평균의 차이를 검정. 
# 독립변수 : 범주형, 종속변수 : 연속형
# 하나의 집단에 대한 평균이 예측된 평균(모집단)과 동일 여부를 확인.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

# 실습 1 : 어느 남성 집단의 평균 키 검정
# 귀무 : 집단 간의 평균 키가 177이다. (모수)
# 대립 : 집단 간의 평균 키가 177이 아니다. 
one_sample = [167.0, 182.7, 169.6, 176.8, 185.0]
print(f"표본 평균: {np.mean(one_sample):.2f}")  # 176.22

result = stats.ttest_1samp(one_sample, popmean=177)  # (데이터, 예상평균값(모수의 평균))
print(f"t-통계량: {result.statistic:.4f}")  # t-통계량: -0.2214
print(f"p-value: {result.pvalue:.4f}")      #  p-value: 0.8356
# [판정] 유의수준 0.05 기준
# p-value(0.8356) >= 0.05 이므로 귀무가설을 채택한다. (평균 키가 177이다)"
print('\n--------------------------')
result2 = stats.ttest_1samp(one_sample, popmean=165)
print(f"t-통계량: {result2.statistic:.4f}")  # t-통계량: 3.1847
print(f"p-value: {result2.pvalue:.4f}")      # p-value: 0.0334
# [판정] 유의수준 0.05 기준
# p-value(0.0334) < 0.05 이므로 대립가설을 채택한다. (평균 키가 165가 아니다)"

sns.displot(one_sample, bins=10, kde=True)
plt.xlabel('data')
plt.ylabel('value')
plt.show()



# 2. 독립표본 t-검정 (Independent samples t-test): 서로 독립된 두 집단 간의 평균 차이 검정





# 3. 대응표본 t-검정 (Paired samples t-test): 동일 집단에 대해 처치 전후의 평균 차이 검정
