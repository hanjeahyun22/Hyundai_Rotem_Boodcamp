# 터미널창 초기화
import os
os.system('cls')

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

'''
pandas 문제 1)
a) 표준정규분포를 따르는 9 X 4 형태의 DataFrame을 생성하시오. 
np.random.randn(9, 4)
b) a에서 생성한 DataFrame의 칼럼 이름을 - No1, No2, No3, No4로 지정하시오
c) 각 컬럼의 평균을 구하시오. mean() 함수와 axis 속성 사용
'''
# a)
print("\n---------------------- Problem_1_a ----------------------")
print()
mat1 = np.random.randn(9,4)
df_1_a = pd.DataFrame(mat1)
print(df_1_a)

# b)
print("\n---------------------- Problem_1_b ----------------------")
print()
ans_1_b = pd.DataFrame(mat1, columns=["No1", "No2", "No3", "No4"])
print(ans_1_b)

# c)
print("\n---------------------- Problem_1_c ----------------------")
print()
ans_1_c = mat1.mean(axis=0)
print(ans_1_c)

'''
pandas 문제 2)

    numbers
a   10
b   20
c   30
d   40

a) DataFrame으로 위와 같은 자료를 만드시오. colume(열) name은 numbers, row(행) name은 a~d이고 값은 10~40.
b) c row의 값을 가져오시오.
c) a, d row들의 값을 가져오시오.
d) numbers의 합을 구하시오.
e) numbers의 값들을 각각 제곱하시오. 아래 결과가 나와야 함.

numbers
a   100
b   400
c   900
d   1600

f) floats 라는 이름의 칼럼을 추가하시오. 값은 1.5, 2.5, 3.5, 4.5    아래 결과가 나와야 함.

numbers floats

a   10  1.5
b   20  2.5
c   30  3.5
d   40  4.5

g) names라는 이름의 다음과 같은 칼럼을 위의 결과에 또 추가하시오. Series 클래스 사용.

    names
d   길동
a   오정
b   팔계
c   오공
'''

# a)
print("\n---------------------- Problem_2_a ----------------------")
print()
mat2 = np.arange(10, 50, 10).T
print(mat2)
df_2_a = pd.DataFrame(data=mat2, columns=['numbers'], index=['a', 'b', 'c', 'd'])
print(df_2_a)

# b)
print("\n---------------------- Problem_2_b ----------------------")
print()
ans_2_b = df_2_a.loc["c", :]
print(ans_2_b)

# c)
print("\n---------------------- Problem_2_c ----------------------")
print()
ans_2_c = df_2_a.loc[["a", "d"], :]
print(ans_2_c)

# d)
print("\n---------------------- Problem_2_d ----------------------")
print()
ans_2_d = df_2_a.sum(axis=0)
print(ans_2_d)

# e)
print("\n---------------------- Problem_2_e ----------------------")
print()
print(df_2_a.mul(df_2_a))

# f)
print("\n---------------------- Problem_2_f ----------------------")
print()
vec2_f = np.arange(1.5, 5.5, 1.0).T
df_2_a["floats"] = vec2_f
print(df_2_a)

# g)
print("\n---------------------- Problem_2_g ----------------------")
print()
vec2_g = pd.Series(['길동', '오정', '팔계', '오공'], index=df_2_a.index)
df_2_a["names"] = vec2_g
print(df_2_a)


'''
pandas 문제 3)
1) 5 x 3 형태의 랜덤 정수형 DataFrame을 생성하시오. (범위: 1 이상 20 이하, 난수)
2) 생성된 DataFrame의 컬럼 이름을 A, B, C로 설정하고, 행 인덱스를 r1, r2, r3, r4, r5로 설정하시오.
3) A 컬럼의 값이 10보다 큰 행만 출력하시오.
4) 새로 D라는 컬럼을 추가하여, A와 B의 합을 저장하시오.
5) 행 인덱스가 r3인 행을 제거하되, 원본 DataFrame이 실제로 바뀌도록 하시오.
6) 아래와 같은 정보를 가진 새로운 행(r6)을 DataFrame 끝에 추가하시오.
        A     B    C     D
r6   15   10    2   (A+B)
'''
# 1)
print("\n---------------------- Problem_3_1 ----------------------")
print()
val3 = np.random.randint(1, 21, 15).reshape(5, 3)
df_3 = pd.DataFrame(data=val3)
print(df_3)

# 2)
print("\n---------------------- Problem_3_2 ----------------------")
print()
df_3.columns=["A", "B", "C"]
df_3.index=["r1", "r2", "r3", "r4", "r5"]
print(df_3)

# 3)
print("\n---------------------- Problem_3_3 ----------------------")
print()
print(df_3[df_3["A"] > 10])

# 4)
print("\n---------------------- Problem_3_4 ----------------------")
print()
df_3["D"] = df_3["A"] + df_3["B"]
print(df_3)

# 5)
print("\n---------------------- Problem_3_5 ----------------------")
print()
df_3.drop("r3", axis=0, inplace=True)
print(df_3)

# 6)
print("\n---------------------- Problem_3_6 ----------------------")
print()
new_row = pd.DataFrame(data=np.random.randint(1,15,3).reshape(1,3), columns=["A", "B", "C"])
new_row["D"] = new_row["A"] + new_row["B"]
print(new_row)
df_3.loc["r6"] = new_row.iloc[0]
print(df_3)


'''
pandas 문제 4)
다음과 같은 재고 정보를 가지고 있는 딕셔너리 data가 있다고 하자.
data = {
    'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'price':   [12000,     25000,      150000,    900000],
    'stock':   [  10,         5,          2,          3 ]
}
1) 위 딕셔너리로부터 DataFrame을 생성하시오. 단, 행 인덱스는 p1, p2, p3, p4가 되도록 하시오.
2) price와 stock을 이용하여 'total'이라는 새로운 컬럼을 추가하고, 값은 'price x stock'이 되도록 하시오.
3) 컬럼 이름을 다음과 같이 변경하시오. 원본 갱신
    product → 상품명,  price → 가격,  stock → 재고,  total → 총가격
4) 재고(재고 컬럼)가 3 이하인 행의 정보를 추출하시오.
5) 인덱스가 p2인 행을 추출하는 두 가지 방법(loc, iloc)을 코드로 작성하시오.
6) 인덱스가 p3인 행을 삭제한 뒤, 그 결과를 확인하시오. (원본이 실제로 바뀌지 않도록, 즉 drop()의 기본 동작으로)
7) 위 DataFrame에 아래와 같은 행(p5)을 추가하시오.
            상품명             가격     재고    총가격
 p5       USB메모리    15000     10    가격*재고
'''
data = {
    'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'price':   [12000,     25000,      150000,    900000],
    'stock':   [  10,         5,          2,          3 ]
}

# 1)
print("\n---------------------- Problem_4_1 ----------------------")
print()
df_4 = pd.DataFrame(data=data, index=["p1", "p2", "p3", "p4"])
print(df_4)

# 2)
print("\n---------------------- Problem_4_2 ----------------------")
print()
df_4["total"] = df_4["price"] * df_4["stock"]
print(df_4)

# 3)
print("\n---------------------- Problem_4_3 ----------------------")
print()
df_4.columns = ["상품명", "가격", "재고", "총가격"]
print(df_4)