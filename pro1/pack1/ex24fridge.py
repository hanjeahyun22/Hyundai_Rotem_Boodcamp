# 클래스의 포함관계 연습 - 냉장고 객체에 음식 객체 담기

class Fridge:
    isOpened = False
    foods = []

    def open(self):
        self.isOpened = True
        print('냉장고 문을 열기')

    def close(self):
        self.isOpened = False
        print('냉장고 문을 닫기')

    def foodsList(self):                            # 냉장고 문이 열린 경우 음식물 확인
        for f in self.foods:
            print(f'- {f.name} {f.expiry_data}')

    def put(self, thing):
        if self.isOpened:
            self.foods.append(thing)
            print(f'냉장고에 {thing.name} 넣음')
            self.foodsList()
        else:
            print('냉장고 문이 닫여있음')


class FoodData:
    def __init__(self, name, expiry_data):
        self.name = name
        self.expiry_data = expiry_data

    
fObj = Fridge()
apple = FoodData('사과', '2026-8-1')

fObj.put(apple)                         # class의 포함관계 : Fridge class에 FoddDadta class를 포함시킴
fObj.open()
fObj.put(apple)
fObj.close()



cola = FoodData('콜라', '2027-11-1')
# fObj.put(cola)
fObj.open()
fObj.put(cola)
fObj.close()