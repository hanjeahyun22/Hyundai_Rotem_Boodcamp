# 추상 클래스 연습문제
from abc import *

class Employee(metaclass=ABCMeta):  # 추상클래스
    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai

    @abstractmethod
    def pay(self):     #추상메소드
        pass

    @abstractmethod
    def data_print(self):     #추상메소드
        pass

    def irumnai_print(self):  # 이름, 나이 출력용
        print('이름:' + self.irum + ', 나이:' + str(self.nai), end=' ')

class Temporary(Employee):
    def __init__(self,irum,nai,ilsu,ildang):
        Employee.__init__(self, irum, nai)
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):
        return self.ilsu * self.ildang
        
    def data_print(self):
        super().irumnai_print()
        print(', 월급: ' + str(self.pay()))

t = Temporary('홍길동',25,20,150000)
t.data_print()


class Regular(Employee):
    def __init__(self,irum,nai,salary):
        super().__init__(irum,nai)
        self.salary = salary

    def pay(self):
        return self.salary 
        
    def data_print(self):
        super().irumnai_print()
        print(', 급여: ' + str(self.pay()))

r = Regular('한국인', 27, 3500000)
r.data_print()


class Salesman(Regular):
    def __init__(self,irum,nai,salary,sales,commission):
        super().__init__(irum,nai,salary)
        self.sales = sales
        self.commission = commission

    def pay(self):
        return super().pay() + (self.sales * self.commission)

    def data_print(self):
        super().irumnai_print()
        print('수령액: ' + str(round(self.pay())))

s = Salesman('손오공',29,1200000, 5000000, 0.25)
s.data_print()
