# 터미널창 초기화
import os
os.system('cls')

print("####################################################################################################################################")
print("                                                     numpy 배열 연산")
print("####################################################################################################################################")

# 배열에 행, 열 추가

import numpy as np

aa = np.eye(3)
print(aa)

# 열 추가
bb = np.c_[aa, aa[2]]       # a행렬의 2열과 동일한 열 추가
print(bb)

# 행 추가
cc = np.r_[aa, [aa[2]]]     # a행렬의 2행과 동일한 행 추가
print(cc)

print("##################################################################")
print("           --- 1차원 : append, insert, delete ---")
print("##################################################################")

a = np.array([1,2,3])
print(a)

# append
# b = np.append(a, [4,5])
b = np.append(a, [4,5], axis=0)     # 행 기준
print(b)

# insert
c = np.insert(a, 0, [6, 7])
print(c)

# delete
d = np.delete(a, 1)
print(d)
print(c)

print("##################################################################")
print("           --- 2차원 : append, insert, delete ---")
print("##################################################################")
aa = np.arange(1, 10).reshape(3,3)
print(aa)
print()
print(np.insert(aa, 1, 99))                 # 1차원으로 축소
print()
print(np.insert(aa, 1, 99, axis=0))         # 2차원 유지    # axis=0 : 행 기준
print()
print(np.insert(aa, 1, 99, axis=1))         # 2차원 유지    # axis=1 : 열 기준
print()


print("##################################################################")
print("           조건 연산 where(조건, 참, 거짓)")
print("##################################################################")
x = np.array([1,2,3])
y = np.array([4,5,6])
conditionData = np.array([True, False, True])
result = np.where(conditionData, x, y)
print(result)
print()

aa = np.where(x >= 2)
print(aa)               # (array([1, 2]),) : 인덱스 -> aa 배열의 1, 2번 index값을 받음.
print(a[aa])
print()

print("##################################################################")
print("                          배열 결합 / 분할")
print("##################################################################")

# 배열 결합
kbs = np.concatenate([x, y])
print(kbs)
print()

# 1차원 배열 분할
mbc, sbs = np.split(kbs, 2)
print(mbc)
print(sbs)
print()

# 2차원 배열 분할
a = np.arange(1, 17).reshape(4,4)       # 4*4 행렬
print(a)
x1, x2 = np.hsplit(a, 2)
print(x1)
print(x2)
print()
print(np.vsplit(a, 2))


print("##################################################################")
print("                표본 추출(sampling) - 복원, 비복원")
print("##################################################################")
li = np.array([1,2,3,4,5,6,7])

# 복원(한번 뽑힌 값도 다시 뽑힐 수 있음)
for _ in range(5):
    print(li[np.random.randint(0, len(li)-1)], end = " ")
print()

# 비복원(한번 뽑은 값은 제외)
import random
print(random.sample(li.tolist(), 5))        # random.sample()은 대상이 list type
print()

# choice
print(np.random.choice(range(1, 46), 6))
print(np.random.choice(range(1, 46), 6, replace=True))        # 복원
print(np.random.choice(range(1, 46), 6, replace=False))       # 비복원