# 터미널창 초기화
import os
os.system('cls')

# 공분산(Covariance), 상관계수(Correlation Coefficient)

# 변수가 1개    -->>    분산은 거리(kernel)와 관련 있음.
# 변수가 2개    -->>    분산은 방향을 가짐.

import numpy as np

# np.cov(x, y)는 공분산 행렬을 반환함
# 양의 상관관계  [[2.5 2.5]  [2.5 2.5]]
print("양의 상관관계\n", np.cov(np.arange(1, 6), np.arange(2, 7)))                      # 공분산: 2.5 (데이터 간격이 1일 때)

# 양의 상관관계  [[250. 250.]  [250. 250.]]
print("양의 상관관계\n", np.cov(np.arange(10, 60, 10), np.arange(20, 70, 10)))          # 공분산: 250.0 (데이터 간격이 10배 커지면 공분산은 100배 커짐)

# 양의 상관관계  [[25000. 25000.]  [25000. 25000.]]
print("양의 상관관계\n", np.cov(np.arange(100, 600, 100), np.arange(200, 700, 100)))    # 공분산: 25000.0 (단위/규모에 민감함)

# 상관관계 없음  [[2.5 0. ]  [0.  0. ]]
print("\n상관관계 없음\n", np.cov(np.arange(1, 6), (3, 3, 3, 3, 3)))                    # 상관관계 없음: 한 변수가 고정됨

# 음의 상관관계  [[ 2.5 -2.5]  [-2.5  2.5]]
print("\n음의 상관관계\n", np.cov(np.arange(1, 6), np.arange(6, 1, -1)))                # 음의 상관관계: 한 변수가 증가할 때 다른 변수는 감소
print()




# 두 데이터의 단위에 따른 패턴이 일치하더라도,
# 공분산의 크기가 달라지므로, 절대적 크기 판단 불가능
# -->> 공분산을 표준화해서 상관계수(r) -1, 0, 1 범위로 만듦.
x = [8,3,6,6,9,4,3,9,3,4]
# x값 평균 :  5.5  x값 분산 :  5.45
print("x값 평균 : ", np.mean(x), "\nx값 분산 : ", np.var(x))
y = [6,2,4,6,9,5,1,8,4,5]
# y값 평균 :  5.0  y값 분산 :  5.4
print("y값 평균 : ", np.mean(y), "\ny값 분산 : ", np.var(y))
print()
import matplotlib.pyplot as plt
plt.plot(x, y, 'or')
plt.show()
plt.close()
# x, y의 공분산 :   5.222222222222222
print("x, y의 공분산 : \n", np.cov(x, y)[0,1])

x2 = [80,30,60,60,90,40,30,90,30,40]
y2 = [60,20,40,60,90,50,10,80,40,50]
# x*10, y*10의 공분산 :   522.2222222222222
print("x*10, y*10의 공분산 : \n", np.cov(x2, y2)[0,1])
plt.plot(x2, y2, 'og')
plt.show()
plt.close()

# 상관계수(r) : correlation coefficient (Pearson correlation coeifficient)
# 피어슨 상관계수의 범위에 따른 관계 정도:
# 0.7 ~ 1.0 : 강한 양의 상관관계
# 0.3 ~ 0.7 : 뚜렷한 양의 상관관계
# 0.1 ~ 0.3 : 약한 양의 상관관계
# -0.1 ~ 0.1 : 상관관계 거의 없음
# -1.0 ~ -0.7 : 강한 음의 상관관계

# x, y의 상관계수 :   [[1.         0.86636865]  [0.86636865 1.        ]]
# x2, y2의 상관계수 :   [[1.         0.86636865]  [0.86636865 1.        ]]
print("x, y의 상관계수 : \n", np.corrcoef(x, y))
print("x2, y2의 상관계수 : \n", np.corrcoef(x2, y2))
print()


# 비선형 데이터인 경우, 공분산, 상관계수 의미 X
m = [-3, -2, -1, 0, 1, 2, 3]
n = [9, 4, 1, 0, 1, 4, 9]
print(np.cov(m, n))
print(np.cov(m, n)[0,1])
print()
print(np.corrcoef(m, n))
print(np.corrcoef(m, n)[0,1])
print()

plt.plot(m, n, 'or')
plt.show()
plt.close()

#