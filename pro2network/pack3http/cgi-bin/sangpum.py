# 한글 깨짐 방지
import sys
sys.stdout.reconfigure(encoding='utf-8')

import MySQLdb
import pickle

with open("cgi-bin/mydb.dat", mode="rb") as obj:
    config = pickle.load(obj)


print("Content-Type: text/html; charset=utf-8")
print()
print("""
    <html>
    <body>
        <b>** 상품 정보 **</b>
        <br/>
        <table border='1'>
        <tr>
        <td>코드</td>
        <td>상품명</td>
        <td>수량</td>
        <td>단가</td>
        </tr>""")

try:
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()

    cursor.execute("select * from sangdata order by code desc")
    datas = cursor.fetchall()
    for code, sang, su, dan in datas:
        print("""
            <tr>
                <td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>
            </tr>
        """.format(code, sang, su, dan))
except Exception as e:
    print('err : ', e)
finally:
    cursor.close()
    conn.close()



print("</table>")
print("</body>")
print("</html>")
