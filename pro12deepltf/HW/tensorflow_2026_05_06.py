'''
문제2) 21세 이상의 피마 인디언 여성의 당뇨병 발병 여부에 대한 dataset을 이용하여
    당뇨 판정을 위한 분류 모델을 작성한다.
피마 인디언 당뇨병 데이터는 아래와 같이 구성되어 있다.

Pregnancies: 임신 횟수
Glucose: 포도당 부하 검사 수치
BloodPressure: 혈압(mm Hg)
SkinThickness: 팔 삼두근 뒤쪽의 피하지방 측정값(mm)
Insulin: 혈청 인슐린(mu U/ml)
BMI: 체질량지수(체중(kg)/키(m))^2
DiabetesPedigreeFunction: 당뇨 내력 가중치 값
Age: 나이
Outcome: 5년 이내 당뇨병 발생여부 - 클래스 결정 값(0 또는 1)
당뇨 판정 칼럼은 outcome 이다.   1 이면 당뇨 환자로 판정

train / test 분류 실시
모델 작성은 Sequential API, Function API 두 가지를 사용한다.
ModelCheckPoint, EarlyStopping 사용
loss, accuracy에 대한 시각화를 실시한다.
'''

################################################################################
# [1] 라이브러리 로드 및 환경 설정
# - os.system("cls"): 콘솔 화면 초기화
################################################################################
import os
os.system("cls")
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

################################################################################
# [2] 데이터 로드 및 전처리
# - pima-indians-diabetes.data.csv: 피마 인디언 당뇨병 데이터셋
# - StandardScaler: 평균 0, 표준편차 1로 스케일링 (신경망 학습 효율 증대)
################################################################################
df = pd.read_csv("pima-indians-diabetes.data.csv")
df.columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
print(df.head(2))

# Feature(x)와 Label(y) 분리
x = df.drop("Outcome", axis=1)
# Outcome: 0(정상), 1(당뇨)
y = df["Outcome"]
print(x.head(2))
print(y.head(2))


# Scaling
scalar = StandardScaler()
x_scaled = scalar.fit_transform(x)
print(x[:3])

# 데이터 분할 (학습용 80%, 테스트용 20%)
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)
print(x_train[:2], x_train.shape)
print(y_train[:2], y_train.shape)

################################################################################
# [3] 모델 생성 (Sequential API)
# - Input: 입력 데이터의 특성 수(8개) 정의
# - Dense: 완전 연결층 (활성화 함수 ReLU 사용)
# - Output: 이진 분류를 위해 노드 1개, Sigmoid 함수 사용 (0~1 사이 확률값)
################################################################################
# modeling (Sequential API)
model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(units=16, activation="relu"),
    Dense(units=8, activation="relu"),
    Dense(units=1, activation="sigmoid")
])
print(model.summary())

################################################################################
# [4] 모델 설정 및 컴파일
# - loss="binary_crossentropy": 이진 분류용 손실 함수
# - optimizer="adam": 경사하강법의 한 종류 (가장 범용적)
# - metrics=["accuracy"]: 평가지표로 정확도 사용
################################################################################
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
print(model.summary())
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"테스트 결과 손실 : {loss}, 정확도 : {acc}")

################################################################################
# [5] 학습 최적화 설정 (Callbacks)
# - EarlyStopping: 검증 손실(val_loss)이 개선되지 않으면 학습 조기 종료
#   * restore_best_weights=True: 최적의 가중치를 복원
# - ModelCheckpoint: 학습 중 성능이 좋아진 모델을 파일로 자동 저장
#   * save_best_only=True: 가장 좋은 성능의 모델만 기록
################################################################################
# 조기 종료
early_stop = EarlyStopping(monitor="val_loss", restore_best_weights=True)

# 모델 저장
MODEL_DIR = "./diabetesmodel/"
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

# 조건 설정
modelpath = "./diabetesmodel/{epoch:02d}-{val_loss:.4f}.keras"
chkpoint = ModelCheckpoint(filepath=modelpath, monitor="val_loss", mode="auto", save_best_only=True)

################################################################################
# [6] 모델 학습 (Fit)
# - validation_split=0.2: 학습 데이터 중 20%를 검증용으로 사용
# - batch_size=32: 한 번에 학습할 데이터 묶음 크기
################################################################################
# 학습 모델
history = model.fit(x_train, y_train, epochs=100, validation_split=0.2, batch_size=32, callbacks=[early_stop, chkpoint])

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"훈련된 모델의 정확도 : {acc*100}%")

################################################################################
# [7] 결과 시각화
# - Loss(손실) 및 Accuracy(정확도) 추이를 그래프로 출력
################################################################################
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

################################################################################
# [8] 예측 (Prediction)
# - model.predict(): 0~1 사이의 확률값 반환
# - np.where(pred > 0.5, 1, 0): 임계값 0.5를 기준으로 당뇨 여부 판정
################################################################################

new_data = x_test[:5, :]
print("새로운 데이터 : \n", new_data)

new_pred = model.predict(new_data)
print("예측값 : \n", new_pred)
print("예측 결과 : ", np.where(new_pred > 0.5, 1, 0).ravel())
