# 2번 문제 시작 부분은 160번째 줄
# 1번 문제 솔루션 시작부분

print("\n\n\n\n\n연습문제1) 리스트를 통해 직원 자료를 입력받아 가공 후 출력하기")

# 입력 함수 :  [사번, 이름, 기본급, 입사년도]
def inputfunc_1():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

def solution_func_first(datas):
    len_arr = len(datas)

    # 출력 보드: [사번, 이름, 기본급, 근무년수, 근속수당, 공제액, 수령액]
    board_first = [[0] * 7 for _ in range(len_arr)]

    # import datetime 없이: 예시 출력 기준(2026년 기준으로 근무년수 계산)
    current_year = 2026

    for row, emp in enumerate(datas):
        emp_no, name, base_pay, join_year = emp

        # 1) 근무년수 
        work_years = current_year - join_year

        # 2) 근속수당
        if 0 <= work_years <= 3:
            allowance = 150000
        elif 4 <= work_years <= 8:
            allowance = 450000
        else:
            allowance = 1000000

        # 3) 급여액
        pay = base_pay + allowance

        # 4) 공제세율
        if pay >= 3000000:
            rate = 0.5
        elif pay >= 2000000:
            rate = 0.3
        else:
            rate = 0.15

        # 5) 공제액, 수령액
        tax = int(pay * rate)
        net = pay - tax

        # (7 * 3)보드 채우기
        board_first[row][0] = emp_no
        board_first[row][1] = name
        board_first[row][2] = base_pay
        board_first[row][3] = work_years
        board_first[row][4] = allowance
        board_first[row][5] = tax
        board_first[row][6] = net

    # 출력
    print("출력 결과 :")
    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 60)

    for row in range(len_arr):
        emp_no, name, base_pay, work_years, allowance, tax, net = board_first[row]
        print(f"{emp_no:<4} {name:<6} {base_pay:>8} {work_years:>8} {allowance:>8} {tax:>8} {net:>8}")

    print(f"처리 건수 : {len_arr} 건")


if __name__ == "__main__":
    first_problem_arr = inputfunc_1()
    solution_func_first(first_problem_arr)






"""
함수를 두 개 작성

처리 함수 : processfunc(datas) : datas에 기억된 내용을 출력한다. 

처리 조건 : 
1) 급여액은 기본급 + 근속수당 
2) 수령액은 급여액 – 공제액

* 근무년수에 대한 수당표	* 급여 상한액에 대한 공제세율표
근무년수     근속수당
0~3년        150000
4~8년        450000
9년 이상    1000000	급여액                공제세율
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









print("\n\n\n\n\n연습문제2) 리스트를 통해 상품 자료를 입력받아 가공 후 출력하기\n")
"""
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





# 2번 문제 솔루션 시작부분
def inputfunc_2():
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

def solution_func_second():
    price_by_name = {"새우깡":450, "감자깡":300, "양파깡": 450}

    arr_items = inputfunc_2()

    len_arr = len(arr_items) # 12개

    count_by_name = {name: 0 for name in price_by_name}
    # {'새우깡': 0, '감자깡': 0, '양파깡': 0}

    # amt_by_name == amount_by_name
    amt_by_name = {name: 0 for name in price_by_name}
    # {'새우깡': 0, '감자깡': 0, '양파깡': 0}

    names = []; cnts = []
    for arr_item in arr_items:

        # nms_dt == Names_data, cs_dt == cnts_data
        nms_dt, cs_dt = arr_item.split(",")
        names.append(nms_dt); cnts.append(cs_dt)
        # 이름, 갯수 모음

        int_cd, int_pp = int(cs_dt), int(price_by_name[nms_dt])
        # 정수형 변환

        count_by_name[nms_dt] += int_cd     
        # {'새우깡': 135, '감자깡': 115, '양파깡': 105}

        amt_by_name[nms_dt] += int_cd * int_pp
        # {'새우깡': 60750, '감자깡': 34500, '양파깡': 47250}

    # print(names); print(cnts) # 이름과 갯수의 리스트

    order_table = [[0] * 4 for _ in range(len_arr)] # 상품의 출력 보드

    for row, item in enumerate(arr_items):
        int_cnts, int_pp = int(cnts[row]), int(price_by_name[names[row]])

        order_table[row][0] = names[row]
        order_table[row][1] = cnts[row]
        order_table[row][2] = price_by_name[names[row]]
        order_table[row][3] = int_cnts * int_pp

    # print(order_table)

    print("출력 형태:")
    print(f"{'상품명':<6} {'수량':>6} {'단가':>5} {'금액':>6}")
    print("-" * 35)
    for row in range(len_arr):
        print(f"{order_table[row][0]:<6}  {order_table[row][1]:>6}  {order_table[row][2]:>6}  {order_table[row][3]:>8}")

    print("\n소계")

    sum_eps = 0; sum_as = 0
    for name in price_by_name:
        print(f"{name} : {count_by_name[name]}건   소계액 : {amt_by_name[name]}원")
        sum_eps += int(count_by_name[name])
        sum_as += int(amt_by_name[name])

    print("총계")
    print(f"총 건수 : {sum_eps}")
    print(f"총 액   : {sum_as}")





if __name__ == "__main__":
    solution_func_second()




"""
소계
새우깡 : 135건   소계액 : 60750원
감자깡 : 115건   소계액 : 34500원
양파깡 : 105건   소계액 : 36750원
총계
총 건수 : 355
총 액  : 132000원
"""