'''

[문항15] 아래 코드가 동작하도록 자전거 클래스(Bicycle class)를 정의하시오.

조건1 : 멤버 변수는 name, wheel, price 이다.
조건2 : 바퀴 가격은 바퀴수 * 가격이다.

실행 및 출력 결과)
gildong = Bicycle('길동', 2, 50000) # 생성자로 name, wheel, price 입력됨
gildong.display()

길동님 자전거 바퀴 가격 총액은 100000원 입니다. (배점:10)
'''


class Bicycle:
    def __init__(self, name, wheel, price):
        self.name = name
        self.wheel = wheel
        self.price = price

    def display(self):
        tot_var = self.wheel * self.price
        print(f'{self.name}님 바퀴 가격 총액은 {tot_var}원 입니다.')

gildong = Bicycle('길동', 2, 50000)
gildong.display()