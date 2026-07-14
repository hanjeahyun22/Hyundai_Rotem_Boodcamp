'''
[문항6] 아래 Mbc 함수에서 c 는 전역, b는 Kbs 함수의 b를 취하려고 한다.
빈 칸에 알맞은 키워드를 차례대로 적으시오. (배점:5)
a = 1.5; b = 2; c = 3;
def Kbs:
  a = 20
  b = 30
  def Mbc():
      1)_____________  c
      2)_____________  b
      print(‘Mbc 내의 a:{}, b:{}, c:{}’.format(a, b, c))
      c = 40
      b = 50
  Mbc()
Kbs()
'''

a = 1.5; b = 2; c = 3

def Kbs():
    a = 20
    b = 30
    def Mbc():
        global c
        nonlocal b
        print('Mbc 내의 a:{}, b:{}, c:{}'.format(a, b, c))
        c = 40
        b = 50
    Mbc()

Kbs()

