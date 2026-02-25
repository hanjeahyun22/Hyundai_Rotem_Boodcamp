from socket import * 
import sys

# HOST = '127.0.0.1'
HOST = ''               # 이 파일을 다른 사람과 공유할 때, 알아서 '' 빈 공간에 개인의 local  ip 가 들어감
PORT = 7788

serversock = socket(AF_INET, SOCK_STREAM)

try:
    serversock.bind((HOST, PORT))
    serversock.listen(5)
    print('서버(무한 루핑) 서비스 중...')

    while True:
        conn, addr =  serversock.accept()
        print('client info : ', addr[0], ' ', addr[1])              # addr[0] : ip 주소, addr[1] : 포트번호
        
        # 수신 메세지 출력
        print(conn.recv(1024).decode())
        
        # 메세지 송신
        conn.send(('from server : ' + str(addr[1]) + '너도 잘 지내').encode('utf_8'))

except Exception as e:
    print('err : ', e)
    sys.exit()
finally:
    conn.close()
    serversock.close()