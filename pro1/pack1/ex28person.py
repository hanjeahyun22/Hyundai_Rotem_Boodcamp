# 상속

class Person:
    say = '난 사람이야'                                                 # 접근 권한 : public
    nai = '20'
    __msg = 'good : private 멤버'                                       # 접근 권한 : private       -->>    __멤버명 : private으로 접근 권한 설정 -->> 다른 class에서는 참조 불가능 멤버


    def __init__(self, nai):
        print('Person 생성자')
        self.nai = nai

    def printInfo(self):
        print(f'나이 : {self.nai}, 이야기 : {self.say}')                # self.nai, self.say : 현재 Person class 내부의 say, nai 멤버를 이용하겠다

    def helloMethod(self):
        print('안녕')
        print('hello : ', self.say, self.nai, self.__msg)

print(Person.say, Person.nai)
# Person.printInfo()
per = Person('25')                                                      # Person의 생성자에 'def __init__(self, nai):' nai 변수가 있으므로 값을 줘야됨
per.printInfo()
per.helloMethod()

# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

class Employee(Person):
    subject = '근로자'
    say = '일하는 동물'                                                 # hiding(shadowing) : 부모가 가진 멤버를 자식이 다시 선언 -->> 자식의 멤버를 사용

    def __init__(self):
        print('Employee 생성자')

    def printInfo(self):                                                # Shadowing : 부모가 가진 메소드를 자식이 다시 선언 -->> 자식의 메소드를 사용
        print('Employee 클래스의 printInfo 호출됨') 

    def ePrintInfo(self):
        print(self.subject, self.say, self.nai)                                   
        # self.say : Employee 자식 class에 say 멤버가 있으므로, 'say = '일하는 동물' 이용
        # self.nai : Employee 자식 class가 Person 부모 class를 상속하고 있으므로, 먼저 자식 클래스를 탐색하고, 부모 클래스를 탐색해서 Person 클래스의 nai 멤버 이용
        
        
        # print('hello : ', self.say, self.nai, self.__msg)             # self.__msg 는 부모 class에서 'private member'로 선언했기 때문에, 자식 클래스에서 호출 불가능
        
        self.helloMethod()                                              # Person 부모 class를 상속하고 있으므로, 부모 class의 메소드를 self. 뒤에 붙여서 사용 가능
        self.printInfo()
        print(super().say)                                              # super().부모class_멤버 : 자식 class 안에서도 부모 class의 멤버를 읽어옴           -->> 바로 윗 부모 class 권한에만 접근 가능
        super().printInfo()                                             # super().부모class_메소드 : 자식 class 안에서도 부모 class의 메소드를 읽어옴 
        

emp = Employee()
print(emp.subject, emp.nai, emp.say)
emp.ePrintInfo()

# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

class Worker(Person):
    def __init__(self, nai):
        print('Worker 생성자')
        super().__init__(nai)                                           # 부모 class의 생성자 호출      :       자식 class에 생성자가 있지만, 부모 class의 생성자를 명시적으로 호출하고 싶은 경우 -->> 하나의 class에는 하나의 생성자만 가능하므로, 부모 class의 생성자를 호출

    def wPrintInfo(self):
        # self.printInfo()                                                # self.     :   일단 자식 class를 탐색하고, 없으면 부모 class 탐색
        super().printInfo()                                             # super().  :   곧바로 부모 class에서 탐색

wor = Worker('30')                                                      # 'super().__init__(nai)' 에 의해서 명시적으로 부모 class의 생성자를 실행하므로, nai 입력변수 필요
print(wor.say, wor.nai)
wor.wPrintInfo()
"""
Worker 생성자                   -->>        자식 생성자 먼저 실행
Person 생성자                   -->>        super().__init__(nai) 에 의해서 부모 생성자 실행
난 사람이야 30
나이 : 30, 이야기 : 난 사람이야
"""


# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)

class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer 생성자')
        super().__init__(nai)
        # super().__init__(nai)                     # Bound call
        Worker.__init__(self, nai)                  # Unbound call

    def pPrintInfo(self):
        print('Programmer - pPringInfo 처리하였음')

    def wPrintInfo(self):                           # 자식 class에서 부모 class의 메소드와 동일 메소드 선언 -->> 부모 class인 Worker class에 이미 wPrintInfo 메소드가 있지만, 자식 class인 Programmer class에 동일한 이름의 메소드를 다시 선언
        print('Programmer에서 overriding')

pro = Programmer(35)
print(pro.say, pro.nai)
pro.pPrintInfo()
pro.wPrintInfo()


print('\n클래스 타입 확인')
a = 3; print(type(a))
print(type(pro))
print(type(wor))
print(Person.__bases__)             # class명.__bases__ : 해당 class의 super class확인 : Person class의 type는 'object'라는 super class에 상속되어있음 -->> 기초에 메이커들이 만들어 놓은 class 상속관계
print(Employee.__bases__)
print(Worker.__bases__)
print(Programmer.__bases__)