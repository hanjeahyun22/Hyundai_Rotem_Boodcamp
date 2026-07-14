# 재귀문제 :  리스트 자료 v = [7, 9, 15, 43, 32, 21] 에서 최대값 구하기 - 재귀 호출 사용 
                #   print(find_max(v, len(v)))
# for문으로 
def find_max_for(v):
    max_value = v[0]  

    for i in range(1, len(v)):  
        if v[i] > max_value: 
            max_value = v[i] 

    return max_value 

v = [7, 9, 15, 43, 32, 21]
print(find_max_for(v))

print('------------')
def find_max(v, n):
    if n == 1: 
        return v[0]   # 리스트의 첫 번째 값을 반환하고 재귀 종료
    # 재귀 호출
    prev_max = find_max(v, n - 1)
        # 앞의 (n-1)개 원소 중 최대값을 구함. 이 호출이 끝나야 아래 코드로 내려옴

    # 마지막 값과 비교
    if v[n - 1] > prev_max:
        # 현재 단계에서 마지막 원소 v[n-1]과 이전 단계에서 구한 최대값(prev_max)을 비교
        return v[n - 1]  # 마지막 값이 더 크면 그 값을 최대값으로 반환
    else:
        return prev_max 

v = [7, 9, 15, 43, 32, 21] 
print(find_max(v, len(v)))

print('-- 좀 더 파이썬 스럽게 ---')
def find_max(v, n):
    if n == 1:
        return v[0]         # 재귀 탈출    

    return max(             # max 내장 함수 : 최대값
        v[n - 1],           #  현재 단계의 마지막 원소
        find_max(v, n - 1)  #  앞의 (n-1)개 중 최대값을 재귀로 구함
    )   # 두 값 중 큰 값을 반환

print(find_max(v, len(v)))

