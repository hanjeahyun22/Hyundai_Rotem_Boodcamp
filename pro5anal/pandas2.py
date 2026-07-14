# 터미널창 초기화
import os
os.system('cls')

# 재색인
from pandas import Series, DataFrame
import numpy as np

# Sereies의 재색인
data = Series([1,2,3], index = (1,4,2))         # index는 순서대로 1, 4, 2, 값은 순서대로 1, 2, 3
print(data)

# 행의 순서를 바꾸는 re-indexing    -->> value도 순서가 같이 바뀜
data2 = data.reindex((1,2, 4))
print(data2)

print('n재색인 할 때 값 채워 넣기')
data3 = data2.reindex([0, 1, 2, 3, 4, 5])
print(data3)

# 대응값이 없는 인덱스(0, 3, 5 번째 값)에는 fill_value라는 특정값 사용
data3 = data2.reindex([0,1,2,3,4,5], fill_value=777)
print(data3)
print()

# 값이 없다면, 이전 값으로 Nan을 채움  -->> 이전 값이 없는 경우(0번째 index)는 NaN으로 채움
data3 = data2.reindex([0,1,2,3,4,5], method='ffill')
print(data3)
data3 = data2.reindex([0,1,2,3,4,5], method='pad')
print(data3)


# 값이 없다면, 다음 값으로 Nan을 채움  -->> 다음 값이 없는 경우(마지막번째 index)는 NaN으로 채움
data3 = data2.reindex([0,1,2,3,4,5], method='bfill')
print(data3)
data3 = data2.reindex([0,1,2,3,4,5], method='backfill')
print(data3)

print('\nDataFrame : bool 처리')
df = DataFrame(np.arange(12).reshape(4,3), index=['1월', '2월', '3월', '4월'], columns=['강남', '강북', '서초'])
print()
print(df)
print()

print(df["강남"])
print()

print(df['강남'] > 3)
print()

print('강남 열의 값이 3을 초과하는 True값만 출력')
print(df[df['강남'] > 3])
print()

print(df < 3)
print()

df[df < 3] = 0
print(df)
print()

print("\n슬라이싱 관련 메소드 : loc() : 라벨 지원, iloc() : 숫자 지원")
print(df.loc['3월', :])     # Series로 출력
print()
print(df.loc[:'2월'])
print()
print(df.loc[:"2월", ["서초"]])
print()
print('---- iloc 함수 ----')
print(df.iloc[2])
print(df.iloc[2, :])
print()
print(df.iloc[:3])
print()
print(df.iloc[:3, 2])