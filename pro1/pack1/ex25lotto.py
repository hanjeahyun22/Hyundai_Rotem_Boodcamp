import random

class LottoBall:                                        # LottoBall class는 num을 self.num으로 반환하는 생성자 메소드만 있음.
    def __init__(self, num):
        self.num = num

class LottoMachine:
    def __init__(self):
        self.ballList = []
        for i in range(1, 46):
            self.ballList.append(LottoBall(i))          # class의 포함관계 : LottoMachine class안에 LottoBall class가 포함됨        -->> 1~45개의 lottoball 생성

    def selectBalls(self):
        # for a in range(45):
            # print(self.ballList[a].num, end = ' ')      # 섞기 전 45개의 ball 차례대로 프린트
        # print('\n----------')
        random.shuffle(self.ballList)                   # random.shuffle : 랜덤하게 섞어주는 기능
        # for a in range(45):
            # print(self.ballList[a].num, end = ' ')      # 섞은 후, 프린트
        return self.ballList[0:6]                       # 랜덤하게 섞은 1~45의 총 45개의 ball 중에서, 앞의 6개 return

class LottoUI:
    def __init__(self):
        self.machine = LottoMachine()                   # class의 포함관계 : LottoUI class안에 LottoMachine class가 포함됨

    def playLotto(self):
        input('로또를 시작하려면 엔터키를 누르세요')
        selectedBalls = self.machine.selectBalls()
        for ball in selectedBalls:
            print('%d'%(ball.num))

if __name__ == '__main__':
    # machine = LottoMachine()
    # print(machine.selectBalls())
    
    # lot = LottoUI()
    # lot.playLotto()
    LottoUI().playLotto()