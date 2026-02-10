# 문제 1
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

def processfunc(datas):
    CURRENT_YEAR = 2026

    for data in datas:
        emp_no, name, base_pay, hire_year = data

        work_years = CURRENT_YEAR - hire_year

        if work_years <= 3:
            bonus = 150000
        elif work_years <= 8:
            bonus = 450000
        else:
            bonus = 1000000

        salary = base_pay + bonus

        if salary >= 3000000:
            tax_rate = 0.5
        elif salary >= 2000000:
            tax_rate = 0.3
        else:
            tax_rate = 0.15

        tax = int(salary * tax_rate)
        net_pay = salary - tax

        data.append(work_years)
        data.append(bonus)
        data.append(tax)
        data.append(net_pay)

    print("사번  이름    기본급    근무년수  근속수당  공제액    수령액")
    print("-" * 75)

    for d in datas:
        print(f"{d[0]:<4} {d[1]:<6} {d[2]:<8} {d[4]:<8} {d[5]:<8} {d[6]:<8} {d[7]}")

    print("-" * 75)
    print(f"처리 건수 : {len(datas)} 건")


datas = inputfunc()
processfunc(datas)





# 문제 2
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

def processfunc(datas):
    pt = {
        "새우깡": 450,
        "감자깡": 300,
        "양파깡": 350
    }

    qq = {
        "새우깡": 0,
        "감자깡": 0,
        "양파깡": 0
    }
    aa = {
        "새우깡": 0,
        "감자깡": 0,
        "양파깡": 0
    }

    tq = 0
    ta = 0

    print("상품명   수량   단가   금액")
    print("-" * 35)

    for data in datas:
        name, qty = data.split(",")
        qty = int(qty)

        price = pt[name]

        amount = qty * price

        print(f"{name:<6} {qty:<6} {price:<6} {amount}")

        qq[name] += qty
        aa[name] += amount

        tq += qty
        ta += amount

    print("\n소계")
    for name in pt:
        print(f"{name} : {qq[name]}건   소계액 : {aa[name]}원")

    print("\n총계")
    print(f"총 건수 : {tq}")
    print(f"총 액  : {ta}원")


datas = inputfunc()
processfunc(datas)
