# 재귀함수 : 함수가 자기 자신을 호출 - 반복 처리
# 재귀함수는 내려가는 중간에는 계산 X -->> 모든 재귀 literation 끝나고 계산
# 재귀함수를 사용해서 반복적인 함수를 처리할 때, 각 함수는 개개인의 주소를 가짐 -->> Overflow 가능성 존재
"""
사용 목적에 따른 선택 기준
  - 반복문이 적합한 경우 : 단순 반복, 배열/리스트 순회, 반복 횟수가 명확, 성능이 중요한 경우
    예 : 최대값 찾기, 합계 계산, 카운팅
  - 재귀가 적합한 경우 : 문제 구조가 자기 자신과 동일, 분할 정복, 트리/그래프 탐색
    예 : 팩토리얼, 피보나치, 트리 순회, DFS, 퀵정렬, 병합정렬
"""

def countDown(n):
    if n == 0:
        print('완료')
        return                          # 의미 없는 return 이지만, 명시적으로 적어줌
    else:
        print(n, end = ' ')
        countDown(n - 1)                # 재귀(Recusion)
        
countDown(5)


print(' ')
print('-----------'*5)
print(' ')


print('     1부터 n까지의 합        ')
def totFunc(n):
    if n == 0:
        print('탈출')
        return 1
    return n + totFunc(n - 1)           # 재귀(Recusion)            [5 + 4] -->> [5 + 4 + 3] -->> [5 + 4 + 3 + 2] -->> [5 + 4 + 3 + 2 + 1] -->> [5 + 4 + 3 + 2 + 1 + 1]=16

result = totFunc(5)
print('result : ', result)


print(' ')
print('-----------'*5)
print(' ')


print('     5 factorial 계산        ')
def factFunc(a):
    if a == 1: return 1                 # 재귀함수가 끝나는 지점
    print(a)
    return a * factFunc(a - 1)          # 재귀(Recusion)            

result2 = factFunc(5)
print('result2 : ', result2)

print('end')