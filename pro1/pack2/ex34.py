import os

print('------- 파일 처리 -------')                                           # file / database / network 등 외부 작업물을 불러올 때는 try~ except~ 반드시 예외 처리해주기

try:
    print('------- 파일 읽기 -------')
    print(os.getcwd())                                                      # C:\work\projects\pro1\pack2
    # f1 = open(os.getcwd() + r"\ftext.txt", encoding='utf-8')                # os.getcwd() 를 통해서 상대경로 입력
    # f1 = open("ftext.txt", encoding='utf-8')                                # ftext.txt 파일과 현재 파일이 동일한 디렉토리 안에 있기 때문에 이렇게도 열림
    f1 = open("ftext.txt", mode='r', encoding='utf-8')                      # mode의 종류 : r(reading), w(writing), a(append : 추가), b(binary : 2진수 데이터로 저장)
    print(f1)
    print(f1.read())
    f1.close()

    print('------- 파일 저장 -------')
    f2 = open("ftext.txt", mode='w', encoding='utf-8')
    f2.write('내 친구들\n')
    f2.write('홍길동, 한국인')
    f2.close()
    print('파일 저장 성공')

    print('------- 파일 내용 추가 -------')
    f3 = open('ftext.txt', mode='a', encoding='utf-8')
    f3.write('\n사오정')
    f3.write('\n저팔계')
    f3.write('\n손오공')
    f3.close
    print('파일 추가 성공')

    f4 = open('ftext.txt', mode='r', encoding='utf-8')
    print(f4.read())
    f4.close()

except Exception as e:          
    print('파일 처리 오류')