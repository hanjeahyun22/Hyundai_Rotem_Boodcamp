# 터미널창 초기화
import os
os.system('cls')

# BeautofulSoup 객체를 이용한 웹 문서 처리
import requests
from bs4 import BeautifulSoup

beseurl = "https://www.naver.com"
headers = {"User-Agent":"Mozilla/5.0"}

source = requests.get(beseurl, headers=headers)
print(source, type(source))             # <Response [200]> class
print(source.status_code)
print(source.text, type(source.text))   # <class 'str'>
# print(source.content)                   # Binary 데이터로 넘어옴.

conv_data = BeautifulSoup(source.text, 'lxml')
# print(conv_data, type(conv_data))       # <class 'bs4.BeautifulSoup'>

for atag in conv_data.find_all('a'):
    href = atag.get('href')
    title = atag.get_text(strip=True)
    if title:
        print(href)
        print(title)
        print("-----"*3)