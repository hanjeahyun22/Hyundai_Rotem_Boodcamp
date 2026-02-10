# 예외 처리 : 파일, 네트워크, DB 작업, 실행 에러 등의 에러 예외 대처

def divide(a, b):
    return a / b

print('이런 저런 작업 진행...')
# c = divide(5, 2)
# print(c)

try:   
    # 실행문(예외 발생 가능 구문)
    c = divide(5, 2)
    # c = divide(5, 0)
    print(c)

    aa = [1, 2]
    print(aa[0])
    # print(aa[3])
    
    # open("c:/work/abc.txt")

except ZeroDivisionError:                   # 예외 종류 관련 class를 적어줌             # try 부분에서 에러가 발생하자마자, 그 밑의 내용은 실행하지 않고, except 구문으로 넘어감
    print('두번째 값은 0을 주면 안돼요')                                        
except IndexError as err:
    print('참조 범위 오류 : ', err)
except Exception as e:
    print('에러 : ', e)


finally:
    print('에러 유무에 상관없이 반드시 시행')

print('end')
print('종료')
