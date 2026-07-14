"""
연습문제1) 리스트를 통해 직원 자료를 입력받아 가공 후 출력하기

함수를 두 개 작성

처리 함수 : processfunc(datas) : datas에 기억된 내용을 출력한다.


처리 조건 : 

1) 급여액은 기본급 + 근속수당 

2) 수령액은 급여액 – 공제액

* 근무년수에 대한 수당표	
근무년수     근속수당
 0~3년        150000
 4~8년        450000
 9년 이상    1000000	
 
* 급여 상한액에 대한 공제세율표
급여액                공제세율
 300만원 이상          0.5
 200만원 이상          0.3
 200만원 미만          0.15

 

 출력 결과 : 

사번  이름    기본급    근무년수  근속수당  공제액    수령액
-------------------------------------------------------------------------------
1    강나루    1500000   16       1000000   750000   1750000
2    이바다    2200000   8          450000    795000   1855000
3    박하늘    3200000   21       1000000   2100000  2100000
처리 건수 : 4 건

 
"""

print('========================'*3)
print('Q1 =====================================================================')
print('========================'*3)

# 입력 함수 :  [사번, 이름, 기본급, 입사년도]
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

import time

# -- 사용자 정의 함수 --
def decide_pay(entering_year):
    # current_year = time.daylight().year
    working_day = 2026 - entering_year
    if 0 <= working_day <= 3:
        bonus = 150000
    elif 4<= working_day <= 8:
        bonus = 450000
    else:
        bonus = 1000000
    return working_day, bonus

def taxfunc(origin, bonus):
    if origin + bonus < 2000000:
        tax_rate = 0.15
    elif 2000000 <= origin + bonus < 3000000:
        tax_rate = 0.3
    else:
        tax_rate = 0.5
    
    missing_money = (origin + bonus) * tax_rate
    final_money = (origin + bonus) - missing_money
    return missing_money, final_money

# -- main 함수 --
Mat = inputfunc()
print('사번', '\t이름', '\t기본급', '\t근무년수', '\t근속수당', '\t공제액', '\t수령액')
print('-------------------------------------------------------------------------------')
for i in range(0,len(Mat)):
    print(Mat[i][0], '\t', Mat[i][1], Mat[i][2], '\t', decide_pay(Mat[i][3])[0] ,'\t' , decide_pay(Mat[i][3])[1], '\t', \
            taxfunc(Mat[i][2], decide_pay(Mat[i][3])[1])[0], '\t', taxfunc(Mat[i][2], decide_pay(Mat[i][3])[1])[1])
    i += 1



"""
연습문제2) 리스트를 통해 상품 자료를 입력받아 가공 후 출력하기

처리 조건 :  
  1) 한 개의 상품명과 가격은 문자열로 입력됨. 문자열 나누기 필요.
  2) 취급 상품 예는 아래와 같다.
 * 취급상품표
  상품명   단가
  새우깡    450
  감자깡    300
  양파깡,   450

출력 형태:
상품명   수량   단가   금액
-----------------------------------
새우깡    15    450   6750
감자깡    20    300   6000
양파깡    10    350   3500
새우깡    30    450   13500
감자깡    25    300   7500
양파깡    40    350   14000
새우깡    40    450   18000
감자깡    10    300   3000
양파깡    35    350   12250
새우깡    50    450   22500
감자깡    60    300   18000
양파깡    20    350   7000


소계
새우깡 : 135건   소계액 : 60750원
감자깡 : 115건   소계액 : 34500원
양파깡 : 105건   소계액 : 36750원
총계
총 건수 : 355
총 액  : 132000원
"""
print('========================'*3)
print('Q2 =====================================================================')
print('========================'*3)
import re


# 입력 함수
def inputfunc():
    datas = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas

# -- 사용자 정의 함수 --
def calculator(temp, num):
    
    num_onion = 0
    num_shrimp = 0
    num_potato = 0

    if temp == '새우깡':
        value = 450
        num_shrimp = num
    elif temp == '감자깡':
        value = 300
        num_potato = num
    elif temp == '양파깡':
        value = 450
        num_onion = num
    
    total = num * value

    return value, total, num_shrimp, num_potato, num_onion  


# -- main 함수 --
# split_data = inputfunc()[0].split(',')
# print(split_data)

print('상품명\t', '수량', '\t단가', '\t금액', '\n-----------------------------------')

tot_sh = 0; tot_po = 0; tot_on = 0

for i in range(0, len(inputfunc()), 1):
    split_data = inputfunc()[i].split(',')
    result = calculator(split_data[0], int(split_data[1]))
    
    # print(result)
    
    tot_sh += result[2]
    tot_po += result[3]
    tot_on += result[4]

    print(split_data[0], '\t', split_data[1], '\t', result[0], '\t', result[1])

print(' ')
print('소계')
print(f'새우깡 : {tot_sh}   소계액 : {tot_sh * 450}')
print(f'감자깡 : {tot_po}   소계액 : {tot_po * 300}')
print(f'양파깡 : {tot_on}   소계액 : {tot_on * 400}')
print(' ')
print('총계')
print('총 건수 : ', tot_sh + tot_po + tot_on)
print(f'총 액 : {tot_sh * 450 + tot_po * 300 + tot_on * 400}')