# 이원카이제곱
# 동질검 검정 : 두 집단의 분포가 동일한지? 아니면 다른 분포인지?를 검증하는 방법
# 분포 비율 차이 검정
# 두 집단 이상에서 각 범주 집단 간의 비율이 서로 동일한가를 점정
# 두 개 이상의 범주형 자료가 동일한 분포를 갖는 모집단에서 추출된 것인지 검정하는 방법.

# 동질성 검정 실습:
# 교육방법(독립변수)에 따른 교육생들의 만족도(종속변수) 분석 동질성 검정
# surver_mthod.csv

# 귀무가설(H0) : 교육 방법과 만족도는 관계 X
# 대립가설(H1) : 교육 방법과 만족도는 관계 O

import pandas as pd
import scipy.stats as stats

# 만족도에 대한 설문조사 수집 자료
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv")
print(data.head(3))
print()
print(data["method"].unique())      # [1 2 3]
print(data["survey"].unique())      # [1 2 3 4 5]
print()

# 교차표 작성
ctab = pd.crosstab(index=data["method"], columns=data["survey"])
ctab.index = ["방법1", "방법2", "방법3"]
ctab.columns = ["매우만족", "만족", "보통", "불만족", "매우불만족"]
print(ctab)

chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f"chi2 : {chi2}, p : {p}, dof : {dof}")               # chi2 : 6.544667820529891, p : 0.5864574374550608, dof : 8
print("expected : \n", expected)                            # 예측 비율

# 해석 : 유의수준(alpha = 0.05) < p_value(= 0.5864574374550608)     -->>    귀무가설(H0) 채택
# -->> surver_mthod.csv의 자료는 우연히 발생된 자료임.
# -->> 교육방법과 만족도는 관계 X
print("============"*10)

# 동질성 검정 실습 : 연령대별 sns 이용률의 동질성 검정
# 20대에서 40대까지 연령대별로 서로 조금씩 그 특성이 다른 SNS 서비스들에 대해 이용 현황을 조사한 자료를 바탕으로
# 연령대별 홍보 전략 세우기
# 연령대별로 이용 현황이 서로 동일한지 검정.

# 귀무가설(H0) : 연령대별로 SNS 서비스별 이용율 현황은 동일하다.
# 대립가설(H1) : 연령대별로 SNS 서비스별 이용율 현황은 동일하지 않다.

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv")
print(data.head(3))
print()

print(data["age"].unique())
print(data["service"].unique())
print()

ctab2 = pd.crosstab(index=data["age"], columns=data["service"])
ctab2.index = ["20대", "30대", "40대"]
print(ctab2)
print()

chi2, p, dof, expected = stats.chi2_contingency(ctab2)
print(f"chi2 : {chi2}, p : {p}, dof : {dof}")               # chi2 : 102.75202494484225, p : 1.1679064204212775e-18, dof : 8
print("expected : \n", expected)

# 판정 : 유의수준(alpha = 0.05) > p_value(= 1.1679064204212775e-18)     -->>    귀무가설(H0) 기각   -->>    대립가설(H1) 채택
# 연령대별로 SNS 서비스별 이용률 현황은 동일 X

print("전체 건수 : ", len(data))
# 위 자료는 샘플 자료지만, 모집단이라고 가정하고, 샘플링 후 검정
samp_data = data.sample(n=500, replace=True, random_state=1)        # replace=True : 복원추출
print("샘플 건수 : ", len(samp_data))
print()

ctab2_sample = pd.crosstab(index=samp_data["age"], columns=samp_data["service"])
ctab2_sample.index = ["20대", "30대", "40대"]
print(ctab2_sample)
print()

chi2_sample, p_sample, dof_sample, expected_sample = stats.chi2_contingency(ctab2)
print(f"chi2 : {chi2_sample}, p : {p_sample}, dof : {dof_sample}")               # chi2 : 102.75202494484225, p : 1.1679064204212775e-18, dof : 8
print("expected : \n", expected_sample)