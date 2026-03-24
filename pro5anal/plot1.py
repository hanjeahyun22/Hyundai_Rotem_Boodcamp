# 터미널창 초기화
import os
os.system('cls')


# matplotlib : Plotting 라이브러리.
# 그래프 생성을 위한 다양한 함수를 제공
# 시각화의 중요성

import numpy as np
import matplotlib.pyplot as plt
plt.rc("font", family="malgun gothic")
plt.rcParams['axes.unicode_minus'] = False

# x = ["서울", "인천", "수원"]
x = ("서울", "인천", "수원")
# x = {"서울", "인천", "수원"}      # set 형식은 x축으로 입력 불가능(set형태는 순서(index)가 없음 -->> 중복을 제거할 때 사용)


y = [5, 3, 7]

plt.plot(x,y)
plt.xlim([-1, 3])
plt.ylim([0, 10])

# tick 설정(y축 label을 인위적으로 표시)
plt.yticks(list(range(0, 11, 3)))
plt.plot(x,y)
plt.show()


data = np.arange(1, 11, 2)
plt.plot(data)                  # x축의 구간은 자동으로 설정됨.
x = [0,1,2,3,4]
for a, b in zip(x,data):
    plt.text(a, b, str(b))
plt.show()



x = np.arange(10)
y = np.sin(x)
print(x,y)
# plt.plot(x,y)
plt.plot(x,y, "--or", linewidth=2, markersize=12)
plt.show()

# hold : 복수의 plot을 하나의 figure에서 시각화
x = np.arange(0, np.pi * 3, 0.1)
print(x)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.figure(figsize=(10, 5))         # figsize=(너비, 높이)
plt.plot(x, y_sin, 'r-')
plt.scatter(x, y_cos)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Sine & Cosine Graph[0 < x < 3*pi]")

plt.show()

print()

# subplot : 하나의 Figure를 여러개의 Axes(plot)으로 나누기
plt.subplot(2, 1, 1)        # 2행1열 짜리 subplot 열을 만들고, 1행에 plot
plt.plot(x, y_sin)
plt.title("Sine Graph [0 < x < 3*pi]")
plt.subplot(2, 1, 2)        # # 2행1열 짜리 subplot 열을 만들고, 2행에 plot
plt.plot(x, y_cos)
plt.title("Cosine Graph [0 < x < 3*pi]")
plt.show()
print()

irum = ['a', 'b', 'c', 'd', 'e']
kor = [80, 50, 70, 70, 90]
eng = [60, 70, 80, 90, 100]
plt.plot(irum, kor, 'ro-')
plt.plot(irum, eng, 'bo--')
plt.ylim([50, 100])
plt.title("시험 점수")
# plt.legend(['국어', '영어'], loc=4)
plt.legend(['국어', '영어'], loc='best')
plt.grid(True)

fig = plt.gcf()
plt.show()
fig.savefig("plot1.png")



from matplotlib.pyplot import imread
img = imread("plot1.png")
plt.imshow(img)
plt.show()