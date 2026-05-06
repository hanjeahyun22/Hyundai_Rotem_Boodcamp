# 주식 데이터로 다중선형회귀모델 작성
# 전날 데이터로 다음날 종가 예측
# train/test split 후 scaling,  x뿐만 아니라 y도 scaling
# 예측 후 y를 원래 종가 단위로 복원한 뒤 R² 계산
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

np.random.seed(123)
torch.manual_seed(123)

# 1. 데이터 읽기
datas = np.loadtxt(
    "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/stockdaily.csv",
    delimiter=",", skiprows=1
)
print(datas[:2], datas.shape)  # (732, 5)

# 2. feature / label 분리
# datas 컬럼 구조: [Open, High, Low, Volume, Close]
# feature : Open, High, Low, Volume --- label:Close
x_data = datas[:, 0:-1]
y_data = datas[:, [-1]]
print("원본 x_data shape:", x_data.shape)
print("원본 y_data shape:", y_data.shape)

print("\n정렬 전")
print("x_data[0]:", x_data[0])
print("y_data[0]:", y_data[0])
print("x_data[1]:", x_data[1])
print("y_data[1]:", y_data[1])

# 3. 전날 feature로 다음날 종가를 예측하도록 데이터 한 칸 이동
# x_data[0] → y_data[1]
# x_data[1] → y_data[2]
# x_data[2] → y_data[3]
# 마지막 x는 대응되는 다음날 y가 없으므로 제거
# y는 첫 번째 값을 제거
x_data = np.delete(x_data, -1, axis=0)
y_data = np.delete(y_data, 0, axis=0)
print("\n정렬 후")
print("x_data[0] → 다음날 종가 y_data[0]")
print("x_data[0]:", x_data[0])
print("y_data[0]:", y_data[0])
print("\n최종 x_data shape:", x_data.shape)
print("최종 y_data shape:", y_data.shape)

# 4. train / test split
# 시계열 데이터이므로 shuffle=False 유지. 미래 데이터가 과거 학습에 섞이면 안 됨
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.3, random_state=123, shuffle=False
)
print("\ntrain/test split 결과")
print("x:", x_train.shape, x_test.shape)
print("y:", y_train.shape, y_test.shape)
print("\ny_train min/max:", y_train.min(), y_train.max())
print("y_test  min/max:", y_test.min(), y_test.max())

# 5. Scaling
# 중요: scaler는 반드시 train 데이터에만 fit 해야 함
# test 데이터에는 transform만 적용
# x뿐만 아니라 y도 scaling 해야 PyTorch 최적화가 안정적임
x_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler = MinMaxScaler(feature_range=(0, 1))

x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

print("\n스케일링 후")
print("x_train_scaled[:2] : ", x_train_scaled[:2])
print("y_train_scaled[:2] : ", y_train_scaled[:2])

# 6. train 내부에서 validation 분리
# Keras validation_split=0.15와 비슷한 방식
# 시계열이므로 shuffle하지 않고 train의 뒤쪽 15%를 validation으로 사용
val_ratio = 0.15
train_count = int(len(x_train_scaled) * (1 - val_ratio))

x_sub_train = x_train_scaled[:train_count]
y_sub_train = y_train_scaled[:train_count]

x_val = x_train_scaled[train_count:]
y_val = y_train_scaled[train_count:]

print("\nsub train / validation split")
print("x_sub_train:", x_sub_train.shape)
print("x_val      :", x_val.shape)

# 7. NumPy 배열을 PyTorch Tensor로 변환
x_sub_train_tensor = torch.tensor(x_sub_train, dtype=torch.float32)
y_sub_train_tensor = torch.tensor(y_sub_train, dtype=torch.float32)

x_val_tensor = torch.tensor(x_val, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.float32)

x_test_tensor = torch.tensor(x_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test_scaled, dtype=torch.float32)

# 8. PyTorch 다중선형회귀 모델 정의
# 입력 feature 4개 → 출력 1개
# 수식: 다음날 종가 = w1*Open + w2*High + w3*Low + w4*Volume + b
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(4, 1)

    def forward(self, x):
        return self.linear(x)

model = LinearRegressionModel()

# 9. 손실 함수와 optimizer
# 손실 함수: MSE, optimizer: Adam
# SGD보다 Adam이 학습률에 덜 민감하고 회귀 문제에서 안정적으로 수렴하는 경우가 많음
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 10. 모델 학습
epochs = 1000
train_loss_history = []
val_loss_history = []

for epoch in range(epochs):
    # train mode
    model.train()

    pred_train = model(x_sub_train_tensor)
    train_loss = criterion(pred_train, y_sub_train_tensor)

    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()

    # validation mode
    model.eval()

    with torch.no_grad():
        pred_val = model(x_val_tensor)
        val_loss = criterion(pred_val, y_val_tensor)

    train_loss_history.append(train_loss.item())
    val_loss_history.append(val_loss.item())

    if (epoch + 1) % 200 == 0:
        print(
            f"epoch {epoch + 1:4d} | "
            f"train loss: {train_loss.item():.6f} | "
            f"val loss: {val_loss.item():.6f}"
        )

# 11. test 데이터 예측
model.eval()

with torch.no_grad():
    pred_test_scaled = model(x_test_tensor)
    test_loss_scaled = criterion(pred_test_scaled, y_test_tensor)

print("\nscaled 기준 test loss:", test_loss_scaled.item())

# 12. 예측값을 원래 종가 단위로 복원
# 모델은 scaled y를 학습했기 때문에 예측값도 scaled 값임
# 따라서 y_scaler.inverse_transform()으로 원래 종가 단위로 복원해야 함
pred_test = y_scaler.inverse_transform(pred_test_scaled.numpy())
y_test_original = y_test

# 13. 평가
mse = mean_squared_error(y_test_original, pred_test)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_original, pred_test)

print("\n[test 평가 결과 - 원래 종가 단위]")
print("MSE :", round(mse, 4))
print("RMSE:", round(rmse, 4))
print("R²  :", round(r2, 4))

# 14. 실제값 vs 예측값 시각화
plt.figure(figsize=(10, 5))
plt.plot(y_test_original, "b", label="real close")
plt.plot(pred_test, "r--", label="pred close")
plt.title("PyTorch Linear Regression - Next Day Close Prediction")
plt.xlabel("Test data index")
plt.ylabel("Close price")
plt.legend()
plt.grid(True)
plt.show()

# 15. train loss / validation loss 시각화
# train loss와 validation loss가 함께 감소하면 일반화가 비교적 양호
# train loss만 감소하고 validation loss가 증가하면 과적합 의심

plt.figure(figsize=(10, 5))
plt.plot(train_loss_history, label="train loss")
plt.plot(val_loss_history, label="validation loss")
plt.title("Train Loss vs Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss - scaled y")
plt.legend()
plt.grid(True)
plt.show()

# 16. 학습된 가중치와 절편 확인
# 주의: 이 weight는 scaled x → scaled y 기준의 계수임
weight = model.linear.weight.detach().numpy()
bias = model.linear.bias.detach().numpy()
print("\n학습된 가중치 weight")
print(weight)
print("\n학습된 절편 bias")
print(bias)