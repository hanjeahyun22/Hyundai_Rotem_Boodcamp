# ==========================================
# [자료구조] 스택 (Stack)
# ==========================================
# 이론적 정의:
# 1. LIFO (Last-In, First-Out): '후입선출' 구조.
#    가장 나중에 들어온 데이터가 가장 먼저 나가는 방식.
# 2. 주요 연산:
#    - Push: 데이터를 스택의 맨 위에 추가 (Python의 append)
#    - Pop: 스택의 맨 위 데이터를 제거하고 반환 (Python의 pop)
# 3. 활용 사례: 웹 브라우저 뒤로가기, 실행 취소(Undo), 함수 호출 스택 등
# ==========================================

# 1. 스택 초기화
stack = []              # Python의 List를 Stack 자료구조로 활용
print("--- 놀이공원 입장 ---")

# 2. 데이터 추가 (Push)
# 놀이 기구 탑승 기록을 순차적으로 스택에 쌓음
stack.append("T-express 탑승")
print("기록 추가:", stack)

stack.append("바이킹 탑승")
print("기록 추가:", stack)

stack.append("회전목마 탑승")
print("기록 추가:", stack)

# [주의] stack[1]과 같이 인덱스로 접근하는 것은 Python 리스트의 기능이며, 
# 순수한 Stack의 개념(Top을 통해서만 접근)에는 어긋남.

# 3. 데이터 삭제 (Pop)
# 가장 최근(마지막)에 추가된 기록을 삭제
last_action = stack.pop()               
print(f"\n[취소] '{last_action}' 기록을 삭제했습니다.")

# 4. 최종 결과 확인
print("현재 남은 기록:", stack)
print("--------------------")


# LIFO를 class로 연습
class MyStack:
    def __init__(self, iterable = None):
        self._data = []
        if iterable is not None:
            for x in iterable:
                self.push(x)

    # 맨 위에 요소 추가(삽입)
    def push(self, x):
        self._data.append(x)
        return x
    
    # 맨 위에 요소 제거
    def pop(self):
        if not self._data:
            raise IndexError("Stack이 비어 있음")
        return self._data.pop()
    
    def is_empty(self):
        return not self._data
    

    def __repr__(self):             # 파이썬 실행 시, 자동 호출(특별 메소드)
        top_to_bottom = list(reversed(self._data))
        return f"Stack(top -> bottom {top_to_bottom})"


def demo1Func():
    s = MyStack()
    for item in ["A", "B", "C", "D"]:
        s.push(item)
        print(f"push {item} -> ", s)
    
    print("LIFO에 따라, 하나씩 추출")
    while not s.is_empty():
        print("pop -> ", s.pop(), "| 현재는 : ", s)

def demo2Func(text : str) -> str:
    s = MyStack(text)
    out = []        # 뒤집힌 문자 기억
    while not s.is_empty():
        out.append(s.pop())
    return "".join(out)




if __name__ == "__main__":
    demo1Func()
    print(demo2Func("Python is good"))