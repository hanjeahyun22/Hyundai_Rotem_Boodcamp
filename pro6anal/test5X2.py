# 이원카이제곱 : 교차 분할표 이용
# -> 두 개 이상의 변인 집단 또는 범주를 대상으로 검정 수행
# 분석 대상의 집단 수에 의해서, '독립석 검정', '동질성 검정'으로 나뉨
# 독립성 : 동일 집단의 두 변인 학력 수준과 대학 진학 여부를 대상으로 관련성이 있는
# 독립성 검정은 두 변수 사이의 연관성을 검정함.

# 실습
# 교육수준(독립변수, x)가 흡연률(종속변수, y) 간의 관련성 분석 -> smoke.csv

# 귀무 가설 : 교육 수준과 흡연률 간에 관계가 없음. (independent)
# 대립 가설 : 교육 수준과 흡연률 간에 관계가 있음. (dependent)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head())
print(data["education"].unique())                           # [1:대학원졸 2:대졸 3:고졸]
print(data["smoking"].unique())                             # [1:과흡연 2:보통 3:비흡연]
print()

# 학력 수준별 흡연 빈도수 : 교차표 사용
ctab = pd.crosstab(index=data["education"], columns=data["smoking"])
ctab.index = ["대학원졸", "대졸", "고졸"]
ctab.columns = ["과흡연", "보통", "비흡연"]
print(ctab)

# 이원카이제곱 검정
chi_result = [ctab.loc["대학원졸"], ctab.loc["대졸"], ctab.loc["고졸"]]
chi2, p, dof, expected = stats.chi2_contingency(chi_result)
print(f"chi2 : {chi2}, p : {p}, dof : {dof}")               # chi2 : 18.910915739853955, p : 0.0008182572832162924, dof : 4
print("expected : \n", expected)                            # 예측된 기대 도수

# 판정1 : 유의수준(= 0.05) > p_value(=0.0008182572832162924) 이므로, 귀무가설(H0) 기각
# 교육수준과 흡연율 간에 관계가 있다. smoke.csv(수집자료)는 우연히 발생된 자료가 아니다.

# 판정2 : chi2: 18.910915, dof:4, critical value : 9.49("카이제곱분포표" 에 의한 값)
# chi2 값이 임계치 우측에 있으므로, 귀무가설(H0) 기각, 대립가설(H1) 채택

# 이후 다양한 자료, 의견등으로 보고서 작성



print("=====================  독립성 검정 : 실습2) ====================")
# 남성과 여성의 스포츠 음료 선호도 검정

# 귀무가설(H0) : 성별과 음료 선호는 서로 관련이 없다.
# 대립가설(H1) : 성별과 음료 선호는 서로 관련이 있다.

data = pd.DataFrame({
    "게토레이":[30, 20],
    "포카리":[20, 30],
    "비타500":[10, 30]
}, index=["남성", "여성"])
print(data)

chi2, p, dof, expected = stats.chi2_contingency(data)
print("p_value : ", p)
print("chi2 value : ", chi2)
print("dof : ", dof)
print("expected : \n", expected)

# p_value :  0.003388052521834713
# chi2 value :  11.375
# dof :  2
# expected :
#  [[21.42857143 21.42857143 17.14285714]
#  [28.57142857 28.57142857 22.85714286]]

# 판정 : 예상된 기대도수와 관측값은 서로 관련이 있는가?
# 유의수준(alpha = 0.05) > p_value(=0.003388052521834713) -->> 귀무가설(H0) 기각
# -->> 성별과 음료 선호는 서로 관련 있음.

