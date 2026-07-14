# BeautifulSoup 객체 메소드 활용
from bs4 import BeautifulSoup

html_page = """
<html>
<body>
    <h1>제목 태그</h1>
    <p>웹문서 연습</p>
    <p>원하는 자료 확인</p>
</body>
</html>
"""
print(type(html_page))
soup = BeautifulSoup(html_page, "html.parser")
print(type(soup))
print()
h1 = soup.html.body.h1
print("h1 : ", h1.string)
p1 = soup.html.body.p
print("p1 : ", p1.string)
p2 = p1.next_sibling.next_sibling
print("p2 : ", p2.string)

print("\n----- find() method 사용 ----")
html_page2 = """
<html>
<body>
    <h1 id="title">제목 태그</h1>
    <p>웹문서 연습</p>
    <p id="my" class="our"0>원하는 자료 확인</p>
</body>
</html>
"""
soup2 = BeautifulSoup(html_page2, "html.parser")
# find(tag명, attrs, recursive, string)
print(soup2.p, " ", soup2.p.string)
print(soup2.find("p").string)
print(soup2.find("p", id="my").string)
print(soup2.find(id="title").string)
print(soup2.find(id="my").string)
print(soup2.find(class_="our").string)

print("\n----- find_all(), findAll() method 사용 -----")
html_page3 = """
<html>
<body>
    <h1 id="title">제목 태그</h1>
    <p>웹문서 연습</p>
    <p id="my" class="our"0>원하는 자료 확인</p>
</body>
<div>
    <a href="https://naver.com></a><br>
    <a href="https://daum.net></a>
</div>
</html>
"""
soup3 = BeautifulSoup(html_page3, "html.parser")
print(soup3.find_all(['a']))
print(soup3.find_all(['a', 'p']))
print()

links = soup3.find_all("a")
# print(links)
for i in links:
    href = i.attrs["href"]
    text = i.text       # i.string
    print(href, " ", text)

print("\n---- 정규표현식 사용 ----")
import re
links2 = soup3.find_all(href=re.compile(r'^https'))
# print(links2)
for k in links2:
    print(k.attrs["href"])

print("---- bugs 사이트 음악 순위 읽기 ----")
import requests
url = "https://music.bugs.co.kr/chart"
response = requests.get(url)
# print(response.text)
bsoup = BeautifulSoup(response.text, "html.parser")
