"""
재귀문제 :  리스트 자료 v = [7, 9, 15, 43, 32, 21] 에서 최대값 구하기 - 재귀 호출 사용 

                  print(find_max(v, len(v)))
"""

v = [7, 9, 15, 43, 32, 21]

def find_max(var, num):

    
    if num == 1:
        prev_max = var[0]
        return prev_max
    
    prev_max = find_max(var, num - 1)
    
    if prev_max >= var[num - 1]:
        pass
    elif prev_max < var[num - 1]:
        prev_max = var[num - 1]
    return prev_max

print(find_max(v, len(v)))






# def find_max(var, num):
#     # bigger_var = var[num - 1]
#     if num == 0:
#         print('완료')
#         return bigger_var
#     else:
#         if var[num - 1] > var[num - 2]:
#             bigger_var = var[num - 1]
#             print('--')
#             print(bigger_var)
#             print(num)
#             print('--')
#         else:
#             bigger_var = var[num - 2]
#             print('****')
#             print(bigger_var)
#             print(num)
#             print('****')
#         return bigger_var, find_max(var, num - 1)
    
# print(find_max(v, len(v)))
