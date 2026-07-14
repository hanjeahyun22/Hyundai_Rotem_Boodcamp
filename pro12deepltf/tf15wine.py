import os
os.system("cls")

import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf


# 와인의 등급, 맛, 산도 등을 측정하여 red / white 와인 분류
wdf = pd.read_csv("wine.csv", header=None)
print(wdf.head(2))
print(wdf.info())
print(wdf.iloc[:, 12].unique())         # [1 0]
print(len(wdf[wdf.iloc[:, 12]==0]))     # 4898
print(len(wdf[wdf.iloc[:, 12]==1]))     # 1599

# array로 변화
dataset = wdf.values
x = dataset[:, 0:12]
y = dataset[:, -1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y, shuffle=True)
print(x_train[:2], x_train.shape)
print(y_train[:2], y_train.shape)

# 모델
model = Sequential()
model.add(Input(shape=(12,)))

# 뉴런의 개수 (24 -> 12 -> 8 -> 1) : 정해진 방법 X  -->>    tuning 필요
model.add(Dense(24, activation="relu"))
model.add(Dense(12, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(1, activation="sigmoid"))
print(model.summary())

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"훈련되지 않은 모델의 정확도 : {acc*100}%")

# 조기 종료
early_stop = EarlyStopping(monitor="val_loss", restore_best_weights=True)

# 모델 저장
MODEL_DIR = "./winemodel/"
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

# 조건 설정
modelpath = "./winemodel/{epoch:02d}-{val_loss:.4f}.keras"
chkpoint = ModelCheckpoint(filepath=modelpath, monitor="val_loss", mode="auto", save_best_only=True)

# 학습 모델
history = model.fit(x_train, y_train, epochs=1000, validation_split=0.2, batch_size=64, callbacks=[early_stop, chkpoint])

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"훈련된 모델의 정확도 : {acc*100}%")

# 시각화
epoch_len = np.arange(len(history.epoch))
plt.plot(epoch_len, history.history["val_loss"], c="red", label="val_loss")
plt.plot(epoch_len, history.history["loss"], c="blue", label="loss")
plt.xlabel("epochs")
plt.ylabel("loss")
plt.legend()
plt.grid(True)
plt.show()
plt.close()

plt.plot(epoch_len, history.history["val_accuracy"], c="red", label="val_accuracy")
plt.plot(epoch_len, history.history["accuracy"], c="blue", label="accuracy")
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.legend()
plt.grid(True)
plt.show()
plt.close()


# 저장된 모델로 예측
from tensorflow.keras.models import load_model

new_data = x_test[:5, :]
print("새로운 데이터 : \n", new_data)

new_pred = model.predict(new_data)
print("예측값 : \n", new_pred)
print("예측 결과 : ", np.where(new_pred > 0.5, 1, 0).ravel())