# 단순한 HTTP Server 구축 - 기본적인 socket 연결 관리

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777

# SimpleHTTPRequestHandler : get 요청에 의해, 문서를 읽고 client로 전송하는 역할
handler = SimpleHTTPRequestHandler

# HTTPServer 객체 생성
serv = HTTPServer(('192.168.0.82', PORT), handler)
print('웹 서비스 시작...')

# 웹 서비스를 시작하고, 무한루프에 빠트림   == while TRUE
serv.serve_forever()
