# 우편 정보 파일 자료 읽기
# 키보드에서 입력한 동이름으로 해당 주소 정보 출력

def zipProcess():
    # dongIrum = input('동 이름 입력 : ')
    dongIrum = "개포1동"
    # print(dongIrum)
    with open(r'zipcode_seoul.txt', mode = 'r', encoding='euc-kr') as f:
        line = f.readline()                                                         # .readline : 하나의 행만 읽음
        # print(line)
        # lines = line.split('\t')                                                    # .split('\t) : 구분자 tab키로 분리
        # lines = line.split(chr(9))                                                  # chr(9) : tab에 해당하는 ASCII 코드 = 9
        # print(lines)
        while line:
            lines = line.split(chr(9))
            if lines[3].startswith(dongIrum):
                # print(lines)
                print('우 : ' + lines[0], ', ' + ' ' + lines[2] + lines[3])

            line = f.readline()                                                      # while 문의 반복 실행을 위해서, 그 다음 라인을 읽으라는 의미

if __name__ == '__main__':
    zipProcess()