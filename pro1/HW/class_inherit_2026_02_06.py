class ElecProduct:
    volume = 0
    def volumeControl(self, volume):
        self.volume = volume
        print(self.volume)

class ElecTv(ElecProduct):
    def volumeControl(self, volume):
        self.volume = volume
        print('자식 class ElecTv로 volumeControl 메소드를 overriding,       volume은', self.volume)

class ElecRadio(ElecProduct):
    def volumeControl(self, volume):
        self.volume = volume
        print('자식 class ElecRadio로 volumeControl 메소드를 overriding,       volume은', self.volume)

# a = ElecTv()
# a.volumeControl(2)
# a = ElecRadio()
# a.volumeControl(4)




elecdevice = [ElecTv(), ElecRadio()]                         # 인스턴스 : class 설계도로 객체 'payments' 생성

# elecdevice: list[ElecProduct] = [ElecTv(), ElecRadio()]  # ✅ 타입 명시

for p in elecdevice:                                              # p가 [ElecTv(), ElectRadio()] 리스트 안의 값을 차례대로 받음
    vol = input('얼마를 넣을건데 - 숫자')
    p.volumeControl(vol)


# ---------------------------------------------------------------------------------------------------------------------------
print('-----'*10)



class Animal:
    def move(self):
        # print('최상위 Animal class')
        pass                            # 하위 class에서 overriding 할 때, move()라는 이름으로 하기를 권장한다는 의미

class Dog(Animal):
    name = '개'

    def move(self):
        print("중간 class 개")

class Cat(Animal):
    name = '고양이'

    def move(self):
        print("중간 class 고양이")

class Wolf(Dog, Cat):
    pass                                # Wolf class 하위에 자식이 있다고 판단

class Fox(Cat, Dog):
    def move(self):
        print('최하위 class 여우')

    def foxMethod(self):
        print('fox 고유 메소드 : foxMethod 실행')


# a = Fox()
# a.foxMethod()
# a.move()

# a = Dog()
# a.move()

animal = [Dog(), Cat(), Wolf(), Fox()]
for i in animal:
    print(i.move())