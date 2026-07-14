# 터미널창 초기화
import os
os.system('cls')


print("""
# ######################################################################################################################
#                                   리스트 안에 들어있는 자료를 오름차순 정렬
# ######################################################################################################################
""")

print("========================================== 3) 병합(merge) 정렬 ==========================================")
print("설명 : 리스트 자료를 나누고, 요소가 1개씩 남을 때 까지 반복\n분할된 리스트를 정렬하며, 하나로 합친다.(정렬 상태 유지)")
print("\n-------------- 방법1) 이해 위주  - 배열을 하나 더 사용 --------------")
d = [6, 8, 3, 1, 2, 4, 7, 5]
def merge_sort(a):
    n = len(a)

    if n <= 1:
        return a
    
    mid = n // 2                    # 중간을 기준으로 두 group으로 분할
    
    # 함수는 독립적인 공간을 가짐. 아래의 group1, group2는 서로 independent -->>> 서로 다른 메모리 사용
    group1 = merge_sort(a[:mid])    # 재귀 호출
    group2 = merge_sort(a[mid:])    # 재귀 호출

    # 두 그룹의 앞자리를 비교해서, 더 작은 값을 앞으로 뺌
    result = []
    while group1 and group2:
        if group1[0] < group2[0]:
            result.append(group1.pop(0))
        else:
            result.append(group2.pop(0))
        print("result : ", result)
    
    # group1과 group2 중, 소진된 것은 스킵
    while group1:
        result.append(group1.pop(0))
    while group2:
        result.append(group2.pop(0))
    return result


print(merge_sort(d))


print("\n-------------- 방법2) 일반적인 알고리즘 작성 방식 기존의 d 배열만 사용 --------------")
# 재귀호출이 정렬된 리스트를 반환
# 병합도 새 리스트를 만들어 반환
# 원본 리스트는 그대로이고, 정렬된 결과는 새 리스트에 저장
d = [6, 8, 3, 1, 2, 4, 7, 5]

def merge_sort2(a):
    if len(a) <= 1:
        return a
    
    mid = len(a) // 2
    group_left = merge_sort2(a[:mid])
    group_right = merge_sort2(a[mid:])

    result = []
    i = 0           # group_left의 index
    j = 0           # group_right의 index

    # 병합
    while i < len(group_left) and j < len(group_right):
        if group_left[i] < group_right[j]:
            result.append(group_left[i])
            i += 1
        else:
            result.append(group_right[j])
            j += 1

    # 남은 요소 추가
    result += group_left[i:]
    result += group_right[j:]

    return result


sorted_d = merge_sort2(d)
print(sorted_d)