# pack1/ex15module - main

# 사용자 정의 모듈
print('사용자 정의 모듈 처리하기')

s = 20                                      # 작업을 하던 중, 내가 정의했던 pack1.mymod1 모듈이 필요한 경우

print('\n경로 지정 방법1 : import 모듈명')
import pack1.mymod1                               # 같은 패키지(pack1)에 들어있더라도, 보조기억장치로 import 필요
print(dir(pack1.mymod1))                          # dir : 모듈의 멤버 확인
print(pack1.mymod1.__file__)                      
print(pack1.mymod1.__name__)
list1 = [1, 2]
list2 = [3, 4, 5]
pack1.mymod1.listhap(list1, list2)

if __name__ == '__main__': print('와우 메인 모듈')      # python.exe 파일로 실행하는 그 파일이 mian 모듈


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n경로 지정 방법2 : from 모듈명 imort 함수명(메소드명), 변수, ...')      # from 모듈명 import 후에, [crtl + spacebar] -->> 멤버 명 확인 가능

from pack1.mymod1 import kbs
kbs()

from pack1.mymod1 import mbc, tot
mbc()
print(tot)

from pack1.mymod1 import *                                # import * : 해당 모듈의 모든 멤버 로딩(비권장)
print('tot: ', tot)

# from pack1.pack1.mymod1 import mbc                        # from 패키지명.모듈명 import 멤버명          -->>  상위 디렉토리에서 실행 가능

from pack1.mymod1 import mbc as mmmmmm                    # as : 불러온 멤버의 이름을 바꿔줄 수 있음
mmmmmm()


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n경로 지정 방법3 : import 하위패키지.모듈명')
import pack1.subpack.sbs
print(pack1.subpack.sbs.sbsMansae())
pack1.subpack.sbs.sbsMansae()

import pack1.subpack.sbs as nickname
nickname.sbsMansae()


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n경로 지정 방법4 : 현재 패키지와 동등한 다른 패키지 모듈 읽기')

# import ../pack1_other.mymod2          # 개념은 맞지만, vsCode는 인정 X
from pack1_other import mymod2
mymod2.hapFunc(4, 3)


import mymod3                                           # 원래 사용자 정의 모듈로 만든 'momod3'을 '.../anaconda3/envs/myproject/Lib' 디렉토리로 복사 했으므로, 표준 module 처럼 import
                                                        # 경로가 등록된 경우, 표준 module처럼 import 가능
result = mymod3.gopFunc(4, 3)
print('path가 설정된 곳의 module 읽기 - result : ', result)



print('end')