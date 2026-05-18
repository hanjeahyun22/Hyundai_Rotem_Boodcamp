# 연결된 리스트(Linked list)

import os
os.system('clear')

# 놀이공원에 줄서기
class Node:
    def __init__(self, name):
        self.name = name
        self.next = None            # pointer


# 연결된 리스트 관리
class LinkedList:
    def __init__(self):
        self.head = None
    
    # 새로운 Node를 추가(줄 뒤에 다음 사람 추가)
    def append(self, name):
        new_node = Node(name)       # 새 노드 생성

        if self.head is None:       # 줄(List)이 비어있는 경우
            self.head = new_node
            return
        
        # 줄의 맨 끝 사람 찾기(이미 노드가 있다면 마지막 노드까지 이동)
        current = self.head
        while current.next is not None:
            current = current.next
        
        current.next = new_node

    def show(self):
        current = self.head
        while current is not None:
            print(current.name, end="->")
            current = current.next
        print("끝")

    # 특정 사람 뒤에 새 사람 끼워넣기
    # target node를 찾고, 새 노드를 만들고, 기존 연결
    def insert_after(self, target_name, new_name):
        current = self.head

        while current is not None:
            if current.name == target_name:
                new_node = Node(new_name)
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next

    # 특정 사람 삭제
    def remove(self, name):
        # 맨 앞사람이 나가는 경우
        if self.head and self.head.name == name:
            self.head = self.head.next              # head를 두번째 노드의 주소로 변경
            return
        # 삭제 대상이 맨 앞사람이 아닌 경우
        current = self.head
        while current and current.next:
            if current.next.name == name:
                current.next = current.next.next
                return
            current = current.next


# [실행 및 데이터 확인]
# 이론: 연결 리스트는 각 노드가 데이터와 다음 노드의 주소를 가짐으로써 논리적인 순서를 유지함
# 순서: 1. 리스트 객체 생성 -> 2. 데이터 순차적 추가 -> 3. 포인터를 통한 노드 간 연결 형성

line = LinkedList()                 # 1. 빈 연결 리스트 생성
line.append("철수")                 # 2. 첫 번째 노드(Head) 추가
line.append("영희")                 # 3. 두 번째 노드 추가 (철수의 next가 영희를 가리킴)
line.append("민수")                 # 4. 세 번째 노드 추가 (영희의 next가 민수를 가리킴)
line.remove("영희")
line.show()