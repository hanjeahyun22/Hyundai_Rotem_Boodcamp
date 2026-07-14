import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

# 실습 2 : 복부 지방 제거 수술의 효과 검정

# 데이터 생성 (사전, 사후)
baseline = [67.2, 67.4, 71.5, 77.6, 86.0, 89.1, 59.5, 81.9, 105.5]
follow_up = [62.4, 64.6, 70.4, 62.6, 80.1, 73.2, 58.2, 71.0, 101.0]

# 가설 설정
# 귀무(H0): 수술 참여 전과 후의 복부 지방량 평균에 차이가 없다. (차이의 평균 = 0)
# 대립(H1): 수술 참여 전과 후의 복부 지방량 평균에 차이가 있다. (차이의 평균 != 0)

print(f"사전 평균: {np.mean(baseline):.2f}")  # 사전 평균: 78.41
print(f"사후 평균: {np.mean(follow_up):.2f}")   # 사후 평균: 71.50
print(f"차이 평균: {np.mean(np.array(baseline) - np.array(follow_up)):.2f}")  # 차이 평균: 6.91

# 시각화
plt.bar(np.arange(2), [np.mean(baseline), np.mean(follow_up)])
plt.xlim(0,1)
plt.xlabel("수술 전/후", fontdict={'fontsize':12, 'fontweight':'bold'})
plt.show()

# 대응표본 t-검정 수행
# stats.ttest_rel(a, b) 함수 사용
t_stat, p_val = stats.ttest_rel(baseline, follow_up)

print(f"t-통계량: {t_stat:.4f}")  # t-통계량: 6.6923
print(f"p-value: {p_val:.4f}")    # p-value: 0.0001

# [최종 판정] 유의수준 0.05 기준
# p-value(0.0001) < 0.05 이므로 귀무가설을 기각한다.
# 결론: 복부 지방 제거 수술은 효과가 있다고 할 수 있다. (평균 차이가 유의미함)
