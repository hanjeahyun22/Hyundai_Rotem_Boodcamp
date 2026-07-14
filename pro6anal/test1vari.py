# 터미널창 초기화
import os
os.system('cls')


print("""
# ######################################################################################################################
#                                               표준편차, 분산의 중요성
# ######################################################################################################################
""")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(42)

# 목표 평균
target_mean = 60
std_dev_small = 10
std_dev_large = 20

# data
class1_raw = np.random.normal(target_mean, std_dev_small, size=100)
class2_raw = np.random.normal(target_mean, std_dev_large, size=100)
# print(class1_raw)
# print(class2_raw)

# 평균 보정
class1_adjusted = class1_raw - np.mean(class1_raw) + target_mean
class2_adjusted = class2_raw - np.mean(class2_raw) + target_mean

# 정수화
# np.clip(배열, lower_bound, upper_bound) : 배열의 값 중에서, lower_bound보다 작은 값은 lower_bound로변환 / upper_bound보다 큰 값은 upper_bound로 변환
# ex) 배열 : (5, 45, 78, ...)   -->>    np.clip(배열, 10, 60)   -->>    (10, 45, 60, ...)
class1_clipped = np.clip(class1_adjusted, 0, 100).astype(int)
class2_clipped = np.clip(class2_adjusted, 0, 100).astype(int)
# print(class1_clipped)
# print(class2_clipped)

# 통계 계산
mean1, mean2 = np.mean(class1_clipped), np.mean(class2_clipped)
std1, std2 = np.std(class1_clipped), np.std(class2_clipped)
var1, var2 = np.var(class1_clipped), np.var(class2_clipped)

print("1반(성적 편차 작음)")
print(f"평균: {mean1:.2f}, 표준편차: {std1:.2f}, 분산: {var1:.2f}")
print()
print("2반(성적 편차 큼)")
print(f"평균: {mean2:.2f}, 표준편차: {std2:.2f}, 분산: {var2:.2f}")
print()

df = pd.DataFrame({
    "class": ["1반"] * 100 + ["2반"] * 100,
    "score": np.concatenate([class1_clipped, class2_clipped])
})
print(df.head())
df.to_csv("test1vari.csv", index=False, encoding="utf-8-sig")
print()

# 시각화
print('--------- 시각화 ---------')
x1 = np.random.normal(1, 0.05, size=100)
x2 = np.random.normal(2, 0.05, size=100)

# 산점도
plt.figure(figsize=(10, 6))
plt.scatter(x1, class1_clipped, alpha=0.8, label=f'Class 1(평균 = {mean1:2f}, 표준편차 = {std1:2f})')
plt.scatter(x2, class2_clipped, alpha=0.8, label=f'Class 2(평균 = {mean2:2f}, 표준편차 = {std2:2f})')
plt.hlines(target_mean, 0.5, 2.5, colors='r', linestyles='dashed', label=f'공통평균={target_mean}')
plt.xticks([1, 2], ['1반', '2반'])
plt.ylabel('시험 점수')
plt.title('Scatter Plot of Two Classes')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
print()

# Box plot
plt.figure(figsize=(8, 5))
plt.boxplot([class1_clipped, class2_clipped], labels=['1반', '2반'])
plt.title('Box Plot of Two Classes')
plt.grid(True)
plt.show()
print()

# Histogram plot
plt.figure(figsize=(10, 6))
plt.hist(class1_clipped, bins=15, alpha=0.6, label=f'Class 1(평균 = {mean1:2f}, 표준편차 = {std1:2f})', edgecolor='black')
plt.hist(class2_clipped, bins=15, alpha=0.6, label=f'Class 2(평균 = {mean2:2f}, 표준편차 = {std2:2f})', edgecolor='blue')
plt.axvline(target_mean, color='r', linestyle='dotted', label=f'공통평균={target_mean}')
plt.xlabel('시험 점수')
plt.ylabel('빈도')
plt.title('Histogram of Two Classes')
plt.legend()
plt.tight_layout()
plt.show()
print()


print("""
####################################################################################################
[가설 검정 (Hypothesis Testing) 정리]

1. 가설 설정
- 귀무가설 (H0) : 두 집단 간 차이가 없다 (기존 주장)
- 대립가설 (H1) : 두 집단 간 차이가 있다 (새로운 주장)
※ 목표 : H0를 기각할 수 있는지 판단
----------------------------------------------------------------------------------------------------
2. p-value (유의확률)
- 정의 :
    귀무가설(H0)이 참이라고 가정했을 때,
    현재 관측된 결과(또는 더 극단적인 결과)가 나올 확률
- 해석 기준 (보통 α = 0.05 사용)
    p-value < 0.05  → H0 기각 → 통계적으로 유의미한 차이 있음
    p-value ≥ 0.05 → H0 기각 불가 → 차이가 있다고 말할 수 없음
- 주의
  * p-value ≠ H0가 맞을 확률
  * p-value는 “우연일 가능성”을 의미
----------------------------------------------------------------------------------------------------
3. t-test (평균 비교 검정)
- 목적 :
    두 집단의 평균 차이가 통계적으로 유의미한지 확인
- 기본 개념 :
    t = (평균 차이) / (데이터의 변동성)
    → 평균 차이가 크고, 데이터 분산이 작을수록 t값이 커짐
    → t값이 클수록 p-value는 작아짐 → 차이 있다고 판단
----------------------------------------------------------------------------------------------------
4. t-test 종류
- 독립표본 t-test (Independent)
    : 서로 다른 집단 비교 (예: A그룹 vs B그룹)
- 대응표본 t-test (Paired)
    : 동일 대상의 전후 비교 (예: 치료 전 vs 후)
- 단일표본 t-test (One-sample)
    : 집단 평균 vs 기준값 비교
----------------------------------------------------------------------------------------------------
5. 분석 절차 (Workflow)
1) 가설 설정 (H0, H1)
2) 유의수준 설정 (α = 0.05)
3) t-test 수행 → p-value 계산
4) 결과 해석
    - p < 0.05 → H0 기각 → 차이 있음
    - p ≥ 0.05 → H0 유지 → 차이 판단 불가
----------------------------------------------------------------------------------------------------
6. 한 줄 핵심 정리
- t-test : 평균 차이를 검정하는 방법
- p-value : 그 차이가 우연인지 판단하는 기준
- p < 0.05 : 통계적으로 유의미
####################################################################################################
""")
