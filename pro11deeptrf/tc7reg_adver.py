# 다중선형회귀 : tv, radio, newspaper가 sales에 얼마나 영향을 주는지 파악
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

# 1. 데이터 읽기
data = pd.read_csv(
    "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv"
)
print(data.head(2))
del data['no']
print(data.head(2))

# 2. feature / label 분리
# feature : 독립변수 - tv, radio, newspaper 광고비가 sales에 영향을 주는지 확인
fdata = data[['tv', 'radio', 'newspaper']]
# label : 종속변수 - sales 예측
ldata = data.iloc[:, [3]]
print(fdata.head(2))
print(ldata[:2])

# 3. feature 정규화
# feature 간 단위 차이가 클 경우 정규화/표준화 작업이 모델 성능에 도움
# minmax_scale(axis=0)은 각 feature column 기준으로 0~1 범위로 정규화
fedata = minmax_scale(fdata, axis=0, copy=True)
print(fedata[:3])

# 4. train / test 데이터 분리
x_train, x_test, y_train, y_test = train_test_split(
    fedata, ldata, shuffle=True, test_size=0.3, random_state=123
)
print(x_train[:2], x_train.shape)  # (140, 3)
print(x_test[:2], x_test.shape)    # (60, 3)

# 5. NumPy / DataFrame 데이터를 PyTorch Tensor로 변환
# PyTorch 모델은 torch.Tensor를 입력으로 사용
x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32)

y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

# 6. validation_split=0.2 와 같은 효과 만들기
# Keras의 validation_split=0.2는 train data 중 20%를 검증용으로 사용
# PyTorch에서는 random_split()으로 직접 분리
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)

val_size = int(len(train_dataset) * 0.2)
train_size = len(train_dataset) - val_size

train_subset, val_subset = random_split(
    train_dataset,
    [train_size, val_size],
    generator=torch.Generator().manual_seed(123)
)

batch_size = 32

# DataLoader는 PyTorch에서 데이터를 미니배치 단위로 꺼내주는 도구.
# 전체 데이터를 한 번에 모델에 넣지 않고, 지정한 개수만큼 잘라서 반복적으로 공급.
train_loader = DataLoader(
    train_subset,
    batch_size=batch_size,
    shuffle=True
    # train_subset 데이터를 batch_size 개수만큼 묶어서
    # 매 epoch마다 섞은 뒤 모델 학습에 사용할 수 있게 준비한다
)

val_loader = DataLoader(
    val_subset,
    batch_size=batch_size,
    shuffle=False
)

test_dataset = TensorDataset(x_test_tensor, y_test_tensor)

test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False
)

# 7. 학습 함수 정의
def train_model(model, train_loader, val_loader, criterion, optimizer, epochs=100):
    """
    학습 순서: 1. model.train() -> 2. 예측값 계산 -> 3. 손실 계산 ->
    4. gradient 초기화 -> 5. 역전파 -> 6. 파라미터 갱신 -> 7. validation loss 계산
    """

    history = {
        "loss": [],
        "val_loss": []
    }

    for epoch in range(epochs):
        model.train()

        train_loss_sum = 0

        for x_batch, y_batch in train_loader:
            pred = model(x_batch)  # 1. 예측값 계산
            loss = criterion(pred, y_batch) # 2. 손실값 계산
            optimizer.zero_grad()  # 3. 이전 gradient 초기화
            loss.backward()   # 4. 역전파
            optimizer.step()  # 5. W, b 갱신
            train_loss_sum += loss.item()

        train_loss = train_loss_sum / len(train_loader)

        model.eval()  # 검증
        val_loss_sum = 0

        with torch.no_grad():
            for x_val, y_val in val_loader:
                val_pred = model(x_val)
                val_loss = criterion(val_pred, y_val)
                val_loss_sum += val_loss.item()

        val_loss = val_loss_sum / len(val_loader)

        history["loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        print(
            f"Epoch [{epoch + 1}/{epochs}] "
            f"loss: {train_loss:.6f} "
            f"val_loss: {val_loss:.6f}"
        )

    return history

# 8. 평가 함수 정의
def evaluate_model(model, x_test_tensor, y_test_tensor, criterion):
    model.eval()

    with torch.no_grad():
        pred = model(x_test_tensor)
        loss = criterion(pred, y_test_tensor)

    return loss.item(), pred


# 9. Sequential 방식 모델 작성
print()
print("PyTorch nn.Sequential을 사용한 방법 ----------")
model = nn.Sequential(
    nn.Linear(3, 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)

print(model)

# 손실 함수와 옵티마이저 정의
# criterion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters())
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 모델 학습
history = train_model(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=criterion,
    optimizer=optimizer,
    epochs=100
)

# 모델 평가
ev_loss, pred_tensor = evaluate_model(
    model=model,
    x_test_tensor=x_test_tensor,
    y_test_tensor=y_test_tensor,
    criterion=criterion
)
print("ev_loss : ", ev_loss)

# history 값 확인
print("history val_loss : ", history["val_loss"])
print("history loss : ", history["loss"])

# loss 시각화
plt.plot(history["val_loss"], label="val_loss")
plt.plot(history["loss"], label="loss")
plt.legend()
plt.show()

# Tensor를 NumPy 배열로 변환
pred_np = pred_tensor.detach().numpy()

print("설명력:", r2_score(y_test, pred_np))

# predict
with torch.no_grad():
    pred_5 = model(x_test_tensor[:5])

print("예측값 : ", pred_5.detach().numpy().ravel())
print("실제값 : ", y_test[:5].values.ravel())


# 10. nn.Module 상속 방식 모델 작성
print("\n\nPyTorch nn.Module 상속을 사용한 방법 ----------")
# PyTorch에는 Keras와 동일한 의미의 Functional API 모델 생성 방식은 없지만,
# nn.Module을 상속받아 __init__()에서 layer를 정의하고,
# forward()에서 데이터 흐름을 직접 작성하는 방식이 가장 비슷하다.
# 이 방식은 다중 입력, 다중 출력, 분기 구조, 병합 구조 등
# 복잡한 신경망 모델을 작성할 때 효과적이다.

class AdvertisingRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()

        # layer 정의
        self.hidden_layer1 = nn.Linear(3, 16)
        self.hidden_layer2 = nn.Linear(16, 8)
        self.output_layer = nn.Linear(8, 1)

        self.relu = nn.ReLU()  # activation 정의

    def forward(self, inputs):
        # 데이터 흐름 정의
        x = self.hidden_layer1(inputs)
        x = self.relu(x)

        x = self.hidden_layer2(x)
        x = self.relu(x)

        outputs = self.output_layer(x)

        return outputs

func_model = AdvertisingRegressionModel()
print(func_model)

criterion = nn.MSELoss()
optimizer = optim.Adam(func_model.parameters(), lr=0.01)

func_history = train_model(
    model=func_model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=criterion,
    optimizer=optimizer,
    epochs=100
)

func_ev_loss, func_pred_tensor = evaluate_model(
    model=func_model,
    x_test_tensor=x_test_tensor,
    y_test_tensor=y_test_tensor,
    criterion=criterion
)

print("func_model ev_loss : ", func_ev_loss)
func_pred_np = func_pred_tensor.detach().numpy()
print("설명력:", r2_score(y_test, func_pred_np))
