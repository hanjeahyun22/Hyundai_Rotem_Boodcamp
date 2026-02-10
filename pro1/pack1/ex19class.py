# oop - object oriented programming (객체 중심 프로그래밍 가능) : 새로운 타입 생성, 포함, 상속, 다형성 등을 구사
# class(설계도)로 인스턴스 해서 객체를 생성(별도의 이름 공간을 갖음)
# 객체는 멤버 필드(변수)와 메소드로 구성
# JAVA랑 차이점 : 파이썬은 접근 지정자 X, 메소드 오버로딩 X
# 모듈의 멤버 : 변수, 명령문, 험수, 모듈, 클래스
# 메소드 : Class 안에서 정의된 함수 -->> 반드시 argument 를 지녀야함 -->> self
# __init__ : 생성자 : 객체 생성 시, 가장 먼저 1회만 호출 -->> 초기화 담당                       생성자가 굳이 필요 없다면 안써도 상관 X
# __del__ : 소멸자 : 프로그램 종료 시, 자동실행 -->> 마무리 작업
# 클래스이름() : '클래스이름' 타입의 객체 'test'를 생성함 -->> 가장 먼저 __init__ 실행(초기화)   --->>> 가장 나중에 __del__ 실행(종료)
# 클래스로 만든 객체.(멤버/메소드/ ...)
# 인스턴스 : '객체 = 클래스이름()'

# 메소드 호출
## 방법 1) Bound Method call 
## 방법 2) UnBound Method call


print('뭔가를 하다가 class를 이용해서 객체 만들기')

class TestClass:
    aa = 1                                                                      # 멤버 필드(변수),  현재 클래스 내에서 전역,    있어도 되고 없어도 됨.

    def __init__(self):                                                         # __init__ : 특별한 메소드
        print('생성자 : 객체 생성 시, 가장 먼저 1회만 호출 -->> 초기화 담당')

    def __del__(self):
        print('소멸자 : 프로그램 종료 시, 자동실행 -->> 마무리 작업')

    def printMsg(self):                                                         # 일반 메소드
        name = '한국인'                                                         # local 변수 : printMsg 메소드 안에서만 유효한 변수
        print(name)

print(TestClass)                                                                # '<class '__main__.TestClass'>' -->> int, float 같은 사용자 정의 class 속성 'TestClass'

test = TestClass()                                                              # 인스턴스 : 객체 생성      -->>        클래스이름() : 'TestClass' 타입의 객체 'test'를 생성함 -->> 가장 먼저 __init__ 실행(초기화)

# 멤버 호출
print("test 객체의 멤버 aa : ", test.aa)


# 메소드 호출
## 방법 1) Bound Method call                                                    # Bound Method call로 메소드를 호출하면, 객체변수의 주소를 () 안에 넣었다고 인정
test.printMsg()
## 방법 2) UnBound Method call
TestClass.printMsg(test)                                                        # UnBound Method call로 메소드를 호출하면, 객체변수를 직접 () 안에 넣어야됨.

print('-----------'*5)
print(type(1))                                                                  # <class 'int'>
print('-----------'*5)
print(type(1.0))                                                                # <class 'float'>
print('-----------'*5)
print(type(test))                                                               # <class '__main__.TestClass'>
print('-----------'*5)

print(id(TestClass))                                                            # 1930067872048
print('-----------'*5)
print(id(test))                                                                 # 1930063671856     -->>    새로운 객체를 만듦
print('-----------'*5)
test2 = TestClass()
print(id(test2))                                                                # 1695481663952     -->>    또 다른 객체 생성