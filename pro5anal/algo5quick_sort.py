# 터미널창 초기화
import os
os.system('cls')


print("""
# ######################################################################################################################
#                                   리스트 안에 들어있는 자료를 오름차순 정렬
# ######################################################################################################################
""")

print("========================================== 4) Quick 정렬 ==========================================")
print("설명 : 하나의 기준점을 중심으로 '작은 값'과 '큰 값'으로 나눠서 각각 정렬 후, 마지막에 이어 붙임")
print("group_small : 기준값보다 작은 그룹")
print("group_large : 기준값보다 큰 그룹")

print("\n-------------- 방법1) 이해 위주  - 배열을 하나 더 사용 --------------")
d = [6, 8, 3, 1, 2, 4, 7, 5]


def quick_sort(a):
    n = len(a)
    if n <= 1:
        return a
    
    # 기준값 (편의상 가장 마지막 값을 취함)
    pivot = a[-1]

    group_small = []
    group_large = []

    for i in range(0, n-1):
        if a[i] < pivot:
            group_small.append(a[i])
        else:
            group_large.append(a[i])
    
    return quick_sort(group_small) + [pivot] + quick_sort(group_large)

print(quick_sort(d))


print("\n-------------- 방법2) 일반적인 알고리즘 작성 방식 기존의 d 배열만 사용 --------------")
d = [6, 8, 3, 1, 2, 4, 7, 5]

def quick_sort2_sub(a, start, end):
    # 종료 조건 : 정렬 대상이 한 개 이하면 정렬 X
    if end - start <= 0:
        return

    pivot = a[end]
    i = start
    for j in range(start, end):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[end] = a[end], a[i]

    quick_sort2_sub(a, start, i-1)      # 기준값 보다 작은 그룹 재귀로 다시 정렬
    quick_sort2_sub(a, i+1, end)        # 기준값 보다 큰 그룹 재귀로 다시 정렬
    
def quick_sort2(a):
    quick_sort2_sub(a, 0, len(a)-1)     # 자료, 시작 index, 끝 index
    
    

quick_sort2(d)
print(d)