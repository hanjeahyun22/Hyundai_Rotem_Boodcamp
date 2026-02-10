# Module : 소스 코드의 재사용을 가능하게 하며, 소스 코드를 하나의 이름 공간으로 구분하고 관리
# 하나의 파일은 하나의 모듈이 된다
# 표준 모듈, 사용자 작성 모듈, 제3자 모듈(thirt party)로 구분 할 수 있다
# import 모듈명
# from 모듈명 import (멤버 / 함수 / 변수)

print(print.__module__)         # print 함수가 'builtins'의 멤버임

print(' ')
print('-----------'*5)
print(' ')

print('뭔가를 하다가... 외부 모듈 사용하기')

import sys                      # 표준 module이지만 많이 쓰이지 않기 때문에, import 필요
print(sys.path)                 # 일반 멤버

a = 5
if a > 7:
    sys.exit()                  # sys.exit() : 응용 프로그램의 강제 종료                                 # 함수인지 멤버인지 파악 불가 -->> api를 읽어봐야 알 수 있음

import math
print(math.pi)                  # pi는 (pi) 이런식으로 안쓰므로, module의 멤버 


import calendar
calendar.setfirstweekday(6)
calendar.prmonth(2026,2)
del calendar                    # del : import 했던 module 삭제


import random
print(random.random())          # random.random() : 0 ~ 1 사이의 random 실수
print(random.randrange(1, 10))
print(random.randint(0,9))


from random import random, choice, randrange       # 이런식으로 'from 모듈명 import 멤버' 선언하면, 곧바로 member사용
from random import *                               # from 모듈명 import * : 모듈의 모든 멤버를 물러옴
print(random())

print('end')