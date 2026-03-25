# 터미널창 초기화
import os
os.system('cls')

# pandas의 DataFrame의 자료를 원격 DB의 테이블에 저장
# pip install sqlalchemy

import pandas as pd
from sqlalchemy import create_engine
import pymysql

from dotenv import load_dotenv
load_dotenv()


data = {
    "code":[10, 11, 12],
    "sang":["사이다", "맥주", "와인"],
    "su":[20, 22, 5],
    "dan":[5000, '3000', "70000"]
}



try:
    frame = pd.DataFrame(data)
    print(frame)
    print()

    # engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test?charset=utf8")
    engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@127.0.0.1:3306/test?charset=utf8")
    
    # 저장  -->> 한번 작업 했으면, Primary Key 수정 이슈로 다시 실행하면 에러 발생
    # frame.to_sql(name="sangdata", con=engine, if_exists="append", index=False)

    # 읽기
    df = pd.read_sql("select * from sangdata", engine)
    print(df)
except Exception as e:
    print("err : ", e)
finally:
    pass


