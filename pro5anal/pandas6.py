import pandas as pd

print("######################################################################################################")
print("                                     DataFrame 저장 방식")
print("######################################################################################################")

items = {
    "apple" :   {"count" :  10, "price" :   1500},
    "orange":   {"count" :  5, "price"  :   800}
}

df = pd.DataFrame(items)
print(df)

print("---- 클립보드로 저장 ----")
df.to_clipboard()

print("---- html로 저장 ----")
print(df.to_html())
print()

print("---- json으로 저장 ----")
print(df.to_json())
print()

print("---- csv로 저장 ----")
df.to_csv("result1.csv", sep=",")
df.to_csv("result2.csv", sep=",", index=False)                  # 이상적인 방법
df.to_csv("result3.csv", sep=",", index=False, header=False)

print(" 전치행렬(Transpose)")
df2 = df.T
print(df)
print()
print(df2)
print()

df2.to_csv("result4.csv", sep=",", index=False, encoding="utf-8-sig")       # urf-8-sig : 엑셀에서 한글 깨짐 방지 인코딩 형식
rdata = pd.read_csv("result4.csv")
print(rdata)
print()

print("######################################################################################################")
print("                                         EXCEL 파일i/o")
print("######################################################################################################")

df3 = pd.DataFrame({
    "name"  :   ["Alice", "Bob", "Oscar"],
    "age"   :   [24, 22, 29],
    "city"  :   ["seuol", "suwon", "incheon"],
})
print("<df3>\n",df3)
print()

# 저장
print("---- .xlsx로 저장 ----")
df3.to_excel("result.xlsx", index=False, sheet_name="work1")
print()

# 읽기
print("---- 엑셀 파일 읽기 ----")
exdf = pd.ExcelFile("result.xlsx")
print(exdf.sheet_names)
df4 = exdf.parse("work1")
print(df4)
print()


