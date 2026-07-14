# 매개변수 유형
# 위치 매개변수     : 인수와 순서대로 대응
# 기본값 매개변수   : 매개변수에 입력값이 없으면 기본값 사용
# 키워드 매개변수   : 실인수와 가인수 간 동일 이름으로 대응
# 가변 매개변수     : 인수의 갯수가 동적인 경우


# ################################################################################################
#                                       위치 매개변수
# ################################################################################################

def showGugu(start, end):                                               # 가인수 : start, end
    for dan in range(start, end + 1, 1):
        print(str(dan) + '단 출력')
        for i in range(1, 10):
            print(str(dan) + "*" + \
                  str(i) + "=" + str(dan * i), end = ' ')               # \ : print 구문을 쓸 때, 너무 긴 경우  -->>  \ 후 enter로 줄 변경
        print()

showGugu(2, 3)                                                          # 실인수 : 2, 3


# ################################################################################################
#                                       기본값 매개변수
# ################################################################################################
print('====='*20)
print('====='*20)

def showGugu(start, end = 5):                                               # 가인수 : start, end
    for dan in range(start, end + 1, 1):
        print(str(dan) + '단 출력')
        for i in range(1, 10):
            print(str(dan) + "*" + \
                  str(i) + "=" + str(dan * i), end = ' ')               # \ : print 구문을 쓸 때, 너무 긴 경우  -->>  \ 후 enter로 줄 변경
        print()
# showGugu(2, 3)     
print()
showGugu(2)                                                         


# ################################################################################################
#                                       키워드 매개변수
# ################################################################################################
print('====='*20)
print('====='*20)

def showGugu(start, end):                                               # 가인수 : start, end
    for dan in range(start, end + 1, 1):
        print(str(dan) + '단 출력')
        for i in range(1, 10):
            print(str(dan) + "*" + \
                  str(i) + "=" + str(dan * i), end = ' ')               # \ : print 구문을 쓸 때, 너무 긴 경우  -->>  \ 후 enter로 줄 변경
        print()

showGugu(start=7, end=9)
print()
showGugu(end=9, start=7)
print()
showGugu(7, end=9)
# showGugu(start=7, 9)                                                  # error
# showGugu(end=9, 7)                                                    # error


# ################################################################################################
#                                       가변 매개변수
# ################################################################################################
print('====='*20)
print('====='*20)

def func1(*ar):                                         # *가인수 : 여러 개의 인자를 tuple 형식으로 묶어서 반환
    print(ar, type(ar))
    for i in ar:
        print('밥 : ' + i)

func1('김밥', '비빔밥', '볶음밥')                       # ('김밥', '비빔밥', '볶음밥') 이 모양으로 전달됨  -->> tuple 형식
print('-----------'*5)
func1('김밥', '비빔밥')
print('-----------'*5)
func1('김밥')                                           # ('김밥', ) 이 모양으로 전달됨  -->> tuple 형식
print('-----------'*5)

# def func2(*ar, a):                                      # 실행 오류  -->>  TypeError: func2() missing 1 required keyword-only argument: 'a'
def func2(a, *ar):
    print(a)
    print(ar)

func2('김밥', '비빔밥')
print('-----------'*5)
func2('김밥', '비빔밥', '볶음밥', '공기밥')
print('-----------'*5)

print()

def func3(w, h, **other):                               # **가변수 : dict 형식으로 받음
    print(f'몸무게 : {w}, 키 : {h}')
    print(f'기타 : {other}')

func3(80, 180, irum = '신기루', nai = 23)
# func3(80, 180, {irum : '신기루', nai : 23})             # error  -->> 그렇다고 실변수를 dict형식으로 주면 안됨
print()


print('-----------'*5)
print()

def func4(a, b, *c, **d):
    print(a, b)
    print(c)
    print(d)

func4(1,2)
print('-----------'*5)
func4(1, 2, 3, 4, 5)
print('-----------'*5)
func4(1, 2, 3, 4, 5, kbs = 9, mbc = 11)


# ################################################################################################
#                        type hint : 함수의 인자와 반환값에 type을 적어 가독성 향상
# ################################################################################################
print('====='*20)
print('====='*20)

def typeFunc(num:int, data:list[str]) -> dict[str, int]:                    # type hint : num이라는 변수는 int 형식, data는 list[str] 형식을 받음       # -> 결과값에 대한 type hint
    print(num)
    print(data)
    result = {}                                                             # {} 중괄호 만으로는 set인지 dict인지 모름
    for idx, item in enumerate(data, start=8):                              # enumerate : 묶음형 자료형에서 index랑 value를 뽑아줌          # 인덱스 카운팅 start 기본값 : 0
        print(f'idx : {idx}, item : {item}')
        result[item] = idx                                                  # dict 형식이라고 명시
    return result

re_data = typeFunc(1.2, ['일', '이', '삼'])                                 # num 변수에 1.2라는 float를 줘도 에러는 발생 X  -->> 구속력 X  -->>  오직 가독성을 위한 type hint
print(re_data)
print('-----------'*5)
re_data = typeFunc('한 개', [10, 20, 30])
print(re_data)


