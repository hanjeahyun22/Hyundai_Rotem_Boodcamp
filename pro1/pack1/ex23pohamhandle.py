# 어딘가에서 필요한 부품(핸들 클래스) 작성
class PohamHandle:
    # quantity = 0        # 핸들 회전량               # 멤버 필드 -->> 공유 자원
    
    def leftTurn(self, quantity):                   # 지역 변수
        self.quantity = quantity
        return "좌회전"
    
    def rightTurn(self, quantity):
        self.quantity = quantity
        return "우회전"
    
    def straight(self, quantity):
        self.quantity = quantity
        return "직진"