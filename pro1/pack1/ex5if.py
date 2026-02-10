# 조건 판단문 if

# ------------------------------------------
print('------'*5)
var = 3

if var >= 3:
    print('크네')
    print('vvvvvvv')
print('end')


# ------------------------------------------
print('------'*5)
var = 1

if var >= 3:
    print('크네')
    print('ddddddd')
else:
    print('작네')

print()


# ------------------------------------------
print('------'*5)
import random

money = random.randint(0, 1000)
age = random.randint(10, 50)

if money >= 500:
    item = '사과'
    if age <= 30:
        msg = 'True Ture'
    else:
        msg = "True False"
else:
    item = '한라봉'
    if age <= 20:
        msg = 'False Ture'
    else:
        msg = "False False"

print(f'중복 if 수행후 결과 {item} {msg}')

# ------------------------------------------
print('------'*5)

# jumsu = random.randint(40, 100)
# data = input('점수:')       # 입력값은 모두 문자열로 받기 때문에
# jumsu = int(data)           # int(input 데이터)로 형식 변환 필요
jumsu = 77
if jumsu >= 90:
    print('우수')
elif jumsu >= 80:
    print('보통')
else:
    print('저조')

jum = 80
if 90 <= jum <= 100:
    print("A")
elif 70 <= jum <= 90:
    print("B")
else:
    print("C")

# ------------------------------------------
print('------'*5)

names = ['홍길동', '신선해', '이기자']
if '홍길동' in names: 
    print('친구 이름이야')
else:
    print('누구야')

print('------'*5)
if (count := len(names)) >= 5:                  # 대입 표현식
    print(f"인원수가 {count} 이므로 단체 할인")
else:
    print("할인X")


print('------'*5)
scores = [95, 88, 76, 92, 81]
if (avg := sum(scores) / len(scores)) >= 80:            # ':=' : 값을 대입함과 동시에 사용하겠다는 의미 
    print(f"우수반 : 평균점수 {avg}")

# -----------------------------------------
print('------'*5)

# if 구문의 삼항 연산(세로로 길게 if문을 적는게 아닌, 한줄로 적음)
print('삼항 연산')
a = 'kbs'
b = 9 if a == 'kbs' else 11
print('b : ', b)

print('------'*5)
a = 11
b = 'mbc' if a ==9 else 'kbs'
print('b : ', b)

print('------'*5)
a = 3
# if a < 5:
#     print(0)
# elif a < 10:
#     print(1)
# else:
#     print(2)
print(0 if a < 5 else 1 if a < 10 else 2)



print('------'*5)
print('end')

