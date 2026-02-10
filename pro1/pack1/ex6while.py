# ##################################
# ##################################
print('====='*5)
print('====='*5)

import random

a = random.randint(1, 10)
while a <= 5:
    print(f'index : ',a)
    print('-----  befor  ------')
    print(a, end = '')
    a = a + 1
    print('-----  after  ------')
    print(a)
else:
    print('\n수행 성공')
    


# ##################################
# ##################################
print('====='*5)
print('====='*5)

i = 1
while i <= 3:
    j = 1
    while j <= 4:
        print('i = ' + str(i) + '\tj = ' + str(j))
        j = j + 1
    i = i + 1


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('---- 1~100사이의 정수 중, 3의 배수의 합 ----')       # 나누기 산술자 : /, %, //
su = 1; hap = 0
while su <= 100:
    # print(su)
    if su % 3 == 0:      # 3의 나머지가 0 -> 3의 배수
        # print(su)
        hap += su        # hap = hap + su
    su += 1
print('합은 ', hap)


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print()
colors = ['빨강', '파랑', '노랑']
# num = 0
# print(colors[0])
# print(colors[1])
# print(colors[2])
num = 0
# while num <= 2:
while num <= len(colors) - 1:    
    print(colors[num])
    num += 1


# ##################################
# ##################################
print('====='*5)
print('====='*5)


print('\n----- 별 찍기 ------')
index = 1
while i <= 10:
    j = 1
    msg = ''
    while j <= i:
        msg += "*"
        j += 1
    print(msg)
    i += 1

"""

# ##################################
# ##################################
print('====='*5)
print('====='*5)


print('--- if 블럭 내 while 블럭 사용 ---')
import time

sw = input('폭탄 스위치를 누를까요?[y/n]')
# print("sw : ", sw)

if sw == 'y' or sw == 'Y':
    # pass                        # 만약에 수행 할 내용이 없는 경우 pass -> if문 탈출
    count = 5
    while 1 <= count:
        print('%d초 남았습니다'%count)      # count값이 정수이기 때문에, %d 사용
        time.sleep(1)           # 단위 : sec   -->> 1초 후 다음 문장 실행
        count -= 1
    print('폭발')
elif sw == 'N' or sw == 'n':
    print('작업 취소')
else:
    print('y 또는 n을 누르세요')

"""

# ##################################
# ##################################
print('====='*5)
print('====='*5)

a = random.randint(0,15)
while a < 10:
    a += 1
    if a == 3:
        continue            # continue : 조건을 만족한다면, 아래 실행 사항들을 무시하고, 다시 위의 while 반복문으로 돌아감   -> 바로 밑의 print(a) 건너뜀
    if a == 5: continue     # if문 밑의 실행사항이 단 한 줄 이라면, 그냥 옆으로 적어도 괜찮음
    if a == 7 :
        print('비정상 종료')
        break       # break : while 문 무조건 탈출
    print(a)
else:
    print('정상 종료')

print('while 수행 후 %d'%a)


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n--- 키보드로 숫자를 입력받아 홀수/짝수 확인하기 (무한 반복) ---')
"""
while True  -->  일부로 무한루프를 만들 때 -->  break 아니면 빠져나가지 못함

while False --> 쓸모 없는 반복문  -->> 실행 X
"""
while True:         # bool값, 숫자값, 문자값은 True로 받음(True, 1, 100, -12, 4.5, 'ok', ...)
    mysu = int(input('확인 할 숫자 압력(예:5), 종료 시 0 입력 : '))             # input 값은 str 형식이므로, int로 숫자 형식으로 변환 필요
    if mysu == 0:
        print('프로그램 종료')
        break
    elif mysu % 2 == 0:     # 나누기 부호 % : 나머지값
        print('%d는 짝수'%mysu)
        continue
    elif mysu % 2 == 1:
        print('%d는 홀수'%mysu)


print('\n루프 안에 종속되어 있지 않고 단순한 ex6의 전체 코드 끝 : end')