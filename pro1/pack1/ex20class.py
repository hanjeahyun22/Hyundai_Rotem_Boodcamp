class Car:
    handle = 1
    speed = 0

    def __init__(self, name, speed):
        self.name = name                                # 현재 객체의 name에게 지역변수 name(local 변수) 인자값 치환
        self.speed = speed

    def showData(self):
        km = '킬로미터'
        msg = '속도 : ' + str(self.speed) + km
        return msg
    
    def printhHandle(self):
        return self.handle
    
print(Car.handle)                                       # 원형(prototype) 클래스의 멤버 호출

# Bound Method call
car1 = Car('tom', 10)                                   # 인스턴스 화 : 생성자 호출 후 객체 생성
print('car1 객체의 주소 : ', car1)
print('car1 : ', car1.name, ' ', car1.speed, ' ', car1.handle)
car1.color = '파랑'                                     # 원형클래스(prototype)에는 'color'라는 멤버가 없어도 추가 가능
print('car1.color : ', car1.color)
# tom 이 car1이라는 객체 공간 주소의 car1.name에 들어감
# 10 이 car1이라는 객체 공간 주소의 car1.speed에 들어감
# 늘 local 먼저 불러 읽기 때문에 car1 객체 공간을 탐색     -->>    car1 객체 공간에 handle 이라는 멤버를 주지 않았음     --  >>    원형(prototype) class의 멤버를 참조함.

# Bound Method call
car2 = Car('john', 20)
print('car2 객체의 주소 : ', car2)
print('car2 : ', car2.name, ' ', car2.speed, ' ', car2.handle)
# print(Car.color, ' ', car2.color)                       # error : type object 'Car' has no attribute 'color'
# car1과 car2는 값을 공유하지 못함

print(id(Car), id(car1), id(car2))                      # Car, car1, car2 세 개 객체의 주소가 모두 다름 -->> 객체 3개가 만들어짐

print(car1.__dict__)                                    # {'name': 'tom', 'speed': 10, 'color': '파랑'}
print(car2.__dict__)                                    # {'name': 'john', 'speed': 20}


print('---------  메소드 ------------')
print('car1 speed : ', car1.showData())                 # showData는 메소드이기 때문에, showData() 이렇게 괄호를 써야 실행됨        # interpreter가 객체의 주소를 괄호 안에 넣어줌
print('car2 speed : ', car2.showData())
# self의 기능 : showData 메소드 속, 'msg = '속도 : ' + str(self.speed) + km' 에 있는 "self"에 car1, car2가 각각 들어감.
print('-----'*5)

car1.speed = 80
car2.speed = 110
print('car1 speed : ', car1.showData())
print('car2 speed : ', car2.showData())
print('-----'*5)

print('car1 handle : ', car1.printhHandle())            # handle 멤버가 car1에 없기 때문에, local(car1)에서 탐색 후, 원형클래스(prototype)의 'handle = 1' 값을 사용함
print('car2 handle : ', car2.printhHandle())
