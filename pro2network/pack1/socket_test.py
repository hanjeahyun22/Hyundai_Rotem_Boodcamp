# socket
'''
소켓(Socket)은 프로세스가 드넓은 네트워크 세계로 데이터를 내보내거나 혹은 그 세계로부터 데이터를 받기 위한 실질적인 창구 역할을 한다. 
그러므로 프로세스가 데이터를 보내거나 받기 위해서는 반드시 소켓을 열어서 소켓에 데이터를 써보내거나 소켓으로부터 데이터를 읽어들여야 한다.
'''
# socket이란 TCP/IP의 프로그래머 인터페이스이다.
# 통신 기기간 대화가 가능하도록 하는 통신 방식으로 클라이언트/서버 모델에 기초한다.
# 연결지향      : TCP / IP
# 비연결지향    : UDP

# socket 통신 확인
import socket
# HTTP: 웹 브라우저와 웹 서버 간 웹페이지(HTML 등) 전송
print(socket.getservbyname('http', 'tcp'))              # www환경 전송 규약
# SSH: 원격 서버에 안전하게 접속하기 위한 암호화 통신
print(socket.getservbyname('ssh', 'tcp'))               # 원격 컴퓨터 접속
# FTP: 서버와 클라이언트 간 파일 전송
print(socket.getservbyname('ftp', 'tcp'))               # 파일 전송
# SMTP: 이메일을 서버로 발송하는 프로토콜
print(socket.getservbyname('smtp', 'tcp'))              # 메일 송수신
# POP3: 이메일 서버에서 메일을 내려받는 프로토콜
print(socket.getservbyname('pop3', 'tcp'))              # 이메일
print()

# 특정 웹서버의 ipaddress 확인 예제
print(socket.getaddrinfo('www.daum.net', 80, proto=socket.SOL_TCP))
print(socket.getaddrinfo('www.naver.com', 80, proto=socket.SOL_TCP))