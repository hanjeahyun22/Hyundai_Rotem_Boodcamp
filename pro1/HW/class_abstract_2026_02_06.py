from abc import *

class Employee:
    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai
    
    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self):
        pass

    def irumnai_print(self):
        print('이름 : ' + self.irum + ', 나이' + str(self.nai), end = ' ')

class Temporary(Employee):
    
    def __init__(self, irum, nai, ilsu, ildang):
        super().__init__(irum, nai)
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):
        money = self.ilsu * self.ildang
        self.money = money
        
    def data_print(self):
        self.pay()
        super().irumnai_print()
        print('월급 : ', self.ilsu * self.ildang)



class Regular(Employee):
    def __init__(self, irum, nai, salary):
        super().__init__(irum, nai)
        self.salary = salary
    
    def pay(self):
        money = self.salary
        self.money = money

    def data_print(self):
        self.pay()
        super().irumnai_print()
        print('급여 : ', self.money)

class Salesman(Regular):
    def __init__(self, irum, nai, salary, sales, commissions):
        super().__init__(irum, nai, salary)
        self.sales = sales
        self.commissions = commissions

    def pay(self):
        money = self.salary + self.sales * self.commissions
        self.money = money

    def data_print(self):
        self.pay()
        super().irumnai_print()
        print('수령액 : ', int(self.money))


t = Temporary('홍길동', 25, 20, 15000)
r = Regular('한국인',27, 3500000)
s = Salesman('손오공', 29, 1200000, 5000000, 0.25)

t.data_print()
r.data_print()
s.data_print()