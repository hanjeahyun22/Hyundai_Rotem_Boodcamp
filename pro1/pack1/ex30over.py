# 오버라이딩 : 결제 시스템
class Payment:                  # super class로서, 자식 class에 대한 공통 규칙을 갖고 있음
    def pay(self, amount):
        print(f'부모 class(Payment) - {amount}원 결제 처리')

# Payment의 자식은 결제를 pay()라는 동일 메소드를 이용하기를 기대
# 동일 인터페이스 구사

class CardPayment(Payment):
    # 자식 class 만의 고유 멤버 ...

    # 자식 class 만의 고유 메소드 ...
    def pay(self, amount):
        print(f'자식 class(CardPayment) - {amount}원 카드 결제 승인 완료함')

class CashClass(Payment):
    # 자식 class 만의 고유 멤버 ...

    # 자식 class 만의 고유 메소드 ...
    def pay(self, amount):
        print(f'자식 class(CashClass) - {amount}원 현금 결제 완료함 - 감사합니다')

payments = [CardPayment(), CashClass()]                         # 인스턴스 : class 설계도로 객체 'payments' 생성

for p in payments:                                              # p가 [CardPayment(), CashClass()] 리스트 안의 값을 차례대로 받음
    p.pay(5000)                                                 # 다형성
