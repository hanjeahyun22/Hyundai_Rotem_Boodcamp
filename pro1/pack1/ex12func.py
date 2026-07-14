# 함수 장식자
# 기존 함수 코드를 고치지 않고 함수의 앞/뒤 동작을 추가하기
# 함수를 받아서 기능을 덧붙인 새 함수로 바꿔치기하는 것
# meta 기능이 있다  -->>  정보를 갖고 있음

def make2(fn):
    return lambda:"안녕 " + fn()

def make1(fn):
    return lambda:"반가워 " + fn()

def hello():
    return "홍길동"

# 장식자 없이 실행
hi = make2(make1(hello))
print(hi())
print('-----------'*5)

# decorater(장식자) 실습
@make2                                                      # @ : decorater(장식자)
@make1
def hello2():
    return "신기해"

print(hello2())

print('-----------'*5)

def traceFunc(func):
    def wrapperFunc(a, b):
        r = func(a, b)
        print(f'함수명 : {func.__name__} (a={a}, b={b} -> {r})')                      # __name__ : '함수의 이름' 이라는 의미
        return r                                                                     # 함수 반환값을 반환
    return wrapperFunc                                                               # 내부 함수의 값을 반환하는 Closure


@traceFunc
def addFunc(a, b):
    return a + b

print(addFunc(10, 20))