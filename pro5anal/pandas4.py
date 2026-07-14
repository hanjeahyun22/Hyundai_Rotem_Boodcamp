# 터미널창 초기화
import os
os.system('cls')

# DataFrame 재구조화(열을 행으로, 행을 열로 이동)
import pandas as pd
import numpy as np

df = pd.DataFrame(1000 + np.arange(6).reshape(2,3), index=["대전", "서울"],columns=["2020", "2021", "2022"])
print(df)
print()

print("######################################################################################################")
print("                           --------stack, unstack -------")
print("######################################################################################################")
print("stack : 열을 행으로 변경") 
df_row = df.stack()
print(df_row)
print()

print("unstack : 행을 열로 이동") 
df_col = df_row.unstack()
print(df_col)
print()

print("######################################################################################################")
print("-------- 범주화 : 연속적인 숫자 데이터를 구간(범위)으로 나눠서 그룹으로 묶는 것 -------")
print("                           --------pd.cut, pd.qcut -------")
print("######################################################################################################")
"""
            pd.cut()                        pd.qcut()
기준    구간 크기를 균등하게            데이터 개수를 균등하게
        내가 지정경계값 직접 지정       몇 등분할지 숫자만 지정
"""
print("------------- cut -------------------")
# 그룹 구간 : (a, b]) => a < x <= b
price = [10.3, 5.5, 7.8, 3.6]
cut = [3, 7, 9, 11]
result_cut = pd.cut(price, cut)
print(result_cut)
print()
print(pd.Series(result_cut).value_counts())

# head(n) : 수많은 데이터 중에서 앞의 n개만 보겠다 -> defalt는 5개
# tail(n) : 수많은 데이터 중에서 뒤의 n개만 보겠다 -> defalt는 5개
datas = pd.Series(np.arange(1, 10001))
print(datas.head(3))
print()
print(datas.tail(2))
print()

print("------------- qcut -------------------")
result_cut2 = pd.qcut(datas, 3)
print(result_cut2)
# print(pd.value_counts(result_cut2))
print(pd.Series(result_cut2).value_counts())

print("\nagg함수 : 범주의 그룹별 연산")
group_col = datas.groupby(result_cut2, observed=True)       # ovserved=True : 데이터가 있으면 작업
print(group_col)


print("#################################################################################################################################")
print("agg (aggregate) — 그룹 전체를 하나의 숫자로 요약합니다. 내장 통계 함수 이름을 문자열로 넘기거나 여러 개를 리스트로 넘길 수 있습니다.")
print("#################################################################################################################################")
print(group_col.agg(["count", "mean", "std", "min"]))


print("#################################################################################################################################")
print("\napply — 그룹 데이터 전체를 내가 만든 함수로 자유롭게 처리합니다. 리턴값의 형태에 따라 결과가 달라집니다.")
print("#################################################################################################################################")
# agg 대신 사용자 함수를 작성
def summaryFunc(gr):
    return {
        "count" :   gr.count(),
        "mean"  :   gr.mean(),
        "std"   :   gr.std(),
        "min"   :   gr.min()
    }


print(group_col.apply(summaryFunc))
print(group_col.apply(summaryFunc).unstack())


print("#################################################################################################################################")
print("                                       merge : 데이터 프레임 객체 병합")
print("#################################################################################################################################")
df1 = pd.DataFrame({"data1":range(7), "key":["b", "b", "a", "c", "a", "a", "b"]})
print(df1)
print()
df2 = pd.DataFrame({"key":["a", "b", "d"], "data2":range(3)})
print(df2)
print()

# 교집합(inner join)
print("----------------- inner join(교집합) ----------------------")
print(pd.merge(df1, df2, on="key"))
print()
print(pd.merge(df1, df2, on="key", how="inner"))
print()

# full outer join
print("----------------- full outer join ----------------------")
print(pd.merge(df1, df2, on="key", how="outer"))
print()

# left outer join
print("----------------- left outer join ----------------------")
print(pd.merge(df1, df2, on="key", how="left"))
print()

# right outer join
print("----------------- right outer join ----------------------")
print(pd.merge(df1, df2, on="key", how="right"))
print()

# 공통 column명이 없는 경우
print("----------------- 공통 column명이 없는 경우 ----------------------")
df3 = pd.DataFrame({"key2":["a", "b", "d"]})            # df3 : df1과 공통 column명이 없는 Dataframe(단, 데이터의 성격은 같아야함.)
print(df3)
print("---- inner join(교집합) ----")
print(pd.merge(df1, df3, left_on="key", right_on="key2"))

print("---- concat : 공통 키 없이 그냥 DataFrame을 물리적으로 이어 붙이는 함수 ----")

print("<행 단위>\n", pd.concat([df1, df3], axis=0))
print()
print("<열 단위>\n", pd.concat([df1, df3], axis=1))


print("#################################################################################################################################")
print("                                   pivot_table : pivot과 groupby 명령의 중간적 성격")
print("#################################################################################################################################")
print("pivot : 데이터 열 중에서 두 개의 열(key)을 사용해 데이터의 행렬을 재구성")
print()

data = {"city"  :   ["강남", "강북", "강남", "강북"],
        "year"  :   [2000, 2001, 2002, 2002],
        "pop"   :   [3.3, 2.5, 3.0, 2.0]
        }
df = pd.DataFrame(data)
print(df)
print()

print(df.pivot(index="city", columns="year", values="pop"))
print()
print(df.pivot(index="year", columns="city", values="pop"))
print()

print("---- set_index : 기존 행의 index를 제거하고, 첫번째 열의 index로 설정 ----")
print(df.set_index(["city", "year"]).unstack())
print()

print("---- pivot_table : 설명을 얻는 기능 ----")
print(df["pop"].describe())
print()

print("아무런 옵션을 안주면 기본값 : 평균")
print(df.pivot_table(index=["city"]))
print()
# print(df.pivot_table(index=["city"], aggfunc=np.mean))
print(df.pivot_table(index=["city"], aggfunc="mean"))
print()
print("'aggfunc=len' : 건 수")
print(df.pivot_table(index=["city", "year"], aggfunc=[len, "mean"]))
print()

# 도시별 인구 평균 (aggfunc 미지정 → 기본값 mean)
print(df.pivot_table(values="pop", index="city"))       # aggfunc로 옵션을 안줬으므로, 기본값 평균
print()

# 도시별 데이터 개수 (aggfunc=len → count와 동일)
print(df.pivot_table(values="pop", index="city", aggfunc=len))
print()

# 연도(행) × 도시(열) 교차표 — 각 칸은 인구 평균
print(df.pivot_table(values="pop", index=["year"], columns=["city"]))
print()

# margins=True → 행/열 끝에 전체 합계(All) 행·열 추가
print(df.pivot_table(values="pop", index=["year"], columns=["city"], margins=True))
print()

# fill_value=0 → 데이터 없는 칸(NaN)을 0으로 채움
print(df.pivot_table(values="pop", index=["year"], columns=["city"], margins=True, fill_value=0))
print()

print("#################################################################################################################################")
print("                                   groupby")
print("#################################################################################################################################")
hap = df.groupby(["city"])
print(hap)
print("==")
print("<df.groupby().sum()>\n", df.groupby(["city"]).sum())
print()
print("<df.groupby().mean()>\n",df.groupby(["city"]).mean())