# 터미널창 초기화
import os
os.system('cls')


print("""
# ######################################################################################################################
#                                   리스트 안에 들어있는 자료를 오름차순 정렬
# ######################################################################################################################
""")

print("========================================== 2) 삽입(insert) 정렬 ==========================================")
print("설명 : 앞에서 부터 하나씩 꺼내서, 자기자리를 찾아 끼워 넣는 정렬")
print("\n-------------- 방법1) 이해 위주  - 배열을 하나 더 사용 --------------")
d = [2, 4, 5, 1, 3]

def find_ins_idx(r, v):             # r : 배열,     v : 삽입 할 적절한 위치를 찾아야 하는값
    for i in range(0, len(r)):
        if v < r[i]:
            return i
    # 적정한 삽입 위치를 찾지 못한 경우, 맨 뒤에 삽입
    return len(r)

# print(find_ins_idx(d, 1))

def ins_sort(a):
    result = []
    while a:
        value = a.pop(0)
        ins_idx = find_ins_idx(result, value)
        result.insert(ins_idx, value)
        print("a : ", a)
        print("result : ", result)
    return result

print("\n방법1) Insert_soring 결과\n", ins_sort(d))

print("\n-------------- 방법2) 일반적인 알고리즘 작성 방식 기존의 d 배열만 사용 --------------")
d = [2, 4, 5, 1, 3]
def ins_sort2(a):
    n = len(a)

    # 두 번째 값(index=1)부터 마지막(index=n)까지 차례대로 삽입 할 대상 선택
    for i in range (1, n):
        key = a[i]              # i번째 위치에 있는 값을 key에 임시저장
        j = i - 1               # j를 i 바로 왼쪽 위치로 저장

        while j >= 0 and a[j] > key:
            
            a[j + 1] = a[j]     # 삽입 할 공간이 생기도록 값을 우측으로 밀기
            j -= 1              # 그 다음 왼쪽으로 이동하면서 다시 비교
        a[j + 1] = key          # 찾은 삽입 위치에 key를 저장

ins_sort2(d)
print(d)