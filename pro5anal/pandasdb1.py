# 터미널창 초기화
import os
os.system('cls')

# local db 연동 후, DataFrame에 자료 저장
import sqlite3

sql = "create table if not exists extab(product varchar(10), maker varchar(10), weight real, price integer)"

conn = sqlite3.connect(":memory:")
conn.execute(sql)
conn.commit()

data = [("mouse", "samsung", 12.5, 5000), ["keyboard", "lg", 52.5, 35000]]
isql = "insert into extab values(?, ?, ?, ?)"

conn.executemany(isql, data)
data1 = ("pen", "abc", 5.0, 1200)
conn.execute(isql, data1)
conn.commit()

cursor = conn.execute("select * from extab")
rows = cursor.fetchall()
for a in rows:
    print(a)


print("rows를 DataFrame에 저장")
import pandas as pd
df1 = pd.DataFrame(rows, columns=["product", "maker", "weight", "price"])
print(df1)
print()

print(df1.describe())
print()

df2 = pd.read_sql("select * from extab", conn)
print(df2)
print()

print(pd.read_sql("select count(*) as 건수 from extab", conn))

# DataFrame의 자료를 테이블에 저장(insert)
data = {
    "product":["연필", "볼펜", "지우개"],
    "maker":["모나미", "모나미", "모나미"],
    "weight":[2.3, 3.0, 5.0],
    "price":[1000, 2000, 500]
}
frame = pd.DataFrame(data)
print(frame)
frame.to_sql("extab", conn, if_exists="append", index=False)

df3 = pd.read_sql("select * from extab", conn)
print(df3)


cursor.close()
conn.close()