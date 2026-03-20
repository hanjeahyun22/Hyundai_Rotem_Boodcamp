import xml.etree.ElementTree as etree

xmlfile = etree.parse("my.xml")
print(xmlfile, type(xmlfile))
root = xmlfile.getroot()
print(root.tag)
print(root[0].tag)      # root 요소의 0번째 요소명(노드명) 얻기
print(root[0][0].tag)
print()

myname = root.find("item").find("name").text
mytel = root.find("item").find("tel").text
print(myname + " " + mytel)

print("\n---------- 기상청 제공 XML 자료 읽기 ------------")
import requests
url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
headers = {"User-Agent":"Mozilla/5.0"}

res = requests.get(url, headers=headers)
res.raise_for_status()
print(res.text, type(res.text))             # xml 모양의 <class 'str'>

root = etree.fromstring(res.text)               # <Element '{current}current' at 0x000001979BDA39C0>
print(root)

# {current} namespace 제거      {current}weather -->> weather
for elem in root.iter():
    if "}" in elem.tag:
        elem.tag = elem.tag.split("}", 1)[1]    # "}"를 기준으로 잘라, 태그명

weather = root.find("weather")
year = weather.get("year")                      # 속성값 얻기
month = weather.get("month")
day = weather.get("day")
hour = weather.get("hour")

print(f"{year}년 {month}월 {day}일 {hour}시 기상예보")

# 각 지역(local tag) 순회
for local in weather.findall("local"):
    name = local.text.strip()       # 태그 안에 text
    ta = local.get("ta")            # local 요소(element)의 ta 속성
    print(f"{name} 지역 온도는 {ta}")