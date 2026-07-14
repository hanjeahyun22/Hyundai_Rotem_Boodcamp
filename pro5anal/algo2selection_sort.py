# 터미널창 초기화
import os
os.system('cls')


print("""
# ######################################################################################################################
#                                   리스트 안에 들어있는 자료를 오름차순 정렬
# ######################################################################################################################
""")

print("========================================== 1) 선택(Selection) 정렬 ==========================================")

print("\n-------------- 방법1) 이해 위주 : 기억장소를 기존의 d 배열 외에 하나 더 사용 --------------")
d = [2, 4, 5, 1, 3]
def find_min_idx(a):
    n = len(a)
    min_idx = 0
    for i in range(1, n):
        if a[i] < a[min_idx]:
            min_idx = i
    return min_idx

def sel_sort(a):
    result = []
    while a:                            # 리스트의 값을 전부 반복
        min_idx = find_min_idx(a)
        value = a.pop(min_idx)          # pop : 배열에서 값을 뽑음(기존 배열에서는 없앰 -->> [crtl+x])
        result.append(value)            # append : 배열에 새로운 값을 추가함.
    return result


# print("min_idx : ", find_min_idx(d), "\n최소값 : ", d[find_min_idx(d)])
print(sel_sort(d))

print("\n-------------- 방법2) 일반적인 알고리즘 작성 방식 - 메모리 절약 : 기억장소를 기존의 d 배열만 사용 --------------")
d = [2, 4, 5, 1, 3]
def sel_sort2(a):
    n = len(a)
    for i in range(0, n-1):         # 0부터 n-2회 반복
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]     # 찾은 최소값을 i번 위치로 이동
sel_sort2(d)
print(d)

