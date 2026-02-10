# Closure : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭이다.
# -->> 내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기

def funcTimes(a, b):
    c = a * b
    return c

print(funcTimes(2,3))
# print(c)                          # error

kbs = funcTimes(2,3)
print(kbs)
print('-----------'*5)
kbs = funcTimes
print(kbs)
print('-----------'*5)
print(kbs(2,3))
print('-----------'*5)
print(id(kbs), id(funcTimes))
print('-----------'*5)

mbc = sbs = kbs

del funcTimes                       # funcTimes 변수 삭제
# print(funcTimes(2,3))               # error -->> name 'funcTimes' is not defined
print(mbc(2, 3))                    # del 명령으로 funcTimes 함수를 지웠지만, mbc, sbs, kbs가 funcTimes의 '주소'를 갖고 있기 때문에, 똑같이 실행됨

print()

# ################################################################################################
#                                   클로저를 사용하지 않은 경우
# ################################################################################################
print('====='*20)
print('====='*20)

def out():
    count = 0
    def inn():
        nonlocal count
        count += 1                      # nonlocal 함수로 인해서, inn 함수 내의 'count' 변수는 out 함수의 'count' 사용
        return count
    print(inn())

# print(count)                        # error
out()
print('-----------'*5)
out()
print('-----------'*5)
out()
print('-----------'*5)
out()
print('-----------'*5)
out()



# ################################################################################################
#                                       클로저를 사용한 경우
# ################################################################################################
print('====='*20)
print('====='*20)

def out_closure():
    count = 0
    def inn_count():
        nonlocal count
        count += 1                      
        return count
    return inn_count                    # Closure : 내부함수의 주소를 반환  -->> 주소에 의해서 기존 값 참조

# print(count)                          # error
var1 = out_closure()                    # 내부 함수의 주소를 변수에 저장
print('var1의 주소 : ', var1)
print('-----------'*5)
print(var1())
print('-----------'*5)
print(var1())
print('-----------'*5)
print(var1())
print('-----------'*5)
print(var1())
print('-----------'*5)
print(var1())

myvar = var1()
print('-----------'*5)
print(myvar)
print('-----------'*5)

var2 = out_closure()                    # 새로운 객체(inn_count 함수) 생성 
print(var2())
print('-----------'*5)
print(var2())

print(var1, var2)


# ################################################################################################
#                                       Closure 예시
# ################################################################################################
print('====='*20)
print('====='*20)

print('수량 * 단가 * 세금 한 결과를 출력하는 함수')
def outer2(tax):                                        # tax : local 변수
    def inner2(su, dan):
        amount = su * dan * tax
        return amount
    return inner2                                       # Closure 처리

# 1분기에는 su * dan에 대한 tax가 10% 부과
q1 = outer2(0.1)                                        # q1은 inner2의 주소를 기억함
result1 = q1(5, 50000)
print('result1 : ', result1)

result2 = q1(2, 10000)
print('result2 : ', result2)
print('-----------'*5)

# 2분기에는 su * dan에 대한 tax가 5% 부과
q2 = outer2(0.05)
result3 = q2(5, 50000)
print('result3 : ', result3)

result4 = q2(2, 10000)
print('result4 : ', result4)


# ################################################################################################
#                                           일급함수
#                                       함수 안의 함수
#                                       인자로 함수 전달
#                                       반환값이 함수
# ################################################################################################
print('====='*20)
print('====='*20)

print('\n일급함수 : 함수 안의 함수')
print('-----------'*5)

def func1(a, b):
    return a + b

func2 = func1

print(func1(3, 4))
print(func2(3, 4))
print('-----------'*5)

def func3(fu):
    def func4():
        print('나는 내부함수야')
    func4()
    return fu

mbc = func3(func1)
print(mbc(3, 4))


# ################################################################################################
#                                    축약함수(Lambda function)
#                                    이름이 없는 한 줄 짜리 함수
#                                    형식 : 매개변수들 , , , , : 반환식  / ex) (lambda x, y:x + y)(1,2)
#                                     -->> return 없이 결과를 반환
# ################################################################################################
print('====='*20)
print('====='*20)

print('\n람다함수(Lambda function) - 한 줄로 간략하게 표현')

def hapFunc(x, y):
    return x + y

print(hapFunc(1, 2))
print('-----------'*5)

# Lambda 함수로 표현
print((lambda x, y:x + y)(1,2))
print('-----------'*5)

gg = lambda x, y:x + y
print(gg(1, 2))
print('-----------'*5)

kbs = lambda a, su = 10: a + su
print(kbs(5))                           # 5를 a로 활용, su는 기존 lambda 함수에서 지정한 10 사용
print('-----------'*5)
print(kbs(5, 6))                        # a, su 모두 지금 대입한 값 사용
print('-----------'*5)

sbs = lambda a, *tu, **di:print(a, tu, di)
sbs(1, 2, 3, var1 = 4, var2 = 5)
print('-----------'*5)

li = [lambda a, b:a + b, lambda a, b:a * b]
print(li[0](3, 4))
print(li[1](3, 4))

# ################################################################################################
#                       다른 함수에서 람다(Lambda function) 사용하기
# ################################################################################################
print('====='*20)
print('====='*20)

print('\n다른 함수에서 람다 사용하기')

# filter 함수 -->> filter(함수, iterable)
print(list(filter(lambda a:a<5, range(10))))                    # 함수(5미만인 a)를 사용하는데, 묶음형 자료:iterable(1부터 9까지의 값)을 받는,, list 형식으로 프린트
print('-----------'*5)
print(list(filter(lambda a:a % 2, range(10))))                  # 0 = False, 1 = True   -->>     참인 값만 출력     -->>     홀수만 출력


# 문제) filter 사용, 1~100 사이의 정수 중 5의 배수이거나 7의 배수만 출력
print(list(filter(lambda a:a % 5 == 0 or a % 7 == 0, range(1, 101))))

