# client
from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('127.0.0.1', 7788))                     # 능동적으로 연결을 시도
clientsock.send('안녕 반가워'.encode(encoding='utf_8', errors='strict'))

print('수신자료 : ', clientsock.recv(1024).decode())

clientsock.close()
