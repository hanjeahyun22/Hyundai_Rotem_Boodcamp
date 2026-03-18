# 터미널창 초기화
import os
os.system('cls')

print("####################################################################################################################################")
print("                                                     numpy 기본 예제")
print("####################################################################################################################################")
# numpy의 ndarray는 단순한 배열 X    -->>     벡터/행렬 연산도 가능한 다차원 수치 데이터 구조

import numpy as np

# python의 list 자료형
ss = ['tom', 'james', 'oscar', 1, True]                 # python의 List는 다양한 type의 데이터가 들어가 수 있음
print(ss, ' ', type(ss))

# list 자료형을 numpy.ndarray 형식으로 바꿈
ss2 = np.array(ss)                                      # numpy의 ndarray는 같은 type의 자료로만 구성
print(ss2, ' ', type(ss2))                              # ['tom' 'james' 'oscar' '1' 'True']    -->>    전부 문자열

li = list(range(1, 10))
print(li)
print(li[0], ' ', id(li[0]))

print(li * 10)
for i in li: print(i*10, end =" ")

num_arr = np.array(li)
print(num_arr[0], ' ', num_arr[1], ' ', id(num_arr[0]), id(num_arr[1]))
print(num_arr * 10)
print()

# 여러 타입의 자료가 입력되면 상위 타입으로 자동변환. (int -> float -> complex -> str)
a = np.array([1,2,3], dtype='float32')
print(a, type(a))
print()

b = np.array([[1,2,3], [4,5,6]])                    # 2행 3열
print(b.shape, ' ', b[0,0], ' ', b[[0]])            # b[[0]] 는 팬시 인덱싱(Fancy Indexing) : 리스트로 행을 선택하는 방식  -->  b[[0]] : 행렬 b의 0행
print()

# 0행렬
c = np.zeros((2,2))
print(c)
print()

# 1행렬
d = np.ones((2,2))
print(d)
print()

# 단위행렬
e = np.eye(3)
print(e)
print()

# 랜덤
print(np.random.rand(5))        # 균등 분포
print(np.random.randn(5))       # 정규 분포
print(np.random.randn(2,3))

# 랜덤값인데, 결과값을 고정하고 싶을 때     -->>    시드 넘버를 줌
np.random.seed(0)
print(np.random.randn(2,3))

print(list(range(0, 10)))
print(np.arange(10))
print()

# 인덱싱/슬라이싱
a = np.array([1,2,3,4,5])
print(a, ' ', a[3])
print(a[2:4])                   # a행렬의 2번째부터 4번째전 까지  -> 2 이상 4 미만 번째
print(a[1:])
print(a[1:5:2])                 # a행의 1번째부터 5번째값 전까지 증가치 2  --> 1, 3번째 값 출력
print(a[-2:])

# 주소 치환
b = a
b[0] = 88
print(a[0], ' ', b[0])

# nparray cooy : 복사본 생성
c = np.copy(a)
b[0] = 33
print(a[0], ' ', c[0])