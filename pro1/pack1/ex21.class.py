# 동일한 이름의 변수가 Global, 함수 내의 Local, 클래스 내의 멤버 filed, 클래스 메소드 내의 Local 변수 안에 모두 선언되어 있는 경우

kor = 100                                       # 모듈의 전역변수

def abc():
    kor = 0                                     # 함수 내의 local 변수
    print('모두의 멤버 함수')

class My:
    kor = 80                                    # My 멤버 변수 (필드)
    
    def abc(self):
        print('My 멤버 메소드')

    def show(self):
        # kor = 77                                # 메소드 내의 local 변수                      # 만약 주석처리
        print(kor)                                                                             # 위에서 주석처리 -->> 모듈의 전역(global)변수 'kor = 100' 출력
        print(self.kor)
        self.abc()                              # My class 내의 abc(self) 메소드로 감       -->> print('My 멤버 메소드')
        abc()                                   # 전역(global) 모듈에 선언된 abc() 함수로 감 -->> print('모두의 멤버 함수')

my = My()
my.show()                                       # local 변수의 'kor = 77' 출력

print('-----'*5)

print(My.kor)           # 80
print('-----'*5)
tom = My()
print(tom.kor)          # 80
print('-----'*5)
tom.kor = 88
print(tom.kor)          # 88
print('-----'*5)

oscar = My()
print(oscar.kor)        # 80