# 1회용 서버
from socket import * 

# socket 객체 생성
# socket(socket_family(주소 형식 지정), socket_type(전송 방식), protocol(통신 규약)))
serversock = socket(AF_INET, SOCK_STREAM)       # proto는 기본값 0으로 보통 생략        # 동일한 프로토콜이 둘 이상 존재할 때는 지정

# socket 객체를 특정 컴퓨터와 바인딩
serversock.bind(('127.0.0.1', 8888))

serversock.listen(5)                    # 1~5 범위 : Client와 연결 정보수, Listener 설정
print('서버 서비스 중...')

conn, addr = serversock.accept()        # 수동적으로 연결을 받아들임
print('client addr : ', addr)
print('front client message : ', conn.recv(1024).decode())
conn.close()
serversock.close()