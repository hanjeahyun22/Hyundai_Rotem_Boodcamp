# 메소드 overriding(재정의)
# 부모에서 정의된 메소드를 자식이 동일 이름의 메소드로 내용만 변경 해 사용
# 부모 메소드의 기능을 대체하는 새로운 기능
# 동작의 구체화(공통 틀은 부모가, 실제 행동은 자식이) 실현
# Polymorphism(다형성) - 같은 메소드이지만, 객체에 따라 다른 기능을 수행
# 확장, 유지보수에 도움 - 부모 코드는 유지한 채 자식 코드만 변경

class Parent:
    def printData(self):
        pass

class Child1(Parent):
    def abc():
        print('Child1 고유 메소드')
    
    def printData(self):                            # 메소드 overriding
        a = 5 + 6
        # ...

        print('Child1에서 printData 재정의')        

class Child2(Parent):
    def printData(self):                            # 메소드 overriding
        print('Child2에서 printData override')      
        msg = "부모와 동일 메소드 이름이지만, 내용은 다름"
        print(msg)

c1 = Child1()
c1.printData()
print()
c2 = Child2()
c2.printData

print('\n--- 다형성 ---')
par = Parent()
par = c1
par.printData()
print()
par = c2
par.printData()
"""
--- 다형성 ---
Child1에서 printData 재정의

Child2에서 printData override
부모와 동일 메소드 이름이지만, 내용은 다름

    -->> par.printData() 완전히 똑같은 명령이지만, 
    "Child1에서 printData 재정의" // 
    "Child2에서 printData override" 
    다른 행동 수행 <<--
"""