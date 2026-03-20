from pandas import DataFrame, Series
import numpy as np

# pandas 문제 1)
#   a) 표준정규분포를 따르는 9 X 4 형태의 DataFrame을 생성하시오. 
#      np.random.randn(9, 4)
#   b) a에서 생성한 DataFrame의 칼럼 이름을 - No1, No2, No3, No4로 지정하시오
#   c) 각 컬럼의 평균을 구하시오. mean() 함수와 axis 속성 사용
datas = np.random.randn(9,4)
#a)
df = DataFrame(datas)
print(df)
#b)
df = DataFrame(datas, columns=['No1', 'No2', 'No3', 'No4'])
print(df)
#c)
print(df.mean(axis=1))

# pandas 문제 2)

# a) DataFrame으로 위와 같은 자료를 만드시오. colume(열) name은 numbers, row(행) name은 a~d이고 값은 10~40.
df2 = DataFrame([10,20,30,40], index=['a','b','c','d'], columns=('numbers',))
print(df2)
# b) c row의 값을 가져오시오.
print('c row의 값 : ', df2.loc[['c']])
# c) a, d row들의 값을 가져오시오.
print('a, d row의 값 : ',df2.loc[['a', 'd']])
# d) numbers의 합을 구하시오.
print('numbers의 합 : ',df2.sum())
# e) numbers의 값들을 각각 제곱하시오. 아래 결과가 나와야 함.
print('numbers 제곱', df2**2)
# f) floats 라는 이름의 칼럼을 추가하시오. 값은 1.5, 2.5, 3.5, 4.5    아래 결과가 나와야 함.
df2['floats'] = [1.5, 2.5, 3.5, 4.5]
print(df2)
# g) names라는 이름의 다음과 같은 칼럼을 위의 결과에 또 추가하시오. Series 클래스 사용.
names = Series(['길동','오정','팔계','오공'], index=['d','a','b','c'])
print(names)
df2['names'] = names
print(df2)

# pandas 문제 3)
# 1) 5 x 3 형태의 랜덤 정수형 DataFrame을 생성하시오. (범위: 1 이상 20 이하, 난수)
data3 = np.random.randint(1,21, size=(5,3))
df3 = DataFrame(data3)
print(df3)
# 2) 생성된 DataFrame의 컬럼 이름을 A, B, C로 설정하고, 행 인덱스를 r1, r2, r3, r4, r5로 설정하시오.
df3 = DataFrame(data3, columns=['A','B','C'], index=['r1','r2','r3','r4','r5'])
print(df3)
# 3) A 컬럼의 값이 10보다 큰 행만 출력하시오.
print(df3[df3['A'] > 10])
# 4) 새로 D라는 컬럼을 추가하여, A와 B의 합을 저장하시오.
d = df3['A']+df3['B']
df3['D'] = d
print(df3)
# 5) 행 인덱스가 r3인 행을 제거하되, 원본 DataFrame이 실제로 바뀌도록 하시오.
df3.drop('r3',inplace=True)
print(df3)
# 6) 아래와 같은 정보를 가진 새로운 행(r6)을 DataFrame 끝에 추가하시오.
#          A     B    C     D
#   r6   15   10    2   (A+B)
print('-----'*5)
df3.loc['r6'] = ['15', '10', '2', '25']
print(df3)

# pandas 문제 4)
# 다음과 같은 재고 정보를 가지고 있는 딕셔너리 data가 있다고 하자.
# data = {
#     'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
#     'price':   [12000,     25000,      150000,    900000],
#     'stock':   [  10,         5,          2,          3 ]
# }
# 1) 위 딕셔너리로부터 DataFrame을 생성하시오. 단, 행 인덱스는 p1, p2, p3, p4가 되도록 하시오.
data4 = {
    'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'price':   [12000,     25000,      150000,    900000],
    'stock':   [  10,         5,          2,          3 ]
}
df4 = DataFrame(data4, index=['p1','p2','p3','p4'])
print(df4)
# 2) price와 stock을 이용하여 'total'이라는 새로운 컬럼을 추가하고, 값은 'price x stock'이 되도록 하시오.
total = df4['price'] * df4['stock']
df4['total'] = total
print(df4)
# 3) 컬럼 이름을 다음과 같이 변경하시오. 원본 갱신
#    product → 상품명,  price → 가격,  stock → 재고,  total → 총가격
df4.rename(columns={'product':'상품명','price':'가격','stock':'재고','total':'총가격'}, inplace=True)
print(df4)
# 4) 재고(재고 컬럼)가 3 이하인 행의 정보를 추출하시오.
print(df4[df4['재고'] <= 3])
# 5) 인덱스가 p2인 행을 추출하는 두 가지 방법(loc, iloc)을 코드로 작성하시오.
print(df4.loc['p2'])
print(df4.iloc[1])
# 6) 인덱스가 p3인 행을 삭제한 뒤, 그 결과를 확인하시오. (원본이 실제로 바뀌지 않도록, 즉 drop()의 기본 동작으로)
imsi = df4.drop('p3')
print(imsi)
# 7) 위 DataFrame에 아래와 같은 행(p5)을 추가하시오.
#             상품명             가격     재고    총가격
#  p5       USB메모리    15000     10    가격*재고
df4.loc['p5'] = ['USB메모리', '15000', '10', '150000']
print(df4)