# 터미널창 초기화
import os
os.system('cls')


# 자전거 공유 데이터

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from scipy import stats

plt.style.use("ggplot")                 ## R언어에서 매우 강력한 ggplot style을 사용
train = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv")
print(train.info())
print()
print("dtype : \n",train.dtypes)             # dtype: object
print()
print("shape : \n",train.shape)             # (10886, 12)
print()
print("columns : \n",train.columns)
print()
print("첫 3개 데이터 : \n",train.head(3))
print()
print(train.temp.describe())
print()
print(train.isnull().sum())
print()


# 년, 월, 일, 시, 분, 초 별도 column 추가 생성
train['datetime'] = pd.to_datetime(train['datetime'])

train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train['minute'] = train['datetime'].dt.minute
train['second'] = train['datetime'].dt.second
print(train.head(1))
print(train.columns)

# 대여량 시각화
figure, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4)
figure.set_size_inches(15, 5)
sns.barplot(data=train, x="year", y="count", ax=ax1)
sns.barplot(data=train, x="month", y="count", ax=ax2)
sns.barplot(data=train, x="day", y="count", ax=ax3)
sns.barplot(data=train, x="hour", y="count", ax=ax4)
ax1.set(ylabel="대여 수", title="년도 별 대여")
ax2.set(ylabel="월", title="월 별 대여")
ax3.set(ylabel="일", title="일 별 대여")
ax4.set(ylabel="시간", title="시간 별 대여")
plt.show()

# boxplot
fig, axes = plt.subplots(nrows=2, ncols=2)
figure.set_size_inches(12, 10)
sns.boxplot(data=train, y="count", orient="v", ax=axes[0][0])                       # 0행 0열
sns.boxplot(data=train, y="count", x="season", orient="v", ax=axes[0][1])           # 0행 1열
sns.boxplot(data=train, y="count", x="hour", orient="v", ax=axes[1][0])             # 1행 0열
sns.boxplot(data=train, y="count", x="workingday", orient="v", ax=axes[1][1])       # 1행 1열
axes[0][0].set(ylabel="대여수", title="대여")
axes[0][1].set(xlabel="계절", ylabel="대여 수", title="계절 별 대여량")
axes[1][0].set(xlabel="계절", ylabel="대여 수", title="시간대 별 대여량")
axes[1][1].set(xlabel="근무일", ylabel="대여 수", title="근무일에 따른 대여량")
plt.show()


# 산점도
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)
figure.set_size_inches(12, 5)
sns.regplot(x="temp", y="count", data=train, ax=ax1)
sns.regplot(x="humidity", y="count", data=train, ax=ax2)
sns.regplot(x="windspeed", y="count", data=train, ax=ax3)
plt.show()