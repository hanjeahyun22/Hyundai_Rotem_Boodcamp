## 기본 자료형 : int, float, bool, complex
## 묶은 자료형 : str, list, tuple, set, dict

#1) str : 문자열 묶음 자료형 -> 순서 O, 수정 X
s = 'sequence'
print(s)
print(s, id(s))

print('길이 : ', len(s))
print(s[0], s[2])           # 변수 s(= 'sequence')의 왼쪽부터 n 번째 데이터 s[n] ----->>>>> 순서 O
print('길이 : ', s.find('e'), s.find('e', 3), s.rfind('e'))

# 인덱싱
print(s[5])                 # 변수명[순서], index는 0부터 카운트

# 슬라이싱
print(s[2:5])               # 2번째 이상 ~ 5번째 미만 -> 2,3,4
print(s[:], ' ', s[0:len(s)], s[::1])   # s[:] == s[0:len(s)] == s[::1]
print(s[0:7:2])             # 초기index : 마지막index : 변차
print(s[-1],' ', s[-4:-1:2])                # -1번째는 뒤에서 첫번째
print(s)
s = 'sequenc'               # X수정X O변경O
print(s, id(s))
s = 'bequence'
print(s, id(s))

print('-----'*10)
print('-----'*10)
print('-----'*10)


#2) List : 다양한 종류의 자료 묶음형, 순서O, 수정O, 중복O
a = [1, 2, 3]
print(a, a[0], a[0:2:1], a[0:2:-1])
b=[10, a, 10, 20.5, True, '문자열']
print(b)
print(b, ' ', b[1], ' ', b[1][0])   # b의 첫번째 = a, a의 0번째 = 1
print()
family = ['엄마','아빠','나','여동생']
print(family)
print(id(family))

# List의 .append 수정 -> 마지막에 추가
family.append('남동생')
print(family)
print(id(family))       # 수정했기 때문에, 동일한 id

# List의 .remove 수정 -> 값('나)에 의한 삭제
family.remove('나')
print(family)
print(id(family))

# List의 del 함수에 의한 삭제 -> 순서(2)에 의한 삭제
del family[2]
print(family)

# List의 .insert 수정 -> 원하는 위치에 삽입
family.insert(0, '할머니')
print(family)
print(id(family))

# List의 .extend 수정
family.extend(['삼촌', '고모', '조카'])
print(family)
print(id(family))

# += 수정 -> 마지막에 추가
family += ['고모']
print(family)
print(id(family))

# List의 index 값 찾기
print(family.index('아빠'))

# List의 in 함수 - 있는지 없는지 True/False
print('엄마' in family, '나' in family)

# sort 정렬 -> 원본이 바뀜
print()
kbs = ['123', '34', '234']
kbs.sort()                  # 문자열 정렬
print(kbs)
mbc = [123, 34, 234]
mbc.sort()                  # 숫자 정렬 -> 오름차순
mbc.sort(reverse=True)      # 숫자 정렬 -> 내림차순
print(mbc)

# sorted 정렬 -> 원본은 그대로 유지, sort한 결과값을 새로운 객체에 저장
print('`````'*5)
sbs = [123, 34, 234]
ytn = sorted(sbs)
print(sbs)
print(ytn)
print()

# shallow 카피, deep 카피
name = ['tom', 'james', 'oscar']
name2 = name
print(name, id(name))
print(name2, id(name2))         # name이랑 name2랑 주소가 같음

import copy
name3 = copy.deepcopy(name)     # deepcopy를 하면 주소가 새로운 객체로 넘어감
print(name3, id(name3))         # name2의 주소는 name이랑 같지만, name3은 name의 주소랑 다름

name[0] = '길동'
print(name)                     # ['길동', 'james', 'oscar']
print(name2)                    # ['길동', 'james', 'oscar']
print(name3)                    # ['tom', 'james', 'oscar']     -> name3라는 새로운 객체로 deepcopy 했으므로, name[0]='길동' 이라고 해도 달라지자 않음



print('-----'*10)
print('-----'*10)
print('-----'*10)


#3) tuple : 리스트와 유사, 읽기 전용 -> 수정X
t = (1,2,3,4)           # tuple
print(t, type(t))
t = 1,2,3,4             # tuple 위의 값과 동일
print(t, type(t))

k = (1)
print(k, type(k))       # () 소괄호 안에 값이 단 하나 라면, tuple이 아닌 int값을 가짐

k = (1, )
print(k, type(k))       # tuple
print(t[0], ' ', t[0:2])

# tuple은 수정 불가
# t[0] = 77             # 불가능

imsi = list(t)
imsi[0] = 77
print(t, type(imsi))
t = tuple(imsi)
print(t, type(t))

print('-----'*10)
print('-----'*10)
print('-----'*10)


#4) set : 순서 X, ***** 중복 X *****
# *****************************************
# 중복 데이터를 없앨 때, set함수에 넣었다가 뺌
# *****************************************

ss = {1, 2, 1, 3}
print(ss)
ss2 = {3, 4}

# set의 union 함수 : 합집합
print(ss.union(ss2))

# set의 intersection 함수 : 교집합
print(ss.intersection(ss2))

# set의 차집합(-), 합집합(|), 교집합(&)
print(ss - ss2, ss | ss2, ss & ss2)

# set은 순서가 없음
# print(ss[0])        # error 실행 불가

# set의 수정 : update, discard, remove
ss.update({6, 7})   # 기존의 ss set에 새로 추가
print(ss)

ss.discard(7)       
ss.discard(7)       # discard는 없어도 errorX 그냥 넘어감
print(ss)
ss.remove(6)
# ss.remove(6)        # remove는 없으면 error 발생 -> 실행 안됨
print(ss)

li = ['aa', 'aa', 'bb', 'cc', 'aa']
print(li)
imsi = set(li)      # 중복은 사라지지만, 순서는 지 맘대로 바뀜
li = list(imsi)
print(li)

print('-----'*10)
print('-----'*10)
print('-----'*10)


#5) dict : 사전 자료형 {'키':값} 형태, 순서 X -> value값을 key로 찾음

# 방법 1
mydic = dict(k1 = 1, k2 = 'ok', k3 = 123.4)
print(mydic, type(mydic))

# 방법 2
dic = {'파이썬':'뱀', '자바':'커피', '인사':'안녕'}     # key(='파이썬', '자바', '인사'), value(='뱀', '커피', '안녕')
print(dic)
print(len(dic))
print(dic['자바'])          # '자바'라는 key 가 갖는 값 '커피'

# dict의 get 기능'
ff = dic.get('자바')
print(ff)

# print(dic['커피'])      # 에러    -> dict의 value값은 print 불가능
# print(dic[0])       # 에러      -> dict는 순서X
# dict의 데이터 추가 -> 맨 뒤에 들어가는 개념X (순서 X)

dic['금요일'] = '와우'
print(dic)

# dict의 데이터 삭제
del dic['인사']
print(dic)

# dic의 key, value값 확인
print(dic.keys())
print(dic.values())