# PyTorch TensorBoard 실행용 학습 코드
# dataset : sklearn diabetes 회귀 데이터셋
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import TensorDataset, DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter

from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

import numpy as np
import matplotlib.pyplot as plt
import datetime
import os


# 1. 데이터셋 로드
# diabetes : 여러 건강 관련 feature를 이용해 질병 진행 정도를 예측.
diabetes = load_diabetes()
xdata = diabetes.data
ydata = diabetes.target.reshape(-1, 1)
print("feature shape:", xdata.shape)  # (442, 10)
print("label shape:", ydata.shape)    # (442, 1)
print("feature names:", diabetes.feature_names)

# 2. 데이터 표준화
# 신경망 학습에서는 feature의 스케일을 맞춰주는 것이 좋다.
# StandardScaler는 평균 0, 표준편차 1 기준으로 데이터를 변환.
scaler = StandardScaler()
xdata_scaled = scaler.fit_transform(xdata)

# 3. train / test 분리
x_train, x_test, y_train, y_test = train_test_split(
    xdata_scaled,
    ydata,
    test_size=0.3,
    shuffle=True,
    random_state=123
)
print("x_train shape:", x_train.shape)
print("x_test shape:", x_test.shape)

# 4. NumPy 데이터를 PyTorch Tensor로 변환
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# 5. train data 중 일부를 validation data로 분리
# Keras의 validation_split=0.2와 비슷한 효과.
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)

val_size = int(len(train_dataset) * 0.2)
train_size = len(train_dataset) - val_size

train_subset, val_subset = random_split(
    train_dataset,
    [train_size, val_size],
    generator=torch.Generator().manual_seed(123)
)

batch_size = 32

train_loader = DataLoader(
    train_subset,
    batch_size=batch_size,
    shuffle=True
)

val_loader = DataLoader(
    val_subset,
    batch_size=batch_size,
    shuffle=False
)

# 6. PyTorch 모델 정의
# 입력 feature는 10, 출력은 질병 진행 정도를 예측하는 회귀값 1개.
class DiabetesRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.hidden_layer1 = nn.Linear(10, 64)
        self.hidden_layer2 = nn.Linear(64, 32)
        self.hidden_layer3 = nn.Linear(32, 16)
        self.output_layer = nn.Linear(16, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.hidden_layer1(x))
        x = self.relu(self.hidden_layer2(x))
        x = self.relu(self.hidden_layer3(x))
        x = self.output_layer(x)

        return x

model = DiabetesRegressionModel()
print(model)

# 7. 손실 함수와 옵티마이저 정의
criterion = nn.MSELoss()  # 회귀 문제이므로 평균제곱오차 사용
optimizer = optim.Adam(model.parameters(), lr=0.001)


# 8. TensorBoard 로그 저장 경로 설정
# 실행할 때마다 로그 폴더가 구분되도록 현재 시간을 폴더명에 포함.
log_dir = os.path.join(
    "runs",
    "diabetes_regression",
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
)

writer = SummaryWriter(log_dir=log_dir)
print("TensorBoard 로그 저장 위치:", log_dir)

# 9. TensorBoard에 모델 그래프 기록
# add_graph()는 샘플 입력 데이터가 필요.
sample_input = x_train_tensor[:1]
writer.add_graph(model, sample_input)

# 10. 모델 학습 + TensorBoard 기록
epochs = 200

train_loss_history = []
val_loss_history = []

for epoch in range(epochs):
    # 학습 모드
    model.train()

    train_loss_sum = 0

    for x_batch, y_batch in train_loader:
        pred = model(x_batch)  # 예측값 계산
        loss = criterion(pred, y_batch)  # 손실 계산
        optimizer.zero_grad()  # gradient 초기화
        loss.backward()   # 역전파
        optimizer.step()  # 파라미터 갱신
        train_loss_sum += loss.item()

    train_loss = train_loss_sum / len(train_loader)

    model.eval()
    val_loss_sum = 0

    with torch.no_grad():
        for x_val, y_val in val_loader:
            val_pred = model(x_val)
            val_loss = criterion(val_pred, y_val)
            val_loss_sum += val_loss.item()

    val_loss = val_loss_sum / len(val_loader)

    train_loss_history.append(train_loss)
    val_loss_history.append(val_loss)

    # TensorBoard 기록
    writer.add_scalar("Loss/train", train_loss, epoch)
    writer.add_scalar("Loss/validation", val_loss, epoch)

    # 각 layer의 weight histogram 기록
    for name, param in model.named_parameters():
        writer.add_histogram(name, param, epoch)

    if (epoch + 1) % 10 == 0:
        print(
            f"Epoch [{epoch + 1}/{epochs}] "
            f"train_loss: {train_loss:.4f} "
            f"val_loss: {val_loss:.4f}"
        )

# 11. test data 평가
model.eval()

with torch.no_grad():
    test_pred = model(x_test_tensor)
    test_loss = criterion(test_pred, y_test_tensor)

print("test_loss:", test_loss.item())
test_pred_np = test_pred.detach().numpy()
print("결정계수 R2:", r2_score(y_test, test_pred_np))

# 12. TensorBoard에 최종 test loss 기록
writer.add_scalar("Loss/test", test_loss.item(), epochs)
writer.close()

# 13. loss 시각화
plt.plot(train_loss_history, label="train_loss")
plt.plot(val_loss_history, label="val_loss")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.legend()
plt.show()

# 14. 예측값 일부 확인
print("예측값:", test_pred_np[:5].ravel())
print("실제값:", y_test[:5].ravel())


# 참고 : TensorBoard 실행 안내
# TensorBoard 실행 명령어는 > tensorboard --logdir runs
# 브라우저에서 접속 : http://localhost:6006
