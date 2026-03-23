import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = [
    "https://finance.naver.com/sise/sise_market_sum.naver?&page=1",
    "https://finance.naver.com/sise/sise_market_sum.naver?&page=2"
]

headers = {"User-Agent": "Mozilla/5.0"}
file_name = "market_cap.csv"


with open(file_name, mode='w', encoding='utf-8') as f:
    f.write("종목명,시가총액\n")
    
    for url in urls:
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        rows = soup.select("table.type_2 > tbody > tr")
        for row in rows:
            if not row.select_one("a.tltle"): continue

            name = row.select_one("a.tltle").get_text(strip=True)
            price = row.select(".number")[4].get_text(strip=True).replace(',', '')
            
            f.write(f"{name},{price}\n")

df = pd.read_csv(file_name)
df['시가총액'] = pd.to_numeric(df['시가총액'])
df.index = df.index + 1
print(df[['종목명', '시가총액']].head(5))
