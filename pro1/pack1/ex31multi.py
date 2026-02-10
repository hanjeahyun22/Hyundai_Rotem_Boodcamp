# class의 다중 상속 (부모 class가 여러개)

class Tiger:
    data = "호랑이 세계"

    def cry(self):
        print('호랑이 : 어흥')

    def eat(self):
        print('맹수는 고기를 좋아함')

class Lion:
    def cry(self):
        print('사자 : 으르렁')

    def hobby(self):
        print('백수의 왕은 낮잠이 취미')

class Liger1(Tiger, Lion):                  # class의 다중 상속 -->> 다중 상속은 순서가 중요!!  -->> 이름이 같은 메소드가 있다면, 먼저 적은 부모 class의 메소드 사용
    pass

a1 = Liger1()
print(a1.data)
a1.eat()
a1.hobby()
a1.cry()

# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)


def hobby():
    print('hobby 함수는 모듈의 멤버 : 일반 함수')


class Liger2(Lion, Tiger):                 
    data = '라이거 만세'

    def play(self):
        print('라이거 고유 메소드')

    def hobby(self):
        print('라이거는 공원 걷기를 좋아함')

    def showData(self):
        self.hobby()                    # 일단 Liger2 클래스 안을 탐색 후에, Lion, Tiger class를 차례대로 탐색
        super().hobby()                 # 곧바로 Lion, Tiger class를 탐색
        hobby()                         # class 밖의 전역에 선언된 hobby 함수 사용

        self.eat()
        super().eat()

        print(self.data + ' ' + super().data)


a2 = Liger2()
a2.cry()                                # 'class Liger2(Lion, Tiger):' 의 순서에 따라서, Lion class의 cry() 메소드 이용
a2.showData()
