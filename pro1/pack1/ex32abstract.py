# 추상 클래스(abstract class)
# 추상 메소드를 가진 클래스를 추상 클래스라고 하며
# abstract class는 인스턴스 하지 못함 -->> 객체 생성 불가
# 오직 부모 class로만 사용
# !!!추상메소드는 overriding 필수!!!


from abc import *



class AbstractClass(metaclass=ABCMeta):  #추상클래스

    @abstractmethod                                         # @메소드이름 : 추상클래스 전환 방법
    def abcMethod(self):                                    # 추상메소드 -->> overriding 필수!!
        pass                                                # 추상 메소드는 내용을 적지 않고 pass 처리

    def normalMethod(self):  #일반메소드
        print('추상클래스 내의 일반 메소드')

#parent = AbstractClass()    #에러:추상클래스는 객체 생성 불가

class Child1(AbstractClass):   #상속

    name = '난 Child1'

    def abcMethod(self):    #선언 강요
        print('추상 메소드를 오버라이드함')

class Child2(AbstractClass):   #상속

    def abcMethod(self):    #선언 강요
        print('추상 메소드를 Child2에서도 오버라이드함')

    def normalMethod(self):  #선언 선택적
        print('추상클래스 내의 일반 메소드를 오버라이드함')


c1 = Child1()            #생성된 객체의 주소를 치환
print(c1.name)
c1.abcMethod()          #Bound Method call
c1.normalMethod() 
print()
c2 = Child2             #클래스를 치환
c2.abcMethod(c2)        #UnBound Method call
c2.normalMethod(c2)


print('\n다형성 -----')
parent = AbstractClass   #추상클래스 타입의 변수 선언은 가능
print(type(parent))
parent = c1
parent.abcMethod()
parent.normalMethod()  #추상클래스의 메소드 수행

print()
parent = c2
parent.abcMethod(parent)
parent.normalMethod(c2)  #자식클래스의 메소드 수행



# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

class Child1(AbstractClass):                # 추상 class를 상속받은 Child1 또한 추상 class
    name = '난 Child1'

    def abcMethod(self):                    # 반드시 overriding을 해줘야만 -->> 일반 class로 전환됨
        print('부모 Class(추상 class)가 가진 abcMethod 재정의!!')

c1 = Child1()
print('name : ', c1.name)
c1.abcMethod()
c1.normalMethod()                           # Child1 class안에 normalMethod 메소드가 없으므로, 부모 class에서 탐색해서 실행

# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

class Child2(AbstractClass):                # 추상 class를 상속받은 Child1 또한 추상 class
    name = '난 Child1'

    def abcMethod(self):                    # 반드시 overriding을 해줘야만 -->> 일반 class로 전환됨
        print('추상 class 내의 abcMethod 재정의!!')

    def normalMethod(self):                 # 일반 메소드 재정의(overriding)
        print('일반 메소드 내용 변경 - overriding')

c2 = Child2()
c2.abcMethod()
c2.normalMethod()                           # overriding을 했으므로 Child2 class의 normalMethod 메소드 사용
print()

# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

# 상속 class의 다형성
happy = c1
happy.abcMethod()
happy = c2
happy.abcMethod()
