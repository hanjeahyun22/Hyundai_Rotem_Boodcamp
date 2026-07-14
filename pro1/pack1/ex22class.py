"""
같은 패키지 내의 다른 모듈(python 파일)의 class를 호출

class는 새로운 타입을 만들어 자원을 공유 가능
"""

# class Singer:
#     title_song = "빛나라 대한민국"

#     def sing(self):
#         msg = "노래는 "
#         print(msg, self.title_song)


# 이런식으로 import하면 귀찮음
# import ex22singer
# bts = ex22singer.Singer()

from ex22singer import Singer
bts = Singer()                                  # Singer class 안에 __init__ 생성자로 따로 명시하지 않았지만, 기본 생성자 호출 -->> 객체 생성 -->> 주소를 bts에 치환
bts.sing()
print(type(bts))                                # Singer라는 class로 생성한 type
bts.title_song = "Permission to dance" 
bts.sing()

bts.cop = '빅히트 엔터'
print('소속사 : ', bts.cop)
print()
print('-----'*5)

ive = Singer()
ive.sing()
print(type(ive))
Singer.title_song = "아 대한민국"

bts.sing()
ive.sing()

niceGroup = ive                                 # ive 의 주소를 niceGroup으로 치환  -->>    ive에게 niceGroup이라는 별명
niceGroup.sing()