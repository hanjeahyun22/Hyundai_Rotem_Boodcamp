# 반복문 for

# ##################################
# ##################################
print('====='*5)
print('====='*5)

# for i in [1,2,3,4,5]:               # [] : 묶음형 자료 (str, list, set, tuple, dict)에서 for문으로 반복
# for i in (1,2,3,4,5):
for i in {1,2,3,4,5}:
    print(i, end = ' ')


# ##################################
# ##################################
print('====='*5)
print('====='*5)

"""

값 - 평균 = 편차

전체 (편차)^2 합 / 개수 = 분산

sqrt(분산) = 표준편차

"""
print('--- 분산/표준편차 ---')

# numbers = [1,3,5,7,9]
numbers = [3,4,5,6,7]
# numbers = [-3,4,5,7,12]
tot = 0
for a in numbers:
    tot += a
print(f'합은 {tot}, 평균은 {tot / len(numbers)}')
avg = tot / len(numbers)

# 편차 제곱의 합
hap = 0
for i in numbers:
    hap += (i - avg) ** 2
print(f'편차 제곱의 합 {hap}')

# 분산
var = hap / len(numbers)
print(f'분산은 {var}')

# 표준편차
print(f'표준편차는 {var**(1/2)}')




# ##################################
# ##################################
print('====='*5)
print('====='*5)

colors = ['r', 'g', 'b']        # list 형식이기 때문에, 순서대로 출력하지만, (set) 형식으로 지정하면 순서 X -> 무작위로 출력
for v in colors:
    print(v, end = ' ')
    """
    'r'을 v가 가져서 print 'r' -> 'g'를 v가 가져가서 print 'g' -> 'b'을 v가 가져가서 print 'b'
    """    



print('--- 사전형 ---')
data = {'python':'만능언어', 'java':'웹 전용 언어', 'mariadb':'RDBMS(환경데이터)'}
for i in data.items():          # .items : dict 묶음형에서는 ..items 라는 tuple 형식으로 반환해주는 함수
    # print(i)                    # tuple 타입
    print(i[0], ' ~~ ', i[1])
print()

for key, val in data.items():   # .items : dict 묶음형에서 두개의 변수를 선언해주면 key, value를 차례대로 받아줌 
    print(key, val)
print()

for key in data.keys():   # .keys : dict 묶음형에서 key만 받아줌 
    print(key, end = " ")
print()

for val in data.values():   # .values : dict 묶음형에서 value만 받아줌 
    print(val, end = " ")
print()

print('iter() : 반복 가능한 객체를 하나 씩 꺼낼 수 있는 상태로 만들어 주는 함수')
iteration = iter(colors)
for v in iteration:
    print(v, end = ', ')

print()

for idx, d in enumerate(colors):        # enumerate : 인덱스와 값을 반환해줌
    print(idx, ' ', d)



# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('------ 다중 for ------')
for n in [2,3]:
    print('---{}단---'.format(n))
    for i in [1,2,3,4,5,6,7,8,9]:
        print('{} * {} = {}'.format(n, i, n * i))


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('---- continue, break ----')

nums = [1,2,3,4,5]
for i in nums:
    if i == 2: continue
    if i == 4:
        print('\n강제 종료')
        break
    print(i, end = ' ')
else:
    print('\n정상 종료')


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n정규 표현식 + for')
str = """KF-21 Block-II 개발 성과와 일정 단축
KF-21 보라매는 Block-I의 공대공 임무 최적화에서 벗어나 공대지·공대함 능력을 갖춘 다목적 전투기로 진화하고 있다. 방위사업청이 13일 발표한 바에 따르면 42개월간 약 1600회의 개발 비행시험을 수행했고, 단 한 건의 사고 없이 1만3000여 개의 시험 조건을 통과했다. 이는 한국 항공산업 역사상 전례 없는 안정성 기록으로 평가되며, 개발 과정에서의 기술적 완성도를 입증하는 지표로 활용되고 있다. Block-II 개발 완료 시점은 당초 계획보다 1.5년 앞당겨 2027년 초로 단축됐으며, 이는 단순한 일정 조정이 아닌 독자 기술 역량의 성숙을 보여주는 전환점이다. 개발 일정 단축의 배경에는 국내 방산 생태계의 협력 강화와 핵심 부품의 국산화 진전이 자리하고 있으며, 이러한 기반이 향후 수출 경쟁력의 핵심 요소로 작용할 전망이다.
KF-21 “17년동안 독자개발해 결실 이뤘다” 한국이 전투기 만들자, 해외 공군들이 줄 서는 이유
KF-21 Block-I 양산 로드맵과 전력화 계획
KF-21 Block-I은 공대공 임무에 최적화된 4.5세대 전투기로서 미티어(Meteor)와 IRIS-T 등 유럽제 공대공 미사일 운용이 가능하다. 2026년 9월 1호 양산기가 공군에 전력화될 예정이며, 이후 2027년까지 20대, 2028년까지 추가 20대가 생산돼 총 40대의 Block-I이 우선 양산된다. 이 양산 계획은 공군의 노후 전투기인 F-4와 F-5 계열의 퇴역에 따른 전력 공백을 해소하려는 전략의 일환이다. KAI는 생산 라인의 효율화와 부품 공급망 안정화를 통해 양산 일정을 준수할 계획이며, Block-I의 성공적인 전력화는 Block-II 양산의 기반이 될 것으로 기대된다. 또한 Block-I 운용 과정에서 축적되는 실전 데이터는 Block-II의 성능 개량과 무장 통합에 반영될 예정이다."""

import re
str2 = re.sub(r'[^가-힣\s]', '', str)        # 대괄호 안의 ^ : 부정      # 가-힣 : 한글      # \s : 공백        -->> 한글과 공백 이외의 문자는 공백처리
print(str2)
print('--------'*5)

str3 = str2.split(' ')                      # .split : 문자열 함수 중에서 분리하는 기능              -->> ' ' 공백으로 str2를 분리              -->> 결과물은 list 타입형
print(str3)
print('--------'*5)

# 단어 발생 횟수를 dict로 정리
cou = {}
for i in str3:
    if i in cou:
        cou[i] += 1         # 같은 단어가 있으면 누적
    else:
        cou[i] = 1          # 최초로 카운트 되는 경우, '단어':1로 기록
print(cou)
print('--------'*5)

print('정규 표현식 좀 더 연습')
for test_ss in ['111-1234', '일이삼-일이삼사', '222-1234', '333&1234']:
    if re.match(r'^\d{3}-\d{4}$', test_ss):                     # 대활호 밖의 ^ : 처음부터         # $ : 끝나는         -->> '^' 부터 '$' 사이의 값을 다룸  
        print(test_ss, '전화번호 O')
    else:
        print(test_ss, '전화번호 X')


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('comprehension : 반복문 + 조건문 + 값 생성을 한 줄로 표현')
a = [1,2,3,4,5,6,7,8,9,10]
# li = []
# for i in a:
#     if i % 2 == 0:
#         li.append(i)                  # .append : 요소를 리스트의 맨 뒤에 추가시켜줌
# print(li)

print(list(i for i in a if i % 2 == 0))

print('--------'*5)

# datas = [1, 2, 'a', True, 3.0]
datas = {1, 2, 'a', True, 3.0, 2, 1, 2, 'd'}
# datas = {1, 2, 'a', True, 3.0, 2, 1, 2, 3, 'd'}           #################################   3 을 int로 넣어도 왜 출력 x??
li2 = [i * i for i in datas if type(i) == int]
print(li2)

print('--------'*5)

id_name = {1:'tom', 2:'oscar'}
name_id = {val:key for key, val in id_name.items()}         # 기존 id_name의 key:val 순서로 되어있던 dict 자료 -->> val:key 순서로 바꿔서 출력
print(name_id)
print()
print('--------'*5)

print([1,2,3])                                                              # [1, 2, 3]
print(*[1,2,3])                                         # * : unpack 기호   # 1 2 3
print('--------'*5)

aa = [(1,2), (3,4), (5,6)]
for a, b in aa:
    print(a + b)

print('--------'*5)

print(*[a + b for a, b in aa], sep='\n')                   # sep : seperator 구분자 지정 옵션


# ##################################
# ##################################
print('====='*5)
print('====='*5)

print('\n수열 생성 : range')
print(list(range(1, 6)))                # 1이상 6 미만 list 형식으로 반환하라  -->>  [1, 2, 3, 4, 5]            # 증가치 1은 생략 가능
print(tuple(range(1, 6, 2)))            # range(시작숫자(이상), 마지막 숫자(미만), 증가치)
print(tuple(range(1, 6, 2)))
print(set(range(1, 6, 2)))
print(list(range(-10, -100, -20)))

print()
print('--------'*5)

for i in range(6):                      # 초기값을 지정 안하면 0부터 시작
    print(i, end =' ')                  # 0 1 2 3 4 5

print('--------'*5)

for _ in range(6):                      # for 반복문을 통해서 i 값이 변하기는 하지만, 사용하지 않을 경우, 'for i in range(6):' 이런식으로 두기 보다는, 가독성을 위해서 i를 '_'로 표현
    print('반복')


# ##################################
# ##################################
print('====='*5)
print('====='*5)

# 코딩
tot  = 0
for i in range(1, 11):
    tot += i
print('tot : ', tot)

# 내장함수
print('tot : ', sum(range(1,11)))       

# ##################################
# ##################################
print('====='*5)
print('====='*5)

for i in range(1,10):
    print(f'2 * {i} = {2 * i}')




"""
for 반복문 문제 :

Q1. 2~9 구구단 출력 (단은 행 단위 출력)
Q2. 주사위를 두 번 던져서 나온 숫자들의 합이 4의 배수가 되는 경우만 출력

"""

# ##################################
# ##################################
print('====='*5)
print('====='*5)

for i in range(2,10):
    for j in range(1,10):
        print(f'{i} * {j} = {i * j}')
    print('-----'*3)


# ##################################
# ##################################
print('====='*5)
print('====='*5)

li = []
for i in range(1,7):
    for j in range(1,7):
        if (i + j) % 4 == 0:
            print(f'두 주사위의 합이 4의 배수가 되는 경우만 출력. 합 : {i+j}')
            li.append(i+j)
        else:
            pass
ch = set(li)
li = ch

print('최종적으로, 두 주사위를 굴렸을 때, 합이 4의 배수가 되는 경우의 수(중복 제외) 츨력 : ', li)



print('\n루프 안에 종속되어 있지 않고 단순한 ex7의 전체 코드 끝 : end')
