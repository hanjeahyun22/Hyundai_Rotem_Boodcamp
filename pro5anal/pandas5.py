# 터미널창 초기화
import os
os.system('cls')

# pandas file i/o
import pandas as pd
import numpy as np

print("######################################################################################################")
print("                                     pandas 데이터 불러오기")
print("######################################################################################################")


# read_csv : csv로 읽음
df = pd.read_csv("ex1.csv")
print(df, type(df))
print()

# read_table : table로 읽음 -->> 데이터들이 다 붙어 있음 --->>> sep="," 로 쉼표 기준 데이터 분리
# skip_blank_lines : 데이터 앞의 공백을 지움
df = pd.read_table("ex1.csv", sep=",", skip_blank_lines=True)
print(df)
print()

pd.set_option("display.max_columns", None)      # 모든 column 표시 옵션
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv")
print(df)
print()

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header=None)
print(df)
print()

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header=None, skiprows=1)
print(df)
print()

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv", header=None, names=["a", "b", "c", "d", "e"])
print(df)
print()

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt")
print(df)
print()

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt", sep="\s+")      # \s+ : 정규표현식 -> 공백 한 칸 이상
print(df)
print()
print(df.iloc[:, 0])        # 데이터가 분리 된건지 확인

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt", sep="\s+", skiprows=[1, 3])
print(df)
print()

df = pd.read_fwf("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/data_fwt.txt", header=None, widths=(10, 3, 5), names=("date", "name", "price"), encoding="utf8")
print(df)
print()
print(df.iloc[:, 0])        # 데이터가 분리 된건지 확인
print()


print("######################################################################################################")
print("                             chunk : 대량의 데이터를 부분씩 메모리로 읽어 처리")
print("######################################################################################################")
print("chunk : 데이터를 끊어 처리하는 단위")
print("대용량 자료 로딩 시, 초과 오류 발생 방지 : 메모리 절약")
print("스트리밍 방식(일부만 ***순차*** 처리)으로 읽음")
print("분산처리 효과를 볼 수 있음")
print("하지만, 여러 번 반복해 읽어야 하므로, 속도는 느림.")
print()

import time

n_rows = 10000
data = {
    "id"        :   range(1, n_rows + 1),
    "name"      :   [f"Student_{i}" for i in range(1, n_rows + 1)],
    "score1"    :   np.random.randint(50, 101, size=n_rows),
    "score2"    :   np.random.randint(50, 101, size=n_rows)
}

df = pd.DataFrame(data=data)
print(df.head(5))
print()
print(df.tail(3))

csv_fname = "students.csv"
df.to_csv(csv_fname, index=False)       # 파일 저장

print("----"*20)
# csv파일 읽기 : 전체 한 번에 읽기
start_all = time.time()
df_all = pd.read_csv(csv_fname)
average_all_1 = df_all["score1"].mean()
average_all_2 = df_all["score2"].mean()
time_all = time.time() - start_all

# chunk로 읽기
chunk_size = 1000
total_score1 = 0
total_score2 = 0
total_count = 0
start_chunk_total = time.time()

for i, chunk in enumerate(pd.read_csv(csv_fname, chunksize=chunk_size)):          # enumerate : index를 얻을 수 있음
    start_chunk = time.time()
    
    # chunk 처리 중, 첫 번째 학생 정보 출력
    first_student = chunk.iloc[0]
    print(f"Chunk {i + 1}의 첫 번째 학생 : ID = {first_student["id"]}, 이름 = {first_student["name"]}",
            f"score1 = {first_student["score1"]}, score2 = {first_student["score2"]}")
    total_score1 += chunk["score1"].sum()
    total_score2 += chunk["score2"].sum()
    total_count += len(chunk)

    end_chunk = time.time()
    elapsed = end_chunk - start_chunk                   # Chunk 단위 별로 걸린 처리 시간

    print(f"    처리 시간 : {elapsed:7f}")

time_chunk_total = time.time() - start_chunk_total      # 전체 걸린 시간
average_chunk1 = total_score1 / total_count
average_chunk2 = total_score2 / total_count


    
print("\n처리 결과")
print(f"전체 학생 수 : {total_count}")
print(f"score1의 총 합 : {total_score1}, 평균 : {average_chunk1:3f}")
print(f"score2의 총 합 : {total_score2}, 평균 : {average_chunk2:3f}")
print("전체 한 번에 처리 시간 : ", round(time_all, 7), "[sec]")
print("Chunk로 처리한 총 시간 : ", round(time_chunk_total, 7), "[sec]")

# chunk 처리 시간 시각화
import matplotlib.pyplot as plt
plt.rc("font", family="Malgun Gothic")
labels = ["전체 한번에 처리", "chunk로 처리"]
times = [time_all, time_chunk_total]

plt.figure(figsize=(6, 4))
bars = plt.bar(labels, times, color=["skyblue", "red"])
for bar, time_val in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{time_val:3f}초",
                ha="center", va="bottom",
                fontsize=10
                )
plt.ylabel("처리시간(sec)")
plt.grid(linestyle="--")
plt.tight_layout()
plt.show()
