# 대응표본 t-검정 (Paired samples t-test)

# 동일 대상의 사전/사후 측정치나 짝을 이룬 두 집단 간의 평균 차이가 0인지 검증하는 통계 기법
# 동일한 대상에 대해 처치 전(Pre)과 처치 후(Post)의 평균 차이를 분석하는 방법
# 두 집단의 표본이 독립적이지 않고 서로 짝지어져 있는 경우에 사용한다. (예: 다이어트 약 복용 전/후 몸무게)

# [가정]
# 1. 대응성: 두 집단의 데이터는 서로 대응되어야 함 (표본 수가 동일해야 함).
# 2. 정규성: 두 측정값의 '차이(Difference)'가 정규분포를 따라야 함.

# 실습 1 : 3강의실 학생들을 대상으로 특강이 시험 점수에 영향을 주었는가?
# 귀무 : 특강 전후의 시험점수 차이는 없다.
# 대립 : 특강 전후의 시험점수 차이는 있다.

import pandas as pd
import scipy.stats as stats
import numpy as np

np.random.seed(123)
x1 = np.random.normal(75, 10, 100)
x2 = np.random.normal(80, 10, 100)


# 1. 정규성 검정
import seaborn as sns
import matplotlib.pyplot as plt
sns.displot(x1, kde=True)
sns.displot(x2, kde=True)
plt.show()


print(stats.shapiro(x1).pvalue)  # 0.27487
print(stats.shapiro(x2).pvalue)  # 0.10214
# [판정] 두 집단 모두 p-value > 0.05 이므로 정규성을 만족함.

# 대응표본 t-test
result = stats.ttest_rel(x1, x2)
print(f"t-통계량: {result.statistic:.4f}")  # -3.0031
print(f"p-value: {result.pvalue:.4f}")      # 0.00338
print(f"자유도: {result.df}")               # 99

# [최종 판정] 유의수준 0.05 기준
# p-value(0.0034) < 0.05 이므로 귀무가설을 기각한다.
# 결론: 특강 전후의 시험 점수 차이는 통계적으로 유의미하다. (특강이 효과가 있음)