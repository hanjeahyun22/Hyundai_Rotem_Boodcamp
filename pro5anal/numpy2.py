# 터미널창 초기화
import os
os.system('cls')

print("####################################################################################################################################")
print("                                                     numpy 배열 연산")
print("####################################################################################################################################")

import numpy as np

x = np.array([[1,2], [3, 4]], dtype=np.float32)       # 2*2 행렬
print(x, ' ', x.dtype)

# reshape : 구조 변경 1차원 -> 2차원
y = np.arange(5,9).reshape(2,2)
y = y.astype(np.float32)
print(y, ' ', y.dtype)
print()


print("##################################################################")
print("                       행렬의 각 요소 끼리 계산")
print("##################################################################")


# 더하기
print(x + y)            # 파이썬 연산자
print(np.add(x, y))     # numpy 함수(유니버셜 함수)
print()

# 빼기
print(x - y)            # 파이썬 연산자
print(np.subtract(x, y))     # numpy 함수(유니버셜 함수)
print()

# 곱하기
print(x * y)            # 파이썬 연산자
print(np.multiply(x, y))     # numpy 함수(유니버셜 함수)
print()

# 나누기
print(x / y)            # 파이썬 연산자
print(np.divide(x, y))     # numpy 함수(유니버셜 함수)
print()

print('\ndot은 numpy 모듈의 함수나 배열 객체의 인스턴트 메소드로 사용 가능')
v = np.array([9, 10])
w = np.array([11, 12])
print(v * w)
print()

print("##################################################################")
print("                       행렬 계산 (내적, 외적)")
print("##################################################################")
print('- 행렬 내적의 결과는 Scalar값(크기만 있고 방향 X)')
print(v.dot(w))
print(np.dot(v,w))

print(np.mean(x), ' ', np.var(x))

print(np.max(x), ' ', np.min(x))

# 인덱스 반환
print(np.argmax(x), ' ', np.argmin(x))

# 누적합
print(np.cumsum(x))

# 누적곱
print(np.cumprod(x))
print()

names1 = np.array(['tom', 'james', 'tom', 'oscar'])
names2 = np.array(['tom', 'page', 'john'])
print(np.unique(names1))
print(np.intersect1d(names1, names2))                           # 교집합
print(np.intersect1d(names1, names2, assume_unique=True))       # 교집합(중복 허용)
print(np.union1d(names1, names2))                               # 합집합
print()

print('\n전치(Transpose) - 2차원 배열에서 행과 열의 위치를 바꿈')
print(x)
print(x.T)
print(x.transpose())
print(x.swapaxes(0,1))

print("\nBroadcasting : 크기가 다른 배열 간의 연산 - 작은 배열을 여러 번 반복해 큰 매열과 연산")
x = np.arange(1, 10).reshape(3,3)
y = np.array([1, 0, 1])
print('x : ', x)
print('y : ', y)
print(x + y)

np.savetxt("my.txt", x)