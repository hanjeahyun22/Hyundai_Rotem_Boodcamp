# 상속 : 자원의 재활용을 목적으로 특정 클래스의 멤버를 가져다 쓰는것
# 코드 재사용
# 확장성 - 기존 클래스에 새 기능을 추가한 새로운 클래스 생성
# 구조적 설계 - 공통개념은 부모 클래스, 구체적 내용은 자식 클래스에서 구현
# 다형성 구사 - 메소드 오버라이딩(부모 클래스의 메소드를 자식 클래스에서 “같은 이름”으로 재정의)
"""
클래스의 결합 관계
- 강결합  :   상속 관계 : 다형성 가능(같은 이름의 메소드가 객체의 실제 타입에 따라 다르게 동작하는 것) -> 유지보수 불편
- 약결합  :   포함 관계
"""

class Animal:                               # 동물들이 가져야 할 공통 특성과 행위 선언
    age = 2
    
    def __init__(self):
        print('-- Animal 생성자 --')        
    
    def move(self):
        print('움직이는 생물')

class Dog(Animal):                          # 상속 관계 -->> 자식[sub]으로 사용 할 클래스 뒤에 (부모[super]로 사용할 클래스) 를 붙임
    def __init__(self):
        print('-- Dog 생성자 --')

    def my(self):
        print('댕댕이')

dog1 = Dog()                                # # 부모 class가 상속되었어도, 자식 class에 의해서 이미 객체가 형성되었기 때문에, 부모 class의 생성자 'print('-- Animal 생성자 --')'는 실행 X
dog1.my()
dog1.move()                                 # 자식 class에는 move 메소드가 없지만, 상속관계에 의해 부모 class까지 탐색해서 move 메소드 실행 가능
print('age : ', dog1.age)
print()
dog2 = Dog()
dog2.my()
dog2.move()
print()

# ##################################
# ##################################
print('====='*5)
print('====='*5)

class Horse(Animal):
    pass

horse1 = Horse()
horse1.move()                               # 이번 경우에는 자식 class(Horse class)에 생성자가 없기 때문에, 상속관계임에도 불구하고, 부모 class의 생성자 'print('-- Animal 생성자 --')'실행