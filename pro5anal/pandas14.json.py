# JSON 자료 : XML에 비해 경량.
# -->> 배열 개념만 있으면 처리 가능

import json

dict = {"name":"tom", "age":25, "score":["90", "80", "88"]}
print(dict, type(dict))

print("------------------ json 인코딩 : dict -->> str ------------------")
str_val = json.dumps(dict)
# str_val = json.dumps(dict, indent=4)
print(str_val, type(str_val))       # <class 'str'>

# dict가 아닌 str 문자열이므로, key:value 로 못읽음
# print(str_val["name"])          # 에러

# 문자열 관련 함수만 사용 가능
print(str_val[0:20])

print("------------------ json 디코딩 : str -->> dict ------------------")
json_val = json.loads(str_val)
print(json_val, type(json_val))     # <class "dict">
print(json_val["name"])             # dict 관련 명령어 사용 가능

for k in json_val.keys():
    print(k)
for v in json_val.values():
    print(v)

print("\n----- 서울시 제공 도서관 정보 JSON 샘플 자료(5개) 읽기 ------")
import urllib.request as req

url = url = "http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode()
# print(plainText, type(plainText))   # <class 'str'>

jsonData = json.loads(plainText)
# print(jsonData, type(json))         # <class 'module'>
print(jsonData["SeoulLibraryTimeInfo"]["row"][0]["LBRRY_NAME"])
print()

# dict의 get() 사용
libData = jsonData.get("SeoulLibraryTimeInfo").get("row")
# print(libData)
name = libData[0].get("LBRRY_NAME")
print(name)
print()

datas=[]
for ele in libData:
    name = ele.get("LBRRY_NAME")
    tel = ele.get("TEL_NO")
    addr = ele.get("ADRES")
    print(name, " ", tel, " ", addr)
    datas.append([name, tel, addr])

import pandas as pd
df = pd.DataFrame(datas, columns=["도서관명", "전화", "주소"])
print(df)