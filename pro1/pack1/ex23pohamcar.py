# 여러 개의 부품 객체를 조립해 완성차 생성
# 클래스의 포함 관계 사용   (자원의 재활용)             : OOP의 장점
# 다른 클래스(객체)를 마치 자신의 멤버처럼 선언하고 사용

# import ex23pohamhandle
from ex23pohamhandle import PohamHandle

class PohamCar:
    turnShowMessage = "정지"

    def __init__(self, ownerName):
        
        self.ownerName = ownerName
        self.handle = PohamHandle()                                 # 클래스의 포함관계 : PohamCar의 클래스 안에서 [ex23pohamhandle.py 안의 PohanHandle 클래스]를 사용 -->> quantity 멤버, leftTurn, rightTurn 메소드 이용

    def turnHandle(self, q):
        if q > 0:
            self.turnShowMessage = self.handle.rightTurn(q)         # self.객체.포함관계메소드 : classs의 포함 관계가 적용됨        -->> self. -->> [ctrl + spacebar] 으로 기능 확인
        elif q < 0:
            self.turnShowMessage = self.handle.leftTurn(q)
        elif q == 0:
            self.turnShowMessage = self.handle.straight(q)

if __name__ == '__main__':
    tom = PohamCar('미스터 톰')
    tom.turnHandle(10)
    print(tom.ownerName + '의 회전량은 ' + tom.turnShowMessage + ' ' + str(tom.handle.quantity))     
    # quantity를 알려주기 위해서, [tom = PohamCar('미스터 톰')]에서 인스턴스 후, 객체 생성 -->> 

    john = PohamCar('미스터 존')
    john.turnHandle(-20)
    print(john.ownerName + '의 회전량은 ' + john.turnShowMessage + ' ' + str(john.handle.quantity))

    tttt = PohamCar('미스터 tttt')
    tttt.turnHandle(0)
    print(tttt.ownerName + '의 회전량은 ' + tttt.turnShowMessage + ' ' + str(tttt.handle.quantity))


    