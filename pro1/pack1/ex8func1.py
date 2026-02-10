# function : 여러 개의 수행문을 하나의 이름으로 묶은 실행 단위
# 함수 고유의 실행 공간을 갖음
# 자원의 재활용

# 내장함수
print(sum([1,2,3]))
print(bin(8))
print(eval('4 + 5'))                                # eval : 문자로 된 수식을 계산해줌
print(round(1.2), round(1.6))                       # round : 반올림

import math
print(math.ceil(1.2), ' ', math.ceil(1.6))          # ceil : 올림
print(math.floor(1.2), ' ', math.floor(1.6))        # floor : 내림


b_list = [True, 1, False]
print(all(b_list))                                  # all : 전부 True여야만 결과값이 True
print(any(b_list))                                  # any : 하나라도 True값이 있으면, 결과값이 True

data1 = [10, 20, 30]
data2 = ['a', 'b']
for i in zip(data1, data2):                         # zip : tuple 데이터로 matrix화 시켜줌
    print(i, type(i))