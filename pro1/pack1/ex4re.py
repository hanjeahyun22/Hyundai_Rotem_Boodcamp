import re   # 정규표현식 지원 모듈 로딩
"""
re는 문자열에서 특정 패턴(규칙) 을 찾거나, 바꾸거나, 쪼개는 기능을 제공해.

“123이 포함된 부분 찾아줘”

“숫자 덩어리만 뽑아줘”

“한글 연속 구간만 뽑아줘”

“공백 기준이 아니라 ‘패턴’ 기준으로 split 해줘”
"""

ss = "1234 abc가나다ab\d\n\tcABC_123555_6'Python is fun'"
print(ss)

# findall 의 함수는 결과값의 type이 'List'로 나옴
"""
re.findall(pattern, string)
"""

print(re.findall(r'123', ss))       # 혹시 모를 escape 문자(\n, \t)를 무시하기 위해서 r 을 집어넣음
print(re.findall(r'가나', ss))

ss = "1234 abc가나다abcABC_123555가나가나_6'Python is fun'"
print()
print()
print(re.findall(r'가나', ss))
print()
print()
print(re.findall(r'[0-9]', ss))
print()
print()

# + : 1번 이상 -> 덩어리
print(re.findall(r'[0-9]+', ss))        # ['1234', '123555', '6']
print()
print()

# * : 0번 이상 -> 빈값 ' ' 도 매우 많이 반환
print(re.findall(r'[0-9]*', ss))        # ['1234', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '123555', '', '', '', '', '', '6', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
print()
print()

# ? : 0 또는 1번 이상 
print(re.findall(r'[0-9]?', ss))        # ['1', '2', '3', '4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '2', '3', '5', '5', '5', '', '', '', '', '', '6', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
print()
print()

# {2} : 2개씩 끊어서
print(re.findall(r'[0-9]{2}', ss))      # ['12', '34', '12', '35', '55']
print()
print()

# {2, 3} : 일단 3개 묶음, 안되면 2개 묶음
print(re.findall(r'[0-9]{2,3}', ss))    # ['123', '123', '555']
print()
print()

# [a-zA-Z]+ : 영문자 1개 이상 -> 영문자 덩어리
print(re.findall(r'[a-zA-Z]+', ss))     # ['abc', 'abcABC', 'Python', 'is', 'fun']
print()
print()

# [가-힣]+ : 한글 덩어리
print(re.findall(r'[가-힣]+', ss))      # ['가나다', '가나가나']
print()
print()

# \d : digit -> 숫자 하나씩 == [0-9]
print(re.findall(r'\d', ss))            # ['1', '2', '3', '4', '1', '2', '3', '5', '5', '5', '6']
print()
print()

# \D : not digit -> 숫자가 아닌 글자 하나씩
print(re.findall(r'\D', ss))            # [' ', 'a', 'b', 'c', '가', '나', '다', 'a', 'b', 'c', 'A', 'B', 'C', '_', '가', '나', '가', '나', '_', "'", 'P', 'y', 't', 'h', 'o', 'n', ' ', 'i', 's', ' ', 'f', 'u', 'n', "'"]



###############################################################




ss = "1234 abc가나다ab\d\n\tcABC_123555_6'Python is fun'"
print(ss)

# re.search : re를 통해서 찾은 처음값 한개만
m = re.search(r'[0-9]+', ss)
print(m)

# re.match : 문자열 "처음"부터 매칭 되는지 확인
re.match(r'\d+', ss)

# re.sub() : 치환 -> 숫자 덩어리([0-9]+)를 '#' 하나로 치환
re.sub(r'\d+', '#', ss)  # 숫자 덩어리를 #로 바꾸기

# re.split() : 패턴 기준으로 분리
re.split(r'[_\s]+', ss)  # 언더바/공백 기준 분리