# 터미널창 초기화 (Windows 환경)
import os
os.system('cls')

# 공분산(Covariance) 및 상관계수(Correlation Coefficient) 분석
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 공공데이터(음료수 만족도) 로드
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")

# 1. 표준편차(Standard Deviation) 확인
# 데이터가 평균으로부터 얼마나 퍼져있는지 나타내는 척도
print("친밀도 표준편차:", np.std(data.친밀도))
print("적절성 표준편차:", np.std(data.적절성))
print("만족도 표준편차:", np.std(data.만족도))

# 표준편차 시각화 (히스토그램)
plt.hist([np.std(data.친밀도), np.std(data.적절성), np.std(data.만족도)])
plt.title("Standard Deviation of Variables")
plt.show()
plt.close()

# 2. 공분산(Covariance) 확인
# 두 변수 간의 변화 방향을 나타냄 (양수: 같은 방향, 음수: 반대 방향)
# 하지만 단위(Scale)에 영향을 받으므로 강도를 파악하기는 어려움
print("친밀도 & 적절성 공분산:\n", np.cov(data.친밀도, data.적절성))
print("친밀도 & 만족도 공분산:\n", np.cov(data.친밀도, data.만족도))
print("적절성 & 만족도 공분산:\n", np.cov(data.적절성, data.만족도))

# 산점도(Scatter Plot)를 통한 시각적 관계 파악
plt.scatter(data.친밀도, data.적절성)
plt.xlabel("Intimacy")
plt.ylabel("Appropriateness")
plt.show()

plt.scatter(data.친밀도, data.만족도)
plt.xlabel("Intimacy")
plt.ylabel("Satisfaction")
plt.show()

plt.scatter(data.적절성, data.만족도)
plt.xlabel("Appropriateness")
plt.ylabel("Satisfaction")
plt.show()
plt.close()

# 3. 상관계수(Correlation Coefficient) 확인
# 공분산을 표준화한 값으로 -1에서 1 사이의 값을 가짐
print(np.corrcoef(data.친밀도, data.적절성))
print(np.corrcoef(data.친밀도, data.만족도))
print(np.corrcoef(data.적절성, data.만족도))
print()


print(data.corr()) # 기본값은 pearson

'''
        친밀도       적절성       만족도
친밀도  1.000000    0.499209    0.467145
적절성  0.499209    1.000000    0.766853
만족도  0.467145    0.766853    1.000000

[결과 해석]
1. 적절성과 만족도의 상관계수가 약 0.767로 가장 높음 -> '강한 양의 상관관계'
    즉, 제품의 적절성이 높다고 느낄수록 만족도도 매우 높게 나타나는 경향이 있음.
2. 친밀도와 적절성(0.499), 친밀도와 만족도(0.467)는 '뚜렷한 양의 상관관계'를 보임.
3. 모든 변수가 양의 상관관계를 가지므로, 한 요소가 증가하면 다른 요소도 대체로 증가함.
'''

print(data.corr(method="pearson"))
'''
[Pearson 상관계수]
정의: 두 변수 간의 선형적 관계의 강도를 측정 (모수적 방법)
특징: 연속형 데이터에 사용하며, 정규분포를 가정함

적절성  0.499209    1.000000    0.766853
만족도  0.467145    0.766853    1.000000
'''


print(data.corr(method="kendall"))
'''
[Kendall's tau]
정의: 두 변수 간의 순위 일치 여부를 기반으로 상관성을 측정 (비모수적 방법)
특징: 샘플 사이즈가 작거나 데이터 내에 동순위(tie)가 많을 때 유용함

적절성  0.466729    1.000000    0.703214
만족도  0.459353    0.703214    1.000000
'''


print(data.corr(method="spearman"))
'''
[Spearman 상관계수]
정의: 데이터의 실제 값 대신 순위(rank)를 사용하여 상관관계를 측정 (비모수적 방법)
특징: 비선형 관계(단조 증가/감소)도 포착 가능하며, 이상치에 강건함

적절성  0.511078    1.000000    0.748510
만족도  0.501201    0.748510    1.000000
'''
print()

# 만족도에 따른 다른 특성 사이의 상관관계
co_re = data.corr()
print(co_re["만족도"].sort_values(ascending=False))

# 시각화
data.plot(kind="scatter", x="친밀도", y="만족도")
plt.show()
plt.close()

data.plot(kind="scatter", x="적절성", y="만족도")
plt.show()
plt.close()

data.plot(kind="scatter", x="친밀도", y="적절성")
plt.show()
plt.close()

from pandas.plotting import scatter_matrix
attr = ["친밀도", "적절성", "만족도"]
scatter_matrix(data[attr], figsize=(12, 8))
plt.show()
plt.close()

import seaborn as sns
sns.heatmap(data.corr(), annot=True)
plt.show()
plt.close

# heatmap에 텍스트 표시 추가사항 적용해 보기
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)  # 상관계수값 표시
mask[np.triu_indices_from(mask)] = True
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()