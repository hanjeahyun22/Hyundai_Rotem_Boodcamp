# turtle 모듈(라이브러리)로 그래픽 구현

from turtle import *
p = Pen()
p.color('red', 'yellow')
p.begin_fill()

while True:
    p.forward(200)
    p.left(170)
    if abs(p.pos()) < 1:
        break

p.end_fill()
input()
