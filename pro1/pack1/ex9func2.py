# 사용자 정의 함수
"""
ex9func2의 Docstring

def 함수명(가인수, , , , ):
    # ...

    return 반환값                   # 1개만 반환, return이 없으면 return None

함수명(실인수 , , , , )             # 함수 호출


함수 명명법
1. camel 방법 : doFuncPro
2. snake 방법 : _do_func_pro

변수 찾는 순서 :
Local -> Enclosing function -> Global -> Built-in
"""

# parameter X
def doFunc1():
    print('doFunc1 수행')

# parameter O, return X
def doFunc2(name):
    print('name : ', name)
    return None                     # 원래는 None 이 반환됨

# parameter O, return O
def doFunc3(arg1, arg2):
    re = arg1 + arg2
    return re

def doFunc4(a1, a2):
    imsi = a1 + a2
    if imsi % 2 == 1:
        return
    else:
        return imsi


print('--------'*5)

# 함수를 호출만 함
doFunc1()                   # 함수 호출

print('--------'*5)

# 함수의 '주소'를 print
print(doFunc1)

print('--------'*5)

# 함수의 'return 결과값'을 출력
print(doFunc1())

print('--------'*5)

# 함수의 실행 결과 / 주소를 치환 후 출력
doFunc1()
print('함수 주소 : ', doFunc1)                  # 16진수
print('함수 주소 : ', id(doFunc1))              # 해시코드
print('함수 결과 : ', doFunc1())
print('--------'*5)
imsi  = doFunc1
imsi()
print('--------'*5)
print(doFunc1())

print('--------'*5)

# parameter input값을 갖는 함수 호출
doFunc2(7)
doFunc2('길동')

print('--------'*5)

# paramter input 2개를 갖고, return 결과값을 갖는 함수 호출
doFunc3("대한", "민국")             # doFunc3 함수가 실행은 되어, re값은 생성은 됐으나, 출력 X
print('--------'*5)
print(doFunc3("대한", "민국"))
print('--------'*5)
print(doFunc3(5, 6))
print('--------'*5)
result = doFunc3('5', '6')
print(result)
print('--------'*5)

print(doFunc4(3,4))
print(doFunc4(3,5))

print('--------'*5)


# ##################################
# ##################################
print('====='*5)
print('====='*5)

# 함수가 다른 함수 호출
def triArea(a, b):
    c = a * b / 2
    triAreaPrint(c)

def triAreaPrint(cc):
    print('삼각형의 면적은 ', cc)

triArea(20, 30)


# ##################################
# ##################################
print('====='*5)
print('====='*5)

def passResult(kor, eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False
    
if passResult(20, 20):
    print('합격')
else : 
    print('불합격')

print()
print('--------'*5)

def swqpFunc(a,b):
    return b, a             # return (b, a)                     # 함수는 단 하나의 값만 return -->> return 후에 묶음형 자료(tuple 형) 하나만 반환

a = 10
b = 20
print(a, ' ', b)
print(swqpFunc(a,b))


# ##################################
# ##################################
print('====='*5)
print('====='*5)

# 함수 안에 '내부 함수' 선언해서 함수 내에서 사용하기
def funcTest():
    print('funcTest 멤버 처리')
    
    def funcInner():
        print('내부 함수')
    
    funcInner()

funcTest()


# ##################################
# ##################################
print('====='*5)
print('====='*5)

# if 조건식 안에 함수 사용
def isOdd(para):
    return para % 2 == 1        # 홀수면 True 반환

mydict = {x : x*x for x in range(11) if isOdd(x)}
print(mydict)

# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('--- 변수의 생존 범위 (scope rule) ---')
# 변수가 저장되는 이름 공간은 변수가 어디서 선언되었는가에 따라 생존 시간이 다름
# 전역(global), 지역(local) 변수


# global 변수
name = '한국인'
player = '전국대표'

"""
함수 영역내의 local 변수는 함수 안에서만 쓰임
"""
def funcSoccer():
    # local 변수
    name = '홍길동'
    # player = '지역 대표'                              # 만약 지역 변수에 똑같은 이름의 변수가 없다면, 전역에서 탐색하여 같은 이름의 값을 사용     -->> '전국대표' 값 사용
    """
    player 변수가 local에서 선언되지 않았더라도, 만약 global에 똑같은 이름의 변수와 값이 선언되어 있다면, 그 값을 사용
    """
    city = '서울'
    print(f'이름은 {name} 수준은 {player}')             # 지역 변수(local variations) 사용             -->> 함수 수준 -->> 함수 안에서만 호출 가능
    print(f'지역은 {city}')

funcSoccer()
print(f'이름 : {name} 수준 : {player}')                 # 전역 변수(global variations) 사용            -->> module 수준(.py 파일 main 코드에서 사용) --> 파일 안에 어디에서나 호출 가능
# print(f'지역은 {city}')                                 # 전역 변수로 city가 정의되지 않고, 오직 funcSoccer 함수 안에서 local 변수로만 선언되어 있기 때문에, 사용 불가능


# ##################################
# ##################################
print('====='*5)
print('====='*5)


print()
a = 10; b = 20; c = 30                                              # a, b, c : Global 변수

def Foo():                                                          # Foo 함수 : Bar 함수의 Enclosing 함수
    a = 7                                                           # a : Local 변수 - (Foo 함수)
    b = 100                                                         # b : Local 변수 - (Foo 함수)
    def Bar():                                                      # Bar 함수 : Foo 함수의 내부 함수
        # ##################################
        global c                                                    # Bar 함수의 멤버가 아니라, 모듈(파일)의 멤버가 됨. 즉, Global 변수
        nonlocal b                                                  # nonlocal : Enclosing function(Foo 함수)의 멤버가 됨.                                                  
        # ##################################
        b = 8                                                       # b : Local 변수 - (Bar 함수) // nonlocal 함수에 의해서 Enclosing function(Foo 함수)
        print(f'Bar 함수 수행 후 a:{a}, b:{b}, c:{c}')
        c = 9                                                       # c : 단순히 Local 변수로 선언하면 의미없는 값이라는 에러 발생  -->> Bar 함수 내에서 'c' 변수를 Global로 선언해 줄 필요가 있음

        b = 200                                                     # b : Local 변수 - (Bar 함수) // nonlocal 함수에 의해서 Enclosing function(Foo 함수)
    Bar()
    print(f'Foo 함수 수행 후 a:{a}, b:{b}, c:{c}')                   # b는 Global에 선언된 'b = 20'값 사용 -->> Bar 함수 내의 b는 Bar 함수 안에서만 사용   

Foo()
print(f'함수 수행 후 a:{a}, b:(b), c:{c}')                           # Bar함수 내에서 'c'를 global 변수로 선언한 후, 기존 30에서 9로 값을 바꿨음


# ##################################
# ##################################
print('====='*5)
print('====='*5)

g = 1
print('g : ', g)

def func():
    global g
    a = g
    g = 2
    return a

print(func())
print('g : ', g)