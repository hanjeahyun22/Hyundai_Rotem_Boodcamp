'''
	
[문항10] 아래 코드에서 키보드를 통해 0이 입력되면 에러가 발생하게 된다.
예외 처리를 위한 코드 try ~ except를 이용하여 0 이외의 정수 값은 정상 실행되고 0은 에러 메세지를 출력하도록 변경된 코드를 적으시오.

aa = int(input())
bb = 10 / aa 
(배점:5)
'''



try:
    aa = int(input())
    bb = 10 / aa
    print(bb)
except ZeroDivisionError as e:
    print('err : ', e)