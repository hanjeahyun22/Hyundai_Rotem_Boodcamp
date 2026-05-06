import os
os.system("cls")
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("binary.csv")
print(df.head(2))

# 전처리 : rank는 범주형 자료이므로, one-hot 처리
df = pd.get_dummies(df, columns=["rank"])
print(df.head(2))

# feature, label로 구분
x = df.drop("admit", axis=1)
y = df["admit"]
print(x.head(3))
print(y.head(3))

# Scaling
scalar = StandardScaler()
x_scaled = scalar.fit_transform(x)
print(x[:3])

# train / test data split
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)
print(x_train[:2], x_train.shape)
print(y_train[:2], y_train.shape)

# modelig
model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(units=16, activation="relu"),
    Dense(units=8, activation="relu"),
    Dense(units=1, activation="sigmoid")
])
print(model.summary())



model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
print(model.summary())


history = model.fit(x_train, y_train, epochs=100, validation_split=0.2, batch_size=32)
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"테스트 결과 손실 : {loss}, 정확도 : {acc}")

plt.figure(figsize=(12, 5))

# loss
plt.subplot(1, 2, 1)
plt.plot(history.history["loss"], label="loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.xlabel("epochs")
plt.ylabel("loss")
plt.legend()
plt.grid(True)

# accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history["accuracy"], label="accuracy")
plt.plot(history.history["val_accuracy"], label="val_accuracy")
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.legend()
plt.grid(True)

plt.show()
plt.close()


# 사용자 입력 결과 예측
gre = float(input("gre 점수 입력 : "))
gpa = float(input("gpa 점수 입력 : "))
rank = int(input("rank 점수 입력(1~4) : "))
rank_encoded = [0,0,0,0]    # 입력된 rank one-hot처리
rank_encoded[rank-1] = 1

user_input = np.array([gre, gpa] + rank_encoded)
print(user_input)

user_scaled = scalar.transform(user_input.reshape(1, -1))
print(user_scaled)
new_pred = model.predict(user_scaled)
print(new_pred)
prob = new_pred[0][0]
print("합격 확률 : ", prob)
if prob >= 0.5:
    print("합격 가능성이 높습니다")
else:
    print("불합격 가능성이 높습니다")