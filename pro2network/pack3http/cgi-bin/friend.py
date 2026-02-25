# -*- coding: utf-8 -*-   
# 한글 깨짐 현상 해결 - 위 명령 안 먹으면 아래 방법 사용
import sys
sys.stdout.reconfigure(encoding='utf-8')   

import os
import urllib.parse

# --- get / post 요청 받을 때 ---------
method = os.environ.get("REQUEST_METHOD", "GET")

if method == "POST":                                                # POST Method
    length = int(os.environ.get("CONTENT_LENGTH", 0))
    body = sys.stdin.read(length)
else:                                                               # GET Method
    body = os.environ.get("QUERY_STRING", "")

params = urllib.parse.parse_qs(body)

irum = params.get("name", [""])[0]
junhwa = params.get("phone", [""])[0]
gen = params.get("gen", [""])[0]

print("Content-Type: text/html; charset=utf-8")
print()
print("""
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>world</title>
</head> 
<body>
    입력한 값은 : 이름은 {0}, 전화는 {1}, 성별은 {2} 
</body>
</html>
""".format(irum, junhwa, gen))
