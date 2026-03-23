"""
https://finance.naver.com/sise/sise_market_sum.naver?&page=1
https://finance.naver.com/sise/sise_market_sum.naver?&page=2
with open(파일명, mode='w')

csv 파일로 출력

csv파일로 읽기 후, DataFrame 에 저장
top3 종목명, 시가총액 출력
"""
# 터미널창 초기화
import os
os.system('cls')

import requests
from bs4 import BeautifulSoup
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")
url1 = "https://finance.naver.com/sise/sise_market_sum.naver?&page=1"
url2 = "https://finance.naver.com/sise/sise_market_sum.naver?&page=2"
headers = {'User-Agent':'Mozilla/5.0'}

while True:
    res1 = requests.get(url=url1, headers=headers)
    res2 = requests.get(url=url2, headers=headers)
    soup1 = BeautifulSoup(res1.content, "html.parser")
    soup2 = BeautifulSoup(res2.content, "html.parser")

    nation = soup.select_one("h3.h_lst span.blind").get_text(strip=True)
    print(nation)

    # 환율값
    price = soup.select_one(".value").get_text(strip=True)
    # print(price)

    unit = soup.select_one(".txt_krw .blind").get_text(strip=True)
    # print(unit)

    change = soup.select_one(".change").get_text(strip=True)
    # print(change)

    updown = soup.select("div.head_info.point_up span.blind")[-1].get_text(strip=True)
    # print(updown)

    print(f"{nation.replace(" ", "")} {price}{unit} {updown} {change}")

    time.sleep(5)