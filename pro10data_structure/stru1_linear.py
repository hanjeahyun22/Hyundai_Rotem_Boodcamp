# [자료구조] Linear List (선형 리스트)

# [이론] 선형 리스트(Linear List)
# - 데이터를 일정한 순서로 나열한 자료구조 (순차 리스트)
# - 입력 순서대로 저장되며, 데이터 사이에 빈틈이 없는 것이 특징
# - 특징: 메모리 상에 연속적인 공간에 저장됨 (Contiguous Memory)
# - 장점: 인덱스(Index)를 통한 데이터 접근 속도가 매우 빠름 (O(1))
# - 단점: 삽입/삭제 시 데이터 이동(Shifting)이 발생하여 오버헤드가 생길 수 있음 (O(n))

### [활용 가이드] ###
# 1. 사용하기 좋은 경우: 데이터의 양이 고정적이거나, 삽입/삭제보다 '조회' 작업이 빈번할 때
# 2. 사용하기 나쁜 경우: 데이터의 삽입/삭제가 빈번하게 일어나 데이터 이동 비용이 클 때

# [실습 1] 놀이공원 줄서기 구현
# 연습 1) Python 함수(method) 사용
import os
os.system("cls")

line = ["철수", "영희", "민수"]
print("현재 줄 상태 : \n", line)
print()

# 데이터로 접근 - index를 사용
print("맨 앞사람 : ", line[0])
print("맨 뒷사람 : ", line[2])
print()

# [메소드 설명] list.insert(index, value)
# - index: 삽입할 위치의 번호 / value: 삽입할 데이터
# - 동작: 특정 인덱스 위치에 데이터를 삽입. 기존 데이터들은 뒤로 한 칸씩 밀림(Shift Right)
line.insert(2, "지수")              # 기존 index=2의 "민수"는 뒤로 한칸 밀림
print("현재 줄 상태 : \n", line)
print()

# [메소드 설명] list.remove(value)
# - value: 삭제하고자 하는 데이터 값
# - 동작: 리스트에서 특정 값을 찾아 삭제. 삭제된 위치 이후의 데이터들은 앞으로 당겨짐(Shift Left)
line.remove("영희")
print("현재 줄 상태 : \n", line)
print()

# [메소드 설명] list.pop(index)
# - index: 꺼낼 데이터의 위치 (생략 시 마지막 데이터)
# - 동작: 앞사람 부터 놀이기구 타기 - 첫번째 자료부터 빠져나감. -> 뒤의 자료는 앞으로 한칸 씩 당김
first_person = line.pop(0)
print("첫번째 사람 : ", first_person)
print("첫번째 사람 입장 후, 현재 줄 상태 : \n", line)
print()

# 현재 남은 사람 변화와 함께 출력
for i, person in enumerate(line):
    print(i, '번째 사람 : ', person)


# [실습 2] 선형 리스트의 원리 이해 (로직 직접 구현)
# 연습 2) Python 코드 사용
line = ["철수", "영희", "민수"]
print("현재 줄 상태 : \n", line)
print()

# 데이터로 접근 - index 사용
print("맨 앞사람 : ", line[0])
print("맨 뒷사람 : ", line[2])
print()

# 새치기 - 중간에 새로운 사람 삽입 : "철수", "영희", "민수"에서 "지수"를 "민수"앞으로 새치기
# index 2 위치에 지수 삽입 -> 공간확보 -> index=2 이후로 뒤로 한 칸씩 이동 -> 값 대입
line.append(None)
# range(시작, 끝, 증감) : 리스트 끝부터 삽입할 위치까지 역순으로 반복하며 데이터를 뒤로 한 칸씩 이동
for i in range(len(line)-1, 2, -1):
    line[i] = line[i-1]
line[2] = "지수"
print("지수가 삽입된 후, 현재 줄 상태 : \n", line)
print()

# 줄에서 대기하던 사람(영희) 줄서기 포기 -> 삭제
# 영희의 위치를 찾고, 그 뒤 요소들을 앞으로 이동
remove_index = None
for i in range(len(line)):
    if line[i] == "영희":
        remove_index = i
        break

for i in range(remove_index, len(line)-1):
    line[i] = line[i+1]
line.pop()
print("영희가 줄서기 포기 후, 현재 줄 상태 : \n", line)
print()

# 앞사람 한 명이 놀이기구 타기 -> 앞에서부터 한 칸씩 이동
first_person = line[0]
for i in range(0, len(line)-1):
    line[i] = line[i+1]
line.pop()
print("첫번째 사람 입장 후, 현재 줄 상태 : \n", line)
print()

# 현재 남은 사람 번호와 함께 출력
for i, p in enumerate(line):
    print(i, '번째 사람 : ', p)

# [결론]
# LinearList는 index로 즉시 접근 가능하여 조회에 유리하지만,
# 삽입/삭제 시 데이터 이동 발생(비용)으로 인해 데이터 변화가 잦은 경우 비효율적임.